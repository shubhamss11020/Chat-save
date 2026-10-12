---
conversation_id: 5d0a5d3b-e6a3-4c6c-80da-cedc9a27b7a2
platform: claude
username: "shubham"
title: "3GM Vault MCP edge case testing"
created_at: "2026-10-12T14:59:16.302308Z"
updated_at: "2026-10-12 13:29:49 EDT"
---

# 3GM Vault MCP edge case testing

## User (2026-10-12 13:29:49 EDT)

Evaluate how the 3GM Vault MCP handles edge cases, including empty searches, missing parameters, invalid identifiers, nonexistent records, unusually long inputs, special characters, ambiguous queries, and unsupported request formats. Use safe, read-only tests wherever possible. Record unexpected failures, unclear error messages, inconsistent responses, and cases where the MCP reports success without returning the expected information.

## Claude (2026-10-12 13:29:49 EDT)

I'll start by loading the 3gm-navigator skill, as your preferences require for any 3GM question.
```

```

```

```

The tools are loaded. I'll start with a baseline call and then run a batch of read-only edge cases.
```

```

```

```

```

```

```

```

```

```

```

```

Baseline results: the admin token is not signed in, and empty `search_wiki` returned 10 hits without an error. Next I'll test missing identifiers, bogus IDs, unknown parameters, and special characters.
```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

Several results are useful so far. `find_facts` with no filters returned an arbitrary 3-row sample without complaining, and an unknown mailbox returned a clear error. Next I'll test inverted date ranges, the no-identity `mine` mailbox, empty and oversized inputs, and a real citation round-trip.
```

```

```

```

```

```

```

```

```

```

```

```

```

```

Most of the edge cases behave cleanly. The notable ones so far are an inverted date range that returns an empty "complete" result without an error, and an enormous query that is accepted without any length limit. I'll run one more batch on the remaining tools.
```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

## 3GM Vault MCP edge-case evaluation

I ran about 33 read-only calls across 16 vault tools. Nothing was written, sent, or saved to memory. I did not open the content of personal or sensitive pages beyond the search excerpts. Most edge cases fail cleanly, but a few return a "success" that hides a problem.

### Unexpected results (most serious first)

1. **Inverted date range returns a silent empty success.** `list_emails(since="2026-09-30", until="2026-09-01")` returned 0 messages with `coverage.complete: true` and no error. The caller cannot tell this apart from "no mail that week". It should reject `since > until`.
2. **Unlimited query length is accepted.** `search_raw` ran a query of about 3,000 characters with no size limit. It matched 16,265 messages and echoed the entire query back in the response. A cap or a clear error is needed.
3. **Negative `length` is accepted silently.** `get_attachment_text(length=-100)` returned 18,326 characters, which is neither an error nor the default. It also cut mid-token at the end of the returned slice.
4. **Empty input returns results with no error.**
   - `search_wiki(query="")` returned 10 hits, ordered by page_id, with `score: null`. Nothing is ranked.
   - `find_facts` with no filters returned an arbitrary 3-row sample from one page, presented as results.
   - `find_people(name="")` returned `count: 0` with no error.
5. **Raw database error leaks.** `list_wiki_pages(page_type="spaceship")` surfaced a Postgres message ("invalid input value for enum wiki_page_type", "unnamed portal parameter $1"). Other tools return a clean error for the same kind of input, so this is inconsistent and exposes internals.
6. **`get_source` returns raw HTML.** For message 65122 the body was full HTML with Word styles and a Yesware tracking pixel. Also, a sent item is labelled `received_at`.
7. **Citation inconsistency in `find_facts`.** The `as_of` row is `page_metadata` with no source, yet it still appears in the `sources_line` as a source.
8. **Search output shows stemmed fragments.** Searching for SQL-like text showed `tabl` and `messag` as the "words" searched. This is technically accurate but confusing to a reader.

### Handled correctly

| Test | Result |
|---|---|
| Nonexistent message / page / attachment ID | Clear "no such" error |
| Unknown `source_type`, `mailbox`, `mailbox="mine"` with no sign-in | Clear error listing valid values or the fix |
| Invalid date `2026-02-31` and relative date "Last Tuesday" | Clear error stating the accepted formats |
| Unknown argument `start_date` | Rejected, with the valid parameter list |
| `get_wiki_page` with no identifier; `expand_thread` with no ID; `find_thread` with empty subject | Clear errors |
| Unknown sender name | Error that suggests `find_people` |
| Nonexistent subject, SQL-like and Unicode input | Zero results, no crash, no injection effect |
| Decimal ID for `get_source` | Clear pydantic validation error |

### Notes

- `whoami` returns `signed_in: false` on this admin connection, so `mine` is correctly refused.
- `get_vault_stats` now reports 675 live pages, 32,584 facts, 25,250 messages and 14,250 attachments. The navigator skill's snapshot says 536, 11,728, 22,026 and 10,781 as of 2026-09-30. The skill itself says to treat that snapshot as stale, so this is a documentation refresh, not a bug.
- Not tested: pagination past a real result set (only past zero matches), and `get_source` for attachments by real ID.

Sources: vault stats (get_vault_stats); msg 65122 (get_source); msg 301481 and att 49620 (search_raw); att 49620 text (get_attachment_text).
