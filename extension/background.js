/**
 * Chat-Save Background Service Worker (Manifest V3)
 * Handles durable offline queueing, exponential retry, auth resolution,
 * and telemetry heartbeat for Claude Team web capture.
 */

const DEFAULT_CONFIG = {
  serverUrl: "http://localhost:8000",
  authToken: "",
  autoSync: true
};

let isProcessingQueue = false;

// 1. Initialize client identity and alarms on install/startup
chrome.runtime.onInstalled.addListener(async () => {
  await getClientId();
  chrome.alarms.create("chatsave_queue_worker", { periodInMinutes: 1 });
  chrome.alarms.create("chatsave_heartbeat", { periodInMinutes: 5 });
  chrome.alarms.create("chatsave_reconcile_worker", { periodInMinutes: 20 });
  processQueue();
  sendHeartbeat();
});

chrome.runtime.onStartup.addListener(async () => {
  processQueue();
  sendHeartbeat();
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "chatsave_queue_worker") {
    processQueue();
  } else if (alarm.name === "chatsave_heartbeat") {
    sendHeartbeat();
  } else if (alarm.name === "chatsave_reconcile_worker") {
    triggerReconcileInTabs();
  }
});

/**
 * Returns or generates a persistent unique client ID.
 */
async function getClientId() {
  const data = await chrome.storage.local.get("chatsave_client_id");
  if (data.chatsave_client_id) {
    return data.chatsave_client_id;
  }
  const newId = "ext_" + crypto.randomUUID();
  await chrome.storage.local.set({ chatsave_client_id: newId });
  return newId;
}

/**
 * Resolves configuration:
 * Managed policy (enterprise IT) > Sync storage > Local storage > Defaults
 */
async function getConfig() {
  let managed = {};
  try {
    if (chrome.storage.managed) {
      managed = await chrome.storage.managed.get(null);
    }
  } catch (e) {
    // Managed storage not set, ignore
  }

  const local = await chrome.storage.local.get("chatsave_config");
  const localConfig = local.chatsave_config || {};

  return {
    serverUrl: (managed.serverUrl || localConfig.serverUrl || DEFAULT_CONFIG.serverUrl).replace(/\/+$/, ""),
    authToken: managed.authToken || localConfig.authToken || DEFAULT_CONFIG.authToken,
    // Identity is decided by the server from the token; this is only what it last reported.
    identity: localConfig.identity || null,
    autoSync: managed.autoSync !== undefined ? managed.autoSync : (localConfig.autoSync !== undefined ? localConfig.autoSync : DEFAULT_CONFIG.autoSync),
    isManaged: Boolean(managed.serverUrl || managed.authToken)
  };
}

/**
 * Reads the current local outbox queue.
 */
async function getQueue() {
  const data = await chrome.storage.local.get("chatsave_outbox");
  return data.chatsave_outbox || [];
}

/**
 * Saves the local outbox queue.
 */
async function saveQueue(queue) {
  await chrome.storage.local.set({ chatsave_outbox: queue });
}

// Every read-modify-write of the outbox or dead-letter queue runs through this lock, so
// concurrent enqueues, sends and retries can never overwrite each other's changes.
// Network sends happen outside the lock; only storage updates are serialized.
let queueLock = Promise.resolve();
function withQueueLock(fn) {
  const run = queueLock.then(fn, fn);
  queueLock = run.catch(() => {});
  return run;
}

/**
 * Enqueue a conversation snapshot into the persistent outbox.
 */
async function enqueue(payload) {
  const clientId = await getClientId();
  payload.client_id = clientId;

  const queue = await withQueueLock(async () => {
    const current = await getQueue();

    // Deduplicate in local queue if identical conversation snapshot is already waiting
    const existingIdx = current.findIndex(item => item.payload.conversation_id === payload.conversation_id);
    const queueItem = {
      id: "q_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7),
      payload,
      attempts: 0,
      nextAttemptAt: Date.now(),
      lastError: null,
      addedAt: Date.now()
    };

    if (existingIdx >= 0) {
      const oldMessages = current[existingIdx].payload.messages || [];
      const newMessages = payload.messages || [];
      // Protect earlier messages from being shortened if DOM temporarily trimmed them:
      for (let i = 0; i < newMessages.length; i++) {
        const prior = oldMessages.find(m => m.id === newMessages[i].id || m.sequence === newMessages[i].sequence);
        if (prior && prior.role === newMessages[i].role && prior.content && newMessages[i].content) {
          if (prior.content.trim().length > newMessages[i].content.trim().length) {
            newMessages[i].content = prior.content;
          }
        }
      }
      current[existingIdx] = queueItem;
    } else {
      current.push(queueItem);
    }

    await saveQueue(current);
    return current;
  });

  const currentDlq = await getDeadLetterQueue();
  broadcastToTabs({
    type: "QUEUE_UPDATED",
    pendingCount: queue.length,
    queuedIds: queue.map(q => q.payload?.conversation_id).filter(Boolean),
    dlqIds: currentDlq.map(d => d.payload?.conversation_id).filter(Boolean)
  });
  processQueue();
  return queue.length;
}

/**
 * Automatically moves items that exceeded MAX_RETRIES to Dead Letter Queue
 */
async function purgeExpiredToDLQ() {
  return withQueueLock(async () => {
    const queue = await getQueue();
    if (!queue.length) return false;

    const dlq = await getDeadLetterQueue();
    const surviving = [];
    let movedCount = 0;

    for (const item of queue) {
      const isAuth = item.lastError && (item.lastError.includes("HTTP 401") || item.lastError.includes("Invalid Server URL"));
      const maxAttempts = isAuth ? 4 : 10;
      if (item.attempts >= maxAttempts) {
        dlq.push({
          ...item,
          deadLetterAt: Date.now(),
          failureReason: isAuth
            ? `Delivery blocked (${item.lastError.slice(0, 120)}) - Please check Server URL & Auth Token in settings`
            : `Exceeded ${maxAttempts} attempts: ${item.lastError || "Unknown error"}`
        });
        movedCount++;
        console.error(`[Chat-Save] Item moved to Dead Letter Queue: ${item.id}`, item.lastError);
        broadcastToTabs({
          type: "DEAD_LETTER_EVENT",
          conversationId: item.payload?.conversation_id,
          error: item.lastError
        });
      } else {
        surviving.push(item);
      }
    }

    if (movedCount > 0) {
      await saveQueue(surviving);
      await saveDeadLetterQueue(dlq);
      broadcastToTabs({
        type: "QUEUE_UPDATED",
        pendingCount: surviving.length,
        queuedIds: surviving.map(q => q.payload?.conversation_id).filter(Boolean),
        dlqIds: dlq.map(d => d.payload?.conversation_id).filter(Boolean)
      });
      return true;
    }
    return false;
  });
}

/**
 * Process the local outbox queue with exponential backoff retry and request pacing.
 */
async function processQueue() {
  if (isProcessingQueue) return;
  isProcessingQueue = true;

  try {
    // 1. Purge items that have legitimately exhausted retries
    await purgeExpiredToDLQ();

    const config = await getConfig();
    let queue = await getQueue();
    if (!queue.length) {
      isProcessingQueue = false;
      return;
    }

    const now = Date.now();
    // Results of this run, keyed by item id. Applied to the *fresh* queue at the end, so
    // items enqueued while we were sending are never lost or overwritten.
    const updates = new Map();   // id -> item with new attempts / nextAttemptAt / lastError
    const finished = new Set();  // ids delivered or moved to the dead-letter queue

    for (let i = 0; i < queue.length; i++) {
      const item = queue[i];
      if (item.nextAttemptAt > now) {
        continue;
      }

      // Smooth pacing between requests so we never flood Render or trigger Cloudflare rate limits
      await new Promise(r => setTimeout(r, 600));

      try {
        if (!config.serverUrl || config.serverUrl.includes("claude.ai")) {
          throw new Error(`Invalid Server URL: "${config.serverUrl || ""}". Server URL must be your Chat-Save backend service (e.g. http://localhost:8000 or your Render URL), NOT claude.ai.`);
        }

        // The token identifies the person; no user is sent in the URL or body.
        const url = `${config.serverUrl}/api/extension/ingest`;
        const headers = {
          "Content-Type": "application/json"
        };
        if (config.authToken) {
          headers["Authorization"] = `Bearer ${config.authToken}`;
        }

        const res = await fetch(url, {
          method: "POST",
          headers,
          body: JSON.stringify(item.payload)
        });

        if (!res.ok) {
          const errText = await res.text();
          let summary = `HTTP ${res.status}: ${errText.slice(0, 150)}`;
          if (errText.includes("<title>Blocked</title>") || errText.includes("Cloudflare")) {
            summary = `Blocked by Cloudflare/WAF at ${url} (HTTP ${res.status}). Verify Server URL in extension options.`;
          }
          throw new Error(summary);
        }

        const receipt = await res.json();
        await chrome.storage.local.set({
          chatsave_last_receipt: receipt,
          chatsave_last_sync_time: new Date().toISOString()
        });

        finished.add(item.id);
        broadcastToTabs({
          type: "SYNC_SUCCESS",
          conversationId: item.payload?.conversation_id,
          capturedAt: item.payload?.captured_at,
          receipt
        });

      } catch (err) {
        console.warn("[Chat-Save] Queue delivery failed:", err.message);
        item.attempts += 1;
        item.lastError = err.message;

        const isAuthError = err.message.includes("HTTP 401") || err.message.includes("Invalid Server URL");
        const isRateLimitOrWaf = err.message.includes("Blocked") || err.message.includes("HTTP 403") || err.message.includes("HTTP 429") || err.message.includes("502") || err.message.includes("503") || err.message.includes("Failed to fetch");
        const MAX_RETRIES = isAuthError ? 4 : 10;

        if (item.attempts >= MAX_RETRIES) {
          await moveToDeadLetter({
            ...item,
            deadLetterAt: Date.now(),
            failureReason: isAuthError
              ? `Delivery failed (${err.message.slice(0, 120)}) - Please check Server URL & Auth Token in settings`
              : `Exceeded ${MAX_RETRIES} attempts: ${err.message}`
          });
          finished.add(item.id);
          console.error(`[Chat-Save] Item moved to Dead Letter Queue: ${item.id}`, item.lastError);
          broadcastToTabs({
            type: "DEAD_LETTER_EVENT",
            conversationId: item.payload?.conversation_id,
            error: item.lastError
          });
        } else {
          // Exponential backoff with jitter (longer backoff for rate limiting/WAF blocks)
          const backoffMs = isRateLimitOrWaf
            ? (10000 + Math.random() * 5000)
            : (Math.min(120000, 2000 * Math.pow(2, item.attempts)) + Math.random() * 1000);
          item.nextAttemptAt = Date.now() + backoffMs;
          updates.set(item.id, item);
        }

        broadcastToTabs({
          type: "SYNC_ERROR",
          conversationId: item.payload?.conversation_id,
          error: err.message,
          pendingCount: queue.length - finished.size
        });

        // If rate limited or Cloudflare blocked or server down, pause remaining items instead of failing all 50+ immediately
        if (isRateLimitOrWaf) {
          console.warn("[Chat-Save] Pausing queue batch processing to allow Cloudflare/server to cool down");
          for (let j = i + 1; j < queue.length; j++) {
            const nextItem = queue[j];
            if (nextItem.nextAttemptAt <= now) {
              nextItem.nextAttemptAt = Date.now() + 8000 + Math.random() * 4000;
              updates.set(nextItem.id, nextItem);
            }
          }
          break;
        }
      }
    }

    // Apply this run's results to the current queue (not the snapshot taken at the start).
    const merged = await withQueueLock(async () => {
      const fresh = await getQueue();
      const next = fresh
        .filter(i => !finished.has(i.id))
        .map(i => updates.get(i.id) || i);
      await saveQueue(next);
      return next;
    });

    const currentDlq = await getDeadLetterQueue();
    broadcastToTabs({
      type: "QUEUE_UPDATED",
      pendingCount: merged.length,
      queuedIds: merged.map(q => q.payload?.conversation_id).filter(Boolean),
      dlqIds: currentDlq.map(d => d.payload?.conversation_id).filter(Boolean)
    });

  } catch (globalErr) {
    console.error("[Chat-Save] Queue worker error:", globalErr);
  } finally {
    isProcessingQueue = false;
  }
}

/**
 * Reads the dead letter queue.
 */
async function getDeadLetterQueue() {
  const data = await chrome.storage.local.get("chatsave_dead_letter");
  return data.chatsave_dead_letter || [];
}

/**
 * Saves the dead letter queue.
 */
async function saveDeadLetterQueue(dlq) {
  await chrome.storage.local.set({ chatsave_dead_letter: dlq });
}

// Upload URLs this extension obtained from /api/attachments/presign. UPLOAD_TO_S3 only PUTs to
// a URL in this list, so a page script can't use the extension to write to an arbitrary URL.
const ISSUED_UPLOADS_KEY = "chatsave_issued_uploads";

async function rememberIssuedUpload(url) {
  await withQueueLock(async () => {
    const data = await chrome.storage.local.get(ISSUED_UPLOADS_KEY);
    const list = (data[ISSUED_UPLOADS_KEY] || []).concat(url).slice(-200);
    await chrome.storage.local.set({ [ISSUED_UPLOADS_KEY]: list });
  });
}

async function wasIssuedUpload(url) {
  const data = await chrome.storage.local.get(ISSUED_UPLOADS_KEY);
  return (data[ISSUED_UPLOADS_KEY] || []).includes(url);
}

/**
 * Append one permanently failed item to the dead-letter queue (serialized).
 */
async function moveToDeadLetter(entry) {
  await withQueueLock(async () => {
    const dlq = await getDeadLetterQueue();
    dlq.push(entry);
    await saveDeadLetterQueue(dlq);
  });
}

/**
 * Send telemetry heartbeat to the ingestion server.
 */
async function sendHeartbeat() {
  try {
    const config = await getConfig();
    const clientId = await getClientId();
    const queue = await getQueue();
    const lastSync = (await chrome.storage.local.get("chatsave_last_sync_time")).chatsave_last_sync_time || null;

    const url = `${config.serverUrl}/api/extension/heartbeat`;
    const headers = {
      "Content-Type": "application/json"
    };
    if (config.authToken) {
      headers["Authorization"] = `Bearer ${config.authToken}`;
    }

    const payload = {
      client_id: clientId,
      extension_version: chrome.runtime.getManifest().version,
      browser: "Chrome/Edge",
      pending_queue_count: queue.length,
      last_successful_sync: lastSync,
      last_error: queue.length > 0 ? (queue[0].lastError || null) : null
    };

    await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(payload)
    });
  } catch (err) {
    // Heartbeat failed silently (network down, etc.)
  }
}

/**
 * Broadcast status notifications to active Claude tabs.
 */
function broadcastToTabs(message) {
  chrome.tabs.query({ url: "*://claude.ai/*" }, (tabs) => {
    if (tabs && tabs.length) {
      tabs.forEach(tab => {
        chrome.tabs.sendMessage(tab.id, message, () => {
          if (chrome.runtime.lastError) {
            // Tab is navigating or content script not yet attached; safely ignored
          }
        });
      });
    }
  });
}

// 2. Runtime message handling from content scripts & popup
chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
  if (req.type === "INGEST_CONVERSATION") {
    getConfig().then(async (config) => {
      if (!config.autoSync && !req.force) {
        sendResponse({ queued: false, reason: "auto_sync_disabled" });
        return;
      }
      const pendingCount = await enqueue(req.payload);
      sendResponse({ queued: true, pendingCount });
    });
    return true; // async response
  }

  if (req.type === "GET_STATUS") {
    (async () => {
      await purgeExpiredToDLQ();
      const config = await getConfig();
      const queue = await getQueue();
      const clientId = await getClientId();
      const lastReceipt = (await chrome.storage.local.get("chatsave_last_receipt")).chatsave_last_receipt || null;
      const lastSyncTime = (await chrome.storage.local.get("chatsave_last_sync_time")).chatsave_last_sync_time || null;

      const dlq = await getDeadLetterQueue();

      sendResponse({
        config,
        clientId,
        pendingCount: queue.length,
        deadLetterCount: dlq.length,
        lastReceipt,
        lastSyncTime
      });
    })();
    return true;
  }

  if (req.type === "SYNC_NOW") {
    (async () => {
      const queue = await withQueueLock(async () => {
        const current = await getQueue();
        current.forEach(item => { item.nextAttemptAt = Date.now(); });
        await saveQueue(current);
        return current;
      });
      processQueue();
      sendResponse({ success: true, pendingCount: queue.length });
    })();
    return true;
  }

  if (req.type === "CLEAR_QUEUE") {
    (async () => {
      await withQueueLock(() => saveQueue([]));
      const currentDlq = await getDeadLetterQueue();
      broadcastToTabs({
        type: "QUEUE_UPDATED",
        pendingCount: 0,
        queuedIds: [],
        dlqIds: currentDlq.map(d => d.payload?.conversation_id).filter(Boolean)
      });
      sendResponse({ success: true, pendingCount: 0 });
    })();
    return true;
  }

  if (req.type === "RETRY_DEAD_LETTER") {
    (async () => {
      const { reQueued, queue } = await withQueueLock(async () => {
        const dlq = await getDeadLetterQueue();
        if (!dlq.length) return { reQueued: 0, queue: await getQueue() };
        const current = await getQueue();
        dlq.forEach(item => {
          item.attempts = 0;
          item.nextAttemptAt = Date.now();
          item.lastError = null;
          current.push(item);
        });
        await saveQueue(current);
        await saveDeadLetterQueue([]);
        return { reQueued: dlq.length, queue: current };
      });
      if (!reQueued) {
        sendResponse({ success: true, reQueued: 0 });
        return;
      }
      broadcastToTabs({
        type: "QUEUE_UPDATED",
        pendingCount: queue.length,
        queuedIds: queue.map(q => q.payload?.conversation_id).filter(Boolean),
        dlqIds: []
      });
      processQueue();
      sendResponse({ success: true, reQueued, pendingCount: queue.length });
    })();
    return true;
  }

  if (req.type === "CLEAR_DEAD_LETTER") {
    (async () => {
      const queue = await withQueueLock(async () => {
        await saveDeadLetterQueue([]);
        return getQueue();
      });
      broadcastToTabs({
        type: "QUEUE_UPDATED",
        pendingCount: queue.length,
        queuedIds: queue.map(q => q.payload?.conversation_id).filter(Boolean),
        dlqIds: []
      });
      sendResponse({ success: true, deadLetterCount: 0 });
    })();
    return true;
  }

  if (req.type === "GET_QUEUE_STATE") {
    (async () => {
      await purgeExpiredToDLQ();
      const queue = await getQueue();
      const dlq = await getDeadLetterQueue();
      sendResponse({
        queuedIds: queue.map(q => q.payload?.conversation_id).filter(Boolean),
        dlqIds: dlq.map(d => d.payload?.conversation_id).filter(Boolean)
      });
    })();
    return true;
  }

  if (req.type === "GET_S3_STATUS") {
    (async () => {
      try {
        const config = await getConfig();
        const res = await fetch(`${config.serverUrl}/api/attachments/status`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        sendResponse({ success: true, ...data });
      } catch (err) {
        sendResponse({ success: false, error: err.message, s3_configured: false });
      }
    })();
    return true;
  }

  if (req.type === "PRESIGN_ATTACHMENT") {
    (async () => {
      try {
        const config = await getConfig();
        const headers = { "Content-Type": "application/json" };
        if (config.authToken) {
          headers["Authorization"] = `Bearer ${config.authToken}`;
        }
        const res = await fetch(`${config.serverUrl}/api/attachments/presign`, {
          method: "POST",
          headers,
          body: JSON.stringify({
            filename: req.filename,
            content_type: req.content_type || "application/octet-stream",
            conversation_id: req.conversation_id || "default",
            size_bytes: req.size_bytes || null,
          }),
        });
        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || `HTTP ${res.status}`);
        }
        const data = await res.json();
        await rememberIssuedUpload(data.upload_url);
        sendResponse({ success: true, ...data });
      } catch (err) {
        sendResponse({ success: false, error: err.message });
      }
    })();
    return true;
  }

  if (req.type === "UPLOAD_TO_S3") {
    (async () => {
      try {
        const uploadUrl = req.upload_url;
        if (!(await wasIssuedUpload(uploadUrl))) {
          throw new Error("Upload URL was not issued by this extension's presign step");
        }
        const contentType = req.content_type || "application/octet-stream";
        let body = req.body;

        // If body is base64 string, convert to ArrayBuffer / Blob
        if (typeof body === "string" && body.includes(";base64,")) {
          const b64 = body.split(";base64,")[1];
          const binaryStr = atob(b64);
          const bytes = new Uint8Array(binaryStr.length);
          for (let i = 0; i < binaryStr.length; i++) {
            bytes[i] = binaryStr.charCodeAt(i);
          }
          body = bytes;
        }

        const res = await fetch(uploadUrl, {
          method: "PUT",
          headers: {
            "Content-Type": contentType,
            ...(req.headers || {})
          },
          body: body,
        });

        if (!res.ok) throw new Error(`S3 upload failed: HTTP ${res.status}`);
        sendResponse({ success: true, file_url: req.file_url });
      } catch (err) {
        sendResponse({ success: false, error: err.message });
      }
    })();
    return true;
  }

  if (req.type === "TRIGGER_RECONCILE") {
    chrome.tabs.query({ url: "*://claude.ai/*" }, (tabs) => {
      if (tabs && tabs.length > 0) {
        chrome.tabs.sendMessage(tabs[0].id, { type: "TRIGGER_RECONCILE", maxDays: req.maxDays || 2 }, (res) => {
          if (chrome.runtime.lastError) {
            sendResponse({
              success: false,
              error: "Please refresh your open Claude.ai tab to reconnect the extension."
            });
            return;
          }
          sendResponse(res || { success: true, enqueued: 0, message: "Reconciliation initiated" });
        });
      } else {
        sendResponse({ success: false, error: "No active claude.ai tab open" });
      }
    });
    return true;
  }

  if (req.type === "DETECT_USER") {
      (async () => {
        // 1. Check cached detection
        const stored = await chrome.storage.local.get(["chatsave_detected_user", "chatsave_config"]);
        if (stored.chatsave_detected_user) {
          sendResponse({ success: true, user: stored.chatsave_detected_user });
          return;
        }
        if (stored.chatsave_config?.userId && stored.chatsave_config.userId !== "user" && stored.chatsave_config.userId !== "unknown") {
          sendResponse({ success: true, user: stored.chatsave_config.userId });
          return;
        }
  
        // 2. Query open Claude tabs
        chrome.tabs.query({ url: "*://claude.ai/*" }, (tabs) => {
          if (!tabs || tabs.length === 0) {
            sendResponse({
              success: false,
              error: "No active claude.ai tab found. Please open claude.ai in Chrome and log in, then click Auto-Detect."
            });
            return;
          }
  
          let answered = false;
          let attempts = tabs.length;
          let hadDisconnect = false;
  
          tabs.forEach(tab => {
            chrome.tabs.sendMessage(tab.id, { type: "GET_CLAUDE_USER" }, (res) => {
              if (chrome.runtime.lastError) {
                hadDisconnect = true;
              } else if (res && res.user && !answered) {
                answered = true;
                chrome.storage.local.set({ chatsave_detected_user: res.user });
                sendResponse({ success: true, user: res.user });
                return;
              }
  
              attempts--;
              if (attempts === 0 && !answered) {
                if (hadDisconnect) {
                  sendResponse({
                    success: false,
                    error: "Claude tab found, but was open before extension reload. Please refresh (F5) your claude.ai tab, then click Auto-Detect."
                  });
                } else {
                  sendResponse({
                    success: false,
                    error: "Could not auto-detect Claude user. Make sure you are logged into claude.ai."
                  });
                }
              }
            });
          });
        });
      })();
      return true;
    }
});

/**
 * Sends a message to the active claude.ai tab to reconcile recent conversations from the past 48 hours.
 */
function triggerReconcileInTabs(maxDays = 2) {
  chrome.tabs.query({ url: "*://claude.ai/*" }, (tabs) => {
    if (tabs && tabs.length > 0) {
      chrome.tabs.sendMessage(tabs[0].id, { type: "TRIGGER_RECONCILE", maxDays }, () => {
        if (chrome.runtime.lastError) {
          // Tab not refreshed or script not ready; safely consumed
        }
      });
    }
  });
}

