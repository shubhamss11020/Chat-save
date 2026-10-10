/**
 * Chat-Save Content Script
 * Injected into https://claude.ai/*
 * Captures submitted prompts, monitors assistant streaming to completion,
 * extracts canonical transcripts, and renders a persistent save-status HUD.
 */

(() => {
  let currentConversationId = "";
  let isStreaming = false;
  let debounceTimer = null;
  let lastCapturedHash = "";
  let hudElement = null;
  let hudStatus = "idle"; // "idle" | "streaming" | "syncing" | "synced" | "offline" | "error"
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
    // Strategy 1: Page title
    const docTitle = document.title.replace(/\s*·\s*Claude\s*$/i, "").trim();
    if (docTitle && docTitle !== "Claude") return docTitle;

    // Strategy 2: Chat header title button/element
    const headerTitleEl = document.querySelector('header button[data-testid*="title"], header .text-ellipsis, [data-testid="chat-title"]');
    if (headerTitleEl && headerTitleEl.textContent.trim()) {
      return headerTitleEl.textContent.trim();
    }

    // Strategy 3: First user message snippet
    const firstUserMsg = document.querySelector('[data-testid*="user-message"], .font-user-message');
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

  // 4. Robust extraction of message turns from Claude web DOM
  function extractMessages(convId) {
    const messages = [];

    // Strategy A: Known Claude message container selectors
    // Anthropic uses .font-user-message and .font-claude-message / .font-claude-response
    const userNodes = Array.from(document.querySelectorAll('[data-testid*="user-message"], .font-user-message'));
    const assistantNodes = Array.from(document.querySelectorAll('[data-testid*="assistant-message"], .font-claude-message, .font-claude-response, [data-is-streaming]'));

    // Strategy B: General conversational blocks if specific testids/classes are absent
    if (userNodes.length === 0 && assistantNodes.length === 0) {
      // Fallback: look for alternating prose elements or message rows
      const allRows = Array.from(document.querySelectorAll('div[data-testid*="chat-message"], div.group:has(button[aria-label*="Copy"])'));
      allRows.forEach((row, idx) => {
        const text = row.innerText.trim();
        if (!text) return;
        const isAssistant = Boolean(row.querySelector('button[aria-label*="Copy"], button[aria-label*="Good response"]'));
        messages.push({
          id: `${convId}_turn_${idx + 1}`,
          sequence: idx + 1,
          role: isAssistant ? "assistant" : "user",
          content: text
        });
      });
      return messages;
    }

    // Gather elements and sort them by their appearance order in the DOM
    const combined = [];
    userNodes.forEach(el => combined.push({ el, role: "user" }));
    assistantNodes.forEach(el => combined.push({ el, role: "assistant" }));

    // Sort by document position
    combined.sort((a, b) => {
      const pos = a.el.compareDocumentPosition(b.el);
      if (pos & Node.DOCUMENT_POSITION_FOLLOWING) return -1;
      if (pos & Node.DOCUMENT_POSITION_PRECEDING) return 1;
      return 0;
    });

    let seq = 1;
    let lastRole = null;
    let lastContent = "";

    combined.forEach(({ el, role }) => {
      const content = el.innerText.trim();
      if (!content) return;

      // Avoid immediate consecutive identical chunks from nested wrappers
      if (role === lastRole && content === lastContent) return;
      if (role === lastRole && content.startsWith(lastContent)) {
        // Replace previous partial with complete wrapper content
        if (messages.length > 0) {
          messages[messages.length - 1].content = content;
          lastContent = content;
          return;
        }
      }

      messages.push({
        id: `${convId}_msg_${seq}_${role}`,
        sequence: seq,
        role: role,
        content: content
      });

      lastRole = role;
      lastContent = content;
      seq++;
    });

    return messages;
  }

  // 5. Detect if Claude is currently streaming response
  function checkIsStreaming() {
    // Indicator 1: Stop button present
    const stopBtn = document.querySelector('button[aria-label*="Stop"], button[data-testid*="stop"], button:has(rect)');
    // Indicator 2: Claude streaming attribute
    const streamAttr = document.querySelector('[data-is-streaming="true"]');
    // Indicator 3: Pulsing cursor
    const cursor = document.querySelector('.cursor-pulse, .animate-pulse');

    return Boolean(stopBtn || streamAttr || cursor);
  }

  // 6. Capture and transmit conversation snapshot
  async function triggerCapture(force = false) {
    const convId = getConversationId();
    if (!convId || convId === "new") return;

    const messages = extractMessages(convId);
    if (messages.length === 0) return;

    // Build fingerprint of current conversation text
    const fullText = messages.map(m => `${m.role}:${m.content}`).join("\n");
    const hash = await sha256(fullText);

    if (hash === lastCapturedHash && !force) {
      return; // No changes to transmit
    }

    lastCapturedHash = hash;
    updateHud("syncing");

    const payload = {
      conversation_id: convId,
      title: getConversationTitle(),
      platform: "claude",
      url: window.location.href,
      messages: messages,
      is_final: !checkIsStreaming(),
      captured_at: new Date().toISOString()
    };

    chrome.runtime.sendMessage(
      { type: "INGEST_CONVERSATION", payload, force },
      (res) => {
        if (chrome.runtime.lastError) {
          console.warn("[Chat-Save] Extension background error:", chrome.runtime.lastError.message);
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
  }

  // 7. Debounced DOM observer for chat updates
  function onDomMutated() {
    const activeStreaming = checkIsStreaming();

    if (activeStreaming) {
      isStreaming = true;
      updateHud("streaming");
      // Clear pending finalize timer
      if (debounceTimer) clearTimeout(debounceTimer);
      return;
    }

    if (isStreaming && !activeStreaming) {
      // Just stopped streaming! Finalize promptly
      isStreaming = false;
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        triggerCapture(true);
      }, 800);
      return;
    }

    // Normal typing or DOM update debounce
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      triggerCapture(false);
    }, 1500);
  }

  // 8. Capture prompt submission immediately on Enter / Click
  function setupInputListeners() {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        // User hit Enter on input
        setTimeout(() => {
          triggerCapture(false);
        }, 600);
      }
    }, true);

    document.addEventListener("click", (e) => {
      const target = e.target;
      const sendBtn = target.closest('button[aria-label*="Send"], button[data-testid*="send"], button:has(path)');
      if (sendBtn) {
        setTimeout(() => {
          triggerCapture(false);
        }, 600);
      }
    }, true);
  }

  // 9. URL change monitor (Single Page App navigation)
  let lastUrl = window.location.href;
  setInterval(() => {
    if (window.location.href !== lastUrl) {
      lastUrl = window.location.href;
      currentConversationId = getConversationId();
      lastCapturedHash = "";
      updateHud("idle");
      setTimeout(() => triggerCapture(false), 1200);
    }
  }, 500);

  // 10. Floating HUD on Claude.ai
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
      const count = data.pendingCount || pendingCount;
      label.textContent = `Offline (${count} queued)`;
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

  // 11. Listen for background broadcast events
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

  // 12. Main Initialization
  function init() {
    createHud();
    setupInputListeners();

    // Start MutationObserver on chat body
    const observer = new MutationObserver(onDomMutated);
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });

    // Initial check
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
