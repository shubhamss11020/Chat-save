---
conversation_id: 1c2be0c5-96f0-4c0a-a928-2e9cd30d4e77
platform: claude
username: "shubham"
title: "3GM Vault MCP reliability assessment"
created_at: "2026-10-12T14:59:34.316Z"
updated_at: "2026-10-12 11:23:54 EDT"
---

# 3GM Vault MCP reliability assessment

## User (2026-10-12 11:23:54 EDT)

Assess the observable reliability of the 3GM Vault MCP. Look for repeated timeouts, failed requests, inconsistent response times, intermittent retrieval failures, incomplete responses, and errors that occur when querying larger result sets. Use available logs and existing performance metrics where accessible. Do not claim a performance problem without measurements or supporting evidence, and do not run load tests against production without authorization.

## User (2026-10-12 11:23:54 EDT)

Assess the observable reliability of the 3GM Vault MCP. Look for repeated timeouts, failed requests, inconsistent response times, intermittent retrieval failures, incomplete responses, and errors that occur when querying larger result sets. Use available logs and existing performance metrics where accessible. Do not claim a performance problem without measurements or supporting evidence, and do not run load tests against production without authorization.

## Claude (2026-10-12 11:23:54 EDT)

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

## Claude (2026-10-12 11:23:54 EDT)

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
