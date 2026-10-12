---
conversation_id: 52dcca4b-a943-49be-bf4d-4b72f8f81e22
platform: claude
username: "shubham"
title: "Mac Metal sales invoice"
created_at: "2026-10-12T14:59:34.316Z"
updated_at: "2026-10-12 11:42:32 EDT"
---

# Mac Metal sales invoice

## User (2026-10-12 11:42:32 EDT)

Assess the observable reliability of the 3GM Vault MCP. Look for repeated timeouts, failed requests, inconsistent response times, intermittent retrieval failures, incomplete responses, and errors that occur when querying larger result sets. Use available logs and existing performance metrics where accessible. Do not claim a performance problem without measurements or supporting evidence, and do not run load tests against production without authorization.

## Claude (2026-10-12 11:42:32 EDT)

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

**There is no single "Mac Metal sales invoice" in the vault.** The matches are mostly freight and demurrage invoices from MID-SHIP Logistics billed to Mac Metal Sales. I read two of them in full. I could not check any of them against the ERP, because no ERP tool was available in this session.

**The two invoices I read in full (both billed to Mac Metal Sales, 1650 West Highway 80, Somerset, KY; Net 30; from MID-SHIP Logistics, Port Washington, NY):**

- **Invoice 62279773, dated 24 Sep 2026, total $15,600.00.** Project 52321, "Royal Orion / Mac Metal Sales / July '26". Five barge demurrage charges at $400/day, from 6 to 11 billable days each. Jessica Worley forwarded it to Stefan Brown at 14:56 ET on 24 Sep, and Stefan replied at 15:15 ET (msg 262385). Source: att 46001, msg 262337.
- **Invoice 62269694, dated 14 Sep 2026, total $5,200.00.** Project 52601, "Q3 2026 General Contract Barge Demurrage". One barge (AEP-7179B, MV Star Tokyo), 13 days at $400/day. Jessica forwarded it at 11:04 ET; Stefan and Jessica discussed it at 11:07 and 11:12 ET. Source: att 45698, msg 223888.

**Other invoices in the same pattern (subject lines only; I did not open them):**
- 62253988 (25–26 Aug), 62243604 (21 Aug; Jessica says it covers 7 barges on one vessel), 62240359 (12 Aug), 62231490 (11 Aug), 62189947 (28 Jul), 62219341 (21 Jul), 62201733 (30 Jun), 62183376 (9–10 Jun), 62137865 (20 Apr), 62101040 (3 Apr).
- Sales Inv# 94638315, "MAC METAL (3GM / PHILLIPS) / PO# P04090-P04091 / MV. TOMONI FELICITY 145.540MT / TAMPA" (7 Jul 2026). This one is a 3GM sales invoice naming Mac Metal, so it may be the closest match to what you meant. I did not open it.

**Context from the vault:**
- Jessica Worley's 25 Aug note says the demurrage invoices "probably cancel out" the barge discounts she tracks in a spreadsheet (msg 47039).
- On 23 Sep, Jessica wrote that for Mac Metal KY 3GM invoices only the cost of the coils and then adds freight to the invoice (att 45986, msg 258649).
- A sales order, S12241, transferred six coils (60,000 lbs) from 3GM's Somerset warehouse to Mac Metal on 18 Aug at $1.90/lft (msg 47654). This is an order, not an invoice.
- Mac Metal's Sep 2026 AR aging and the 6 Jul 2026 report both carry an intercompany receivable from 3GM of $9,907,850.00 (att 12469). This is a balance, not an invoice.

**Not available:**
- **ERP:** I could not query it. Invoice status, payment, and the current balance are ERP-owned, so none of the above is confirmed as posted or paid.
- **Mailbox coverage:** the vault covers only Travis's and Stefan's mailboxes.

**Sources searched:**
- Vault wiki: search "Mac Metal sales invoice" (10 hits). Read "Mac Metal Sales, Inc." (page 307), first 40,000 of 118,886 characters and its first facts. The rest of the page was not read.
- Vault raw mail: "Mac Metal invoice" across both mailboxes. 422 messages in 128 conversations, plus 390 attachments. I read the first 50 messages and 100 conversations, so this is not complete.
- Vault attachments: filename search "mac" (587 matches, first 50 read). Full text read for att 46001 and att 45698.
- Vault raw mail, sender "MID-SHIP" (sender matches only; no messages read).
- ERP: not reachable in this session.

Sources: msg 262337 · msg 262385 · msg 223888 · msg 223896 · msg 223905 · msg 47039 · msg 47654 · msg 258649 · att 46001 · att 45698 · att 45986 · att 12469 · wiki page 307 · sales order S12241 (not read in ERP) · Sales Inv# 94638315 (not opened)

Do you want me to open the 94638315 sales invoice, or pull the rest of the Mac Metal Sales wiki page?

## Claude (2026-10-12 11:31:04 EDT)

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

**Conclusion:** This sample shows no timeouts, failed requests, or incomplete retrievals from the Vault MCP. The one reliability issue I observed is oversized responses. I can't assess latency or error rates, because I have no access to server logs or timing metrics.

**What I ran:** Five read-only calls: `get_vault_stats`, a `search_wiki` lookup, a `list_emails` call (25 results), a `search_raw` call (100 results), and a `find_facts` call (500 results). All returned successfully on the first attempt. I didn't record response times, so I can't say whether any were slow. I didn't run any load tests.

**Observations:**
- **Oversized payloads:** The `search_raw` call (limit 100) and the `find_facts` call (limit 500) both exceeded the 25,000-token display limit. The server returned about 136,000 and 199,000 characters, and the tail of each response was cut off on my side. The server doesn't appear to cap or paginate large `find_facts` results by default. Results from those two calls are incomplete for me, though the server itself did not error.
- **Incomplete-looking excerpts:** Some `list_emails` excerpts from newsletters contain raw HTML and CSS rather than readable text. This affects display quality, not retrieval.
- **Pagination worked as designed:** `list_emails` reported `total_matching: 16230` with `truncated: true`, so the server signalled incomplete results correctly.
- **Stale snapshot in the skill:** `get_vault_stats` now reports 675 pages, 32,584 facts, 25,250 messages, and 14,250 attachments. The skill's snapshot from 2026-09-30 lists 536, 11,728, 22,026, and 10,781. This reflects normal growth, not a fault.

**What would settle it:** Server-side logs or metrics for p50/p95 latency, error rates, and timeouts over the past few weeks, plus any record of result-size limits. The skill's maintainer note cites a `search_raw` timing of 258s before an index and 1.55s after it. That's a documented measurement, but I haven't verified it against current performance.

**Suggested next steps:** Check the server's latency and error logs for the past month. If you confirm that large `find_facts` or `search_raw` calls are common, consider a default `limit` cap or a `find_facts` pagination option.

Sources: `get_vault_stats`; `search_wiki` "credit limit" (limit 3); `list_emails` mailbox travis (limit 25); `search_raw` "invoice" (limit 100, human_only); `find_facts` value_contains "USD" (limit 500); skill snapshot dated 2026-09-30.

## Claude (2026-10-12 11:31:04 EDT)

Conclusion: This sample shows no timeouts, failed requests, or incomplete retrievals from the Vault MCP. The one reliability issue I observed is oversized responses. I can’t assess latency or error rates, because I have no access to server logs or timing metrics.

What I ran: Five read-only calls: get_vault_stats, a search_wiki lookup, a list_emails call (25 results), a search_raw call (100 results), and a find_facts call (500 results). All returned successfully on the first attempt. I didn’t record response times, so I can’t say whether any were slow. I didn’t run any load tests.

Observations:

Oversized payloads: The search_raw call (limit 100) and the find_facts call (limit 500) both exceeded the 25,000-token display limit. The server returned about 136,000 and 199,000 characters, and the tail of each response was cut off on my side. The server doesn’t appear to cap or paginate large find_facts results by default. Results from those two calls are incomplete for me, though the server itself did not error.
Incomplete-looking excerpts: Some list_emails excerpts from newsletters contain raw HTML and CSS rather than readable text. This affects display quality, not retrieval.
Pagination worked as designed: list_emails reported total_matching: 16230 with truncated: true, so the server signalled incomplete results correctly.
Stale snapshot in the skill: get_vault_stats now reports 675 pages, 32,584 facts, 25,250 messages, and 14,250 attachments. The skill’s snapshot from 2026-09-30 lists 536, 11,728, 22,026, and 10,781. This reflects normal growth, not a fault.

What would settle it: Server-side logs or metrics for p50/p95 latency, error rates, and timeouts over the past few weeks, plus any record of result-size limits. The skill’s maintainer note cites a search_raw timing of 258s before an index and 1.55s after it. That’s a documented measurement, but I haven’t verified it against current performance.

Suggested next steps: Check the server’s latency and error logs for the past month. If you confirm that large find_facts or search_raw calls are common, consider a default limit cap or a find_facts pagination option.

Sources: get_vault_stats; search_wiki “credit limit” (limit 3); list_emails mailbox travis (limit 25); search_raw “invoice” (limit 100, human_only); find_facts value_contains “USD” (limit 500); skill snapshot dated 2026-09-30.
