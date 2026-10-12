---
conversation_id: 739c8b5d-2ec2-4646-be19-457c0b965c4d
platform: claude
username: "shubham"
title: "3GM Vault MCP testing"
created_at: "2026-10-09T21:14:35.054198Z"
updated_at: "2026-10-12 12:32:04 EDT"
---

# 3GM Vault MCP testing

## User (2026-10-12 12:32:04 EDT)

Test the search and retrieval capabilities of the 3GM Vault MCP using different search terms, partial names, exact matches, similar terms, and available filters. Check for relevant records that are missed, irrelevant records that are returned, inconsistent results for equivalent queries, and failures to retrieve information that is demonstrably available. Document reproducible examples and explain the likely cause of each issue.

## Claude (2026-10-12 12:32:04 EDT)

I'll start by loading the 3GM navigator skill, as your preferences require, and then load the vault tools.
```

```

```

```

The vault tools are loaded. I'll start with the vault's own scale figures and a baseline check of how the wiki and the raw mail agree.
```

```

```

```

```

```

The first pass already shows one thing to check: the vault stats (659 pages, 25,164 messages) are well past the snapshot figures in the skill (536 pages, 22,026 messages on 2026-09-30). That could be ordinary growth, but I'll keep it in view. Next I'll test a wiki figure against its cited source, and check whether the same storage report reads the same way across tools.
```

```

```

```

```

```

Three things need checking now. The Ace Metal Sales page holds two different values for the same price fact with no contradiction flag. The "Storage Tracking Report" subject search returns 45 threads in one call and 72 in another. And `find_thread` appears to merge exact-subject conversations that are more than 30 days apart, which its own description says it shouldn't. I'll pull the two cited sources and the 10/9 storage attachment.
```

```

```

```

```

```

The Ace Metal Sales discrepancy is confirmed, and it's a substantive one. The 2.20 figure is a March order. The 2.33 figure comes from a June email where Jessica is asking whether an order should be priced at the "monthly quoted price" of $2.33, so it is a reference price, not a sold price. Both sit under the same fact key with no flag, and the March fact has no date even though its source carries one. Next I'll check the storage report figures against the attachment itself and against the wiki.
```

```

```

```

```

```

The 10/9 storage figures in the email match the attached workbook (Reliable 422.04 MT and Swiss 146.07 MT, both ending 12/7). The wiki's storage fact is a different claim, so I'll check it against its own citation and against the storage template page.
```

```

```

```

The 362 MT storage figure matches its citation (the 9/1 email), so that one is accurate. The check on the storage template page returned no facts at all, which I'll note. Next I'll test whether counts agree across tools for the same subject, and look for the ERP so I can cross-check credit figures.
```

```

```

```

```

```

The subject search counts agree between `list_emails` and `find_thread` (81 messages), but they group the messages differently: 57 conversations versus 45 threads. More important is that `find_thread` merges five separate exact-subject conversations that span more than 30 days apart, which its own rule forbids. The ERP tools don't appear in this session. I'll make one more attempt to find them, and read how the Ace page's body describes the $2.33 figure.
```

```

```

```

The Ace page is internally coherent, and its own flags admit that several of its citations are unverified. The page's body and fact list cite four messages (63980, 63948, 63942, 63911) as the basis for its 2026-05 narrative, and a flag says a related draft's citations "fail to resolve to any real message." I'll check those four citations directly.
```

```

```

```

```

```

```

```

**Short answer:** Yes, the vault returned wrong or misleading results in two places. `find_thread` merges unrelated conversations against its own stated rule, and `find_facts` returns two different prices for one fact key with no flag. Most other checks were consistent.

## Discrepancies

**1. `find_thread` merges separate conversations (high severity)**
- **Input:** `find_thread(subject="Storage Tracking Report", limit=10)`
- **Observed:** One thread flagged `exact_subject: true`, `recurring_series: true`, 6 messages, 5 branches, spanning 2025-09-04 to 2026-05-12 ET. It combines five separate conversations. The gaps between them are about 22, 35, 105 and 88 days.
- **Expected:** The tool description says a thread has "no gap over 30 days", and its `answer_guide` says exact-subject threads are different conversations and must not be merged.
- **Cross-check:** `list_emails(subject=...)` and `search_raw` both list those same five as separate conversations, each marked `exact_subject: true`. `find_thread` reports `exact_subject_threads: 1`.
- **Counts for the same subject disagree:**
  - `list_emails`: 81 messages in 57 conversations.
  - `find_thread`: 81 messages in 45 threads.
  - `search_raw` (exact phrase, body and attachments): 140 messages in 72 conversations.
- **Impact:** The navigator skill sends "who started X" and "latest on the X thread" to `find_thread`. For this subject it names Kristen Candido as starter on 2025-09-04, which is only one of five unrelated conversations.

**2. Two prices under one fact key, no flag (medium severity)**
- **Input:** `find_facts(page="Ace Metal Sales", key_words="price black 117l per lft")`
- **Observed:**
  - `price_black_117l_per_lft_usd` = 2.20, from msg 69023, with `as_of: null`.
  - `price_black_117l_per_lft_usd` = 2.33, `as_of` 2026-06-10, from msg 62300.
- **Verified:**
  - Msg 69023 (2026-03-17) reads "2- black 117L @2.20". Correct.
  - Msg 62300 (2026-06-10) is Jessica Worley asking "Is this being sold at their monthly quoted price?" and listing "3-Black 117L - $2.33/lft". The value is correct, but it is a reference price in a question, not a price charged.
- **Expected:** Either separate keys for quoted and sold prices, or a label and an ambiguity flag. The page has no contradiction flag. The 2.20 fact also has no date, although its source is dated 2026-03-17.

## Checks that passed
- **Storage Tracking Report 10/9:** The email gives Reliable (Heartland) 422 MT and Swiss 146 MT, both ending 12/7. The attached workbook (att 49585) shows 422.04 and 146.07, ending 2026-12-07. Consistent.
- **Ace Metal Sales citations:** Messages 63980, 63948, 63942 and 63911 all resolve. Their content matches the page's 2026-05 narrative: 2.25 loads, Flack at $2.47 against list at $2.45, the last heavy black sold to Millers, and 5 heavy green in stock. A sibling draft (staging 2935) is flagged for unresolved citations. I could not see that draft, so I have not verified that claim.
- **Storage fact, page 328:** "362 MT at South Carolina Port, storage ended 8/10/2026" matches msg 46440 (sent 2026-09-01 ET).
- **Subject count stability:** `list_emails` returns 81 with and without a date window.

## Inconclusive or not testable
- **Storage template page (269):** `find_facts(page="Storage Tracking Report", key_words="remaining storage ends Swiss Reliable")` returned 0 rows, although `search_wiki` ranks the page first and the page reports 120 facts. I did not enumerate those facts, so I can't say whether the 10/9 figures are missing or stored under different keys. This needs reproducing.
- **ERP cross-check:** No ERP tools are loaded in this session, so I could not verify the EMB figures in the 9/1 email (balance $430,366.44 against a $500,000 limit) or any other live value.
- **Stale snapshot:** `get_vault_stats` now shows 659 pages, 31,230 facts, 25,164 messages and 14,215 attachments. The navigator skill's snapshot from 2026-09-30 says 536, 11,728, 22,026 and 10,781. Ten days of growth could explain this, but the message increase of about 3,100 is large. Treat the skill's counts as stale.

## Reproduction
1. `find_thread(subject="Storage Tracking Report", limit=10)`, then compare the 2025-09-04 and 2026-05-12 entries against `list_emails(subject="Storage Tracking Report", limit=3)`.
2. `find_facts(page="Ace Metal Sales", key_words="price black 117l per lft")`, then `get_source` on 69023 and 62300.
3. `get_source(outlook_message, 63980)` (and 63948, 63942, 63911) to confirm the Ace citations.
4. `find_facts(page="Storage Tracking Report", key_words="remaining storage ends Swiss Reliable")`, and compare with `get_wiki_page(page_id=269)`.

Sources: msg 301381 · att 49585 · att 49584 · msg 291897 · msg 267020 · msg 69023 · msg 62300 · msg 63980 · msg 63948 · msg 63942 · msg 63911 · msg 46440 · page 337 (Ace Metal Sales) · page 269 (Storage Tracking Report) · page 328 (Steel Buildings and Structures) · tools: find_thread, list_emails, search_raw, find_facts, get_source, get_vault_stats (no ERP records checked)
