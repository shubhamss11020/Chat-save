---
conversation_id: ba0bb8d2-143b-464b-9daa-678847bd9d7f
platform: claude
username: "unknown"
title: "System problems and improvement ideas - Claude"
created_at: "2026-10-14 09:29:43 EDT"
updated_at: "2026-10-14 09:31:12 EDT"
---

# System problems and improvement ideas - Claude

## User (2026-10-14 09:31:12 EDT)

check the current system and see what the problems are that can be fixed in the current system and also give me some list of ideas by which our system can be improved with its limitations and working.

## Claude (2026-10-14 09:31:12 EDT)

I checked the AskCruz knowledge system: the thread archive, the synthesized wiki, and the pipeline between them. You didn’t say which system you meant, so I assumed this one. If you meant the Odoo/ERP side, tell me and I’ll audit that instead.

Problems that can be fixed now
The wiki backlog is large. 918 of 1,942 saved threads (47%) aren’t cited by any wiki page, so about half of the team’s work isn’t reachable through the wiki.
Many drafts are stuck in the rework queue. There are 304 promoted drafts against 144 needing rework and 53 rejected.
The largest rework cause is mis_scoped (74), followed by coverage_gap (27), citation_integrity (22) and source_conflict (20).
Of the rejected drafts, 49 are cross_page_conflict. Rejected drafts need a human, so they aren’t clearing themselves.
Pages contradict each other, or rest on sources that were deleted.
The wiki has 2 contradiction flags and 9 needs-review flags. Most of the needs-review flags are pages citing threads that no longer exist, so their claims can’t be verified. Several 3GM Steel and Brannon Steel pages are affected.
Two other pages disagree on facts, including a contract term of 1 year versus 3 years.
The wiki is barely cross-linked. There are only 25 links across 222 pages, so it works as a pile of pages rather than a graph.
Some AskCruz citations can’t be followed. Several wiki pages cite sources marked unresolved, or cite other wiki pages with no fetch path, so you can’t trace them back to the raw record.
Search relevance is weak. A generic query like “overview” returned scores around 0.09, mixing client entities with very long run-on analysis titles and some noisy archive batches (for example recruiting-thread noise filed under product bugs).
Promoted counts don’t match live pages. Staging shows 304 promoted but only 222 pages are live. This may be legitimate merging, but it’s worth confirming.
Citation freshness is healthy. Only 7 of 1,019 citations are stale.
Limits I hit while checking
My account can’t read vault_sync_runs or save_failures, so I couldn’t verify sync health or failed saves.
The repo reference docs list is empty, so no architecture docs are indexed.
Archive queries cut each cell at 160 characters, the archive lags about 15 minutes behind saves, and saved messages can’t be edited or deleted.
Raw SQL isn’t filtered by access_tier, and redacted values appear as $RESTRICTED placeholders, which weakens some pages.
Ideas to improve the system
Idea	What it does	Limitation
Backlog sprint	Prioritize the 918 uncited threads by client or revenue relevance, and batch-synthesize the top ones	Review capacity is the bottleneck; the reviewer agent already rejects mis-scoped drafts
Better scoping rules	Give the drafter clearer topic and entity boundaries, since mis_scoped is the top defect	Needs a feedback loop from the review notes
Contradiction resolver	When a flag names a newer thread, auto-propose a “supersedes” edit	A human still decides which fact wins (for example the 1-year vs 3-year term)
Deleted-source handling	Mark pages with dead citations “unverified” and suggest re-sourcing	Threads deleted on purpose can’t be restored
Link enrichment	Auto-suggest links between pages that share entities, using entity_refs	Links need spot-checking to avoid noise
Search tuning	Boost entity pages, shorten analysis titles, and tag archive noise batches	Needs a small test set of real queries
Health dashboard	Show backlog, rework counts, stale citations and sync status in one place	Needs read access to the sync tables
Unresolved-citation cleanup	Resolve or drop citations with no fetch path	Some sources may be gone

I’d start with the contradiction flags and dead citations, since wrong facts do the most damage. Then I’d work on the mis-scoping rules, because that clears the biggest chunk of the rework queue.

Two setup gaps this session: the askcruz skill file doesn’t exist at any path I can see (only thread-wiki does). The save_chat_transcript tool isn’t connected either, so this conversation hasn’t been archived.

Would you like me to start with the contradiction and dead-citation list, or with the uncited backlog?
