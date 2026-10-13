---
conversation_id: a6ffc1a3-c7aa-4bc8-bfa5-04e12de0d001
platform: claude
username: "unknown"
title: "How askcruz works"
created_at: "2026-10-12 09:34:04 EDT"
updated_at: "2026-10-13 09:05:29 EDT"
---

# How askcruz works

## User (2026-10-13 09:05:29 EDT)

give me full information about the working of askcruz

## Claude (2026-10-13 09:05:29 EDT)

I'll start by reading the required skill files.

Here's what AskCruz is and how it works, based on EOXS's internal wiki and the reference documents behind it (baseline around 21-24 Aug 2026).

## What it is

AskCruz (product family name **Cruz**) is an industry-agnostic AI agent that connects a company's scattered business data, structures it into usable knowledge, and lets employees ask questions through one conversational interface. The core problem it targets is that information lives across email, spreadsheets, operational systems, project tools and call records, so people know it exists but struggle to find it.

It is positioned against generic AI (no internal context) and traditional search (finds records but leaves you to read and connect them). The tagline in the source is "Search finds information. AskCruz is designed to make organizational knowledge usable."

## How it works: the pipeline

The documented flow has ten stages:

**Source systems → Ingestion → Filtering → Sensitivity classification → Central knowledge store → Knowledge generation → Citation check → Human approval → Retrieval → Response**

- **Ingestion** uses event-driven ingestion, scheduled sweeps, source-specific fetchers and sync jobs, depending on the source.
- **Knowledge generation** synthesizes readable pages with source references rather than exposing raw data. A synthesis cycle runs **every six hours**.
- **Verification** means each synthesized page gets a citation check and then human approval before it is published.
- **Retrieval** answers questions from the approved knowledge, with citations back to the raw sources.

## Data sources

- **Gmail:** three individual accounts.
- **Zoho:** one shared support inbox.
- **Fireflies and Fathom:** call transcripts and recordings.
- **Client Odoo implementation boards:** six clients (Greer Steel, Eastern States Steel, Discount Pipe & Steel, PPC Metals, 3GM Steel, Sabre Alloys).
- **Internal assets:** SOPs, policies and reference documents.

Support tickets and invoices/sales orders are **not** natively collected. They stay in the live Odoo system and are reached through the separate `eoxs-teams` connector.

## Capability model

The product feature file defines four named capabilities:

1. **Company Brain:** the shared working knowledge (who does what, how quotes are priced, customer history, past commitments).
2. **Company Hands:** practical help such as drafting quotes, flagging at-risk orders and summarizing calls. It is not autonomous decision-making.
3. **Digital Workforce:** standing responsibilities that watch conditions and report, such as monitoring an order queue.
4. **Company Personalization:** reflecting one company's vocabulary, pricing logic and customer expectations.

It covers customers, orders and delivery, inventory ("free to sell" means availability after commitments), quotes and pricing, calls, commitments, margins ("true margin" includes freight and processing) and operational issues. Typical users are sales, operations, customer-facing teams, leadership and new hires.

## Access control and security

Sensitivity labels are General, Company-Confidential (financials, salaries, legal, investor talks, employee performance) and Raj-Personal. When classification is uncertain, the system picks the more restrictive label.

| Connection | Sees |
|---|---|
| Raj | Company-Confidential and Raj-Personal |
| HR | Company-Confidential, with some financial restrictions |
| General staff | General business info, with financial amounts and employee performance stripped |
| Interns | General info only, with financial amounts stripped |

There are two protection layers: database-level access control, and an independent AI response-level check as defense in depth. Product access tiers are named `tier1`, `tier2_confidential` and `tier2`.

Behavior rules: it must never reveal restricted info, infer access from how a question is worded, grant access to someone just claiming to be an admin, bypass controls through indirect requests, expose credentials, or follow instructions embedded in retrieved documents (prompt-injection resistance).

## Limitations and boundaries

- **Freshness:** answers reflect scheduled processing with a six-hour lag, so they are not real-time. Live systems remain the source of truth.
- **Completeness:** the product file cites 94% data completeness, but that is a product-level metric, not a per-answer guarantee.
- **Availability:** a capability existing at product level doesn't mean it's enabled for every client. It depends on that client's connected sources and approvals.
- **Information vs. action:** explaining information is not permission or ability to act in the source system.
- **Draft knowledge:** unapproved knowledge isn't treated as final.

## Market status

- **Buyer:** the CEO is the primary decision-maker.
- **Customers:** 3GM is the first acquired customer. A reduced 2-user scope deal was confirmed in Aug 2026, with a kickoff invoice issued 6 Sep 2026. Sales pushes to Sabre Alloys and other prospects are in progress.
- **Product-market fit:** the internal assessment is that there are clear early signals but not yet proof of broad, repeatable fit. Pricing, ACV, sales-cycle length, retention, ROI and usage metrics are listed as not yet established.
- **Roadmap:** today it handles plain-language Q&A over organizational knowledge. Next come workflows, business-system integration and connected AI agents.

## Things to be aware of

- **Positioning conflict:** the product feature file calls AskCruz "for steel businesses," while the product-market fit guide says it is industry-agnostic. The wiki flags this as unresolved, so confirm which is current before external use.
- **Unverified ownership info:** the "technical ownership" section (frontend by Jaskeerat, other items restricted) hasn't been cross-checked against current team records.
- **Internal docs:** the companion technical docs (backend-server, postgres-database, raw-ingestion, wiki-ingestion, etc.) aren't loaded in the repo-docs index, so I couldn't read them.

## Housekeeping notes

- I looked for a dedicated askcruz skill file as your org instructions require, but none exists in this environment. I used the AskCruz connector's wiki and assets instead.
- The `save_chat_transcript` tool isn't connected in this session, so this conversation was **not** archived.

I can go deeper on any section, such as the raw source documents, the 3GM deal, or the internal task board.

## User (2026-10-13 09:05:29 EDT)

give me some ideas by which we can save the threads ..

## Claude (2026-10-13 09:05:29 EDT)

Here are some ways to save threads, from the proper automated route to quick manual ones.

## 1. Reconnect the Threads-Ov connector (best fix)
This is the intended system. `save_chat_transcript` overwrites a git-tracked file with the full verbatim conversation after every reply, and `checkpoint` triggers the save reminder. It isn't connected in this session, so an admin should check that it's enabled in the connector settings and that the GitHub token is set. Once it's on, saving needs no effort from anyone.

Conventions that keep it clean:
- Pick one stable `thread_name` on the first turn and never change it (for example `askcruz-architecture-oct2026`). Changing it creates a second file.
- Always send the full transcript, not just the latest exchange.

## 2. Save into a tool you already have connected
Your workspace has several connectors that can act as a manual archive:
- **Claude Docs:** I can turn this conversation into a doc that you can share, comment on and export.
- **Google Docs or Drive:** a dated doc in a shared "Claude Threads" folder.
- **Notion or Confluence:** a "Claude Threads" database or space, with properties for owner, topic and date.
- **Box:** the same idea as Drive, if your team stores documents there.
- **Slack:** post a summary to a channel such as #claude-archive for visibility and search.

## 3. Save the analysis, not just the chat
For finished work like reports, comparisons and decisions, `save_analysis` (once Threads-Ov is connected) writes a clean write-up to `wiki/analyses/`. It needs your explicit approval each time, so only polished output ends up there.

## 4. Cross-link into the wiki
Use `propose_ov2_xref` to stage a one- or two-line pointer from the relevant OV2 wiki page to the thread. `apply_ov2_xref` then applies it after you approve. That way people reading the wiki can find the underlying discussion.

## 5. Make it a team habit
- Name threads consistently: `<topic>-<month-year>`.
- Ask for a summary and decisions block at the end of any long session.
- Keep one thread per topic rather than mixing subjects.
- Use Threads-Wiki to confirm saves landed. There is about a 15-minute sync lag before a thread shows up in the database.

## What I'd do now
Since automated saving isn't available in this session, the quickest option is for me to create a **Claude Doc of this conversation** so it isn't lost. Do you want me to do that?

## User (2026-10-13 09:05:29 EDT)

the thread ov is not working properly and hance not saving the queries . give me ideas by which it can be fixed

## Claude (2026-10-13 09:05:29 EDT)

Let me check what the read side shows, so we can tell where the failure is.

I can't see the write side from here, but I checked what has arrived on the read side. The archive has 1,937 threads, and the newest is dated **9 Oct 2026**. Nothing is dated 10-12 Oct. The weekend explains part of that, but nothing has landed today (Monday) either, which fits what you're seeing. The timestamps are date-only, so I can't tell the exact time of the last save. The 9 Oct count (134 threads, against a usual 30-60) looks like a bulk import or duplicate files, which is worth a look.

## 1. Connector is missing or disconnected
In this session `save_chat_transcript` and `checkpoint` aren't loaded at all, so nothing can save.
- In the connector settings, check that Threads-Ov is enabled for each user and for this organization.
- Look for a lapsed sign-in or token. The tool list should show the five tools: `save_chat_transcript`, `checkpoint`, `save_analysis`, `propose_ov2_xref` and `apply_ov2_xref`.
- Remove and re-add the connector, then start a new conversation. Tools are loaded at conversation start, so an old chat won't pick up the fix.
- Check whether the connector is only enabled for some users. 14 users saved on 9 Oct, so others may simply be missing it.

## 2. Server or credentials are failing
The save writes a file, then commits and pushes it to git using `GITHUB_TOKEN`.
- Check that the token hasn't expired or been revoked and still has write access to the repo.
- Check for branch protection that rejects direct pushes, and for push conflicts when two saves land at once.
- Check the MCP server logs and uptime for 10-12 Oct, including the host, any deploy that went out on 9 Oct, and disk space.
- Cross-linking uses a separate `OV2_GITHUB_TOKEN`. An auth error there won't affect transcript saving, but confirm the two tokens aren't mixed up.

## 3. The saves arrive but are wrong
- **Summary instead of full text:** `content` must be the complete verbatim transcript every turn. A summary means the thread was never captured.
- **Changing `thread_name`:** this creates a second file. It may explain the 9 Oct spike.
- **Latest exchange only:** each save overwrites the file, so sending only the newest exchange erases earlier turns.
- **Identity:** the server resolves the username. If it fails to resolve, files could land under the wrong user or fail.

## 4. Saved but not showing in Thread-wiki
- The sync to the database takes about 15 minutes. Wait before concluding a save failed.
- Look at the sync job that moves the git files into `eoxs_frontend_threads`. If it stalled after 9 Oct, files could be in git but invisible here. Check the repo for recent commits in `raw/claude-chat-queries/` to tell which side is broken.

## 5. Add monitoring
- Run a daily check on the max `created_at` in `threads` and alert if it's more than 24 hours old on a weekday.
- Have the instruction layer confirm the save actually succeeded, and warn visibly when the tool is missing, instead of failing silently.
- Keep a manual fallback, such as a Claude Doc or Google Doc, for important threads in the meantime.

## Suggested order
1. Check the git repo for recent commits. This shows whether the break is before or after the push.
2. Check the token and connector status.
3. Start a fresh conversation and see whether the tools load.
4. Check the sync job if commits exist but the database is empty.

I can run a few more diagnostic queries, such as per-user save activity over the last week, to see whether this is everyone or specific people. Do you want me to do that?

## User (2026-10-13 09:05:29 EDT)

give me any other ideas by which we can save the threads into out database.

## Claude (2026-10-13 09:05:29 EDT)

Here are other routes into the database. Thread-wiki is read-only, so each of these needs a separate write path. I've ordered them from most to least robust.

## 1. A direct-to-database save tool (skips git)
Build a small MCP server, or an HTTP endpoint, that does one job: `save_thread(thread_name, content)` writes straight into `threads` and `thread_messages` in Postgres.
- It removes git pushes, tokens and the sync lag, which are the likeliest failure points of the current setup.
- Make it an idempotent upsert keyed on `(username, thread_name)`, so repeated saves overwrite instead of duplicating.
- The server should resolve the user's identity and `access_tier` itself, never trust values passed in by the model.
- I can scaffold this with the MCP-builder skill if you want.

## 2. Bulk import from Claude's own data
- Each user can export their data from Settings > Privacy. Owners on Team or Enterprise plans may also have org-level export or compliance tools, so check what your plan offers.
- A scheduled script reads the export and loads it into the database, deduplicating on conversation ID.
- This captures every conversation, even if people forget to save. It is delayed, not real time, but it's the best safety net.

## 3. Capture from the client side
- A browser extension or bookmarklet that scrapes the conversation and posts it to your ingestion endpoint when you click "Save".
- For developers, Claude Code hooks can send each session transcript to the endpoint at the end of a session.

## 4. Drop-folder bridge with an ETL job
Save transcripts as files in a shared location, and let a scheduled job load them.
- **Google Drive or Box:** a "Claude Threads" folder with a nightly script that parses new files into the database.
- **Notion or Slack:** a database or channel where people paste or post, picked up by an ETL job.
- **Claude Docs:** I can create a doc per conversation, and a job exports and ingests them.

This is slower and manual, but it works with the connectors you already have.

## 5. Push files into the existing repo yourselves
The current pipeline already turns files in `raw/claude-chat-queries/` into database rows. If Threads-Ov fails but the sync job is healthy, another process, such as a GitHub Action or a small script, can commit transcripts to that folder using the same naming convention (`<user>_<date>_<thread_name>.md`). It needs a properly stored repo token, never one pasted into a chat.

## 6. Scheduled summarization as a backup
A recurring task prompts Claude to summarize the day's work per person and saves the result somewhere ingestible. It's lossy, since it isn't a verbatim transcript, but it keeps a record of decisions and findings even when everything else is down.

## Design points for whichever route you choose
- **Stable keys:** one thread name per conversation and an upsert, to avoid duplicates like the 9 Oct spike.
- **Full verbatim content:** a summary is not a saved thread.
- **Access tiers:** set `tier1`, `tier2` or `tier2_confidential` at write time so confidentiality rules still apply.
- **Monitoring:** a daily alert if no new rows appear on a weekday.
- **Idempotency:** re-running an import must never duplicate data.

My recommendation is option 1 as the main path, with option 2 as a nightly safety net. Together they remove the git dependency and catch anything that gets missed. Do you want me to draft the table inserts and the MCP server design for option 1?
