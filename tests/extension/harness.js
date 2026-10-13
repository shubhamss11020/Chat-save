// Shared sandbox for extension tests: loads background.js (and cloud_sync.js via importScripts)
// into a vm context with a stubbed chrome.* API and a caller-supplied fetch.
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { IDBFactory, IDBKeyRange } = require("fake-indexeddb");

const EXT_DIR = path.join(__dirname, "..", "..", "extension");

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function makeSandbox(fetchImpl) {
  const store = {};
  const listeners = [];
  const chrome = {
    runtime: {
      onInstalled: { addListener() {} },
      onStartup: { addListener() {} },
      onMessage: { addListener(fn) { listeners.push(fn); } },
      getManifest: () => ({ version: "1.0.0" }),
    },
    alarms: { create() {}, onAlarm: { addListener() {} } },
    tabs: {
      query(_q, cb) { cb([]); },
      sendMessage() {},
      onUpdated: { addListener() {} },
    },
    storage: {
      local: {
        async get(keys) {
          const out = {};
          for (const k of Array.isArray(keys) ? keys : [keys]) {
            if (k in store) out[k] = structuredClone(store[k]);
          }
          return out;
        },
        async set(obj) { Object.assign(store, structuredClone(obj)); },
        async remove(keys) { for (const k of [].concat(keys)) delete store[k]; },
      },
    },
  };

  const ctx = vm.createContext({
    chrome, console, setTimeout, Date, Math, Promise, JSON, Set, Map, Array, Object, Error,
    encodeURIComponent, structuredClone, crypto: globalThis.crypto, Number, String, RegExp, Symbol,
    atob, btoa, Uint8Array, TextEncoder, TextDecoder, URL,
    indexedDB: new IDBFactory(), IDBKeyRange,
    fetch: fetchImpl || (async () => { throw new Error("no fetch stub"); }),
  });
  // importScripts loads a sibling file into the same global scope, as a service worker does.
  ctx.importScripts = (...files) => files.forEach((file) =>
    vm.runInContext(fs.readFileSync(path.join(EXT_DIR, file), "utf8"), ctx));
  vm.runInContext(fs.readFileSync(path.join(EXT_DIR, "background.js"), "utf8"), ctx);

  store.chatsave_config = { serverUrl: "http://server.test", authToken: "", autoSync: true };
  // Most tests are about saving, so they start with consent given. Consent tests remove it.
  store.chatsave_consent = { accepted: true, version: 1, at: "2026-10-13T10:00:00Z" };
  return { ctx, store, listeners };
}

async function waitUntil(ctx, expr, timeoutMs = 15000) {
  const start = Date.now();
  while (!vm.runInContext(expr, ctx)) {
    if (Date.now() - start > timeoutMs) throw new Error(`timed out waiting for: ${expr}`);
    await sleep(25);
  }
}

const jsonResponse = (body, status = 200) => ({
  ok: status < 400,
  status,
  json: async () => body,
  text: async () => JSON.stringify(body),
});

/** The outbox lives in IndexedDB now; these read and seed it through the extension's own code. */
const readOutbox = (ctx) => vm.runInContext("loadOutbox()", ctx);
const seedOutbox = (ctx, items) => vm.runInContext("storeOutbox(__items)", Object.assign(ctx, { __items: items }));

module.exports = { makeSandbox, waitUntil, sleep, jsonResponse, readOutbox, seedOutbox };
