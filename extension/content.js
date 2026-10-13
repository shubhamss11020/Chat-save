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
  let currentQueuedIds = new Set();
  let currentDlqIds = new Set();
  let isContextInvalidated = false;
  let urlCheckInterval = null;
  let sidebarInterval = null;
  let domObserver = null;

  // Window error boundary to silence Extension context invalidated errors
  window.addEventListener("error", (e) => {
    if (e.message && e.message.includes("Extension context invalidated")) {
      markContextInvalidated();
      e.preventDefault();
      e.stopImmediatePropagation();
    }
  });

  function markContextInvalidated() {
    if (isContextInvalidated) return;
    isContextInvalidated = true;
    console.info("[Chat-Save] Extension was reloaded in Chrome. Please refresh this tab (F5) to re-bind real-time sync.");

    if (urlCheckInterval) { clearInterval(urlCheckInterval); urlCheckInterval = null; }
    if (sidebarInterval) { clearInterval(sidebarInterval); sidebarInterval = null; }
    if (observerThrottle) { clearTimeout(observerThrottle); observerThrottle = null; }
    if (finalizeTimer) { clearTimeout(finalizeTimer); finalizeTimer = null; }
    if (domObserver) {
      try { domObserver.disconnect(); } catch (e) {}
      domObserver = null;
    }

    if (hudElement) {
      const badge = hudElement.querySelector("#chatsave-badge");
      const label = hudElement.querySelector(".chatsave-label");
      const dot = hudElement.querySelector(".chatsave-dot");
      if (badge) {
        badge.className = "chatsave-badge offline";
        badge.title = "Extension was reloaded. Please refresh this tab (F5) to resume real-time sync.";
      }
      if (label) label.textContent = "Reloaded (Press F5)";
      if (dot) dot.style.background = "#f59e0b";
    }
  }

  function isExtensionValid() {
    if (isContextInvalidated) return false;
    try {
      if (typeof chrome === "undefined" || !chrome.runtime || !chrome.runtime.id) {
        markContextInvalidated();
        return false;
      }
      return true;
    } catch (e) {
      markContextInvalidated();
      return false;
    }
  }

  function safeSendMessage(msg, callback) {
    if (!isExtensionValid()) {
      if (callback) callback(null);
      return;
    }
    try {
      chrome.runtime.sendMessage(msg, (res) => {
        try {
          if (chrome.runtime && chrome.runtime.lastError) {
            const err = chrome.runtime.lastError.message || "";
            if (err.includes("Extension context invalidated") || err.includes("Receiving end does not exist")) {
              markContextInvalidated();
            }
          }
        } catch (e) {
          markContextInvalidated();
        }
        if (callback && !isContextInvalidated) callback(res);
      });
    } catch (e) {
      markContextInvalidated();
      if (callback) callback(null);
    }
  }

  function safeStorageGet(keys) {
    return new Promise((resolve) => {
      if (!isExtensionValid()) {
        resolve({});
        return;
      }
      try {
        chrome.storage.local.get(keys, (res) => {
          try {
            if (chrome.runtime && chrome.runtime.lastError) { /* consumed */ }
          } catch (e) {}
          resolve(res || {});
        });
      } catch (e) {
        markContextInvalidated();
        resolve({});
      }
    });
  }

  function safeStorageSet(items) {
    return new Promise((resolve) => {
      if (!isExtensionValid()) {
        resolve();
        return;
      }
      try {
        chrome.storage.local.set(items, () => {
          try {
            if (chrome.runtime && chrome.runtime.lastError) { /* consumed */ }
          } catch (e) {}
          resolve();
        });
      } catch (e) {
        markContextInvalidated();
        resolve();
      }
    });
  }

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
    // Strip Anthropic unsupported device tool-block placeholders (fenced and unfenced)
    s = s.replace(/```[a-zA-Z0-9_-]*\s*This block is not supported on your current device yet\.?\s*```/gi, "");
    s = s.replace(/(?:^|\n)\s*This block is not supported on your current device yet\.?\s*(?=\n|$)/gi, "\n");
    s = s.replace(/This block is not supported on your current device yet\.?/gi, "");
    // Strip empty markdown code fences (```\n``` or ```xyz\n``` with only whitespace)
    while (/```[a-zA-Z0-9_-]*\s*```/.test(s)) {
      s = s.replace(/```[a-zA-Z0-9_-]*\s*```/g, "");
    }
    s = s.replace(/\n{3,}/g, "\n\n");
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
            const raw = (b.innerText || b.textContent || "").trim();
            if (raw.toLowerCase() === "this block is not supported on your current device yet." ||
                raw.toLowerCase().startsWith("this block is not supported on your current device yet")) {
              return; // skip placeholder element
            }
            const t = sanitizeText(raw);
            if (t) parts.push(t);
          }
        });
        if (parts.length > 0) {
          structured = sanitizeText(parts.join("\n\n"));
        }
      }
    } else {
      // User message: clone and remove attachment chips so chip labels don't pollute prompt text
      const clone = node.cloneNode(true);
      clone.querySelectorAll('[data-testid*="attachment"], [data-testid*="file"], [class*="Attachment"], [class*="FileThumbnail"], [class*="thumbnail"], [class*="file-upload"]').forEach(c => c.remove());
      const userBlocks = clone.querySelectorAll('.whitespace-pre-wrap, [class*="font-user-message"]');
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
      if (!structured) {
        structured = sanitizeText(clone.innerText || clone.textContent || "");
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

  // Helper to determine canonical MIME type (never generic 'image', 'svg', or extension-less)
  function getCanonicalMimeType(name, dataUrl, fallback = "application/octet-stream") {
    if (dataUrl && typeof dataUrl === "string" && dataUrl.startsWith("data:")) {
      const match = dataUrl.match(/^data:([^;,]+)/);
      if (match && match[1] && match[1].includes("/")) {
        return match[1].toLowerCase();
      }
    }
    const ext = (name || "").split(".").pop().toLowerCase();
    const mimeMap = {
      png: "image/png",
      jpg: "image/jpeg",
      jpeg: "image/jpeg",
      gif: "image/gif",
      webp: "image/webp",
      svg: "image/svg+xml",
      pdf: "application/pdf",
      txt: "text/plain",
      md: "text/markdown",
      markdown: "text/markdown",
      json: "application/json",
      csv: "text/csv",
      html: "text/html",
      mp4: "video/mp4",
      mp3: "audio/mpeg"
    };
    return mimeMap[ext] || fallback;
  }

  // Session cache of real binary files uploaded by user (PDFs, images, documents)
  const recentUploadedFiles = new Map();

  function cacheUploadedFile(file) {
    if (!file || !file.name) return;
    try {
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result;
        if (typeof dataUrl === "string" && dataUrl.startsWith("data:")) {
          const rawName = file.name;
          const safeName = rawName.replace(/\s+/g, "_");
          const entry = {
            name: rawName,
            safeName: safeName,
            type: file.type || getCanonicalMimeType(rawName, dataUrl),
            size: file.size,
            dataUrl: dataUrl
          };
          recentUploadedFiles.set(rawName.toLowerCase(), entry);
          recentUploadedFiles.set(safeName.toLowerCase(), entry);
        }
      };
      reader.readAsDataURL(file);
    } catch (e) {
      console.warn("[Chat-Save] Could not cache uploaded file:", e);
    }
  }

  // Intercept file picker dialogs
  document.addEventListener("change", (e) => {
    if (e.target && e.target.type === "file" && e.target.files) {
      for (let i = 0; i < e.target.files.length; i++) {
        cacheUploadedFile(e.target.files[i]);
      }
    }
  }, true);

  // Intercept drag and drop files
  document.addEventListener("drop", (e) => {
    if (e.dataTransfer && e.dataTransfer.files) {
      for (let i = 0; i < e.dataTransfer.files.length; i++) {
        cacheUploadedFile(e.dataTransfer.files[i]);
      }
    }
  }, true);

  // Intercept pasted files
  document.addEventListener("paste", (e) => {
    if (e.clipboardData && e.clipboardData.files) {
      for (let i = 0; i < e.clipboardData.files.length; i++) {
        cacheUploadedFile(e.clipboardData.files[i]);
      }
    }
  }, true);

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
            const mime = getCanonicalMimeType(name, dataUrl, "image/png");
            files.push({
              name: name,
              path: `attachments/${name}`,
              type: mime,
              url: (img.src && img.src.startsWith("http")) ? img.src : undefined,
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

              // Check if chip or child contains an href or download URL
              let fileUrl = "";
              const anchor = chip.tagName === "A" ? chip : chip.querySelector("a");
              if (anchor && anchor.href && !anchor.href.startsWith("javascript:")) {
                fileUrl = anchor.href;
              }

              // Check if we captured the genuine binary data during this session
              const cached = recentUploadedFiles.get(safeName.toLowerCase()) || recentUploadedFiles.get(rawName.toLowerCase());
              const realBinary = cached ? cached.dataUrl : "";

              const mime = getCanonicalMimeType(safeName, realBinary, "application/octet-stream");
              files.push({
                name: safeName,
                path: `attachments/${safeName}`,
                url: fileUrl || undefined,
                type: mime,
                content: realBinary, // Genuine binary data URL or empty, never filename string
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
                  type: "image/svg+xml",
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
            const mime = getCanonicalMimeType(name, dataUrl, "image/png");
            files.push({
              name: name,
              path: `attachments/${name}`,
              type: mime,
              url: (img.src && img.src.startsWith("http")) ? img.src : undefined,
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
    try {
      const artifactPanels = document.querySelectorAll('[data-testid="artifact-content"], .ant-artifact-view, div[class*="artifact-view"], div[class*="ArtifactView"]');
      artifactPanels.forEach(panel => {
        try {
          if (!panel || panel.nodeType !== 1 || panel.tagName === "IFRAME") return;
          let title = "";
          const titleEl = document.querySelector('[data-testid*="artifact-title"], [class*="artifact-title"], div[class*="Artifact"] h3, div[class*="Artifact"] [class*="title"]');
          if (titleEl) {
            title = (titleEl.innerText || titleEl.textContent || "").trim();
          }
          if (!title) title = "README.md";

          const match = title.match(/([\w\-.]+\.(?:md|markdown|py|js|ts|json|sh|html|css|yaml|yml|csv|sql|txt))/i);
          const filename = match ? match[1] : (title.includes(".") ? title : `${title.replace(/\s+/g, "_")}.md`);

          let content = "";
          if (typeof panel.querySelectorAll === "function") {
            const viewLines = panel.querySelectorAll(".view-line");
            if (viewLines && viewLines.length > 0) {
              content = Array.from(viewLines).map(l => l.textContent || "").join("\n");
            }
          }
          if (!content && typeof panel.querySelector === "function") {
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
        } catch (panelErr) {
          // ignore any cross-origin frame or element access restriction safely
        }
      });
    } catch (e) {}

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

    let files = [];
    try {
      files = extractFilesAndAttachments(items, convId);
    } catch (err) {
      files = [];
    }
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
    if (!isExtensionValid()) return;
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

    safeSendMessage(
      { type: "INGEST_CONVERSATION", payload, force },
      (res) => {
        if (!res) {
          updateHud("offline");
          return;
        }
        if (res.queued) {
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
        if (target.id === "chatsave-hud-root" ||
            (target.closest && target.closest("#chatsave-hud-root")) ||
            (target.classList && target.classList.contains("chatsave-sidebar-dot"))) {
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
      updateSidebarDots();
    }, 400);
  }

  // 10. URL change monitor (SPA Navigation)
  let lastUrl = window.location.href;
  urlCheckInterval = setInterval(() => {
    if (!isExtensionValid()) return;
    if (window.location.href !== lastUrl) {
      lastUrl = window.location.href;
      lastCapturedHash = "";
      updateHud("idle");
      fetchQueueStateAndUpdateSidebar();
      setTimeout(() => {
        if (isExtensionValid()) triggerCapture(false);
      }, 1500);
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
          <strong>Chat-Save</strong>
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
            <span>Last save:</span>
            <code id="chatsave-pop-receipt">None yet</code>
          </div>
          <div class="chatsave-row" id="chatsave-pending-row" style="display:none;">
            <span>Waiting to save:</span>
            <strong id="chatsave-pop-queue">0</strong>
          </div>
        </div>
        <div class="chatsave-footer" style="display: flex; gap: 6px;">
          <button id="chatsave-btn-sync" class="chatsave-btn" style="flex: 1;">Sync Thread</button>
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
      if (!isExtensionValid()) return;
      syncBtn.disabled = true;
      syncBtn.textContent = "Syncing...";
      safeSendMessage({ type: "SYNC_NOW" }, () => {
        triggerCapture(true);
        setTimeout(() => {
          syncBtn.disabled = false;
          syncBtn.textContent = "Sync Thread";
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
      label.textContent = count > 0 ? `Waiting to save (${count})` : "Waiting to save";
      dot.style.background = "#f59e0b";
    } else if (status === "error") {
      label.textContent = "Could not save";
      dot.style.background = "#ef4444";
    } else {
      label.textContent = "Chat-Save";
      dot.style.background = "#10b981";
    }

    updatePopoverData();
  }

  const HUD_LABELS = {
    idle: "Connected",
    streaming: "Claude is replying",
    syncing: "Saving",
    synced: "Up to date",
    offline: "Waiting to save",
    error: "Could not save",
  };

  function updatePopoverData() {
    if (!hudElement) return;
    const popStatus = hudElement.querySelector("#chatsave-pop-status");
    const popThread = hudElement.querySelector("#chatsave-pop-thread");
    const popReceipt = hudElement.querySelector("#chatsave-pop-receipt");
    const pendingRow = hudElement.querySelector("#chatsave-pending-row");
    const popQueue = hudElement.querySelector("#chatsave-pop-queue");

    const convId = getConversationId();
    popThread.textContent = convId ? (convId.slice(0, 12) + "...") : "None";
    popStatus.textContent = HUD_LABELS[hudStatus] || "Connected";

    if (lastReceipt) {
      const n = lastReceipt.saved_messages || 0;
      popReceipt.textContent = `${n} message${n === 1 ? "" : "s"} saved`;
    }

    if (pendingCount > 0) {
      pendingRow.style.display = "flex";
      popQueue.textContent = `${pendingCount} conversation(s)`;
    } else {
      pendingRow.style.display = "none";
    }
  }

  // 11b. Claude Sidebar Queue & Sync Status Indicators
  function updateSidebarDots() {
    const links = document.querySelectorAll('a[href*="/chat/"]');
    if (!links || links.length === 0) return;

    links.forEach(link => {
      const href = link.getAttribute("href") || "";
      const match = href.match(/\/chat\/([a-zA-Z0-9_-]+)/);
      if (!match) return;
      const convId = match[1];
      if (convId === "new") return;

      let dot = link.querySelector(".chatsave-sidebar-dot");

      if (currentQueuedIds.has(convId)) {
        if (!dot) {
          dot = document.createElement("span");
          dot.className = "chatsave-sidebar-dot chatsave-dot-queued";
          dot.title = "Waiting to be saved";
          link.appendChild(dot);
        } else if (!dot.classList.contains("chatsave-dot-queued")) {
          dot.className = "chatsave-sidebar-dot chatsave-dot-queued";
          dot.title = "Waiting to be saved";
        }
      } else if (currentDlqIds.has(convId)) {
        if (!dot) {
          dot = document.createElement("span");
          dot.className = "chatsave-sidebar-dot chatsave-dot-dlq";
          dot.title = "Could not be saved. See Chat-Save settings.";
          link.appendChild(dot);
        } else if (!dot.classList.contains("chatsave-dot-dlq")) {
          dot.className = "chatsave-sidebar-dot chatsave-dot-dlq";
          dot.title = "Could not be saved. See Chat-Save settings.";
        }
      } else {
        if (dot) {
          dot.remove();
        }
      }
    });
  }

  function clearSidebarDot(convId) {
    if (!convId) return;
    const links = document.querySelectorAll(`a[href*="/chat/${convId}"]`);
    links.forEach(link => {
      const dot = link.querySelector(".chatsave-sidebar-dot");
      if (dot) {
        dot.className = "chatsave-sidebar-dot chatsave-dot-synced";
        setTimeout(() => {
          if (dot.parentElement) dot.remove();
        }, 500);
      }
    });
  }

  function fetchQueueStateAndUpdateSidebar() {
    safeSendMessage({ type: "GET_QUEUE_STATE" }, (res) => {
      if (!res) return;
      if (Array.isArray(res.queuedIds)) {
        currentQueuedIds = new Set(res.queuedIds);
      }
      if (Array.isArray(res.dlqIds)) {
        currentDlqIds = new Set(res.dlqIds);
      }
      updateSidebarDots();
    });
  }

  // 12. Listen for background broadcast events
  try {
    if (typeof chrome !== "undefined" && chrome.runtime?.onMessage) {
      chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
        if (!isExtensionValid()) return;
        if (msg.type === "SYNC_SUCCESS") {
          lastReceipt = msg.receipt;
          pendingCount = 0;
          updateHud("synced");
          if (msg.conversationId) {
            currentQueuedIds.delete(msg.conversationId);
            currentDlqIds.delete(msg.conversationId);
            clearSidebarDot(msg.conversationId);
          }
          fetchQueueStateAndUpdateSidebar();
        } else if (msg.type === "SYNC_ERROR") {
          pendingCount = msg.pendingCount || 1;
          updateHud("offline", { error: msg.error, pendingCount });
          fetchQueueStateAndUpdateSidebar();
        } else if (msg.type === "DEAD_LETTER_EVENT") {
          if (msg.conversationId) {
            currentQueuedIds.delete(msg.conversationId);
            currentDlqIds.add(msg.conversationId);
          }
          fetchQueueStateAndUpdateSidebar();
        } else if (msg.type === "QUEUE_UPDATED") {
          pendingCount = msg.pendingCount;
          if (Array.isArray(msg.queuedIds)) {
            currentQueuedIds = new Set(msg.queuedIds);
          }
          if (Array.isArray(msg.dlqIds)) {
            currentDlqIds = new Set(msg.dlqIds);
          }
          updateSidebarDots();

          if (pendingCount > 0 && hudStatus !== "syncing") {
            updateHud("offline", { pendingCount });
          } else if (pendingCount === 0 && hudStatus === "offline") {
            updateHud("synced");
          }
        }
      });
    }
  } catch (e) {}

  // 14. Initialization
  function init() {
    if (!isExtensionValid()) return;
    createHud();

    // Fetch initial queue state and draw sidebar dots
    fetchQueueStateAndUpdateSidebar();
    sidebarInterval = setInterval(() => {
      if (!isExtensionValid()) return;
      updateSidebarDots();
    }, 2500);

    // Identity is set by the server from the person's token (Options > Test Connection),
    // so the page no longer guesses a username from the Claude session.

    // Start MutationObserver on chat body
    domObserver = new MutationObserver(onDomMutated);
    domObserver.observe(document.body, {
      childList: true,
      subtree: true
    });

    // Initial capture check on current active page
    setTimeout(() => {
      if (isExtensionValid()) triggerCapture(false);
    }, 2000);

  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
