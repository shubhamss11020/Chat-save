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

  // 3. Save Settings
  btnSave.addEventListener("click", async () => {
    const configToSave = {
      serverUrl: serverUrlInput.value.trim().replace(/\/+$/, ""),
      authToken: authTokenInput.value.trim(),
      userId: userIdInput.value.trim() || "user",
      autoSync: autoSyncCheckbox.checked
    };

    await chrome.storage.local.set({ chatsave_config: configToSave });
    showAlert("Settings saved successfully!", "success");
  });

  // 4. Test Server Connection
  btnTest.addEventListener("click", async () => {
    showAlert("Connecting to server...", "normal");
    btnTest.disabled = true;

    const url = serverUrlInput.value.trim().replace(/\/+$/, "");
    const token = authTokenInput.value.trim();

    try {
      const headers = {};
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${url}/health`, { headers });
      if (!res.ok) {
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
        loadDLQ();
      });
    }
  });

  loadQueue();
  loadDLQ();
});
