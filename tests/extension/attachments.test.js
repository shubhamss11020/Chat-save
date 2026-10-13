// Run with: node --test tests/extension/attachments.test.js
// Inline attachments are uploaded once through a presigned URL; the queued copy keeps only the link.
// If presigning fails, the file stays inline.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const { makeSandbox, waitUntil, jsonResponse } = require("./harness");

const DATA_URL = "data:text/plain;base64,aGVsbG8="; // "hello"

function fakeNetwork({ presignOk = true, posted, uploads }) {
  return async (url, opts = {}) => {
    if (url.endsWith("/api/attachments/presign")) {
      if (!presignOk) return jsonResponse({ detail: "S3 not configured" }, 503);
      return jsonResponse({
        upload_url: "https://s3.test/put/k1",
        file_url: "https://cdn.test/k1",
        s3_key: "attachments/alex/conv/k1_notes.txt",
        headers: { "Content-Type": "text/plain", "Content-Disposition": 'inline; filename="notes.txt"' },
      });
    }
    if (url.startsWith("https://s3.test/put/")) {
      uploads.push({ url, body: Array.from(opts.body), headers: opts.headers });
      return { ok: true, status: 200, json: async () => ({}), text: async () => "" };
    }
    if (url.endsWith("/ingest-batch")) {
      const { items } = JSON.parse(opts.body);
      posted.push(...items);
      return jsonResponse({
        results: items.map((i) => ({ receipt_id: "r", conversation_id: i.conversation_id, saved_messages: 1, status: "persisted" })),
      });
    }
    return jsonResponse({}, 404);
  };
}

const payload = () => ({
  conversation_id: "conv-att",
  title: "With file",
  messages: [{ id: "m1", sequence: 1, role: "user", content: "see attached" }],
  files: [{ name: "notes.txt", path: "attachments/notes.txt", type: "text/plain", content: DATA_URL, role: "user", turn_sequence: 1, is_attachment: true }],
});

test("the queued copy keeps a link, and the bytes are uploaded once", async () => {
  const posted = [];
  const uploads = [];
  const { ctx, store } = makeSandbox(fakeNetwork({ posted, uploads }));

  await vm.runInContext("enqueue(__payload)", Object.assign(ctx, { __payload: payload() }));
  await waitUntil(ctx, "!isProcessingQueue");

  assert.equal(uploads.length, 1, "one upload");
  assert.deepEqual(uploads[0].body, [104, 101, 108, 108, 111], "the uploaded bytes are the decoded file");
  const sent = posted[0].files[0];
  assert.equal(sent.url, "https://cdn.test/k1");
  assert.equal(sent.uploaded_to_s3, true);
  assert.equal(sent.content, "", "no inline bytes in the request body");
  assert.ok(store.chatsave_issued_uploads.includes("https://s3.test/put/k1"), "the upload URL is recorded as issued");
});

test("if presigning fails, the file stays inline", async () => {
  const posted = [];
  const uploads = [];
  const { ctx } = makeSandbox(fakeNetwork({ presignOk: false, posted, uploads }));

  await vm.runInContext("enqueue(__payload)", Object.assign(ctx, { __payload: payload() }));
  await waitUntil(ctx, "!isProcessingQueue");

  assert.equal(uploads.length, 0);
  assert.equal(posted[0].files[0].content, DATA_URL, "the file was not lost; it is still inline");
  assert.equal(posted[0].files[0].uploaded_to_s3, undefined);
});
