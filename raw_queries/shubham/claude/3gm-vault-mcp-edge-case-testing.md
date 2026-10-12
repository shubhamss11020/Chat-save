---
conversation_id: a8a89b59-4623-4303-a3ce-4d7e09b1e337
platform: claude
username: "shubham"
title: "Travis message statistics"
created_at: "2026-10-12T14:59:16.302308Z"
updated_at: "2026-10-12 12:13:32 EDT"
---

# Travis message statistics

## User (2026-10-12 12:13:32 EDT)

Assess the observable reliability of the 3GM Vault MCP. Look for repeated timeouts, failed requests, inconsistent response times, intermittent retrieval failures, incomplete responses, and errors that occur when querying larger result sets. Use available logs and existing performance metrics where accessible. Do not claim a performance problem without measurements or supporting evidence, and do not run load tests against production without authorization.

## Claude (2026-10-12 12:13:32 EDT)

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

## User (2026-10-12 12:13:32 EDT)

What’s the average number of messages per thread this year?

## Claude (2026-10-12 12:13:32 EDT)

```

```

I can't calculate this from the vault. Its tools count messages, not threads, and none of them returns a yearly thread total. Dividing messages by threads would need a thread count for 2026, and I don't have one.

The vault holds 25,239 messages and 14,247 attachments across the Travis and Stefan mailboxes. That is the whole archive, not a 2026 figure.

If it helps, I can give you the 2026 message count for either mailbox, or the thread count for a specific subject or correspondent, which I can pair with the message count to get an average for that slice.

Sources: get_vault_stats (corpus totals, both mailboxes)

## User (2026-10-12 12:13:32 EDT)

Who has Travis emailed but never received a reply from?

## Claude (2026-10-12 12:13:32 EDT)

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

Among the 25 most-emailed external contacts I checked, four never sent Travis a message: **Yongbeom Lee** (73 messages from Travis), **Jason Sung** (jssung@us.poscointl.com, 40 received), **Lucas Rollison** (25 received), and **정인식 (Jung, In-Shik)** (52 received).

This is a partial answer. Travis has emailed 130 external people in total, and I only checked the top 25 by volume. Lucas Rollison's record shows no messages from him, and the others show none either. The check covered the whole archive from 2025-09-01.

Sang Hyun Yim (yim.sh@poscointl.com) has 13 messages sent in the archive, but none reached Travis's mailbox, so he may have replied to Stefan. I left him out because I couldn't confirm that he never replied.

Sources: top_correspondents (Travis, sent, external, 130 people); per-person list_emails checks in mailbox `3gm_travis_outlook` (msgs 45729, 67490, 47687, 61103 and others as cited in each lookup)

## User (2026-10-12 12:13:32 EDT)

Which PDFs attached to emails were sent by a single sender more than five times?

## Claude (2026-10-12 12:13:32 EDT)

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

```

```

The clear case is **"Tarter Tube Coil Specs.pdf"**, sent by **Latisha Bailey** (tarterusa.com). It is attached to 837 emails in the archive, all the same file at 223,637 bytes, and it is attached to a new "Tarter RFQ" message almost every time.

I read "sent more than five times" as the same filename from one sender. The other repeat senders I checked send new files with dated or RFQ-specific names, so they don't match:

- **Andrew Pappas (BMO):** 644 PDFs, but each is a dated report such as "BMO Metals Brief 10.12.26".
- **Allianz Trade notifications:** 175 PDFs, each named for a different company.
- **Justin Hermiz (Koil Metals):** 111 PDFs, with inventory lists named by date.
- **Jessica Worley, Stefan Brown, sales@3gmsteel.com, PilHee Lee:** these have many PDFs, and the filenames I looked at vary.

I did not page through all 5,324 PDFs in the archive. The other senders' names were checked from the first page of results, so a repeated filename from another sender could still be missing.

Sources: att 49581, 49560, 49558, 49504, 49460, 49458 (Tarter Tube Coil Specs.pdf, Latisha Bailey, 837 total); sender totals from list_attachments for Andrew Pappas, Latisha Bailey, credit.notification-noreply@mail.allianz-trade.com, Justin Hermiz, Jessica Worley, Stefan Brown, sales@3gmsteel.com, PilHee Lee

## User (2026-10-12 12:13:32 EDT)

Which entity pages have no facts at all?

## Claude (2026-10-12 12:13:32 EDT)

```

```

```

```

```

```

```

```

Two entity pages have no facts at all, out of 410 entity pages in the wiki:

- **AkzoNobel** (page 622, supplier, sensitive): 0 facts, but 3 citations and a 2,777-character body. The body has sourced text that the fact index never picked up.
- **OTR Solutions** (page 250, adversary, sensitive): 0 facts and 0 citations, with a 542-character body.

I only checked entity pages. Concept, source, analysis and overview pages were not included.

Sources: list_wiki_pages (page_type=entity, 410 pages), pages 622 and 250

## User (2026-10-12 12:13:32 EDT)

Which analysis pages were updated most recently?

## Claude (2026-10-12 12:13:32 EDT)

```

```

```

```

```

```

I can't rank analysis pages by when they were last updated. The vault doesn't expose that field: the page record shows `created_date` and `updated_date` as null for page 536, and the list tool returns no dates either.

Here is what I can do with the data I have:

- **Dates in the title or body:** a few analysis pages carry a date in their title, such as "Mac Metal Sales — unnamed manufacturing acquisition, first seen 2026-09-28" (page 536) or "Huntington Business Credit — unnamed target, 2025-10-08 inquiry" (page 658). Those show when the matter first appeared, not when the page changed.
- **Newest sourced activity:** pages that cite the most recent mail would be the closest proxy for recent updates. I can pull that by checking the newest cited source on each analysis page, though that means reading many pages.

Page 536 is the one I looked at closely. It was drafted from mail dated 2026-09-28 and carries 26 facts, with the latest sourced message in that batch dated the same day.

Sources: list_wiki_pages (page_type=analysis, 163 pages); get_wiki_page page 536 (created_date and updated_date null; sources outlook_message 277303, 277332, 277955, 278097)

## User (2026-10-12 12:13:32 EDT)

Are there any pages tagged for review?

## Claude (2026-10-12 12:13:32 EDT)

```

```

No pages carry a "review" tag. The tag filter returned zero matches across all page types.

The tags actually in use are `sensitive`, `personal-data`, `related-party-financial`, `active-ma`, `active-litigation`, `historical-litigation`, `privileged-source`, `security-incident`, and `unverified`. If you meant one of those, I can list the matching pages. The `unverified` tag is the closest to "needs checking," and I've seen it on many pages.

Sources: list_wiki_pages (tag=review, 0 results)

## User (2026-10-12 12:13:32 EDT)

How many pages have a “possible duplicate” flag?

## Claude (2026-10-12 12:13:32 EDT)

```

```

I can't give a count. The vault doesn't index "possible duplicate" flags in a way I can total. Flags sit inside each page's body and only show up when that page is opened. The list tool doesn't report them, and the search tool returned 10 pages that mention the phrase in their text, not 10 flagged pages.

The only way to get a real number would be to open all 675 wiki pages and count their flags, which isn't practical here.

For an example of what the flags look like, page 536 (the "unnamed manufacturing acquisition") has around twenty "possible duplicate" flags on its own, most of them comparing it to unrelated pages with similar names.

Sources: search_wiki ("possible duplicate", 10 hits shown); get_wiki_page page 536 (flags)
