---
conversation_id: 1f80a0e1-611d-44fc-a427-0275a308d43c
platform: claude
username: "shubham"
title: "3GM Vault MCP QA investigation"
created_at: "2026-10-09T19:53:00.743164Z"
updated_at: "2026-10-12 12:32:13 EDT"
---

# 3GM Vault MCP QA investigation

## User (2026-10-12 12:32:13 EDT)

Act as an independent QA engineer investigating the 3GM Vault MCP. Explore its available capabilities and identify subtle or unexpected failure modes that ordinary testing might miss. Investigate boundary conditions, inconsistent search behavior, incorrect record associations, missing results, malformed outputs, unexpected defaults, and inconsistencies between documented and observed behavior. For every potential bug, provide a reproducible test case, actual result, expected result when verifiable, severity, and recommended next step. Do not invent bugs or claim to have tested functionality that you cannot access.

## Claude (2026-10-12 12:32:13 EDT)

I'll start by reading the 3GM navigator skill, as your preferences require for anything touching the 3GM connectors, then load the Vault tool schemas.
```

```

```

```

Schemas are loaded. I'll start with a baseline: the stats and identity endpoints, then the documented behaviours I can check.
```

```

```

```

Two early observations: the stats report 675 wiki pages and 32,584 facts, while the skill's snapshot says 536 and 11,728 (the skill itself says that snapshot is stale). The connection is unauthenticated (`signed_in: false`), so any "mine" query should now behave differently. I'll probe boundaries and invalid inputs next.
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

First findings: an inverted date range (`since` after `until`) silently returns zero results instead of an error, `limit=0` returns one message, and an oversized `offset` produces a raw database timeout. I'll test identifier handling and the wiki next.
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

New findings: an empty `search_wiki` query returns ten ranked hits with `score: null`, and live wiki excerpts contain drafting-pipeline meta-text ("This draft is an addition to the existing page… deliberately titled to match…"), which is a likely leak of internal maintenance text into published page bodies. Next I'll test unbounded and malformed inputs across the fact, people and attachment tools.
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

Another error-handling finding: `list_wiki_pages` with an invalid `page_type` leaks a raw Postgres error ("unnamed portal parameter $1"), which is an implementation detail exposed to the caller. The `top_correspondents` inverted range also visibly reports `2026-06-01` to `2026-04-01` and still returns an empty success. Now I'll test the remaining parameter validation and check whether the meta-text leak is in the stored page body.
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

Two more findings: `search_raw` silently accepted `order="sideways"` and fell back to newest without an error, and `get_attachment_text` returned empty text at `offset=-5` (negative offset not validated). The `length=0` result may also be a parameter artifact, so I'll retest with defaults. Next I'll check citation integrity: whether facts actually match the messages they cite.
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

The large page dump confirmed several things: duplicated `links_in` entries, a self-link from the Georgia Metals page to itself, and repeated identical flags. I'll run a last round of consistency checks: thread counts across tools, key-matching behaviour, and an empty-range completeness signal.
```

```

```

```

```

```

```

```

**Summary:** I found 14 issues in the Vault MCP. Two are high severity: a fuzzy page filter attributes one entity's facts to another, and draft-pipeline text appears in live page bodies. The rest are medium or low: silent failures on bad input, misleading completeness flags, leaked database errors, and some citation and provenance problems. The connection is unauthenticated (`whoami` returns `signed_in: false`), so I passed `mailbox` explicitly and assumed no identity. All testing was read-only.

| # | Severity | Issue |
|---|---|---|
| F1 | High | `find_facts` with a page filter returns facts from a different entity |
| F2 | High | Draft-pipeline meta text is stored in live wiki bodies |
| F3 | Medium | Inverted date ranges return a silent empty success |
| F4 | Medium | Pre-archive date ranges report `complete: true` |
| F5 | Medium | Raw database errors leak to the caller |
| F6 | Medium | Price facts come back with no recency ordering, and some values are malformed |
| F7 | Medium | Wiki page link and flag lists contain self-links, duplicates and pipeline reasoning |
| F8 | Low–Med | A fact's provenance is labelled `sourced` but the cited message doesn't support it |
| F9 | Low | Invalid parameters are silently coerced instead of rejected |
| F10 | Low | `find_people` ties contradict the documented preference |
| F11 | Low | Empty `search_wiki` query returns ranked hits with `score: null` |
| F12 | Low | `find_facts` gives no total or truncation indicator |
| F13 | Low | Exact `fact_key` misses return zero with no near-key hint |
| F14 | Low | The skill's build snapshot is stale against live stats |

**F1 (High): Cross-entity attribution**
- Repro: `find_facts(page="Georgia Metals", key_words="credit limit")`
- Actual: 7 rows, one from page 217 "Georgia Metal Center" (`credit_limit_usd` 250000, msg 224288). The Georgia Metals page's own `links_out` says Georgia Metal Center is a separate entity with no shared address, domain or contact.
- Expected: no rows from another entity, or rows clearly labelled as belonging to it. The documented fuzzy match covers "near-duplicate pages of the same entity", which this is not.
- Next step: prefer an exact title match and never fuzzy-match onto a page that is a distinct entity. Show `page_title` prominently in every fact row.

**F2 (High): Pipeline text in live bodies**
- Repro: `get_wiki_page(page_id=1, body_chars=1200)`
- Actual: the body opens with "[Merged from a draft by outlook_3gm_travis_outlook] **Addition to the existing 'Georgia Metals' page (live_page_id 1).** Does not restate…". Search excerpts from pages 2, 5, 6, 7, 8 and 12 show the same kind of text ("This draft is an addition to… deliberately titled to match… so that consolidation merges it").
- Expected: entity content only. This body is the authority when facts are stale, so readers and answering models will take the drafting notes as account facts.
- Next step: strip merge boilerplate at promotion, and add a check that fails publication when it is present.

**F3 (Medium): Inverted ranges return silent success**
- Repro: `list_emails(since="2026-10-01", until="2026-09-01")` and `top_correspondents(since="2026-06", until="2026-04-01", mailbox="both")`
- Actual: `messages: []` / `top: []`, `complete: true`. The response even echoes the inverted range (`["2026-10-01 00:00 ET","2026-09-01 23:59 ET"]`).
- Expected: an error stating that `since` is after `until`. Silence here reads as "no mail", which is the failure mode the skill warns about.

**F4 (Medium): Pre-archive ranges report completeness**
- Repro: `list_emails(since="2025-08-01", until="2025-08-31")` and `search_raw(query="invoice", since="2025-08-01", until="2025-08-31")`
- Actual: zero results with `coverage.complete: true`. Nothing says the archive starts on 2025-09-01.
- Expected: `complete: false` or an explicit "outside archive coverage" note.

**F5 (Medium): Raw database errors**
- Repro: `list_wiki_pages(page_type="banana")` and `search_wiki(query="Georgia Metals", page_type="banana")`
- Actual: "invalid input value for enum wiki_page_type… CONTEXT: unnamed portal parameter $1/$7". Enum values go straight into SQL.
- Repro 2: `list_emails(offset=99999999, limit=3)` returns "canceling statement due to statement timeout" with no structured error.
- Expected: validated errors listing valid values, which `search_raw` already does for `recipient_role` and `mailbox`. An out-of-range offset should return an empty page, not a timeout.

**F6 (Medium): Price facts without recency**
- Repro: `find_facts(page="Ace Metal Sales", key_words="price black 117l per lft")`
- Actual: two rows for the same key. One is `2.20 (quantity_raw: "2")` with no `as_of`. The other is `2.33`, `as_of` 2026-06-10. Neither is marked current, and the value string has parser residue. Some `as_of` fields also hold free text (`"2026-04-02, Limit Endorsement No. 00001622"`, `"2026-03-31, status: pending"`).
- Expected: sorted by date, with the undated row flagged. Values clean. `as_of` a date or null.

**F7 (Medium): Wiki page structure**
- Repro: `get_wiki_page(page_id=1, facts_limit=5)`
- Actual: `links_in` lists page 1 as a linker of itself four times. `links_out` has four self-links to page 1 and six entries for page 257. The `flags` array has several verbatim duplicates (for example, the "extensive existing coverage" flag appears at least twice). Flags also contain drafting reasoning ("staging 5855", "flag 6954", "§1.7b").
- Expected: no self-links, one entry per link, deduplicated flags written for a reader.

**F8 (Low–Med): Provenance label not supported by the cited source**
- Repro: `find_facts(page="Georgia Metals"` … or page 188 `stakeholder_notified`, cite msg 64093)
- Actual: "Corey McGlothlin (CEO/Owner, 3GM Steel and Mac Metal Sales)" is marked `sourced`. `get_source(outlook_message, 64093)` shows only a greeting "Corey," and no title.
- Expected: the title is `agent_judgement`, or the citation shows the recipient record that supports it.

**F9 (Low): Silent coercion**
- `search_raw(order="sideways")` runs as newest-first with no error.
- `list_emails(limit=0)` returns one message.
- `get_attachment_text(attachment_id=49596, offset=-5)` and `length=0` return empty text with `has_more: true`.
- Expected: validation errors for each.

**F10 (Low): Ties contradict the documented preference**
- Repro: `find_people(name="Cory")`
- Actual: `used` = Cory Godsey, Cory Parsons, Cory Padgett, all `match_score` 1.0, `ambiguous: true`. The skill says "Cory" resolves to Cory Godsey and that exact spelling beats volume. I didn't confirm whether `list_emails` uses the same set.
- Next step: run `list_emails(sender="Cory")` and compare with `used`.

**F11 (Low): Empty query returns ranked hits**
- `search_wiki(query="")` returns 10 hits with `score: null` and no error. The ordering is undefined. Expected: a validation error, consistent with a minimum query length.

**F12 (Low): No completeness signal on `find_facts`**
- `find_facts()` with no filters returns 50 rows and no `total_matching` or `truncated`. The mail tools report both.

**F13 (Low): Exact-key miss gives no hint**
- `find_facts(page="Georgia Metals", fact_key="credit_limit")` returns zero. The same page has `credit_limit_usd`. The tool is documented as exact-match, so this is usability, not a defect.

**F14 (Low): Stale skill snapshot**
- The skill's build status reports 536 pages, 11,728 facts, 22,026 messages and 10,781 attachments. Live stats report 675, 32,584, 25,248 and 14,250. The skill flags its snapshot as stale, so this is drift rather than a bug, but the snapshot should be refreshed.

**Checks that passed**
- SQL-style input in `value_contains` returned empty with no error (parameterized queries).
- `2026-02-30` was rejected cleanly.
- Unknown mailbox, `recipient_role`, and `source_type` values returned clear errors.
- Nonexistent message IDs, attachment IDs and pages returned clean "no such" errors. Empty person name returned empty.
- Citations spot-checked against source: `lead_times_raw` (msg 63574), `bluescope_terms_raw` (63574), `status_raw` (64093) and `rep_commitment` (46323) are supported by their cited messages.
- `expand_thread(301479)` returns 4 messages, matching `find_thread` and `get_source`'s `thread_message_count`.
- Attachment 49596 returns its full 989 characters with default parameters.

**Not tested:** the signed-in `mailbox="mine"` path, ERP cross-checks, and write operations. The `get_wiki_page` output for page 1 was truncated at 100K characters, so flags after that point were not reviewed.

**Recommended next steps, in order:** fix F1 and F2 first, since both can put wrong facts in front of Travis and Stefan. Then fix date validation (F3, F4) and error handling (F5), then the wiki structure issues (F7, F8).

Sources: page 1 (Georgia Metals, body, flags, links), page 217 (Georgia Metal Center, fact credit_limit_usd, msg 224288), page 188 (.0160 Program, msgs 63574, 64093), page 337 (Ace Metal Sales, msgs 69023, 62300), page 595 (2026 Mid-Year Sales Review, msg 46323), msg 301479 and thread 301477–301481, att 49596 (msg 301401), list_wiki_pages and search_wiki (enum errors), find_people("Cory")

## User (2026-10-12 12:13:05 EDT)

Which customer complaints appear in the mail but have no entry on the customer’s wiki page?

## Claude (2026-10-12 12:13:05 EDT)

I'll start by reading the 3GM navigator skill, as your preferences require for anything touching the 3GM connectors, then load the Vault tool schemas.
```

```

```

```

Schemas are loaded. I'll start with a baseline: the stats and identity endpoints, then the documented behaviours I can check.
```

```

```

```

Two early observations: the stats report 675 wiki pages and 32,584 facts, while the skill's snapshot says 536 and 11,728 (the skill itself says that snapshot is stale). The connection is unauthenticated (`signed_in: false`), so any "mine" query should now behave differently. I'll probe boundaries and invalid inputs next.
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

First findings: an inverted date range (`since` after `until`) silently returns zero results instead of an error, `limit=0` returns one message, and an oversized `offset` produces a raw database timeout. I'll test identifier handling and the wiki next.
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

New findings: an empty `search_wiki` query returns ten ranked hits with `score: null`, and live wiki excerpts contain drafting-pipeline meta-text ("This draft is an addition to the existing page… deliberately titled to match…"), which is a likely leak of internal maintenance text into published page bodies. Next I'll test unbounded and malformed inputs across the fact, people and attachment tools.
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

Another error-handling finding: `list_wiki_pages` with an invalid `page_type` leaks a raw Postgres error ("unnamed portal parameter $1"), which is an implementation detail exposed to the caller. The `top_correspondents` inverted range also visibly reports `2026-06-01` to `2026-04-01` and still returns an empty success. Now I'll test the remaining parameter validation and check whether the meta-text leak is in the stored page body.
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

Two more findings: `search_raw` silently accepted `order="sideways"` and fell back to newest without an error, and `get_attachment_text` returned empty text at `offset=-5` (negative offset not validated). The `length=0` result may also be a parameter artifact, so I'll retest with defaults. Next I'll check citation integrity: whether facts actually match the messages they cite.
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

The large page dump confirmed several things: duplicated `links_in` entries, a self-link from the Georgia Metals page to itself, and repeated identical flags. I'll run a last round of consistency checks: thread counts across tools, key-matching behaviour, and an empty-range completeness signal.
```

```

```

```

```

```

```

```

**Summary:** I found 14 issues in the Vault MCP. Two are high severity: a fuzzy page filter attributes one entity's facts to another, and draft-pipeline text appears in live page bodies. The rest are medium or low: silent failures on bad input, misleading completeness flags, leaked database errors, and some citation and provenance problems. The connection is unauthenticated (`whoami` returns `signed_in: false`), so I passed `mailbox` explicitly and assumed no identity. All testing was read-only.

| # | Severity | Issue |
|---|---|---|
| F1 | High | `find_facts` with a page filter returns facts from a different entity |
| F2 | High | Draft-pipeline meta text is stored in live wiki bodies |
| F3 | Medium | Inverted date ranges return a silent empty success |
| F4 | Medium | Pre-archive date ranges report `complete: true` |
| F5 | Medium | Raw database errors leak to the caller |
| F6 | Medium | Price facts come back with no recency ordering, and some values are malformed |
| F7 | Medium | Wiki page link and flag lists contain self-links, duplicates and pipeline reasoning |
| F8 | Low–Med | A fact's provenance is labelled `sourced` but the cited message doesn't support it |
| F9 | Low | Invalid parameters are silently coerced instead of rejected |
| F10 | Low | `find_people` ties contradict the documented preference |
| F11 | Low | Empty `search_wiki` query returns ranked hits with `score: null` |
| F12 | Low | `find_facts` gives no total or truncation indicator |
| F13 | Low | Exact `fact_key` misses return zero with no near-key hint |
| F14 | Low | The skill's build snapshot is stale against live stats |

**F1 (High): Cross-entity attribution**
- Repro: `find_facts(page="Georgia Metals", key_words="credit limit")`
- Actual: 7 rows, one from page 217 "Georgia Metal Center" (`credit_limit_usd` 250000, msg 224288). The Georgia Metals page's own `links_out` says Georgia Metal Center is a separate entity with no shared address, domain or contact.
- Expected: no rows from another entity, or rows clearly labelled as belonging to it. The documented fuzzy match covers "near-duplicate pages of the same entity", which this is not.
- Next step: prefer an exact title match and never fuzzy-match onto a page that is a distinct entity. Show `page_title` prominently in every fact row.

**F2 (High): Pipeline text in live bodies**
- Repro: `get_wiki_page(page_id=1, body_chars=1200)`
- Actual: the body opens with "[Merged from a draft by outlook_3gm_travis_outlook] **Addition to the existing 'Georgia Metals' page (live_page_id 1).** Does not restate…". Search excerpts from pages 2, 5, 6, 7, 8 and 12 show the same kind of text ("This draft is an addition to… deliberately titled to match… so that consolidation merges it").
- Expected: entity content only. This body is the authority when facts are stale, so readers and answering models will take the drafting notes as account facts.
- Next step: strip merge boilerplate at promotion, and add a check that fails publication when it is present.

**F3 (Medium): Inverted ranges return silent success**
- Repro: `list_emails(since="2026-10-01", until="2026-09-01")` and `top_correspondents(since="2026-06", until="2026-04-01", mailbox="both")`
- Actual: `messages: []` / `top: []`, `complete: true`. The response even echoes the inverted range (`["2026-10-01 00:00 ET","2026-09-01 23:59 ET"]`).
- Expected: an error stating that `since` is after `until`. Silence here reads as "no mail", which is the failure mode the skill warns about.

**F4 (Medium): Pre-archive ranges report completeness**
- Repro: `list_emails(since="2025-08-01", until="2025-08-31")` and `search_raw(query="invoice", since="2025-08-01", until="2025-08-31")`
- Actual: zero results with `coverage.complete: true`. Nothing says the archive starts on 2025-09-01.
- Expected: `complete: false` or an explicit "outside archive coverage" note.

**F5 (Medium): Raw database errors**
- Repro: `list_wiki_pages(page_type="banana")` and `search_wiki(query="Georgia Metals", page_type="banana")`
- Actual: "invalid input value for enum wiki_page_type… CONTEXT: unnamed portal parameter $1/$7". Enum values go straight into SQL.
- Repro 2: `list_emails(offset=99999999, limit=3)` returns "canceling statement due to statement timeout" with no structured error.
- Expected: validated errors listing valid values, which `search_raw` already does for `recipient_role` and `mailbox`. An out-of-range offset should return an empty page, not a timeout.

**F6 (Medium): Price facts without recency**
- Repro: `find_facts(page="Ace Metal Sales", key_words="price black 117l per lft")`
- Actual: two rows for the same key. One is `2.20 (quantity_raw: "2")` with no `as_of`. The other is `2.33`, `as_of` 2026-06-10. Neither is marked current, and the value string has parser residue. Some `as_of` fields also hold free text (`"2026-04-02, Limit Endorsement No. 00001622"`, `"2026-03-31, status: pending"`).
- Expected: sorted by date, with the undated row flagged. Values clean. `as_of` a date or null.

**F7 (Medium): Wiki page structure**
- Repro: `get_wiki_page(page_id=1, facts_limit=5)`
- Actual: `links_in` lists page 1 as a linker of itself four times. `links_out` has four self-links to page 1 and six entries for page 257. The `flags` array has several verbatim duplicates (for example, the "extensive existing coverage" flag appears at least twice). Flags also contain drafting reasoning ("staging 5855", "flag 6954", "§1.7b").
- Expected: no self-links, one entry per link, deduplicated flags written for a reader.

**F8 (Low–Med): Provenance label not supported by the cited source**
- Repro: `find_facts(page="Georgia Metals"` … or page 188 `stakeholder_notified`, cite msg 64093)
- Actual: "Corey McGlothlin (CEO/Owner, 3GM Steel and Mac Metal Sales)" is marked `sourced`. `get_source(outlook_message, 64093)` shows only a greeting "Corey," and no title.
- Expected: the title is `agent_judgement`, or the citation shows the recipient record that supports it.

**F9 (Low): Silent coercion**
- `search_raw(order="sideways")` runs as newest-first with no error.
- `list_emails(limit=0)` returns one message.
- `get_attachment_text(attachment_id=49596, offset=-5)` and `length=0` return empty text with `has_more: true`.
- Expected: validation errors for each.

**F10 (Low): Ties contradict the documented preference**
- Repro: `find_people(name="Cory")`
- Actual: `used` = Cory Godsey, Cory Parsons, Cory Padgett, all `match_score` 1.0, `ambiguous: true`. The skill says "Cory" resolves to Cory Godsey and that exact spelling beats volume. I didn't confirm whether `list_emails` uses the same set.
- Next step: run `list_emails(sender="Cory")` and compare with `used`.

**F11 (Low): Empty query returns ranked hits**
- `search_wiki(query="")` returns 10 hits with `score: null` and no error. The ordering is undefined. Expected: a validation error, consistent with a minimum query length.

**F12 (Low): No completeness signal on `find_facts`**
- `find_facts()` with no filters returns 50 rows and no `total_matching` or `truncated`. The mail tools report both.

**F13 (Low): Exact-key miss gives no hint**
- `find_facts(page="Georgia Metals", fact_key="credit_limit")` returns zero. The same page has `credit_limit_usd`. The tool is documented as exact-match, so this is usability, not a defect.

**F14 (Low): Stale skill snapshot**
- The skill's build status reports 536 pages, 11,728 facts, 22,026 messages and 10,781 attachments. Live stats report 675, 32,584, 25,248 and 14,250. The skill flags its snapshot as stale, so this is drift rather than a bug, but the snapshot should be refreshed.

**Checks that passed**
- SQL-style input in `value_contains` returned empty with no error (parameterized queries).
- `2026-02-30` was rejected cleanly.
- Unknown mailbox, `recipient_role`, and `source_type` values returned clear errors.
- Nonexistent message IDs, attachment IDs and pages returned clean "no such" errors. Empty person name returned empty.
- Citations spot-checked against source: `lead_times_raw` (msg 63574), `bluescope_terms_raw` (63574), `status_raw` (64093) and `rep_commitment` (46323) are supported by their cited messages.
- `expand_thread(301479)` returns 4 messages, matching `find_thread` and `get_source`'s `thread_message_count`.
- Attachment 49596 returns its full 989 characters with default parameters.

**Not tested:** the signed-in `mailbox="mine"` path, ERP cross-checks, and write operations. The `get_wiki_page` output for page 1 was truncated at 100K characters, so flags after that point were not reviewed.

**Recommended next steps, in order:** fix F1 and F2 first, since both can put wrong facts in front of Travis and Stefan. Then fix date validation (F3, F4) and error handling (F5), then the wiki structure issues (F7, F8).

Sources: page 1 (Georgia Metals, body, flags, links), page 217 (Georgia Metal Center, fact credit_limit_usd, msg 224288), page 188 (.0160 Program, msgs 63574, 64093), page 337 (Ace Metal Sales, msgs 69023, 62300), page 595 (2026 Mid-Year Sales Review, msg 46323), msg 301479 and thread 301477–301481, att 49596 (msg 301401), list_wiki_pages and search_wiki (enum errors), find_people("Cory")

## User (2026-10-12 11:30:47 EDT)

Which customer complaints appear in the mail but have no entry on the customer’s wiki page?

## User (2026-10-12 11:30:47 EDT)

Which customer complaints appear in the mail but have no entry on the customer’s wiki page?

## Claude (2026-10-12 11:30:47 EDT)

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

## Claude (2026-10-12 11:30:47 EDT)

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
