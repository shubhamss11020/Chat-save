---
conversation_id: cadbf6a0-c48b-4cf1-adb8-4ac2a2443032
platform: claude
username: "shubham"
title: "3GM Vault MCP tools analysis"
created_at: "2026-10-09T19:58:07.495656Z"
updated_at: "2026-10-12 12:32:07 EDT"
---

# 3GM Vault MCP tools analysis

## User (2026-10-12 12:32:07 EDT)

Examine all tools and operations exposed by the 3GM Vault MCP. For each available operation, determine its intended purpose, required inputs, optional parameters, expected output, and error behavior from the available documentation and observed results. Identify missing tools, inconsistent parameter handling, unexpected output formats, unclear errors, and operations that appear to behave differently from their documented purpose. Do not execute destructive operations or modify production data during testing.

## Claude (2026-10-12 12:32:07 EDT)

I'll start by loading the vault tool schemas and the 3gm-navigator skill, since your preferences require the skill before any 3GM query.
```

```

```

```

The skill is loaded. Next I'll run read-only probes across the vault tools, including a few deliberately malformed calls to check error behavior.
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

Every call failed with the same error: `user_exact_quote` is reported as required, even though the schema marks it optional with a null default. I'll retry with that field populated from your message to see whether the tools work once it's supplied.
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

The main operations now respond. I'll run one more batch of read-only checks on the remaining tools.
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

## Vault MCP audit

No destructive operations were run. Every call was a read or a deliberately malformed read, and the vault exposes no write tools.

### Blocking issue: `user_exact_quote` is effectively required

The schema marks `user_exact_quote` as optional with a null default. The server rejects any call that omits it with `Field required`. This affected every tool I called on the first attempt, and it is the most important finding. Calls succeed only when the field is supplied. The field's description asks for the user's exact raw message, which I did not always follow. Several later calls used a shortened excerpt of the audit request, so the audit trail is inconsistent.

**Fix:** either make the field genuinely optional on the server, or change the schema default so clients stop sending it as a required argument.

### Per-tool results

| Tool | Result | Notes |
|---|---|---|
| `whoami` | Works | Returned `signed_in: false` for this connection. Any "my email" question must then ask which mailbox is meant. I did not test `mailbox="mine"`. |
| `get_vault_stats` | Works | 659 pages, 31,230 facts, 25,164 messages, 14,215 attachments. |
| `list_wiki_pages` | Works | Pagination is reported (`total_matching: 403`, `truncated: true`). |
| `search_wiki` | Works | Returns `raw_mail_matches` and a note to use `search_raw` for counts. |
| `find_facts` | Works, unhelpful on miss | An unknown key returns `count: 0` and an empty `sources_line`. It does not say whether the key is unknown or simply has no matches. |
| `get_wiki_page` | Works on miss | Returns `{"error": "no such page"}` in-band. Fuzzy title matching was not tested. |
| `get_source` | Works on miss | Unknown `source_type` returns an in-band error without listing valid types. |
| `list_emails` | Works | Rejects unknown parameters with a helpful list of valid ones. This is the best error handling of the set. |
| `search_raw` | Works | Stemming and phrase matching are reported in `interpretation`. Completeness and thread counts are clear. |
| `find_thread` | Works | Separates exact-subject threads from near-matches and reports `coverage.complete`. |
| `find_people` | Works | Reports `ambiguous` and `used`. |
| `top_correspondents` | Works | Reports how many automated messages were excluded. |
| `get_email` | In-band error | `message_id: -1` returns `no such message`. Valid-id behaviour was not tested. |
| `get_attachment_text` | In-band error | `attachment_id: -1` returns `no such attachment`. |

**Not tested:** `expand_thread`, `list_attachments`, `get_source` on a valid id, `get_attachment_text` on a valid id, `find_facts` with a real key, and paging with `offset`.

### Inconsistencies and concerns

1. **Two error styles.** Validation problems raise exceptions with a pydantic message. Not-found conditions return in-band JSON `{"error": ...}`. Callers have to handle both.
2. **Stale snapshot in the skill.** The navigator skill quotes 536 pages, 11,728 facts and 22,026 messages. The live stats are 659, 31,230 and 25,164. The skill flags its figures as a dated snapshot, but its numbers are about a third of current. Any agent that trusts the skill's figures will under-report coverage.
3. **Pipeline text leaks into excerpts.** `search_wiki` excerpts for "Ace Metal Sales" and "Mac Metal Sales" contain drafting metadata such as "[Merged from a draft by …]", "staging 1122", and notes about consolidation. These are internal artifacts and should not reach user-facing answers.
4. **Sensitivity tags are visible but not enforced in listings.** `list_wiki_pages` shows `personal-data`, `related-party-financial` and `sensitive` tags on the 3GM Steel and 2B Holdings pages. This is informational only. There is no filter to exclude tagged pages, so callers must handle them manually.
5. **Mailbox-ID mismatch.** `mailbox` accepts `travis`, `stefan`, `mine` and `both`, but results echo internal IDs such as `3gm_travis_outlook` and `mailbox: both`. The vocabulary differs between input and output.
6. **Pagination on `search_wiki`.** It has a `limit` but no `offset`, so results beyond the first page cannot be reached through it.

### Missing or unclear capabilities

- No way to tell whether a fact key exists at all, which makes `find_facts` misses ambiguous.
- No tool lists valid `source_type` values, so callers must guess or read the documentation.
- No obvious mailbox listing or validation call.

Sources: msg 301381 · msg 301383 · msg 291897 · wiki page 337 (Ace Metal Sales, excerpt only) · wiki page 307 (Mac Metal Sales, Inc., excerpt only) · tool outputs from `get_vault_stats`, `list_wiki_pages`, `find_thread`, `top_correspondents` and `find_people`
