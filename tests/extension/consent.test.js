// Run with: node --test tests/extension/consent.test.js
// Nothing is captured or synced until the person has agreed on the welcome page.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { makeSandbox, readOutbox } = require("./harness");

const noNetwork = async () => { throw new Error("no network expected"); };

test("a captured chat is refused when consent has not been given", async () => {
  const { ctx, store, listeners } = makeSandbox(noNetwork);
  delete store.chatsave_consent;
  const result = await new Promise((resolve) => {
    listeners[0]({ type: "INGEST_CONVERSATION", payload: { conversation_id: "c1", messages: [] } }, {}, resolve);
  });
  assert.equal(result.queued, false);
  assert.equal(result.reason, "no_consent");
  assert.equal((await readOutbox(ctx)).length, 0, "nothing was queued");
});

test("a captured chat is queued once consent has been given", async () => {
  const { listeners } = makeSandbox(async () => { throw new Error("stop before sending"); });
  const result = await new Promise((resolve) => {
    listeners[0]({ type: "INGEST_CONVERSATION", payload: { conversation_id: "c2", messages: [] } }, {}, resolve);
  });
  assert.equal(result.queued, true);
});

test("cloud sync does nothing without consent", async () => {
  const { ctx, store } = makeSandbox(noNetwork);
  delete store.chatsave_consent;
  const result = await require("node:vm").runInContext("reconcileFromCloud()", ctx);
  assert.equal(result.success, false);
  assert.match(result.error, /not turned on/);
});

test("consent from an older policy version does not count", async () => {
  const { ctx, store } = makeSandbox(noNetwork);
  store.chatsave_consent = { accepted: true, version: 0, at: "2025-01-01T00:00:00Z" };
  const result = await require("node:vm").runInContext("reconcileFromCloud()", ctx);
  assert.equal(result.success, false);
});
