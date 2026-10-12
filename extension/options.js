/**
 * Options Script for Chat-Save Extension
 */

document.addEventListener("DOMContentLoaded", async () => {
  const serverUrlInput = document.getElementById("serverUrl");
  const authTokenInput = document.getElementById("authToken");
  const userIdInput = document.getElementById("userId");
  const autoSyncCheckbox = document.getElementById("autoSync");
  const btnToggleToken = document.getElementById("btnToggleToken");
  const btnSave = document.getElementById("btnSave");
  const btnTest = document.getElementById("btnTest");
  const alertBox = document.getElementById("alertBox");
  const managedBanner = document.getElementById("managedBanner");

  const queueSummary = document.getElementById("queueSummary");
  const queueTable = document.getElementById("queueTable");
  const queueTbody = document.getElementById("queueTbody");
  const btnRetryQueue = document.getElementById("btnRetryQueue");
  const btnClearQueue = document.getElementById("btnClearQueue");

  // 1. Load settings (managed vs local)
  let managed = {};
  try {
    if (chrome.storage.managed) {
      managed = await chrome.storage.managed.get(null);
    }
  } catch (e) {}

  const local = await chrome.storage.local.get("chatsave_config");
  const localConfig = local.chatsave_config || {};

  serverUrlInput.value = managed.serverUrl || localConfig.serverUrl || "http://localhost:8000";
  authTokenInput.value = managed.authToken || localConfig.authToken || "";
  userIdInput.value = managed.userId || localConfig.userId || "shubham";
  autoSyncCheckbox.checked = managed.autoSync !== undefined ? managed.autoSync : (localConfig.autoSync !== undefined ? localConfig.autoSync : true);

  if (managed.serverUrl || managed.authToken || managed.userId) {
    managedBanner.style.display = "block";
    if (managed.serverUrl) serverUrlInput.disabled = true;
    if (managed.authToken) authTokenInput.disabled = true;
    if (managed.userId) userIdInput.disabled = true;
  }

  // 2. Toggle password visibility
  btnToggleToken.addEventListener("click", () => {
    if (authTokenInput.type === "password") {
      authTokenInput.type = "text";
      btnToggleToken.textContent = "Hide";
    } else {
      authTokenInput.type = "password";
      btnToggleToken.textContent = "Show";
    }
  });

  // 2b. Auto-detect user identity from active Claude session
  const btnAutoDetect = document.getElementById("btnAutoDetect");
  if (btnAutoDetect) {
    btnAutoDetect.addEventListener("click", async () => {
      btnAutoDetect.disabled = true;
      btnAutoDetect.textContent = "Detecting...";

      // Step 1: Check storage cache from content script
      try {
        const stored = await chrome.storage.local.get(["chatsave_detected_user", "chatsave_config"]);
        if (stored.chatsave_detected_user) {
          userIdInput.value = stored.chatsave_detected_user;
          showAlert(`✓ Detected Claude session user: ${stored.chatsave_detected_user}`, "success");
          btnAutoDetect.disabled = false;
          btnAutoDetect.textContent = "Auto-Detect";
          return;
        }
      } catch (e) {}

      // Step 2: Ask background service worker to query active Claude tab
      chrome.runtime.sendMessage({ type: "DETECT_USER" }, async (res) => {
        btnAutoDetect.disabled = false;
        btnAutoDetect.textContent = "Auto-Detect";

        if (chrome.runtime.lastError) {
          showAlert("Extension error: " + chrome.runtime.lastError.message, "error");
          return;
        }

        if (res && res.success && res.user) {
          userIdInput.value = res.user;
          showAlert(`✓ Detected Claude session user: ${res.user}`, "success");
          const cur = await chrome.storage.local.get("chatsave_config");
          const cfg = cur.chatsave_config || {};
          cfg.userId = res.user;
          await chrome.storage.local.set({ chatsave_config: cfg, chatsave_detected_user: res.user });
        } else {
          const errMsg = res?.error || "Could not auto-detect Claude user. Please ensure claude.ai is open in Chrome and refresh the tab (F5).";
          showAlert(errMsg, "error");
        }
      });
    });
  }

  // 3. Save Settings
  btnSave.addEventListener("click", async () => {
    const sUrl = serverUrlInput.value.trim().replace(/\/+$/, "");
    if (!sUrl || sUrl.includes("claude.ai")) {
      showAlert("✕ Error: Do NOT enter claude.ai as the Server URL! The Server URL must be your Chat-Save backend service (e.g. http://localhost:8000 or your Render service like https://chat-save-xxx.onrender.com).", "error");
      return;
    }

    const configToSave = {
      serverUrl: sUrl,
      authToken: authTokenInput.value.trim(),
      userId: userIdInput.value.trim() || "user",
      autoSync: autoSyncCheckbox.checked
    };

    await chrome.storage.local.set({ chatsave_config: configToSave });
    showAlert("✓ Settings saved successfully!", "success");
  });

  // 4. Test Server Connection
  btnTest.addEventListener("click", async () => {
    showAlert("Connecting to server...", "normal");
    btnTest.disabled = true;

    const url = serverUrlInput.value.trim().replace(/\/+$/, "");
    const token = authTokenInput.value.trim();

    if (!url || url.includes("claude.ai")) {
      showAlert("✕ Error: Do NOT use claude.ai as the Server URL! Please enter http://localhost:8000 or your deployed Render URL.", "error");
      btnTest.disabled = false;
      return;
    }

    try {
      const headers = {};
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${url}/health`, { headers });
      if (!res.ok) {
        const text = await res.text();
        if (text.includes("<title>Blocked</title>") || text.includes("Cloudflare")) {
          throw new Error(`Cloudflare/WAF blocked request at ${url} (HTTP ${res.status}). Ensure the URL is your Chat-Save server.`);
        }
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
      showAlert(`✓ Connection successful! Server reported: ${JSON.stringify(data)}`, "success");
    } catch (err) {
      showAlert(`✕ Connection failed: ${err.message}`, "error");
    } finally {
      btnTest.disabled = false;
    }
  });

  function showAlert(msg, type) {
    alertBox.style.display = "block";
    alertBox.textContent = msg;
    if (type === "success") {
      alertBox.className = "alert alert-success";
    } else if (type === "error") {
      alertBox.className = "alert alert-error";
    } else {
      alertBox.className = "alert";
      alertBox.style.background = "#1f2937";
      alertBox.style.color = "#e5e7eb";
    }
  }

  // 5. Queue Inspector
  async function loadQueue() {
    await new Promise(r => chrome.runtime.sendMessage({ type: "GET_STATUS" }, () => {
      if (chrome.runtime.lastError) { /* consumed */ }
      r();
    }));
    const data = await chrome.storage.local.get("chatsave_outbox");
    const queue = data.chatsave_outbox || [];

    if (queue.length === 0) {
      queueSummary.textContent = "Outbox is completely clear. All captured chats delivered.";
      queueTable.style.display = "none";
      btnRetryQueue.disabled = true;
      btnClearQueue.disabled = true;
      return;
    }

    queueSummary.textContent = `${queue.length} item(s) waiting in offline queue:`;
    queueTable.style.display = "table";
    btnRetryQueue.disabled = false;
    btnClearQueue.disabled = false;

    queueTbody.innerHTML = "";
    queue.forEach(item => {
      const tr = document.createElement("tr");
      const title = item.payload.title || item.payload.conversation_id;
      const nextIn = Math.max(0, Math.round((item.nextAttemptAt - Date.now()) / 1000));
      tr.innerHTML = `
        <td><code>${title.slice(0, 24)}...</code></td>
        <td>${item.attempts}</td>
        <td>${nextIn}s</td>
        <td style="color:#f87171;">${item.lastError ? item.lastError.slice(0, 45) + "..." : "None"}</td>
      `;
      queueTbody.appendChild(tr);
    });
  }

  btnRetryQueue.addEventListener("click", () => {
    btnRetryQueue.disabled = true;
    btnRetryQueue.textContent = "Retrying...";
    chrome.runtime.sendMessage({ type: "SYNC_NOW" }, () => {
      if (chrome.runtime.lastError) { /* consumed */ }
      setTimeout(() => {
        loadQueue();
        loadDLQ();
        btnRetryQueue.disabled = false;
        btnRetryQueue.textContent = "Retry Outbox";
      }, 600);
    });
  });

  btnClearQueue.addEventListener("click", () => {
    if (confirm("Are you sure you want to clear all pending items in the offline queue?")) {
      btnClearQueue.disabled = true;
      chrome.runtime.sendMessage({ type: "CLEAR_QUEUE" }, () => {
        if (chrome.runtime.lastError) { /* consumed */ }
        loadQueue();
        loadDLQ();
        btnClearQueue.disabled = false;
      });
    }
  });

  // 6. Dead Letter Queue Inspector
  const dlqSummary = document.getElementById("dlqSummary");
  const dlqTable = document.getElementById("dlqTable");
  const dlqTbody = document.getElementById("dlqTbody");
  const btnRetryDLQ = document.getElementById("btnRetryDLQ");
  const btnClearDLQ = document.getElementById("btnClearDLQ");

  async function loadDLQ() {
    const data = await chrome.storage.local.get("chatsave_dead_letter");
    const dlq = data.chatsave_dead_letter || [];

    if (dlq.length === 0) {
      dlqSummary.textContent = "0 failed items in Dead Letter Queue (all clear).";
      dlqTable.style.display = "none";
      btnRetryDLQ.disabled = true;
      btnClearDLQ.disabled = true;
      return;
    }

    dlqSummary.textContent = `${dlq.length} item(s) permanently failed and saved in Dead Letter Queue:`;
    dlqTable.style.display = "table";
    btnRetryDLQ.disabled = false;
    btnClearDLQ.disabled = false;

    dlqTbody.innerHTML = "";
    dlq.forEach(item => {
      const tr = document.createElement("tr");
      const title = item.payload.title || item.payload.conversation_id;
      tr.innerHTML = `
        <td><code>${title.slice(0, 24)}...</code></td>
        <td>${item.attempts}</td>
        <td style="color:#f87171;">${item.failureReason ? item.failureReason.slice(0, 50) + "..." : "Exceeded retries"}</td>
      `;
      dlqTbody.appendChild(tr);
    });
  }

  btnRetryDLQ.addEventListener("click", () => {
    btnRetryDLQ.disabled = true;
    chrome.runtime.sendMessage({ type: "RETRY_DEAD_LETTER" }, () => {
      if (chrome.runtime.lastError) { /* consumed */ }
      setTimeout(() => {
        loadQueue();
        loadDLQ();
        btnRetryDLQ.disabled = false;
      }, 500);
    });
  });

  btnClearDLQ.addEventListener("click", () => {
    if (confirm("Are you sure you want to discard all items in the Dead Letter Queue?")) {
      chrome.runtime.sendMessage({ type: "CLEAR_DEAD_LETTER" }, () => {
        if (chrome.runtime.lastError) { /* consumed */ }
        loadDLQ();
      });
    }
  });

  const btnOptionsReconcile = document.getElementById("btnOptionsReconcile");
  const reconcileStatusText = document.getElementById("reconcileStatusText");
  if (btnOptionsReconcile) {
    btnOptionsReconcile.addEventListener("click", () => {
      btnOptionsReconcile.disabled = true;
      btnOptionsReconcile.textContent = "Scanning Claude Conversations...";
      if (reconcileStatusText) reconcileStatusText.textContent = "Connecting to open Claude tab to fetch recent conversation list...";
      chrome.runtime.sendMessage({ type: "TRIGGER_RECONCILE", maxDays: 2 }, (res) => {
        if (chrome.runtime.lastError) {
          btnOptionsReconcile.disabled = false;
          btnOptionsReconcile.textContent = "Scan & Sync Recent Chats (Past 48h)";
          if (reconcileStatusText) reconcileStatusText.textContent = "⚠ Could not connect to Claude tab. Please refresh your open claude.ai tab.";
          return;
        }
        setTimeout(() => {
          btnOptionsReconcile.disabled = false;
          btnOptionsReconcile.textContent = "Scan & Sync Recent Chats (Past 48h)";
          if (res && res.enqueued > 0) {
            if (reconcileStatusText) reconcileStatusText.textContent = `✓ Found and queued ${res.enqueued} stale/mobile conversation(s) into outbox for syncing!`;
          } else if (res && res.error) {
            if (reconcileStatusText) reconcileStatusText.textContent = `⚠ ${res.error}`;
          } else {
            if (reconcileStatusText) reconcileStatusText.textContent = "✓ All conversations from the past 48h are already up-to-date.";
          }
          loadQueue();
        }, 1500);
      });
    });
  }

  loadQueue();
  loadDLQ();
});
