/**
 * Durable storage for the outbox (saves waiting to be sent) and the dead-letter list
 * (saves that failed for good), kept in IndexedDB.
 *
 * Loaded by background.js (importScripts) and by options.html (script tag), so both read the
 * same database. Each write is one transaction: a crash mid-write cannot leave a half-saved list.
 * Replaces the earlier single array in chrome.storage.local, which was rewritten in full on
 * every change.
 */

const QUEUE_DB_NAME = "chatsave";
const QUEUE_DB_VERSION = 1;
const OUTBOX_STORE = "outbox";
const DEAD_LETTER_STORE = "deadletter";
const LEGACY_OUTBOX_KEY = "chatsave_outbox";
const LEGACY_DEAD_LETTER_KEY = "chatsave_dead_letter";

let queueDbPromise = null;
let migrationPromise = null;

function openQueueDb(factory) {
  if (!queueDbPromise) {
    queueDbPromise = new Promise((resolve, reject) => {
      const req = (factory || indexedDB).open(QUEUE_DB_NAME, QUEUE_DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(OUTBOX_STORE)) db.createObjectStore(OUTBOX_STORE, { keyPath: "id" });
        if (!db.objectStoreNames.contains(DEAD_LETTER_STORE)) db.createObjectStore(DEAD_LETTER_STORE, { keyPath: "id" });
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => {
        queueDbPromise = null;  // allow a retry on the next call
        reject(req.error);
      };
    });
  }
  return queueDbPromise;
}

async function readStore(name) {
  const db = await openQueueDb();
  return new Promise((resolve, reject) => {
    const req = db.transaction(name, "readonly").objectStore(name).getAll();
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = () => reject(req.error);
  });
}

/** Replace the whole store in one transaction. */
async function writeStore(name, items) {
  const db = await openQueueDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(name, "readwrite");
    const store = tx.objectStore(name);
    store.clear();
    for (const item of items) store.put(item);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
    tx.onabort = () => reject(tx.error);
  });
}

/** One-time move of data from the old chrome.storage arrays into IndexedDB. */
function ensureMigrated() {
  if (!migrationPromise) {
    migrationPromise = (async () => {
      const legacy = await chrome.storage.local.get([LEGACY_OUTBOX_KEY, LEGACY_DEAD_LETTER_KEY]);
      if (Array.isArray(legacy[LEGACY_OUTBOX_KEY])) {
        await writeStore(OUTBOX_STORE, legacy[LEGACY_OUTBOX_KEY]);
        await chrome.storage.local.remove(LEGACY_OUTBOX_KEY);
      }
      if (Array.isArray(legacy[LEGACY_DEAD_LETTER_KEY])) {
        await writeStore(DEAD_LETTER_STORE, legacy[LEGACY_DEAD_LETTER_KEY]);
        await chrome.storage.local.remove(LEGACY_DEAD_LETTER_KEY);
      }
    })().catch((err) => {
      migrationPromise = null;  // try again next time rather than staying broken
      throw err;
    });
  }
  return migrationPromise;
}

/** Items waiting to be sent, oldest first. */
async function loadOutbox() {
  await ensureMigrated();
  const items = await readStore(OUTBOX_STORE);
  return items.sort((a, b) => (a.addedAt || 0) - (b.addedAt || 0));
}

async function storeOutbox(items) {
  await ensureMigrated();
  await writeStore(OUTBOX_STORE, items);
}

/** Saves that failed for good, oldest first. */
async function loadDeadLetter() {
  await ensureMigrated();
  const items = await readStore(DEAD_LETTER_STORE);
  return items.sort((a, b) => (a.deadLetterAt || 0) - (b.deadLetterAt || 0));
}

async function storeDeadLetter(items) {
  await ensureMigrated();
  await writeStore(DEAD_LETTER_STORE, items);
}
