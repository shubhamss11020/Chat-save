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
  broadcastToTabs({ type: "QUEUE_UPDATED", pendingCount: queue.length });
  processQueue();
  return queue.length;
}

/**
 * Process the local outbox queue with exponential backoff retry.
 */
async function processQueue() {
  if (isProcessingQueue) return;
  isProcessingQueue = true;

  try {
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
          throw new Error(`HTTP ${res.status}: ${errText.slice(0, 200)}`);
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

        // Dead Letter Queue after MAX_RETRIES (10 attempts)
        const MAX_RETRIES = 10;
        if (item.attempts >= MAX_RETRIES) {
          const dlq = await getDeadLetterQueue();
          dlq.push({
            ...item,
            deadLetterAt: Date.now(),
            failureReason: `Exceeded ${MAX_RETRIES} attempts: ${err.message}`
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
          const backoffMs = Math.min(300000, 2000 * Math.pow(2, item.attempts)) + Math.random() * 1000;
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
    broadcastToTabs({ type: "QUEUE_UPDATED", pendingCount: remainingQueue.length });

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
        try {
          chrome.tabs.sendMessage(tab.id, message).catch(() => {});
        } catch (e) {}
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
      processQueue();
      sendResponse({ success: true, reQueued: dlq.length, pendingCount: queue.length });
    })();
    return true;
  }

  if (req.type === "CLEAR_DEAD_LETTER") {
    (async () => {
      await saveDeadLetterQueue([]);
      sendResponse({ success: true, deadLetterCount: 0 });
    })();
    return true;
  }
});
