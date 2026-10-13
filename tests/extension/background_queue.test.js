// Run with: node --test tests/extension
// Loads extension/background.js into a sandbox with a stubbed chrome.* API and checks
// that items enqueued while a send is in flight are not lost.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const BACKGROUND = process.env.BACKGROUND_JS
  || path.join(__dirname, "..", "..", "extension", "background.js");
const src = fs.readFileSync(BACKGROUND, "utf8");

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function makeSandbox() {
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
        async remove() {},
      },
    },
    tabs: { query(_q, cb) { cb([]); }, sendMessage() {} },
  };
  // Simulated server: each POST takes 150ms to answer.
  const fetch = async () => {
    await sleep(150);
    return { ok: true, status: 200, json: async () => ({ receipt_id: "r", saved_messages: 1 }), text: async () => "" };
  };
  const ctx = vm.createContext({
    chrome, fetch, console, setTimeout, Date, Math, Promise, JSON, Set, Map, Array, Object, Error,
    encodeURIComponent, structuredClone, crypto: globalThis.crypto,
  });
  vm.runInContext(src, ctx);
  // Server URL that passes the "not claude.ai" check.
  store.chatsave_config = { serverUrl: "http://server.test", authToken: "", userId: "tester", autoSync: true };
  return { ctx, store, listeners };
}

async function waitUntil(ctx, expr, timeoutMs = 10000) {
  const start = Date.now();
  while (!vm.runInContext(expr, ctx)) {
    if (Date.now() - start > timeoutMs) throw new Error(`timed out waiting for: ${expr}`);
    await sleep(25);
  }
}

test("an item enqueued while another is being sent is not lost", async () => {
  const { ctx, store } = makeSandbox();

  // Enqueue A; its background send starts immediately.
  await vm.runInContext("enqueue({ conversation_id: 'conv-a', title: 'A', messages: [] })", ctx);
  await sleep(50); // A's request is now in flight
  // Enqueue B while A is still being sent.
  await vm.runInContext("enqueue({ conversation_id: 'conv-b', title: 'B', messages: [] })", ctx);

  await waitUntil(ctx, "!isProcessingQueue");
  const pending = (store.chatsave_outbox || []).map((i) => i.payload.conversation_id);
  assert.ok(pending.includes("conv-b"), `conv-b was lost; outbox = ${JSON.stringify(pending)}`);
  assert.ok(!pending.includes("conv-a"), "conv-a was delivered and should have left the outbox");

  // B is then delivered on the next run.
  await vm.runInContext("processQueue()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");
  assert.equal((store.chatsave_outbox || []).length, 0);
});

test("UPLOAD_TO_S3 refuses a URL the extension never issued", async () => {
  const { ctx, listeners } = makeSandbox();
  const handler = listeners[0];
  const result = await new Promise((resolve) => {
    const keep = handler({ type: "UPLOAD_TO_S3", upload_url: "https://attacker.example/put", body: "x" }, {}, resolve);
    assert.equal(keep, true, "handler should answer asynchronously");
  });
  assert.equal(result.success, false);
  assert.match(result.error, /not issued by this extension/);
});
