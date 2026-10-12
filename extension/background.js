/**
 * Chat-Save Background Service Worker (Manifest V3)
 * Handles durable offline queueing, exponential retry, auth resolution,
 * and telemetry heartbeat for Claude Team web capture.
 */

const DEFAULT_CONFIG = {
  serverUrl: "http://localhost:8000",
  authToken: "",
  userId: "user",
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
    userId: managed.userId || localConfig.userId || DEFAULT_CONFIG.userId,
    autoSync: managed.autoSync !== undefined ? managed.autoSync : (localConfig.autoSync !== undefined ? localConfig.autoSync : DEFAULT_CONFIG.autoSync),
    isManaged: Boolean(managed.serverUrl || managed.authToken || managed.userId)
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

/**
 * Enqueue a conversation snapshot into the persistent outbox.
 */
async function enqueue(payload) {
  const queue = await getQueue();
  const clientId = await getClientId();
  payload.client_id = clientId;

  // Deduplicate in local queue if identical conversation snapshot is already waiting
  const existingIdx = queue.findIndex(item => item.payload.conversation_id === payload.conversation_id);
  const queueItem = {
    id: "q_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7),
    payload,
    attempts: 0,
    nextAttemptAt: Date.now(),
    lastError: null,
    addedAt: Date.now()
  };

  if (existingIdx >= 0) {
    const oldMessages = queue[existingIdx].payload.messages || [];
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
    queue[existingIdx] = queueItem;
  } else {
    queue.push(queueItem);
  }

  await saveQueue(queue);
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
  const queue = await getQueue();
  if (!queue.length) return false;

  const dlq = await getDeadLetterQueue();
  const surviving = [];
  let movedCount = 0;

  for (const item of queue) {
    const isAuth = item.lastError && (item.lastError.includes("HTTP 401") || item.lastError.includes("HTTP 403") || item.lastError.includes("Blocked") || item.lastError.includes("Invalid Server URL"));
    const maxAttempts = isAuth ? 2 : 5;
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
}

/**
 * Process the local outbox queue with exponential backoff retry.
 */
async function processQueue() {
  if (isProcessingQueue) return;
  isProcessingQueue = true;

  try {
    // 1. Immediately purge any items that have already exceeded max retries
    await purgeExpiredToDLQ();

    const config = await getConfig();
    let queue = await getQueue();
    if (!queue.length) {
      isProcessingQueue = false;
      return;
    }

    const now = Date.now();
    const remainingQueue = [];

    for (const item of queue) {
      if (item.nextAttemptAt > now) {
        remainingQueue.push(item);
        continue;
      }

      try {
        if (!config.serverUrl || config.serverUrl.includes("claude.ai")) {
          throw new Error(`Invalid Server URL: "${config.serverUrl || ""}". Server URL must be your Chat-Save backend service (e.g. http://localhost:8000 or your Render URL), NOT claude.ai.`);
        }

        const url = `${config.serverUrl}/api/extension/ingest?user=${encodeURIComponent(config.userId)}`;
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

        broadcastToTabs({
          type: "SYNC_SUCCESS",
          conversationId: item.payload.conversation_id,
          receipt
        });

      } catch (err) {
        console.warn("[Chat-Save] Queue delivery failed:", err.message);
        item.attempts += 1;
        item.lastError = err.message;

        // Fail fast on non-retryable authentication errors (HTTP 401 / HTTP 403 / Cloudflare blocks)
        const isAuthError = err.message.includes("HTTP 401") || err.message.includes("HTTP 403") || err.message.includes("Blocked by Cloudflare") || err.message.includes("Invalid Server URL");
        const MAX_RETRIES = isAuthError ? 2 : 5;

        if (item.attempts >= MAX_RETRIES) {
          const dlq = await getDeadLetterQueue();
          dlq.push({
            ...item,
            deadLetterAt: Date.now(),
            failureReason: isAuthError
              ? `Delivery failed (${err.message.slice(0, 120)}) - Please check Server URL & Auth Token in settings`
              : `Exceeded ${MAX_RETRIES} attempts: ${err.message}`
          });
          await saveDeadLetterQueue(dlq);
          console.error(`[Chat-Save] Item moved to Dead Letter Queue: ${item.id}`, item.lastError);
          broadcastToTabs({
            type: "DEAD_LETTER_EVENT",
            conversationId: item.payload.conversation_id,
            error: item.lastError
          });
        } else {
          // Exponential backoff with jitter
          const backoffMs = isAuthError ? 4000 : (Math.min(120000, 2000 * Math.pow(2, item.attempts)) + Math.random() * 1000);
          item.nextAttemptAt = Date.now() + backoffMs;
          remainingQueue.push(item);
        }

        broadcastToTabs({
          type: "SYNC_ERROR",
          conversationId: item.payload.conversation_id,
          error: err.message,
          pendingCount: remainingQueue.length
        });
      }
    }

    await saveQueue(remainingQueue);
    const currentDlq = await getDeadLetterQueue();
    broadcastToTabs({
      type: "QUEUE_UPDATED",
      pendingCount: remainingQueue.length,
      queuedIds: remainingQueue.map(q => q.payload?.conversation_id).filter(Boolean),
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

/**
 * Send telemetry heartbeat to the ingestion server.
 */
async function sendHeartbeat() {
  try {
    const config = await getConfig();
    const clientId = await getClientId();
    const queue = await getQueue();
    const lastSync = (await chrome.storage.local.get("chatsave_last_sync_time")).chatsave_last_sync_time || null;

    const url = `${config.serverUrl}/api/extension/heartbeat?user=${encodeURIComponent(config.userId)}`;
    const headers = {
      "Content-Type": "application/json"
    };
    if (config.authToken) {
      headers["Authorization"] = `Bearer ${config.authToken}`;
    }

    const payload = {
      client_id: clientId,
      user_id: config.userId,
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
      const queue = await getQueue();
      queue.forEach(item => { item.nextAttemptAt = Date.now(); });
      await saveQueue(queue);
      processQueue();
      sendResponse({ success: true, pendingCount: queue.length });
    })();
    return true;
  }

  if (req.type === "CLEAR_QUEUE") {
    (async () => {
      await saveQueue([]);
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
      const dlq = await getDeadLetterQueue();
      if (!dlq.length) {
        sendResponse({ success: true, reQueued: 0 });
        return;
      }
      const queue = await getQueue();
      dlq.forEach(item => {
        item.attempts = 0;
        item.nextAttemptAt = Date.now();
        item.lastError = null;
        queue.push(item);
      });
      await saveQueue(queue);
      await saveDeadLetterQueue([]);
      broadcastToTabs({
        type: "QUEUE_UPDATED",
        pendingCount: queue.length,
        queuedIds: queue.map(q => q.payload?.conversation_id).filter(Boolean),
        dlqIds: []
      });
      processQueue();
      sendResponse({ success: true, reQueued: dlq.length, pendingCount: queue.length });
    })();
    return true;
  }

  if (req.type === "CLEAR_DEAD_LETTER") {
    (async () => {
      await saveDeadLetterQueue([]);
      const queue = await getQueue();
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
        chrome.tabs.sendMessage(tabs[0].id, { type: "TRIGGER_RECONCILE", maxDays: req.maxDays || 7 }, (res) => {
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
});

/**
 * Sends a message to the active claude.ai tab to reconcile recent conversations from the past N days.
 */
function triggerReconcileInTabs(maxDays = 7) {
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

