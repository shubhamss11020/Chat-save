// Run with: node --test tests/extension/queue_store.test.js
// The outbox and dead-letter list live in IndexedDB. Old data in chrome.storage moves over once.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const { makeSandbox, readOutbox, seedOutbox } = require("./harness");

test("data from the old chrome.storage array moves into IndexedDB once, then the old key is removed", async () => {
  const { ctx, store } = makeSandbox(async () => { throw new Error("no network in this test"); });
  store.chatsave_outbox = [{ id: "q1", addedAt: 1, payload: { conversation_id: "old-1" }, attempts: 0 }];

  const items = await readOutbox(ctx);
  assert.deepEqual(items.map((i) => i.payload.conversation_id), ["old-1"]);
  assert.equal(store.chatsave_outbox, undefined, "legacy key removed after migration");

  // A second read does not bring anything back.
  assert.equal((await readOutbox(ctx)).length, 1);
});

test("outbox items come back oldest first, and the dead-letter list is kept separate", async () => {
  const { ctx } = makeSandbox(async () => { throw new Error("no network in this test"); });
  await seedOutbox(ctx, [
    { id: "q3", addedAt: 3, payload: { conversation_id: "third" } },
    { id: "q1", addedAt: 1, payload: { conversation_id: "first" } },
    { id: "q2", addedAt: 2, payload: { conversation_id: "second" } },
  ]);
  const order = (await readOutbox(ctx)).map((i) => i.payload.conversation_id);
  assert.deepEqual(order, ["first", "second", "third"]);

  await vm.runInContext("storeDeadLetter(__d)", Object.assign(ctx, { __d: [{ id: "d1", deadLetterAt: 9, payload: { conversation_id: "dead" } }] }));
  assert.equal((await readOutbox(ctx)).length, 3, "dead letters do not appear in the outbox");
  const dead = await vm.runInContext("loadDeadLetter()", ctx);
  assert.deepEqual(dead.map((d) => d.payload.conversation_id), ["dead"]);
});
