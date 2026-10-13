// Run with: node --test tests/extension/cloud_sync.test.js
// Checks the cloud sync: which conversations are sent, Claude's own timestamps are kept,
// and a conversation is only marked saved after the server accepts it.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const { makeSandbox, waitUntil, jsonResponse } = require("./harness");

const HOUR = 3600 * 1000;
const iso = (hoursAgo) => new Date(Date.now() - hoursAgo * HOUR).toISOString();

const OLD_UPDATED = iso(3);
const NEW_UPDATED = iso(1);

const LIST = [
  { uuid: "c-new", name: "New chat", created_at: iso(5), updated_at: NEW_UPDATED },
  { uuid: "c-old", name: "Old chat", created_at: iso(10), updated_at: OLD_UPDATED },
  { uuid: "c-ancient", name: "Ancient", created_at: iso(300), updated_at: iso(300) },
];

const DETAILS = {
  "c-new": {
    chat_messages: [
      { sender: "human", created_at: iso(1.5), text: "hi from phone" },
      { sender: "assistant", created_at: iso(1.2), text: "hello" },
    ],
  },
  "c-old": { chat_messages: [{ sender: "human", created_at: iso(3), text: "old" }] },
};

function claudeFetch(seen, serverStatus = 200) {
  return async (url, opts = {}) => {
    if (url.startsWith("http://server.test")) {
      if (serverStatus !== 200) return jsonResponse({ detail: "boom" }, serverStatus);
      const { items } = JSON.parse(opts.body);
      items.forEach((item) => seen.posts.push(item));
      return jsonResponse({
        results: items.map((i) => ({ receipt_id: "r", conversation_id: i.conversation_id, saved_messages: 2, status: "persisted" })),
      });
    }
    if (url.endsWith("/api/organizations")) return jsonResponse([{ uuid: "org1" }]);
    if (url.includes("/chat_conversations/")) {
      const id = url.split("/chat_conversations/")[1].split("?")[0];
      seen.details.push(id);
      return jsonResponse(DETAILS[id] || { chat_messages: [] });
    }
    if (url.includes("/chat_conversations")) return jsonResponse(LIST);
    return jsonResponse({}, 404);
  };
}

test("sends only conversations the server lacks at their latest version, with Claude's times", async () => {
  const seen = { details: [], posts: [] };
  const { ctx, store } = makeSandbox(claudeFetch(seen));
  store.chatsave_synced_threads = { "c-old": OLD_UPDATED };  // already saved at this version

  const result = await vm.runInContext("reconcileFromCloud()", ctx);
  assert.equal(result.success, true, JSON.stringify(result));
  assert.equal(result.enqueued, 1);
  assert.deepEqual(seen.details, ["c-new"], "c-old is current and c-ancient is older than 2 days");

  await waitUntil(ctx, "!isProcessingQueue");

  assert.equal(seen.posts.length, 1);
  const sent = seen.posts[0];
  assert.equal(sent.conversation_id, "c-new");
  assert.equal(sent.source, "reconcile");
  assert.equal(sent.captured_at, NEW_UPDATED, "conversation keeps Claude's updated time");
  assert.equal(sent.messages[0].timestamp, DETAILS["c-new"].chat_messages[0].created_at, "each turn keeps its own prompt time");
  assert.equal(sent.messages[0].content, "hi from phone");
  assert.equal(sent.messages[0].id, "c-new_msg_1_user", "same id scheme as the page capture");
});

test("a conversation is marked saved only after the server accepts it", async () => {
  const seen = { details: [], posts: [] };
  const { ctx, store } = makeSandbox(claudeFetch(seen));
  store.chatsave_synced_threads = { "c-old": OLD_UPDATED };

  await vm.runInContext("reconcileFromCloud()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");

  assert.equal(store.chatsave_synced_threads["c-new"], NEW_UPDATED);
  assert.equal(store.chatsave_synced_threads["c-old"], OLD_UPDATED, "untouched conversations keep their mark");
});

test("a failed save is not marked, so the next run sends it again", async () => {
  const seen = { details: [], posts: [] };
  const { ctx, store } = makeSandbox(claudeFetch(seen, 500));
  store.chatsave_synced_threads = {};

  await vm.runInContext("reconcileFromCloud()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");

  assert.equal(store.chatsave_synced_threads["c-new"], undefined, "server rejected it, so it must stay unsynced");
});

test("repeat runs within the minimum gap do nothing", async () => {
  const seen = { details: [], posts: [] };
  const { ctx } = makeSandbox(claudeFetch(seen));

  await vm.runInContext("reconcileFromCloud()", ctx);
  await waitUntil(ctx, "!isProcessingQueue");
  const detailsAfterFirst = seen.details.length;
  const second = await vm.runInContext("reconcileFromCloud()", ctx);

  assert.equal(second.reason, "ran recently");
  assert.equal(seen.details.length, detailsAfterFirst, "no second round of detail requests");
});
