/**
 * Options Script for Chat-Save Extension
 */

/**
 * Build a table cell from untrusted text. Uses textContent so conversation titles
 * and server error bodies can never be interpreted as HTML.
 */
function cell(text, { code = false, color = "" } = {}) {
  const td = document.createElement("td");
  const el = code ? document.createElement("code") : td;
  el.textContent = text;
  if (code) td.appendChild(el);
  if (color) td.style.color = color;
  return td;
}

document.addEventListener("DOMContentLoaded", async () => {
  const serverUrlInput = document.getElementById("serverUrl");
  const authTokenInput = document.getElementById("authToken");
  const identityEl = document.getElementById("identityValue");
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
  autoSyncCheckbox.checked = managed.autoSync !== undefined ? managed.autoSync : (localConfig.autoSync !== undefined ? localConfig.autoSync : true);
  showIdentity(localConfig.identity);
  loadConsentStatus();

  if (managed.serverUrl || managed.authToken) {
    managedBanner.style.display = "block";
    if (managed.serverUrl) serverUrlInput.disabled = true;
    if (managed.authToken) authTokenInput.disabled = true;
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
    const sUrl = serverUrlInput.value.trim().replace(/\/+$/, "");
    if (!sUrl || sUrl.includes("claude.ai")) {
      showAlert("✕ Error: Do NOT enter claude.ai as the Server URL! The Server URL must be your Chat-Save backend service (e.g. http://localhost:8000 or your Render service like https://chat-save-xxx.onrender.com).", "error");
      return;
    }

    // Host access is optional: ask for the backend's origin (must run inside this click, before any await).
    let origin;
    try {
      origin = new URL(sUrl).origin + "/*";
    } catch (e) {
      showAlert("✕ Error: Server URL is not a valid address.", "error");
      return;
    }
    const granted = await chrome.permissions.request({ origins: [origin] }).catch(() => false);
    if (!granted) {
      showAlert(`✕ Chrome did not grant access to ${origin}, so settings were not saved.`, "error");
      return;
    }

    // Keep the identity last confirmed by the server; it is not editable here.
    const previous = (await chrome.storage.local.get("chatsave_config")).chatsave_config || {};
    const newToken = authTokenInput.value.trim();
    const unchanged = previous.serverUrl === sUrl && previous.authToken === newToken;
    const configToSave = {
      serverUrl: sUrl,
      authToken: newToken,
      autoSync: autoSyncCheckbox.checked,
      identity: unchanged ? (previous.identity || null) : null  // stale after a token/server change
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

      await res.json();
      // Ask the server who this token belongs to. The name comes from the server, not the page.
      const who = await fetch(`${url}/api/whoami`, { headers });
      if (who.status === 401) {
        throw new Error("the server rejected this token. Check it with your Chat-Save admin.");
      }
      if (!who.ok) throw new Error(`whoami failed: HTTP ${who.status}`);
      const identity = await who.json();
      showIdentity({ user: identity.user, tokenBound: identity.token_bound });
      await chrome.storage.local.set({
        chatsave_config: {
          serverUrl: url,
          authToken: token,
          autoSync: autoSyncCheckbox.checked,
          identity: { user: identity.user, tokenBound: identity.token_bound }
        }
      });
      showAlert(`✓ Connected as ${identity.user}${identity.token_bound ? "" : " (shared owner token)"}.`, "success");
    } catch (err) {
      showAlert(`✕ Connection failed: ${err.message}`, "error");
    } finally {
      btnTest.disabled = false;
    }
  });

  /** Show whether the person agreed to saving, and let them withdraw that agreement. */
  async function loadConsentStatus() {
    const { chatsave_consent: c } = await chrome.storage.local.get("chatsave_consent");
    const status = document.getElementById("consentStatus");
    status.textContent = c && c.accepted
      ? `You agreed to saving on ${new Date(c.at).toLocaleString()}.`
      : "Saving is not turned on. Open the welcome page to agree.";
  }

  document.getElementById("btnWithdraw").addEventListener("click", async () => {
    if (!confirm("Stop saving your chats? Nothing new will be saved until you agree again.")) return;
    await chrome.storage.local.remove("chatsave_consent");
    const cur = (await chrome.storage.local.get("chatsave_config")).chatsave_config || {};
    await chrome.storage.local.set({ chatsave_config: { ...cur, autoSync: false } });
    autoSyncCheckbox.checked = false;
    loadConsentStatus();
    showAlert("Saving is stopped. You can turn it on again from the welcome page.", "success");
  });

  /** Show who the server says this token belongs to. Text only, never HTML. */
  function showIdentity(identity, tokenBound) {
    identityEl.replaceChildren();
    if (!identity || !identity.user) {
      const s = document.createElement("strong");
      s.textContent = "Not connected yet";
      identityEl.append(s, document.createTextNode(" — click Test Connection."));
      return;
    }
    const name = identity.user;
    const bound = identity.tokenBound;
    const s = document.createElement("strong");
    s.textContent = name;
    identityEl.append(document.createTextNode("Signed in as "), s,
      document.createTextNode(bound ? "" : " (shared owner token)"));
  }

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

  // 5. Waiting to save
  async function loadQueue() {
    await new Promise(r => chrome.runtime.sendMessage({ type: "GET_STATUS" }, () => {
      if (chrome.runtime.lastError) { /* consumed */ }
      r();
    }));
    const queue = await loadOutbox();

    if (queue.length === 0) {
      queueSummary.textContent = "Everything has been saved. Nothing is waiting.";
      queueTable.style.display = "none";
      btnRetryQueue.disabled = true;
      btnClearQueue.disabled = true;
      return;
    }

    queueSummary.textContent = `${queue.length} conversation(s) waiting to be saved:`;
    queueTable.style.display = "table";
    btnRetryQueue.disabled = false;
    btnClearQueue.disabled = false;

    queueTbody.innerHTML = "";
    queue.forEach(item => {
      const title = item.payload.title || item.payload.conversation_id || "";
      const nextIn = Math.max(0, Math.round((item.nextAttemptAt - Date.now()) / 1000));
      const tr = document.createElement("tr");
      tr.appendChild(cell(`${title.slice(0, 24)}...`, { code: true }));
      tr.appendChild(cell(String(item.attempts)));
      tr.appendChild(cell(`${nextIn}s`));
      tr.appendChild(cell(item.lastError ? `${item.lastError.slice(0, 45)}...` : "None", { color: "#f87171" }));
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
        btnRetryQueue.textContent = "Try again now";
      }, 600);
    });
  });

  btnClearQueue.addEventListener("click", () => {
    if (confirm("Discard all conversations waiting to be saved? They will not be saved.")) {
      btnClearQueue.disabled = true;
      chrome.runtime.sendMessage({ type: "CLEAR_QUEUE" }, () => {
        if (chrome.runtime.lastError) { /* consumed */ }
        loadQueue();
        loadDLQ();
        btnClearQueue.disabled = false;
      });
    }
  });

  // 6. Could not save
  const dlqSummary = document.getElementById("dlqSummary");
  const dlqTable = document.getElementById("dlqTable");
  const dlqTbody = document.getElementById("dlqTbody");
  const btnRetryDLQ = document.getElementById("btnRetryDLQ");
  const btnClearDLQ = document.getElementById("btnClearDLQ");

  async function loadDLQ() {
    const dlq = await loadDeadLetter();

    if (dlq.length === 0) {
      dlqSummary.textContent = "Nothing has failed.";
      dlqTable.style.display = "none";
      btnRetryDLQ.disabled = true;
      btnClearDLQ.disabled = true;
      return;
    }

    dlqSummary.textContent = `${dlq.length} conversation(s) could not be saved:`;
    dlqTable.style.display = "table";
    btnRetryDLQ.disabled = false;
    btnClearDLQ.disabled = false;

    dlqTbody.innerHTML = "";
    dlq.forEach(item => {
      const title = item.payload.title || item.payload.conversation_id || "";
      const tr = document.createElement("tr");
      tr.appendChild(cell(`${title.slice(0, 24)}...`, { code: true }));
      tr.appendChild(cell(String(item.attempts)));
      tr.appendChild(cell(item.failureReason ? `${item.failureReason.slice(0, 50)}...` : "Exceeded retries", { color: "#f87171" }));
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
    if (confirm("Discard conversations that could not be saved? This cannot be undone.")) {
      chrome.runtime.sendMessage({ type: "CLEAR_DEAD_LETTER" }, () => {
        if (chrome.runtime.lastError) { /* consumed */ }
        loadDLQ();
      });
    }
  });

  loadQueue();
  loadDLQ();
});
