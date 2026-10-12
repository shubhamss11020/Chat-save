---
conversation_id: 0506a4f8-9548-4277-b479-079071411ba2
platform: claude
username: "shubham"
title: "3GM Vault MCP QA investigation - Claude"
created_at: "2026-10-09T19:53:00.743164Z"
updated_at: "2026-10-12 11:17:32 EDT"
---

# 3GM Vault MCP QA investigation - Claude

## User (2026-10-12 11:17:32 EDT)

Act as an independent QA engineer investigating the 3GM Vault MCP. Explore its available capabilities and identify subtle or unexpected failure modes that ordinary testing might miss. Investigate boundary conditions, inconsistent search behavior, incorrect record associations, missing results, malformed outputs, unexpected defaults, and inconsistencies between documented and observed behavior. For every potential bug, provide a reproducible test case, actual result, expected result when verifiable, severity, and recommended next step. Do not invent bugs or claim to have tested functionality that you cannot access.

## Claude (2026-10-12 11:17:32 EDT)

I'll start by reading the 3gm-navigator skill, since it governs how the Vault connector should be used.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```


The skill is loaded and the Vault tools are available. I'll start with a baseline: identity, corpus stats, and a sample of the wiki.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```



Baseline is in. Identity isn't bound on this connection, and the corpus has grown since the skill's snapshot, which is expected. Next I'll probe boundary and malformed inputs, which is where I expect the failures to be.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```






The date and mailbox validation has some gaps: a reversed date range and a pre-archive range both return a silent "complete: true" empty result, and `limit=0` and a negative offset are accepted without complaint. Next I'll probe the lookup-by-id tools and the wiki's fuzzy matching.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```






Two more findings. The wiki's fuzzy title match resolved "3GM Roofing" to "3MG Roofing", a different company, and only flagged it as `closest`. And `search_raw` with empty input returns an empty result rather than an error. Next I'll check consistency between search tools and the no-argument paths.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```






Found a reproducible inconsistency. `list_emails` reports two attachments on the 10/9 report, and `get_source` shows an `.xlsx` named "Storage Tracking Report.xlsx", but `search_raw` for that exact phrase returns zero attachments. I'll confirm it directly and test the `mine` mailbox path, which should fail on an unbound connection.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```





Confirmed the attachment search gap. `search_raw` matches zero attachments for "Storage Tracking Report", while `list_attachments` finds 61 files with that exact filename. Last, I'll test the Eastern date boundary at the archive start and check pagination consistency.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```




## 3GM Vault MCP: QA findings

I tested read-only behaviour across the search, list, lookup, and wiki tools. I did not test writes (none are exposed), concurrency, rate limits, `expand_thread`, `top_correspondents`, or paging beyond the first page of attachment text. The connection is not bound to a user (`whoami` returns `signed_in: false`), so all tests ran with `mailbox="both"`.

Overall the error handling is mostly good. Invalid calendar dates, unknown mailboxes, unknown source types, nonexistent message IDs, and nonexistent page IDs all return clear errors. The defects below are where the tools return confident-looking results that are wrong or incomplete.

### Bugs

**BUG-1: `search_raw` misses attachments whose filenames match. Severity: High.**
- Repro: `search_raw(query="Storage Tracking Report", since="2026-10-01")`, default `search_attachments`.
- Actual: `attachments: []`, `attachment_total: 0`, `coverage.attachments_total: 0`.
- Expected: the tool's own docstring says it searches "subjects, bodies and attachment text" and that `search_raw` "also matches filenames." `list_attachments(filename_contains="Storage Tracking Report")` returns 61 matches, including att 49585 (msg 301381, 2026-10-09) and att 46347 (msg 291897, 2026-10-02) for this same phrase.
- BUG-1b: `search_attachments=false` returns output identical to the default. The flag has no visible effect here.
- Impact: attachments often hold the hard figures (the skill says so). A topic search can report nothing where attachments exist.
- Next step: check whether the filename field is in the `search_raw` tsvector or join path. Add a regression test with this exact phrase.

**BUG-2: Pre-archive date ranges return "complete: true" with zero results. Severity: High.**
- Repro: `list_emails(since="2025-01-01", until="2025-08-31")`.
- Actual: `messages: []`, `total_matching: 0`, `coverage.complete: true`, no note.
- Expected: the skill says the archive starts 2025-09-01 and that the tool should say the mail "does not reach back that far," not that nothing happened. The response should carry an out-of-coverage flag, not `complete: true`.
- Impact: a reader will take "no mail" as "no business."
- Next step: return a `coverage_start` field and set `complete: false` or add a `note` when the range falls before it.

**BUG-3: Reversed date ranges fail silently. Severity: Medium.**
- Repro: `list_emails(since="2026-09-10", until="2026-09-01")` and the same with `search_raw`.
- Actual: empty result, `complete: true`, no error.
- Expected: an error like the one for `2026-02-30`. Calendar validity is checked, but range order is not.

**BUG-4: Fuzzy title lookup crosses companies. Severity: Medium.**
- Repro: `get_wiki_page(title="3GM Roofing")`.
- Actual: returns page 384 "3MG Roofing", a different company, with `title_match: "closest"`. The body, facts, and `escalation_advised: true` are returned as if the page were the answer.
- Expected: for an entity title, return "no exact match" with suggestions, or require explicit confirmation. The response already lists unrelated roofing companies in `other_close_titles`, which shows the fuzzy matcher is treating "Roofing" as the identity.
- Impact: 3GM and 3MG differ by one letter, and the skill says never to merge identifiers without positive evidence. The wiki's own flags say these are distinct companies, so a caller that ignores `title_match` gets the wrong entity's prices.
- Next step: treat `title_match: "closest"` as a not-found for entity pages unless the match score is very high. Also make the returned title more visible in the body.

**BUG-5: Invalid pagination values are accepted and echoed. Severity: Low.**
- Repro A: `list_emails(limit=0)` returned 1 message.
- Repro B: `list_emails(offset=-5, limit=3)` returned 3 messages but echoed `"offset": -5` in the top-level result and in `coverage`.
- Expected: `limit=0` returns 0 results or an error. A negative offset should be rejected or clamped, with the clamped value echoed.
- Impact: a caller paging with a negative offset cannot tell from the response that the page is wrong.

**BUG-6: Inconsistent recurring-series labelling. Severity: Low.**
- Repro: `list_emails(subject="Storage Tracking Report", since="2026-10-01")` and `find_thread(subject="Storage Tracking Report", since="2026-10-01")`.
- Actual: `list_emails` says "2 separate conversations share these words (a recurring series, e.g. one per invoice or report)". `find_thread` says `recurring_series: false` for both threads. Both results say `exact_subject: false` even though the subject contains the phrase.
- Expected: the two tools agree on series status.

**BUG-7: Display name is an email address. Severity: Low.**
- Repro: `find_people(name="Cory")`.
- Actual: one candidate has `name: "greg.cors@custombiltmetals.com"` and kind `person`.
- Expected: a display name, or a clear fallback label.

### Behaviour to verify

- **Corpus growth.** `get_vault_stats` now reports 659 pages, 31,230 facts, 25,164 messages, and 14,215 attachments. The skill's snapshot from 2026-09-30 said 536 pages, 11,728 facts, 22,026 messages, and 10,781 attachments. Messages and pages grew plausibly over about ten days, but facts grew about 2.7x. Check whether fact counting changed or whether the snapshot was wrong. I did not confirm either.
- **Eastern time handling.** Message 301381 has `received_at` 19:06:40 UTC and displays as 15:06 ET, which is correct for EDT. The boundary at 2025-09-01 is also consistent.
- **Pagination.** Offset 0 and offset 1 with limit 2 overlap as expected.
- **Content anomaly (not a tool bug).** The 10/9 storage report lists Longhorn with "202MT remaining, storage ended on 9/26." Remaining stock on a storage that has already ended may be a real business issue. It needs checking against the ERP or with Kendra, not a fix in the tool.

### Summary

| ID | Severity | Area | Summary |
|---|---|---|---|
| BUG-1 | High | `search_raw` | Filename and attachment matches missing; `search_attachments` flag has no effect |
| BUG-2 | High | Date coverage | Pre-2025-09-01 ranges return `complete: true` with no warning |
| BUG-3 | Medium | Date validation | Reversed range returns silent empty result |
| BUG-4 | Medium | `get_wiki_page` | Fuzzy title resolves "3GM Roofing" to a different company (3MG) |
| BUG-5 | Low | Pagination | `limit=0` accepted; negative offset echoed uncorrected |
| BUG-6 | Low | Series labelling | `list_emails` and `find_thread` disagree on recurring series |
| BUG-7 | Low | `find_people` | Email address returned as display name |

**Sources:** msg 301381 · msg 291897 · msg 301383 · msg 301382 · msg 208716 · msg 208715 · att 49585 · att 46347 · att 46030 (+58 more matching "Storage Tracking Report.xlsx" from `list_attachments`) · wiki page 384 "3MG Roofing" · wiki page 595 "2026 Mid-Year Sales Review" (vault stats and tool responses only; no ERP queries run)

## User (2026-10-12 11:17:32 EDT)

Which customer complaints appear in the mail but have no entry on the customer’s wiki page?

## Claude (2026-10-12 11:17:32 EDT)

Claude responded: I'll start by searching the mail and the wiki for complaint language, then compare the two.
Investigating missing complaint records on the customer's page
Investigating missing complaint records on the customer's page
Investigating missing complaint records on the customer's page.
Investigating missing complaint records on the customer's page.

I’ll start by searching the mail and the wiki for complaint language, then compare the two.

Narrowing the search to customer-specific claim threads
Narrowing the search to customer-specific claim threads
Used 3gm vault

Used 3gm vault

The first pass found about 20 complaint threads that name a customer. Next I’ll check whether those customers have wiki pages and whether the pages record the complaints.

Checking remaining customers for matching complaint records
Checking remaining customers for matching complaint records
Used 3gm vault

Used 3gm vault

Georgia Metal Center is covered: its page records the July damaged-coil complaint with its source. Next I’ll check the other customers’ pages for claim and complaint entries.

Tracing unidentified complaint threads back to their customers
Tracing unidentified complaint threads back to their customers
Used 3gm vault

Used 3gm vault

Several customers have claim facts on separate analysis pages but not on the customer’s own entity page. I’ll check the customer pages directly for the complaint details, and identify two complaint threads whose customers I haven’t yet named.

Listing customer threads missing claim entries on their pages
Listing customer threads missing claim entries on their pages
Used 3gm vault

Used 3gm vault

Most of the customer pages I checked either record the complaint or have it only in narrative text. One complaint thread, “Re: Damaged Coil,” still has no customer name, so I’ll open its first message to identify the customer.

Drafting the gap summary table with per-customer source details
Drafting the gap summary table with per-customer source details
Used 3gm vault

Used 3gm vault

Four customers have complaints in the mail with no entry on their customer page, and two more have only narrative mentions. This is a partial answer. The complaint search returned 189 messages across 41 conversations, and I reviewed about 13 customer threads.

Customer	Complaint in the mail	Customer page	Gap
Carolina Carports Inc.	Coil claim after an accident, 28 Sep 2026 (msgs 276978, 277020)	Page 164 has no fact about a claim or damage	No entry. Full body not read
Englert Inc.	Wrong-material claims against Wheeling-Nippon, open since 28 Sep 2026; on 12 Oct Matt Inman put the claim file at almost 130,000 lb (msgs 277095, 282378, 301465)	Page 181 has no claim or defect fact. The dispute sits only on separate page 535	No entry on the customer page. Full body not read
Pine View Buildings, LLC	Damaged blue coil, Apr–Aug 2026 (thread from msg 48716)	Page 357 has no damage fact	No entry. Body not read
Farris Metal Products	Customer claim on black painted coil, settled by release 8 Sep 2026	No customer page found; the only entry is analysis page 499	No customer page exists
Porta Grace MFG	Bright White quality claim, 26 Aug–2 Sep 2026 (msgs 46952, 46955)	Page 111 mentions the claim in narrative only; detail is on pages 109 and 110	Narrative only
B & C Metals LLC	Claim notice, 20 Aug–9 Sep 2026, closed by credit memo RINV/2026/0044	Page 606 mentions the claim in narrative; its facts record only the credit status	Narrative only

Covered (complaint recorded on the customer page): Georgia Metal Center (page 217, damaged coils, msg 49409); Vertex Building Supply (page 155, damaged-coil claim, msg 47972); Swiss Metals (page 141, June claim, att 13626); Timber Building Company (page 466, PO2490 claim, msg 65764); Five Star Metal Buildings LLC (page 648, claim test results, msgs 48809 and 48829).

Excluded as supplier-side claims, not customer complaints: the white-spotting claim on paint code 1K303Q1 filed against Prosperity Tieh (msg 50271), the Precoat claims, and the PT Acrylic claims. I did not check whether the Ternium Black Crinkle claim (23 messages) is a customer or supplier claim.

Scope and caveats

I checked structured facts on each page for claim and damage wording, plus the page excerpts. For Carolina Carports and Englert the full bodies are 85,000 and 112,000 characters, and I did not read them. A narrative mention may exist, so confirm before acting on those two.
The rest of the 189 messages are unreviewed, so there may be more customers in the gap.

Sources: page 217 (msg 49409, 49388); page 155 (msg 47972); page 141 (att 13626, msg 64769); page 466 (msg 64606, 65764); page 648 (msgs 48809, 48829, att 11931); page 62; page 499; page 111; pages 109, 110; page 606 (msg 45639); page 164 (msgs 276978, 277020); page 181 (msgs 277095, 282378, 301465); page 535; page 357 (msg 48716); msg 46952, 46955; msg 50271


Create a spreadsheet
