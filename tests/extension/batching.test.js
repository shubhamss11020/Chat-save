// Run with: node --test tests/extension/batching.test.js
// The outbox sends due items in groups, handles per-item failures, and falls back to single
// sends for servers that predate the batch endpoint.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const { makeSandbox, waitUntil, jsonResponse, readOutbox, seedOutbox } = require("./harness");

function queued(ids) {
  return ids.map((id) => ({
    id: `q_${id}`,
    payload: { conversation_id: id, title: id, messages: [] },
    attempts: 0,
    nextAttemptAt: 0,
    lastError: null,
    addedAt: Date.now(),
  }));
}

test("several due items are sent in one request", async () => {
  const calls = [];
  const fetchImpl = async (url, opts = {}) => {
    calls.push(url);
    const { items } = JSON.parse(opts.body);
    return jsonResponse({
      results: items.map((i) => ({ receipt_id: "r", conversation_id: i.conversation_id, saved_messages: 1, status: "persisted" })),
    });
  };
  const { ctx, store } = makeSandbox(fetchImpl);
  await seedOutbox(ctx, queued(["a", "b", "c"]));

  await vm.runInContext("processQueue()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");

  assert.deepEqual(calls, ["http://server.test/api/extension/ingest-batch"]);
  assert.equal(((await readOutbox(ctx)) || []).length, 0, "all three were saved");
});

test("one failed item in a batch is retried alone; the others are saved", async () => {
  const fetchImpl = async (url, opts = {}) => {
    const { items } = JSON.parse(opts.body);
    return jsonResponse({
      results: items.map((i) => (i.conversation_id === "b"
        ? { conversation_id: "b", status: "error", error: "disk full" }
        : { receipt_id: "r", conversation_id: i.conversation_id, saved_messages: 1, status: "persisted" })),
    });
  };
  const { ctx, store } = makeSandbox(fetchImpl);
  await seedOutbox(ctx, queued(["a", "b", "c"]));

  await vm.runInContext("processQueue()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");

  const left = (await readOutbox(ctx)).map((i) => i.payload.conversation_id);
  assert.deepEqual(left, ["b"], "only the failed item stays queued");
  assert.equal((await readOutbox(ctx))[0].attempts, 1);
  assert.match((await readOutbox(ctx))[0].lastError, /disk full/);
});

test("an older server without the batch endpoint receives every item one at a time", async () => {
  const urls = [];
  const fetchImpl = async (url, opts = {}) => {
    urls.push(url);
    if (url.endsWith("/ingest-batch")) return jsonResponse({ detail: "Not Found" }, 404);
    const body = JSON.parse(opts.body);
    return jsonResponse({ receipt_id: "r", conversation_id: body.conversation_id, saved_messages: 1, status: "persisted" });
  };
  const { ctx, store } = makeSandbox(fetchImpl);
  await seedOutbox(ctx, queued(["a", "b"]));

  await vm.runInContext("processQueue()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");

  assert.equal(urls[0], "http://server.test/api/extension/ingest-batch");
  assert.deepEqual(urls.slice(1), ["http://server.test/api/extension/ingest", "http://server.test/api/extension/ingest"]);
  assert.equal(((await readOutbox(ctx)) || []).length, 0);
});
