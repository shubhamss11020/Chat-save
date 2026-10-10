/**
 * Chat-Save Content Script
 * Injected into https://claude.ai/*
 * High-performance, non-blocking transcript capture with zero DOM freeze.
 */

(() => {
  let isStreaming = false;
  let finalizeTimer = null;
  let observerThrottle = null;
  let lastCapturedHash = "";
  let hudElement = null;
  let hudStatus = "idle";
  let lastReceipt = null;
  let pendingCount = 0;

  // 1. Extract Conversation ID from URL
  function getConversationId() {
    const path = window.location.pathname;
    const match = path.match(/\/chat\/([a-zA-Z0-9_-]+)/);
    return match ? match[1] : (path.includes("/new") ? "new" : "");
  }

  // 2. Extract Conversation Title
  function getConversationTitle() {
    const docTitle = document.title.replace(/\s*·\s*Claude\s*$/i, "").trim();
    if (docTitle && docTitle !== "Claude") return docTitle;

    const headerTitleEl = document.querySelector('header button[data-testid*="title"], header .text-ellipsis, [data-testid="chat-title"]');
    if (headerTitleEl && headerTitleEl.textContent.trim()) {
      return headerTitleEl.textContent.trim();
    }

    const firstUserMsg = document.querySelector('[data-testid="user-message"], .font-user-message');
    if (firstUserMsg && firstUserMsg.textContent.trim()) {
      return firstUserMsg.textContent.trim().slice(0, 50);
    }

    return "Untitled conversation";
  }

  // 3. Compute SHA-256 for a string
  async function sha256(str) {
    const buf = new TextEncoder().encode(str);
    const digest = await crypto.subtle.digest("SHA-256", buf);
    return Array.from(new Uint8Array(digest))
      .map(b => b.toString(16).padStart(2, "0"))
      .join("");
  }

  function sanitizeText(str) {
    if (!str) return "";
    let s = str.replace(/[\uE000-\uF8FF]/g, ""); // Strip icon font PUA glyphs (copy, retry, etc.)
    s = s.replace(/(?:\r?\n)?\s*(?:\d+\s*(?:second|minute|hour|day|week|month)s?\s*ago|just now)\s*$/i, "");
    return s.trim();
  }

  // 4. Fast, complete text extraction gathering all paragraphs and markdown blocks
  function extractCleanText(node, isAssistant) {
    if (!node) return "";

    let structured = "";
    if (isAssistant) {
      // Collect ALL markdown content blocks in this turn (paragraphs, lists, code blocks, tables)
      const blocks = node.querySelectorAll('.standard-markdown, .progressive-markdown, [class*="font-claude-message"], .prose');
      if (blocks && blocks.length > 0) {
        const parts = [];
        blocks.forEach(b => {
          // Avoid duplicate nested text
          const hasMatchedParent = Array.from(blocks).some(other => other !== b && other.contains(b));
          if (!hasMatchedParent) {
            const t = sanitizeText(b.innerText || b.textContent || "");
            if (t) parts.push(t);
          }
        });
        if (parts.length > 0) {
          structured = sanitizeText(parts.join("\n\n"));
        }
      }
    } else {
      // User message
      const userBlocks = node.querySelectorAll('.whitespace-pre-wrap, [class*="font-user-message"]');
      if (userBlocks && userBlocks.length > 0) {
        const parts = [];
        userBlocks.forEach(b => {
          const hasMatchedParent = Array.from(userBlocks).some(other => other !== b && other.contains(b));
          if (!hasMatchedParent) {
            const t = sanitizeText(b.innerText || b.textContent || "");
            if (t) parts.push(t);
          }
        });
        if (parts.length > 0) {
          structured = sanitizeText(parts.join("\n\n"));
        }
      }
    }

    // Direct fallback from node text
    const raw = sanitizeText(node.innerText || node.textContent || "");

    // Always prefer the more complete text representation to prevent any trimming
    if (structured && structured.length >= raw.length * 0.8) {
      return structured;
    }
    return raw || structured;
  }

  // Helper to convert an image element to a base64 data URL
  function getImgDataUrl(img) {
    if (!img) return "";
    if (img.src && img.src.startsWith("data:image/")) return img.src;
    try {
      const w = img.naturalWidth || img.width || 0;
      const h = img.naturalHeight || img.height || 0;
      if (w > 0 && h > 0) {
        const canvas = document.createElement("canvas");
        canvas.width = Math.min(w, 1200);
        canvas.height = Math.min(h, 1200);
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        return canvas.toDataURL("image/png");
      }
    } catch (e) {}
    return img.src || "";
  }

  // 5. Extract files, artifacts, and attachments from turns and artifact panels
  function extractFilesAndAttachments(items, convId) {
    const files = [];
    const seenFiles = new Set();
    let userAttachIdx = 1;
    let assistantMediaIdx = 1;

    // A. Extract attachments from turns (both user and assistant)
    items.forEach(({ el, role }, itemIdx) => {
      const turnSeq = itemIdx + 1;

      if (role === "user") {
        // Look for image uploads in user turn
        const imgs = el.querySelectorAll("img");
        imgs.forEach(img => {
          if ((img.width && img.width < 40) || (img.naturalWidth && img.naturalWidth < 40)) return;
          const dataUrl = getImgDataUrl(img);
          if (!dataUrl) return;

          let name = img.alt || "";
          const match = name.match(/[\w\-.]+\.(?:png|jpe?g|gif|webp)/i);
          if (match) {
            name = match[0];
          } else {
            name = `user_image_${userAttachIdx}.png`;
            userAttachIdx++;
          }

          if (!seenFiles.has(name)) {
            seenFiles.add(name);
            files.push({
              name: name,
              path: `attachments/${name}`,
              type: "image",
              content: dataUrl,
              role: "user",
              turn_sequence: turnSeq,
              is_attachment: true
            });
          }
        });

        // Look for document attachment chips (PDFs, MD files, docs)
        const fileChips = el.querySelectorAll('[data-testid*="attachment"], [data-testid*="file"], [class*="Attachment"], [class*="FileThumbnail"], [class*="thumbnail"], [class*="file-upload"]');
        fileChips.forEach(chip => {
          const chipText = (chip.innerText || chip.textContent || "").trim();
          const match = chipText.match(/([\w\-.\s]+\.(?:pdf|md|markdown|txt|csv|json|py|ts|js|docx?|xlsx?))/i);
          if (match) {
            const rawName = match[1].trim();
            const safeName = rawName.replace(/\s+/g, "_");
            if (!seenFiles.has(safeName)) {
              seenFiles.add(safeName);
              const ext = safeName.split(".").pop().toLowerCase();
              files.push({
                name: safeName,
                path: `attachments/${safeName}`,
                type: ext,
                content: chipText,
                role: "user",
                turn_sequence: turnSeq,
                is_attachment: true
              });
            }
          }
        });
      } else if (role === "assistant") {
        // Look for SVGs (Mermaid diagrams, flowcharts, graphics)
        const svgs = el.querySelectorAll("svg");
        svgs.forEach(svg => {
          const rect = svg.getBoundingClientRect();
          if (rect.width < 60 || rect.height < 60) return;
          try {
            const svgXml = new XMLSerializer().serializeToString(svg);
            if (svgXml && svgXml.length > 100) {
              const name = `diagram_${assistantMediaIdx}.svg`;
              assistantMediaIdx++;
              if (!seenFiles.has(name)) {
                seenFiles.add(name);
                files.push({
                  name: name,
                  path: `attachments/${name}`,
                  type: "svg",
                  content: svgXml,
                  role: "assistant",
                  turn_sequence: turnSeq,
                  is_attachment: true
                });
              }
            }
          } catch (e) {}
        });

        // Look for generated images in assistant turn
        const imgs = el.querySelectorAll("img");
        imgs.forEach(img => {
          if ((img.width && img.width < 50) || (img.naturalWidth && img.naturalWidth < 50)) return;
          const dataUrl = getImgDataUrl(img);
          if (!dataUrl) return;

          const name = `assistant_image_${assistantMediaIdx}.png`;
          assistantMediaIdx++;
          if (!seenFiles.has(name)) {
            seenFiles.add(name);
            files.push({
              name: name,
              path: `attachments/${name}`,
              type: "image",
              content: dataUrl,
              role: "assistant",
              turn_sequence: turnSeq,
              is_attachment: true
            });
          }
        });

        // Look for code blocks that represent standalone files (e.g. README.md, scripts)
        const codeBlocks = el.querySelectorAll("pre code, pre, .code-block__code");
        codeBlocks.forEach(codeEl => {
          const codeText = (codeEl.innerText || codeEl.textContent || "").trim();
          if (codeText.length < 20) return;

          let foundName = "";
          const header = codeEl.closest("pre") ? (codeEl.closest("pre").previousElementSibling || codeEl.closest("pre").querySelector('[class*="header"], [class*="filename"]')) : null;
          if (header) {
            const hText = (header.innerText || header.textContent || "").trim();
            const m = hText.match(/([\w\-.]+\.(?:md|markdown|py|js|ts|json|sh|html|css|yaml|yml|csv|sql|txt))/i);
            if (m) foundName = m[1];
          }

          if (!foundName) {
            const firstLine = codeText.split("\n")[0] || "";
            const m = firstLine.match(/^(?:#|\/\/|\/\*|<!--)\s*(?:filename:?\s*)?([\w\-.]+\.(?:md|markdown|py|js|ts|json|sh|html|css|yaml|yml|csv|sql|txt))/i);
            if (m) foundName = m[1];
          }

          if (!foundName && (codeText.startsWith("# ") || codeText.includes("\n# ")) && (codeText.toLowerCase().includes("readme") || codeText.length > 200)) {
            foundName = "README.md";
          }

          if (foundName) {
            const safeName = foundName.trim();
            if (!seenFiles.has(safeName)) {
              seenFiles.add(safeName);
              const ext = safeName.split(".").pop().toLowerCase();
              files.push({
                name: safeName,
                path: safeName,
                type: ext,
                content: codeText,
                role: "assistant",
                turn_sequence: turnSeq,
                is_artifact: true
              });
            }
          }
        });
      }
    });

    // B. Extract from Active Claude Artifact Side Panel / View (if present)
    const artifactPanels = document.querySelectorAll('[data-testid="artifact-content"], .ant-artifact-view, div[class*="artifact-view"], div[class*="ArtifactView"]');
    artifactPanels.forEach(panel => {
      let title = "";
      const titleEl = document.querySelector('[data-testid*="artifact-title"], [class*="artifact-title"], div[class*="Artifact"] h3, div[class*="Artifact"] [class*="title"]');
      if (titleEl) {
        title = (titleEl.innerText || titleEl.textContent || "").trim();
      }
      if (!title) title = "README.md";

      const match = title.match(/([\w\-.]+\.(?:md|markdown|py|js|ts|json|sh|html|css|yaml|yml|csv|sql|txt))/i);
      const filename = match ? match[1] : (title.includes(".") ? title : `${title.replace(/\s+/g, "_")}.md`);

      let content = "";
      const viewLines = panel.querySelectorAll(".view-line");
      if (viewLines && viewLines.length > 0) {
        content = Array.from(viewLines).map(l => l.textContent).join("\n");
      } else {
        const code = panel.querySelector("pre, code, textarea");
        if (code) {
          content = (code.innerText || code.value || code.textContent || "").trim();
        } else {
          content = (panel.innerText || panel.textContent || "").trim();
        }
      }

      if (content && content.length > 10 && !seenFiles.has(filename)) {
        seenFiles.add(filename);
        const ext = filename.split(".").pop().toLowerCase();
        files.push({
          name: filename,
          path: filename,
          type: ext,
          content: content,
          role: "assistant",
          is_artifact: true
        });
      }
    });

    return files;
  }

  // 6. Extract message sequence & files from the DOM
  function extractConversation(convId) {
    const messages = [];

    // Anthropic turn selectors
    const userElements = Array.from(document.querySelectorAll('[data-testid="user-message"], .font-user-message'));
    const assistantElements = Array.from(document.querySelectorAll('[data-testid="assistant-message"], .font-claude-message, .font-claude-response, div.standard-markdown'));

    const topUsers = userElements.filter(el => !userElements.some(other => other !== el && other.contains(el)));
    const topAssistants = assistantElements.filter(el => !assistantElements.some(other => other !== el && other.contains(el)));

    if (topUsers.length === 0 && topAssistants.length === 0) {
      return { messages, files: [] };
    }

    const items = [];
    topUsers.forEach(el => items.push({ el, role: "user" }));
    topAssistants.forEach(el => items.push({ el, role: "assistant" }));

    items.sort((a, b) => {
      const pos = a.el.compareDocumentPosition(b.el);
      if (pos & Node.DOCUMENT_POSITION_FOLLOWING) return -1;
      if (pos & Node.DOCUMENT_POSITION_PRECEDING) return 1;
      return 0;
    });

    let seq = 1;
    let prevTextHash = "";

    items.forEach(({ el, role }) => {
      const text = extractCleanText(el, role === "assistant");
      if (!text || text.length === 0) return;

      const hashKey = `${role}:${text}`;
      if (hashKey === prevTextHash) return;
      prevTextHash = hashKey;

      messages.push({
        id: `${convId}_msg_${seq}_${role}`,
        sequence: seq,
        role: role,
        content: text
      });
      seq++;
    });

    const files = extractFilesAndAttachments(items, convId);
    return { messages, files };
  }

  // 7. Fast non-blocking streaming check (simple attribute/button check, no :has)
  function checkIsStreaming() {
    const stopBtn = document.querySelector('button[aria-label*="Stop" i], button[data-testid*="stop-button" i]');
    if (stopBtn) return true;

    const streamAttr = document.querySelector('[data-is-streaming="true"]');
    if (streamAttr) return true;

    return false;
  }

  // 8. Capture and send conversation snapshot
  async function triggerCapture(force = false) {
    const convId = getConversationId();
    if (!convId || convId === "new") return;

    const { messages, files } = extractConversation(convId);
    if (!messages || messages.length === 0) return;

    const fullText = messages.map(m => `${m.role}:${m.content}`).join("\n") + "\n" + (files || []).map(f => `${f.name}:${(f.content || "").slice(0, 100)}`).join("\n");
    const hash = await sha256(fullText);

    if (hash === lastCapturedHash && !force) {
      return;
    }

    lastCapturedHash = hash;
    updateHud("syncing");

    const payload = {
      conversation_id: convId,
      title: getConversationTitle(),
      platform: "claude",
      url: window.location.href,
      messages: messages,
      files: files,
      is_final: !checkIsStreaming(),
      captured_at: new Date().toISOString()
    };

    try {
      chrome.runtime.sendMessage(
        { type: "INGEST_CONVERSATION", payload, force },
        (res) => {
          if (chrome.runtime.lastError) {
            updateHud("offline", { error: chrome.runtime.lastError.message });
            return;
          }
          if (res && res.queued) {
            pendingCount = res.pendingCount || 0;
            if (pendingCount > 1) {
              updateHud("offline", { pendingCount });
            } else {
              updateHud("synced");
            }
          }
        }
      );
    } catch (e) {
      updateHud("offline");
    }
  }

  // 8. Lightweight, throttled check for streaming lifecycle
  function checkChatState() {
    const active = checkIsStreaming();

    if (active) {
      if (!isStreaming) {
        isStreaming = true;
        updateHud("streaming");
      }
      return; // Do nothing while Claude is actively outputting text
    }

    if (isStreaming && !active) {
      // Claude just finished outputting response!
      isStreaming = false;
      if (finalizeTimer) clearTimeout(finalizeTimer);
      // Wait 800ms for markdown DOM to settle before capturing
      finalizeTimer = setTimeout(() => {
        triggerCapture(true);
      }, 800);
      return;
    }
  }

  // 9. Throttled DOM Mutation Observer (ignores HUD and throttles to 2x/sec)
  function onDomMutated(mutations) {
    let hasPageMutation = false;
    for (let i = 0; i < mutations.length; i++) {
      const target = mutations[i].target;
      if (target && target.nodeType === 1) {
        if (target.id === "chatsave-hud-root" || (target.closest && target.closest("#chatsave-hud-root"))) {
          continue;
        }
      }
      hasPageMutation = true;
      break;
    }
    if (!hasPageMutation) return;

    // Throttle to at most one lightweight check every 400ms
    if (observerThrottle) return;
    observerThrottle = setTimeout(() => {
      observerThrottle = null;
      checkChatState();
    }, 400);
  }

  // 10. URL change monitor (SPA Navigation)
  let lastUrl = window.location.href;
  setInterval(() => {
    if (window.location.href !== lastUrl) {
      lastUrl = window.location.href;
      lastCapturedHash = "";
      updateHud("idle");
      setTimeout(() => triggerCapture(false), 1500);
    }
  }, 1000);

  // 11. Floating HUD on Claude.ai
  function createHud() {
    if (document.getElementById("chatsave-hud-root")) return;

    const root = document.createElement("div");
    root.id = "chatsave-hud-root";
    root.className = "chatsave-hud";

    root.innerHTML = `
      <div class="chatsave-badge" id="chatsave-badge">
        <span class="chatsave-dot"></span>
        <span class="chatsave-label">Chat-Save</span>
      </div>
      <div class="chatsave-popover" id="chatsave-popover" style="display: none;">
        <div class="chatsave-header">
          <strong>Chat-Save Connector</strong>
          <span class="chatsave-close" id="chatsave-popover-close">✕</span>
        </div>
        <div class="chatsave-body">
          <div class="chatsave-row">
            <span>Status:</span>
            <strong id="chatsave-pop-status">Active</strong>
          </div>
          <div class="chatsave-row">
            <span>Thread ID:</span>
            <code id="chatsave-pop-thread">-</code>
          </div>
          <div class="chatsave-row">
            <span>Last Receipt:</span>
            <code id="chatsave-pop-receipt">None yet</code>
          </div>
          <div class="chatsave-row" id="chatsave-pending-row" style="display:none;">
            <span>Offline Queue:</span>
            <strong id="chatsave-pop-queue" style="color: #eab308;">0 pending</strong>
          </div>
        </div>
        <div class="chatsave-footer">
          <button id="chatsave-btn-sync" class="chatsave-btn">Sync Now</button>
        </div>
      </div>
    `;

    document.body.appendChild(root);
    hudElement = root;

    const badge = root.querySelector("#chatsave-badge");
    const popover = root.querySelector("#chatsave-popover");
    const closeBtn = root.querySelector("#chatsave-popover-close");
    const syncBtn = root.querySelector("#chatsave-btn-sync");

    badge.addEventListener("click", () => {
      popover.style.display = popover.style.display === "none" ? "block" : "none";
      updatePopoverData();
    });

    closeBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      popover.style.display = "none";
    });

    syncBtn.addEventListener("click", () => {
      syncBtn.disabled = true;
      syncBtn.textContent = "Syncing...";
      chrome.runtime.sendMessage({ type: "SYNC_NOW" }, () => {
        triggerCapture(true);
        setTimeout(() => {
          syncBtn.disabled = false;
          syncBtn.textContent = "Sync Now";
        }, 1000);
      });
    });
  }

  function updateHud(status, data = {}) {
    // Prevent redundant DOM updates that trigger mutation cascades
    if (hudStatus === status && status === "streaming") return;
    hudStatus = status;

    if (!hudElement) return;
    const badge = hudElement.querySelector("#chatsave-badge");
    const label = hudElement.querySelector(".chatsave-label");
    const dot = hudElement.querySelector(".chatsave-dot");

    badge.className = "chatsave-badge " + status;

    if (status === "streaming") {
      label.textContent = "Claude typing...";
      dot.style.background = "#3b82f6";
    } else if (status === "syncing") {
      label.textContent = "Saving...";
      dot.style.background = "#6366f1";
    } else if (status === "synced") {
      label.textContent = "Saved ✓";
      dot.style.background = "#10b981";
      setTimeout(() => {
        if (hudStatus === "synced") {
          label.textContent = "Chat-Save";
        }
      }, 4000);
    } else if (status === "offline") {
      const count = data.pendingCount !== undefined ? data.pendingCount : pendingCount;
      label.textContent = count > 0 ? `Offline (${count} queued)` : "Offline";
      dot.style.background = "#f59e0b";
    } else if (status === "error") {
      label.textContent = "Sync Error ⚠";
      dot.style.background = "#ef4444";
    } else {
      label.textContent = "Chat-Save";
      dot.style.background = "#10b981";
    }

    updatePopoverData();
  }

  function updatePopoverData() {
    if (!hudElement) return;
    const popStatus = hudElement.querySelector("#chatsave-pop-status");
    const popThread = hudElement.querySelector("#chatsave-pop-thread");
    const popReceipt = hudElement.querySelector("#chatsave-pop-receipt");
    const pendingRow = hudElement.querySelector("#chatsave-pending-row");
    const popQueue = hudElement.querySelector("#chatsave-pop-queue");

    const convId = getConversationId();
    popThread.textContent = convId ? (convId.slice(0, 12) + "...") : "None";
    popStatus.textContent = hudStatus.toUpperCase();

    if (lastReceipt) {
      popReceipt.textContent = `${lastReceipt.receipt_id || "OK"} (${lastReceipt.saved_messages || 0} msgs)`;
    }

    if (pendingCount > 0) {
      pendingRow.style.display = "flex";
      popQueue.textContent = `${pendingCount} item(s) waiting`;
    } else {
      pendingRow.style.display = "none";
    }
  }

  // 12. Listen for background broadcast events
  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === "SYNC_SUCCESS") {
      lastReceipt = msg.receipt;
      pendingCount = 0;
      updateHud("synced");
    } else if (msg.type === "SYNC_ERROR") {
      pendingCount = msg.pendingCount || 1;
      updateHud("offline", { error: msg.error, pendingCount });
    } else if (msg.type === "QUEUE_UPDATED") {
      pendingCount = msg.pendingCount;
      if (pendingCount > 0 && hudStatus !== "syncing") {
        updateHud("offline", { pendingCount });
      } else if (pendingCount === 0 && hudStatus === "offline") {
        updateHud("synced");
      }
    }
  });

  // 13. Initialization
  function init() {
    createHud();

    // Start MutationObserver on chat body
    const observer = new MutationObserver(onDomMutated);
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    // Initial capture check after page loads
    setTimeout(() => {
      triggerCapture(false);
    }, 2000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
