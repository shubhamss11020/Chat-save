/**
 * Cloud sync: save conversations from the Claude cloud (web, desktop app, phone).
 * Loaded by background.js with importScripts(). Shares its global scope, so it uses
 * enqueue(), getConfig(), withQueueLock() and processQueue() from background.js.
 *
 * It runs when any claude.ai page loads and on a timer while the browser is open.
 * It uses the browser's claude.ai login, so no tab has to stay open.
 */

const RECONCILE_EVERY_MINUTES = 5;
const CLAUDE_API = "https://claude.ai/api";
const SYNCED_KEY = "chatsave_synced_threads";
const RECONCILE_MIN_GAP_MS = 60 * 1000;  // never run more often than this
let reconcileRunning = false;
let lastReconcileStarted = 0;

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function claudeGet(path) {
  const res = await fetch(`${CLAUDE_API}${path}`, { credentials: "include" });
  if (!res.ok) throw new Error(`claude.ai${path} returned HTTP ${res.status}`);
  return res.json();
}

/** conversation id -> the Claude updated_at the server has confirmed saving. */
async function getSyncedThreads() {
  return (await chrome.storage.local.get(SYNCED_KEY))[SYNCED_KEY] || {};
}

async function markSynced(conversationId, updatedAt) {
  await withQueueLock(async () => {
    const map = await getSyncedThreads();
    map[conversationId] = updatedAt;
    await chrome.storage.local.set({ [SYNCED_KEY]: map });
  });
}

function cleanApiText(str) {
  return String(str || "")
    .replace(/[-]/g, "")
    .replace(/```[a-zA-Z0-9_-]*\s*This block is not supported on your current device yet\.?\s*```/gi, "")
    .replace(/This block is not supported on your current device yet\.?/gi, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/** Text of one Claude API message, including thinking, tool calls and tool results. */
function apiMessageText(m) {
  const parts = [];
  const add = (t) => {
    const v = cleanApiText(t);
    if (v && !parts.includes(v)) parts.push(v);
  };
  if (typeof m.text === "string") add(m.text);
  if (typeof m.content === "string") {
    add(m.content);
  } else if (Array.isArray(m.content)) {
    for (const b of m.content) {
      if (!b) continue;
      if (typeof b === "string") { add(b); continue; }
      if (typeof b.text === "string") add(b.text);
      else if (typeof b.content === "string") add(b.content);
      else if (b.type === "thinking" && typeof b.thinking === "string") {
        add("> *Thinking:*\n> " + b.thinking.trim().replace(/\n/g, "\n> "));
      } else if (b.type === "tool_use" && b.name) {
        const input = b.input ? `\n\`\`\`json\n${JSON.stringify(b.input, null, 2)}\n\`\`\`` : "";
        add(`*Tool Call: ${b.name}*${input}`);
      } else if (b.type === "tool_result") {
        const result = typeof b.content === "string" ? b.content : JSON.stringify(b.content || b.output || "");
        if (result && result.trim()) add(`*Tool Result:*\n\`\`\`\n${result.slice(0, 500)}\n\`\`\``);
      }
    }
  }
  return cleanApiText(parts.join("\n\n"));
}

/**
 * Turn one Claude conversation (list entry + full detail) into an ingest payload.
 * Each message keeps Claude's own timestamp, and the conversation keeps Claude's
 * created/updated times, so the archive shows when things were said, not when they were saved.
 */
function buildCloudPayload(meta, detail) {
  const chatMsgs = [...(detail.chat_messages || [])].sort((a, b) => {
    const ta = a.created_at ? Date.parse(a.created_at) : 0;
    const tb = b.created_at ? Date.parse(b.created_at) : 0;
    if (ta && tb && ta !== tb) return ta - tb;
    return (a.index ?? 0) - (b.index ?? 0);
  });

  const messages = [];
  const files = [];
  for (const m of chatMsgs) {
    const role = (m.sender === "human" || m.sender === "user") ? "user" : "assistant";
    const atts = [...(m.attachments || []), ...(m.files || [])];
    const seq = messages.length + 1;
    let body = apiMessageText(m);
    if (!body && atts.length) {
      body = `*(Attached: ${atts.map(a => a.file_name || a.name || "document").join(", ")})*`;
    }
    if (!body && role === "user") body = `*(User Prompt ${seq})*`;
    if (!body) continue;

    const last = messages[messages.length - 1];
    if (last && last.role === role && last.content === body) continue;

    messages.push({
      id: `${meta.uuid}_msg_${seq}_${role}`,  // same id scheme as the live page capture
      sequence: seq,
      role,
      content: body,
      timestamp: m.created_at || null,
    });
    for (const att of atts) {
      const fname = att.file_name || att.name || "attachment";
      const safeName = fname.replace(/\s+/g, "_");
      files.push({
        name: safeName,
        path: `attachments/${safeName}`,
        url: att.url || att.download_url || undefined,
        type: "application/octet-stream",
        content: "",
        extracted_text: att.extracted_content && att.extracted_content !== fname ? att.extracted_content : "",
        role,
        turn_sequence: seq,
        is_attachment: true,
      });
    }
  }

  if (!messages.length) return null;
  return {
    conversation_id: meta.uuid,
    title: meta.name || "Untitled conversation",
    platform: "claude",
    url: `https://claude.ai/chat/${meta.uuid}`,
    messages,
    files,
    is_final: true,
    created_at: meta.created_at || null,
    captured_at: meta.updated_at || null,
    source: "reconcile",
  };
}

/**
 * Save every recent Claude conversation the server does not yet have at its latest version.
 * A conversation counts as saved only after the server accepts it (see processQueue).
 */
async function reconcileFromCloud(maxDays = 2) {
  if (!(await hasConsent())) {
    return { success: false, error: "Saving is not turned on. Open the Chat-Save welcome page to start." };
  }
  if (reconcileRunning) return { success: false, reason: "already running" };
  if (Date.now() - lastReconcileStarted < RECONCILE_MIN_GAP_MS) {
    return { success: true, enqueued: 0, reason: "ran recently" };
  }
  reconcileRunning = true;
  lastReconcileStarted = Date.now();
  try {
    const config = await getConfig();
    if (!config.serverUrl || config.serverUrl.includes("claude.ai")) {
      return { success: false, error: "Server URL is not set" };
    }
    const orgs = await claudeGet("/organizations");
    if (!Array.isArray(orgs) || !orgs.length) {
      return { success: false, error: "Not logged in to claude.ai in this browser" };
    }
    const orgId = orgs[0].uuid;
    const list = await claudeGet(`/organizations/${orgId}/chat_conversations`);
    const cutoff = Date.now() - maxDays * 24 * 60 * 60 * 1000;
    const recent = (Array.isArray(list) ? list : [])
      .filter(c => Date.parse(c.updated_at || c.created_at || 0) >= cutoff);

    const synced = await getSyncedThreads();
    const stale = recent.filter(c => synced[c.uuid] !== c.updated_at);

    let enqueued = 0;
    for (const meta of stale) {
      await delay(1200);  // pace requests so claude.ai does not rate-limit this login
      try {
        const detail = await claudeGet(`/organizations/${orgId}/chat_conversations/${meta.uuid}?tree=True&rendering_mode=messages`);
        const payload = buildCloudPayload(meta, detail);
        if (payload) {
          await enqueue(payload);
          enqueued++;
        }
      } catch (err) {
        console.warn("[Chat-Save] Could not fetch conversation", meta.uuid, err.message);
      }
    }
    await chrome.storage.local.set({ chatsave_last_reconcile_time: Date.now() });
    return { success: true, enqueued, checked: recent.length };
  } catch (err) {
    console.warn("[Chat-Save] Cloud sync failed:", err.message);
    return { success: false, error: err.message };
  } finally {
    reconcileRunning = false;
  }
}

// Opening or reloading any claude.ai page also triggers a sync.
chrome.tabs.onUpdated.addListener((tabId, info, tab) => {
  if (info.status === "complete" && tab.url && tab.url.startsWith("https://claude.ai/")) {
    reconcileFromCloud();
  }
});
