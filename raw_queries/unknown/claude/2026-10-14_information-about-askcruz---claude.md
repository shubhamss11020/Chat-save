---
conversation_id: 5cc933b2-b2dd-424b-b286-3f9fd9a5ae21
platform: claude
username: "unknown"
title: "Information about askcruz - Claude"
created_at: "2026-10-14 09:05:43 EDT"
updated_at: "2026-10-14 09:12:08 EDT"
---

# Information about askcruz - Claude

## User (2026-10-14 09:12:08 EDT)

give me all the information you know about askcruz

## Claude (2026-10-14 09:12:08 EDT)

Here’s what I found in the AskCruz wiki. Two caveats first. There’s no separate askcruz skill file in this session, so I only read the thread-wiki skill. And the transcript-saving tool (save_chat_transcript) isn’t connected here, so this conversation won’t be archived.

What it is

AskCruz (product family name Cruz) is EOXS’s AI-powered company knowledge base and conversational assistant, a “second brain.” Its one-line definition: an AI agent that connects a company’s scattered business data, structures it into usable knowledge, and lets employees reach it through a single conversational interface. The core problem it targets is that employees know information exists across email, spreadsheets, operational systems, project tools and call records, but struggle to find it.

Capabilities

The feature file describes four named capabilities:

Company Brain: the company’s shared working knowledge, such as who does what, how quotes are priced, and customer history.
Company Hands: practical help like drafting quotes, flagging at-risk orders, and summarizing calls. It is explicitly not autonomous decision-making.
Digital Workforce: standing responsibilities that watch and report on business conditions, such as an order queue.
Company Personalization: reflects one company’s own vocabulary, pricing logic and tolerances.

Typical users are sales, operations, customer-facing teams, leadership and new hires. Domain terms include “free to sell” (material available after commitments) and “true margin” (after freight and processing).

Architecture

The pipeline has ten stages: source systems, ingestion, filtering, sensitivity classification, central knowledge store, knowledge generation, citation check, human approval, retrieval, response.

Sources: three Gmail accounts, one shared Zoho support inbox, Fireflies and Fathom call data, and Odoo implementation boards for six clients (Greer Steel, Eastern States Steel, Discount Pipe & Steel, PPC Metals, 3GM Steel, Sabre Alloys).
Not native: support tickets and invoices/sales orders are not part of Cruz’s collection. They live in the separate eoxs-teams Odoo connection.
Freshness: synthesis runs every six hours, so it is not real-time. The product file cites 94% data completeness, but that is a status metric, not a per-answer guarantee.
Access control: there are General, Company-Confidential and Raj-Personal sensitivity labels, and tier1/tier2/tier2_confidential access terms. Database-level controls are backed by an independent AI response-level check. Interns and general staff get financial amounts stripped.
Security rules: it must never infer access from how a question is worded, accept an admin claim at face value, expose credentials, or follow instructions embedded in retrieved documents.
Market position
ICP: defined by data fragmentation rather than industry. The primary buyer is the CEO.
Competitive framing: pitched against generic AI and traditional search, not as “another chatbot.”
Traction: 3GM Steel is the first confirmed customer, at a reduced two-user scope after a proposal call in Aug 2026. A kickoff invoice followed in Sept.
Pipeline: the Sabre Alloys proposal and services agreement is still being negotiated as of Oct 2026. Other wiki pages mention Three D Metals and Lumberman’s Wholesale Supply as prospects.
Product-market fit: the internal guide says there is no proof yet of broad, repeatable fit. Retention, ROI, usage, pricing acceptance and CAC are listed as not yet established.
Roadmap: today it handles Q&A over organizational knowledge. Next are workflows, business-system integration and connected AI agents.
Internal operations

There is an AskCruz project board in the teams-askcruz Odoo instance, with daily and weekly scrum reports. The wiki also covers an August 2026 intern mailbox rollout, a marketing push into verticals such as car dealerships plus LinkedIn outreach, and a new SDR who started Aug 27.

Inconsistencies in the sources
Positioning: the feature file calls AskCruz “a company-specific AI product for steel businesses.” The product-market fit guide and the client-facing catalog say it is industry-agnostic. The wiki flags this as unresolved, so confirm the current positioning before using it externally.
Technical ownership: the wiki flags the ownership details as unverified and possibly stale.
Restricted content: some pricing and deal details are marked [restricted], so I left them out.

I can go deeper on any of these, such as the 3GM or Sabre deals, the board status, or the raw reference documents.

## User (2026-10-14 09:12:08 EDT)

what are the current difficulties which is being faced in the implementation of askcruz or any improvements which can be made to increase the functionality of askcruz. search through everything you have and then give me correct answer.

## Claude (2026-10-14 09:12:08 EDT)

I searched the AskCruz wiki, emails, call transcripts and the live teams-askcruz task board (data through Oct 13, 2026). The ERP implementation tasks for Discount Pipe & Steel and Eastern States Steel are EOXS ERP work, not AskCruz product issues, so I left them out. I’m marking what is documented separately from what is my own suggestion.

Current difficulties

1. Data privacy and access control (the biggest commercial blocker)

Task #526 is marked high priority. It says prospects keep asking who at AskCruz/EOXS can see their ingested data, and that this is a recurring objection in every deal.
The honest answer today is that a few engineers with server and database credentials technically can. There is no documented access policy for client deployments, no access logging, and no SOC 2 certification.
The architecture doc lists multi-tenant isolation as an open item, not a confirmed capability.
The one verifiable claim is Zero Data Retention with Anthropic. That covers whether the model provider retains data, not whether staff can see it.
The Sabre Alloys deal also hit data-privacy pushback in Sept 2026. The Sabre services agreement was sent Oct 12 and no signature is confirmed.
On Sept 2, a team meeting flagged a salary-data exposure issue as a major security and compliance failure. The wiki redacts the details.
Task #753 (audit employee access rights) is stuck: changes to revoke access are not saving. The team consulted Talal and the problem is unresolved as of Oct 10.
An Oct 6 QA run on the new per-user OAuth sign-in found HR leave and health emails (557) and 6 HR wiki pages visible to the internal-team and intern tiers. The HR-tier rules were fixed in code, but the relabel script and re-QA were still pending.
Fathom and Fireflies calls were wrongly marked Tier 1 (Raj only). A sweep with a dead classifier key caused it, and 25 calls plus their wiki pages were re-tiered on Oct 8–9.

2. Retrieval accuracy

Task #751, “Diagnose why AI can’t pull the right context from the backend”, is still at intake.
Raj asked the AI to find “Trip’s” email and it couldn’t (#519). It was still unresolved on Sept 30.
The same marketing-data query worked for Raj but not for Ayan (#510). Missing skill files and instructions on Ayan’s account were the cause. Results varied between users, and consistency across users is still unchecked.
Search is keyword-only today. Rajat’s Oct 2 email to Sabre describes semantic search as a proposed addition, not something live.
Raw threads were saved unstructured, which hurt accuracy (#522). They now live in a separate structured Threads Wiki vault.

3. Ingestion reliability

Attachments (#503):
Extracted text was silently cut off at 50,000 characters. This lost part of the August payroll data.
No OCR existed for scanned or image attachments. A Claude Vision fix went in Sept 10–11, and about 10,222 older images needed backfilling.
Identically named images were overwriting each other. A hash suffix fixed that.
Multi-tab Excel handling was still to be verified.
Zoho support emails had not been ingested into the wiki for a long time, until a Sept 14 fix.
Wiki ingestion was reported failing again on Oct 12 (#799).
The Oct 12 system audit found a faulty database-connection guard. It refused to start the drafting agents and left 140 emails marked failed, though they are still queued.
A review backlog of 279 pages delays new mail by hours. The tracking sheet also can’t tell “pending” from “failed”.
3GM’s Forcht bank notification emails land in Stefan’s Outlook Junk folder, which is deliberately not synced, so they never reach the vault.
The same raw file can feed multiple wiki pages. CC recipients weren’t captured until Sept 30.

4. Model and platform issues

Claude Sonnet 5.5 returns a “reasoning extraction” error on prompts that ask the model to show its reasoning in a fixed format. Removing that request avoids it.
A separate cybersecurity safeguard flag fires on some queries, including when the Threads connector was off. This suggests the model’s own classification, not an AskCruz bug.
GPT-4 avoided the error but took over 14 minutes on a complex prompt.
Thread auto-saving is inconsistent. QA saw 2–3 of 40+ queries unsaved, and migrated chats lack the tool entirely.
Per Aug 12 notes on #82, token and spend limits were set per group, and a view-limit option in settings was requested.
A spam-filter automation consumed a lot of tokens (#162).

5. Adoption and process

3GM’s VP of Trading Operations reportedly refuses to use AI, which is a practical obstacle to Raj’s pitch to expand AskCruz to inside-sales inboxes.
Open-task hygiene on the board is weak. There are no deadlines on tasks. A stage named “Complete” sits next to “Completed”, so finished tasks keep resurfacing. Many tasks have gone idle or have no log notes.
Several R&D items are Tabled: voice call-in, the iOS app, the sales AI agent, the calendar and LinkedIn tools.
Improvements already in progress
Semantic and hybrid search (#757): pgvector inside PostgreSQL was chosen over an external vector database. A private MCP and comparison dashboard are built, and deployment on Render is hitting timeouts.
Per-user OAuth sign-in (#747): each person signs in themselves, so tiers are enforced per user. Header tokens still work, which is why the QA gaps above matter.
Watchtower and Airflow monitoring (#504): mail, meeting and health-check DAGs run four times a day. Critical incidents trigger alert emails, and a log-and-fixes sheet exists.
Write-access MCP (#391): waiting on Talal.
Other items: a source-of-truth architecture (#588, #508), a real-time ingestion pipeline (#283), an admin panel for threads (#603), and a 3GM MCP for Raj (#782, done).
My suggestions (not in the sources)
Finish #526 in the order it lists: a written least-privilege policy, then access logging, then a tenant-isolation review, then SOC 2 Type II.
Fix the Junk-folder gap with a trusted-sender allowlist, as the audit recommended. Also draft the last 7 days of mail before the review backlog.
Add Pending versus Failed states to the ingestion sheet, and have it read the real outcome from the database.
Test retrieval after every skill-file change, using a fixed set of queries run under several user tiers, since consistency varies by account.
Clean up the board: standardize the stage names, add deadlines, and set a rule that a task isn’t closed without a log note.
Re-run access-tier QA after every re-tiering script. The recurring mislabeling suggests tiers should be recalculated when sources change. A Sept 2026 task note says live pages are never recalculated.

Some items are still open. It is unconfirmed whether the reasoning-extraction bug affects client deployments, whether the vector search has shipped, and whether the HR tier fix is fully deployed. Is there a particular area, such as the 3GM or Sabre rollout, that you’d like me to go deeper on?
