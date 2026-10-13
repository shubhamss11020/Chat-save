// Run with: node --test tests/extension/background_queue.test.js
// Checks the outbox: items enqueued while a send is in flight are not lost, and the
// background only uploads to URLs its own presign step issued.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const { makeSandbox, waitUntil, sleep, jsonResponse, readOutbox, seedOutbox } = require("./harness");

// Simulated server: each request takes 150ms to answer.
const slowServer = async (url, opts = {}) => {
  await sleep(150);
  if (url.endsWith("/ingest-batch")) {
    const { items } = JSON.parse(opts.body);
    return jsonResponse({
      results: items.map((i) => ({ receipt_id: "r", conversation_id: i.conversation_id, saved_messages: 1, status: "persisted" })),
    });
  }
  return jsonResponse({ receipt_id: "r", saved_messages: 1 });
};

test("an item enqueued while another is being sent is not lost", async () => {
  const { ctx, store } = makeSandbox(slowServer);

  // Enqueue A; its background send starts immediately.
  await vm.runInContext("enqueue({ conversation_id: 'conv-a', title: 'A', messages: [] })", ctx);
  await sleep(50); // A's request is now in flight
  // Enqueue B while A is still being sent.
  await vm.runInContext("enqueue({ conversation_id: 'conv-b', title: 'B', messages: [] })", ctx);

  await waitUntil(ctx, "!isProcessingQueue");
  const pending = ((await readOutbox(ctx)) || []).map((i) => i.payload.conversation_id);
  assert.ok(pending.includes("conv-b"), `conv-b was lost; outbox = ${JSON.stringify(pending)}`);
  assert.ok(!pending.includes("conv-a"), "conv-a was delivered and should have left the outbox");

  // B is then delivered on the next run.
  await vm.runInContext("processQueue()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");
  assert.equal(((await readOutbox(ctx)) || []).length, 0);
});

test("UPLOAD_TO_S3 refuses a URL the extension never issued", async () => {
  const { listeners } = makeSandbox(slowServer);
  const handler = listeners[0];
  const result = await new Promise((resolve) => {
    const keep = handler({ type: "UPLOAD_TO_S3", upload_url: "https://attacker.example/put", body: "x" }, {}, resolve);
    assert.equal(keep, true, "handler should answer asynchronously");
  });
  assert.equal(result.success, false);
  assert.match(result.error, /not issued by this extension/);
});

test("a 429 with Retry-After schedules the retry at that time and is not counted as a failed attempt", async () => {
  const rateLimited = async () => ({
    ok: false, status: 429,
    headers: { get: (h) => (h.toLowerCase() === "retry-after" ? "30" : null) },
    text: async () => "slow down",
    json: async () => ({}),
  });
  const { ctx, store } = makeSandbox(rateLimited);
  const before = Date.now();
  await vm.runInContext("enqueue({ conversation_id: 'conv-rl', title: 'RL', messages: [] })", ctx);
  await waitUntil(ctx, "!isProcessingQueue");

  const item = (await readOutbox(ctx)).find((i) => i.payload.conversation_id === "conv-rl");
  assert.ok(item, "item must still be queued");
  assert.equal(item.attempts, 0, "rate-limit replies must not count as failed attempts");
  const waitMs = item.nextAttemptAt - before;
  assert.ok(waitMs >= 29000 && waitMs <= 35000, `retry should be ~30s away, was ${waitMs}ms`);
});
