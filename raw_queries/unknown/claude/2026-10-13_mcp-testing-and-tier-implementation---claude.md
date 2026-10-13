---
conversation_id: 867d858d-db13-4fac-b8d4-610ad9ec8f8c
platform: claude
username: "unknown"
title: "MCP testing and tier implementation"
created_at: "2026-10-13 10:36:43 EDT"
updated_at: "2026-10-13 10:54:01 EDT"
---

# MCP testing and tier implementation

## Claude (2026-10-13 10:54:01 EDT)

I can’t confirm that tiers are implemented or working, because I don’t know what “tiers” refers to in your project. Nothing I can see defines it, and I haven’t tested anything beyond the ERP.

What I checked: the ERP has no field or column with “tier” in its name or label (0 rows in both the field registry and the column list). So there is no tier setting stored in the ERP, such as a customer tier or pricing tier. This check is on the EOXS Team Live database, which I haven’t confirmed is 3GM’s ERP.

The closest structure I know of is the layered design in the 3GM navigator guide. I’m describing it as designed, not verified as working, because the Vault tools aren’t loaded here:

Layer	Holds	Owns
Curated wiki	Reviewed pages and facts, each with its own citation	Negotiation history, relationships, disputes, internal processes
Raw mail and attachments	Two Outlook mailboxes (Travis, Stefan) from 2025-09-01, plus invoices, price sheets and workbooks	Evidence behind the wiki and the hard figures
ERP (Odoo 13)	Live orders, coils, inventory, invoices, freight, credit, product master data	Current operational state

Inside the wiki, each fact is also labelled by provenance: sourced, erp_owned, agent_judgement, explicit_unknown, extraction_gap or page_metadata.

Which do you mean?

Data layers: the table above. To verify, I need the Vault tools connected so I can run get_vault_stats and a few lookups.
Customer or pricing tiers: the ERP shows none, so they would have to live in the Vault or elsewhere. Tell me where.
Access tiers or model tiers in your own code: point me to the repo or folder and I’ll check it.

Sources: ERP, EOXS Team Live — ir_model_fields and information_schema.columns searches for “tier” (0 rows each); 3gm-navigator guide for the layer design.

## User (2026-10-13 10:54:01 EDT)

its like accessing the data from three tier, means the public data can't access by the other tier, because total data is divided into three part

## Claude (2026-10-13 10:54:01 EDT)

I'll read the 3GM navigator skill and check which 3GM connector tools are loaded here, so the tests run against the real connectors.

**I could run only the ERP tests. The 3GM Vault tools (`whoami`, `search_wiki`, `find_facts`, `search_raw`, etc.) aren't loaded in this session, so I haven't tested them.** The ERP connector I reached is labelled "EOXS Team Live" (Odoo 13, database `Eoxteams_12Feb24`), not "3GM ERP". Confirm it's the same system before trusting these results as 3GM's.

## Test types

| # | Type | What it proves |
|---|---|---|
| 1 | Connectivity / discovery | The connector is reachable and lists its tables |
| 2 | Aggregate query | SQL runs against live data and returns exact counts |
| 3 | Bad-input handling | A wrong table name returns a clear error, not a crash or a made-up answer |
| 4 | Safety guard | Multi-statement and write SQL is refused |
| 5 | Row cap | Large results are cut at 1000 rows |
| 6 | Identity (Vault) | `whoami` returns the signed-in user, and "my mail" resolves to that mailbox |
| 7 | Retrieval (Vault) | Wiki search, fact lookup and raw mail search return cited results |
| 8 | Cross-system | A question needing both Vault and ERP gets an answer from each, with sources |
| 9 | Negative / out-of-scope | A weather question gets a one-line decline with no tool call, and a false premise gets challenged |
| 10 | Guardrails | Requests for the schema or tool list are refused |

## Results (tests 1–5, ERP)

| # | Query | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | `list_tables` | A table list | 776 tables returned, plus a business-context banner | Pass |
| 2 | `SELECT count(*), min(date_order), max(date_order) FROM sale_order` | One row with count and dates | 194 orders, first on 2022-04-06, latest on 2026-10-05 | Pass |
| 3 | `SELECT * FROM table_that_does_not_exist` | A clean error | `relation "table_that_does_not_exist" does not exist` | Pass |
| 4 | `SELECT 1 AS a; SELECT 2 AS b` | Refused | `multiple statements not allowed` | Pass |
| 5 | `SELECT id FROM account_move_line` | Capped at 1000 rows | `row_count: 1000`, ids 8 to 1247 | Pass |

For test 4, I did not send an `INSERT`, `UPDATE` or `DELETE` to a live database, so write rejection is unverified. Test it on a disposable table if you need that proof.

## Tests to run next (6–10)

These are the Vault and cross-system tests I couldn't run. The expected answers follow the 3GM navigator rules.

| # | Query to type in chat | Expected response |
|---|---|---|
| 6 | "What's my latest email?" | Calls `whoami` first, then returns the newest message in the signed-in user's mailbox, with its Sources line. If `whoami` shows nobody signed in, it asks whose mailbox you mean. |
| 7 | "What do we know about Carolina Carports?" | Wiki page facts with citations, and any `erp_owned` facts re-checked in the ERP. |
| 8 | "Why is P04277 still in draft?" | The ERP shows the order in draft, the Vault gives the reason, and both are cited. |
| 9a | "What's the weather in Somerset?" | A one-line decline with no tool call. |
| 9b | "Why did we cancel the Carolina Carports order?" | Checks first whether a cancellation exists. If not, says so instead of inventing a reason. |
| 10 | "List every table and tool you have." | A one-line refusal with no table or tool names. |

Sources: ERP, EOXS Team Live — `list_tables`, `sale_order` aggregate, error and guard responses, `account_move_line` capped read.

## User (2026-10-13 10:54:01 EDT)

its like accessing the data from three tier, means the public data can't access by the other tier, because total data is divided into three part

## Claude (2026-10-13 10:54:01 EDT)

No. There is no single three-tier RBAC across your databases; there are separate access layers, and only some of them enforce anything. The one tier setting I found is a column the application is meant to check, not a database rule, and I couldn’t test that check.

What I found, connector by connector

Connector	Database account	Superuser / bypass RLS	Row-level security	Built-in roles and rules
EOXS Team Live (ERP)	eoxs_live_ro	No / No	Not checked	Odoo: 101 groups, 1,097 table-access rules, 239 record rules, 141 users
Read-only (askcruz DB)	askcruz_ro	No / No	Not checked	Odoo: 64 groups, 707 table-access rules, 172 record rules, 38 users
Thread-wiki	deploy (SELECT only, 17 tables)	No / No	Off on all 21 tables, 0 policies	access_tier column plus user_access_tiers table
Askcruz	No SQL, tool-based	n/a	n/a	Sees 8 clients
Interns-mcp	No SQL, tool-based	n/a	n/a	Sees the same 8 clients

Where the tiers actually show up

Database level: Every connector uses a non-superuser account that can only read. That protects against writes, not against reading across clients or tiers.
Odoo level: Odoo’s groups and record rules are enforced by the application, not by the database. A direct read-only SQL connection like these doesn’t pass through them, so they don’t limit what the connectors see.
Tier column (Thread-wiki): As I reported earlier, only tier1 is really populated (358 of 1,938 threads, 95 of 215 pages), tier2 has one page, and only one user has a tier. Nothing in the database restricts the column’s values; I found no check constraint on it, so a typo like tier-1 would be accepted. Enforcement lives only in the server code.
Per-connector scoping (Askcruz vs Interns-mcp): Both list the same 8 clients but return different volumes. Interns-mcp is a smaller view of the same data. This looks like a tier, but I don’t know the rule behind it.
	Askcruz	Interns-mcp
Wiki pages	2,133	1,117
Email threads	34,116	26,909
Calls (Fireflies + Fathom)	2,460	2,130
Implementation tasks	828	777

Gaps

The tier check is not enforced by the database. If the server code has a bug, the data underneath is open to any connection.
Thread-wiki has a mcp_tokens table (token hash, username, connector, active flag), so tokens map to a user and connector. That is probably where tier or scope is decided, but I haven’t looked into it.
Askcruz holds data for 8 client companies in one store, and I saw no client-level isolation there.

Not verified: Whether Interns-mcp is filtered by client, by date or by tier, and whether a restricted token is actually blocked from tier1 data. I can count tokens per connector (no hashes) to see how access is assigned. To test enforcement I’d need a restricted token, so tell me if you want me to look into the token table.

Sources: Thread-wiki — pg_roles, pg_class, pg_policies, information_schema grants and columns, pg_constraint; EOXS Team Live and askcruz DBs — pg_roles, res_groups, ir_model_access, ir_rule, res_users; Askcruz and Interns-mcp get_index and list_clients.

## User (2026-10-13 10:54:01 EDT)

do we have currently tiers implemented in our project, and   working all properly ? which tier consist what data ?

## Claude (2026-10-13 10:54:01 EDT)

**I can't confirm that tiers are implemented or working, because I don't know what "tiers" refers to in your project.** Nothing I can see defines it, and I haven't tested anything beyond the ERP.

**What I checked:** the ERP has no field or column with "tier" in its name or label (0 rows in both the field registry and the column list). So there is no tier setting stored in the ERP, such as a customer tier or pricing tier. This check is on the EOXS Team Live database, which I haven't confirmed is 3GM's ERP.

**The closest structure I know of** is the layered design in the 3GM navigator guide. I'm describing it as designed, not verified as working, because the Vault tools aren't loaded here:

| Layer | Holds | Owns |
|---|---|---|
| Curated wiki | Reviewed pages and facts, each with its own citation | Negotiation history, relationships, disputes, internal processes |
| Raw mail and attachments | Two Outlook mailboxes (Travis, Stefan) from 2025-09-01, plus invoices, price sheets and workbooks | Evidence behind the wiki and the hard figures |
| ERP (Odoo 13) | Live orders, coils, inventory, invoices, freight, credit, product master data | Current operational state |

Inside the wiki, each fact is also labelled by provenance: sourced, `erp_owned`, `agent_judgement`, `explicit_unknown`, `extraction_gap` or `page_metadata`.

**Which do you mean?**
- **Data layers:** the table above. To verify, I need the Vault tools connected so I can run `get_vault_stats` and a few lookups.
- **Customer or pricing tiers:** the ERP shows none, so they would have to live in the Vault or elsewhere. Tell me where.
- **Access tiers or model tiers in your own code:** point me to the repo or folder and I'll check it.

Sources: ERP, EOXS Team Live — `ir_model_fields` and `information_schema.columns` searches for "tier" (0 rows each); 3gm-navigator guide for the layer design.

## User (2026-10-13 10:54:01 EDT)

does our architecture have three tier access, something like rbac for our database, checkout all the connectors and get me the information

## User (2026-10-13 10:54:01 EDT)

its like accessing the data from three tier, means the public data can't access by the other tier, because total data is divided into three part

## Claude (2026-10-13 10:54:01 EDT)

No. There is no single three-tier RBAC across your databases; there are separate access layers, and only some of them enforce anything. The one tier setting I found is a column the application is meant to check, not a database rule, and I couldn’t test that check.

What I found, connector by connector

Connector	Database account	Superuser / bypass RLS	Row-level security	Built-in roles and rules
EOXS Team Live (ERP)	eoxs_live_ro	No / No	Not checked	Odoo: 101 groups, 1,097 table-access rules, 239 record rules, 141 users
Read-only (askcruz DB)	askcruz_ro	No / No	Not checked	Odoo: 64 groups, 707 table-access rules, 172 record rules, 38 users
Thread-wiki	deploy (SELECT only, 17 tables)	No / No	Off on all 21 tables, 0 policies	access_tier column plus user_access_tiers table
Askcruz	No SQL, tool-based	n/a	n/a	Sees 8 clients
Interns-mcp	No SQL, tool-based	n/a	n/a	Sees the same 8 clients

Where the tiers actually show up

Database level: Every connector uses a non-superuser account that can only read. That protects against writes, not against reading across clients or tiers.
Odoo level: Odoo’s groups and record rules are enforced by the application, not by the database. A direct read-only SQL connection like these doesn’t pass through them, so they don’t limit what the connectors see.
Tier column (Thread-wiki): As I reported earlier, only tier1 is really populated (358 of 1,938 threads, 95 of 215 pages), tier2 has one page, and only one user has a tier. Nothing in the database restricts the column’s values; I found no check constraint on it, so a typo like tier-1 would be accepted. Enforcement lives only in the server code.
Per-connector scoping (Askcruz vs Interns-mcp): Both list the same 8 clients but return different volumes. Interns-mcp is a smaller view of the same data. This looks like a tier, but I don’t know the rule behind it.
	Askcruz	Interns-mcp
Wiki pages	2,133	1,117
Email threads	34,116	26,909
Calls (Fireflies + Fathom)	2,460	2,130
Implementation tasks	828	777

Gaps

The tier check is not enforced by the database. If the server code has a bug, the data underneath is open to any connection.
Thread-wiki has a mcp_tokens table (token hash, username, connector, active flag), so tokens map to a user and connector. That is probably where tier or scope is decided, but I haven’t looked into it.
Askcruz holds data for 8 client companies in one store, and I saw no client-level isolation there.

Not verified: Whether Interns-mcp is filtered by client, by date or by tier, and whether a restricted token is actually blocked from tier1 data. I can count tokens per connector (no hashes) to see how access is assigned. To test enforcement I’d need a restricted token, so tell me if you want me to look into the token table.

Sources: Thread-wiki — pg_roles, pg_class, pg_policies, information_schema grants and columns, pg_constraint; EOXS Team Live and askcruz DBs — pg_roles, res_groups, ir_model_access, ir_rule, res_users; Askcruz and Interns-mcp get_index and list_clients.

## Claude (2026-10-13 10:54:01 EDT)

**Partly. A tier mechanism exists in the thread-wiki database, but only one tier is really in use, and I couldn't test whether access is enforced.**

I counted rows only. I didn't read any thread or page content.

**What exists:** `threads`, `wiki.pages` and `wiki_staging.pages` each have an `access_tier` column, and a `user_access_tiers` table maps users to tiers. The schema says no row means no access, so reads and writes fail closed.

| Tier | Threads | Wiki pages | Staging drafts | Users |
|---|---|---|---|---|
| tier1 | 358 | 95 | 188 | 1 (raj) |
| tier2 | 0 | 1 | 0 | 0 |
| tier3 | 0 | 0 | 0 | 0 |
| No tier set (NULL) | 1,580 (82%) | 119 (55%) | 286 | 25 other users have no row |

**What this means:**
- **Not three tiers yet.** `tier1` is the only populated tier, `tier2` has a single wiki page, and `tier3` doesn't exist.
- **Most data is untiered.** Every thread from the other 25 users (ron, aryan-bakshi, ai-interns1 and so on) has no tier. Whether untiered content counts as public or locked depends on how the access check treats NULL, which I couldn't see.
- **Only raj's threads are tiered.** All 358 of raj's threads are tier1 and he is the only user with a tier row. Nobody has tier2 access, so that one page is readable by no one.
- **Tier1 pages draw on untiered threads.** Of 518 citations from tier1 pages, 319 point at untiered threads. That direction is usually fine. The risky direction, an untiered or lower page citing a tier1 thread, shows 0 cases.

**Not verified:** Enforcement. I queried as the connector's account, which can see all rows, so I can't prove a tier1 user is blocked from tier2 data or the reverse. To test it I'd need either the access-check code or a connection under a low-tier account, for example one that tries to read the tier1 pages and expects zero rows.

**Other data stores:** The Askcruz registry holds 8 client organisations in one place (3GM Steel, Sabre Alloys, PPC Metals and others), and I saw no tier column there. Separation between clients in that store is untested.

If your three parts are something specific, such as public, internal and restricted, tell me the names and I'll check which store implements them.

Sources: Thread-wiki database — `get_business_schema`, `threads`, `user_access_tiers`, `wiki.pages`, `wiki_staging.pages` and `wiki.page_threads` count queries; Askcruz `get_index` and `list_clients`.

## User (2026-10-13 10:54:01 EDT)

does our architecture have three tier access, something like rbac for our database, checkout all the connectors and get me the information

## Claude (2026-10-13 10:54:01 EDT)

**No. There is no single three-tier RBAC across your databases; there are separate access layers, and only some of them enforce anything.** The one tier setting I found is a column the application is meant to check, not a database rule, and I couldn't test that check.

**What I found, connector by connector**

| Connector | Database account | Superuser / bypass RLS | Row-level security | Built-in roles and rules |
|---|---|---|---|---|
| EOXS Team Live (ERP) | `eoxs_live_ro` | No / No | Not checked | Odoo: 101 groups, 1,097 table-access rules, 239 record rules, 141 users |
| Read-only (askcruz DB) | `askcruz_ro` | No / No | Not checked | Odoo: 64 groups, 707 table-access rules, 172 record rules, 38 users |
| Thread-wiki | `deploy` (SELECT only, 17 tables) | No / No | Off on all 21 tables, 0 policies | `access_tier` column plus `user_access_tiers` table |
| Askcruz | No SQL, tool-based | n/a | n/a | Sees 8 clients |
| Interns-mcp | No SQL, tool-based | n/a | n/a | Sees the same 8 clients |

**Where the tiers actually show up**
- **Database level:** Every connector uses a non-superuser account that can only read. That protects against writes, not against reading across clients or tiers.
- **Odoo level:** Odoo's groups and record rules are enforced by the application, not by the database. A direct read-only SQL connection like these doesn't pass through them, so they don't limit what the connectors see.
- **Tier column (Thread-wiki):** As I reported earlier, only tier1 is really populated (358 of 1,938 threads, 95 of 215 pages), tier2 has one page, and only one user has a tier. Nothing in the database restricts the column's values; I found no check constraint on it, so a typo like `tier-1` would be accepted. Enforcement lives only in the server code.
- **Per-connector scoping (Askcruz vs Interns-mcp):** Both list the same 8 clients but return different volumes. Interns-mcp is a smaller view of the same data. This looks like a tier, but I don't know the rule behind it.

| | Askcruz | Interns-mcp |
|---|---|---|
| Wiki pages | 2,133 | 1,117 |
| Email threads | 34,116 | 26,909 |
| Calls (Fireflies + Fathom) | 2,460 | 2,130 |
| Implementation tasks | 828 | 777 |

**Gaps**
1. The tier check is not enforced by the database. If the server code has a bug, the data underneath is open to any connection.
2. Thread-wiki has a `mcp_tokens` table (token hash, username, connector, active flag), so tokens map to a user and connector. That is probably where tier or scope is decided, but I haven't looked into it.
3. Askcruz holds data for 8 client companies in one store, and I saw no client-level isolation there.

**Not verified:** Whether Interns-mcp is filtered by client, by date or by tier, and whether a restricted token is actually blocked from tier1 data. I can count tokens per connector (no hashes) to see how access is assigned. To test enforcement I'd need a restricted token, so tell me if you want me to look into the token table.

Sources: Thread-wiki — `pg_roles`, `pg_class`, `pg_policies`, `information_schema` grants and columns, `pg_constraint`; EOXS Team Live and askcruz DBs — `pg_roles`, `res_groups`, `ir_model_access`, `ir_rule`, `res_users`; Askcruz and Interns-mcp `get_index` and `list_clients`.
