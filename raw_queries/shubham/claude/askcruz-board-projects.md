---
conversation_id: d3db9c81-2dce-4b42-aa24-0e4e21ab81e7
platform: claude
username: "shubham"
title: "Askcruz board projects"
created_at: "2026-10-09T16:07:49.252675Z"
updated_at: "2026-10-12 12:32:55 EDT"
---

# Askcruz board projects

## User (2026-10-12 12:32:55 EDT)

can u give me the information about all the projects in askcruz board

## Claude (2026-10-12 12:32:55 EDT)

I'll start by reading the thread-wiki skill and loading the Askcruz and transcript-saving tools.
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

The summary is above, and this chat is saved as `askcruz-board-projects-overview`.

## User (2026-10-12 12:32:55 EDT)

Give some five to 10 comprehensive prompt which can use all the connectors efficiently

## Claude (2026-10-12 12:32:55 EDT)

Two caveats first:
- **Thread-wiki and Threads-Ov disconnected in this session**, so I couldn't save this turn's transcript. Prompts that use them need those connectors back.
- **I haven't inspected the Eoxs-Teams or Read-only schemas.** The prompts tell Claude to check the schema first rather than assume what's in them.

Each prompt names a rigor level (and a craft level where it builds something), so Claude won't stop to ask. Swap in your own client names and dates.

---

**1. Client 360 brief**
> Rigor: 50 ft deep. Craft: Draft, as a Doc. Build a 360 brief on [client slug]. From Askcruz, pull the client profile, contacts, last 90 days of emails and calls, open implementation tasks, assets and wiki pages. Check Thread-wiki for any internal Claude threads that mention them. Report relationship health, open risks, overdue items, what the client has asked for and not received, and the 3 things we should do this week. Cite the source (email, call, task ID, thread) for every claim, and flag conflicts between sources.

**2. Implementation board health review**
> Rigor: 10 ft deep. List all implementation tasks across all clients. Report by client: stage distribution, High-priority count, overdue deadlines, tasks with no update in 30+ days, and owner load. Then cross-check the 5 stalest or most overdue tasks against emails and calls to see if the client has chased us on them. Recommend which tasks to unblock first and why.

**3. Pre-call prep**
> Rigor: 10 ft deep. Craft: Sketch. I have a call with [client/contact] on [date]. Pull the last 3 calls and last 10 emails with them, their open tasks and anything in wiki or repo docs about their setup. Give me a one-page prep: where we left off, what they'll likely raise, our open commitments, and 3 questions I should ask.

**4. Promise audit**
> Rigor: 50 ft deep. For [client], search calls and emails from the last [60] days for commitments our team made (dates, deliverables, "we'll send", "we'll fix"). Match each commitment to an implementation task or asset. Output a table: commitment, who said it and when, matching task or none, status, and risk. Highlight commitments with no matching task.

**5. Cross-database reconciliation**
> Rigor: 10 ft deep. First run list_tables and get_business_schema on both Eoxs-Teams and Read-only and tell me what each contains. Then, for [client], compare what those databases say (users, usage, records, whatever is relevant) against what Askcruz says (tasks, assets, emails). List mismatches and which source is likely right. State clearly which numbers come from underlying rows and which from summary fields.

**6. Team workload and activity digest**
> Rigor: 5 ft deep. Using Thread-wiki, list what [team member] worked on in Claude in [month]. Using Askcruz, list the implementation tasks they own and their stages. Using Eoxs-Teams, add anything relevant from team records. Summarize in 10 lines or less: what they did, what's stuck, and where their time went versus where it should go.

**7. Recurring issue and root-cause hunt**
> Rigor: 50 ft deep. Search Askcruz tasks, emails and calls across all clients for repeated issue themes (e.g. "packing list", "weight", "tags", "reporting"). Group them, count by client and month, and check wiki and repo docs for whether a documented fix exists. Tell me which themes are product problems versus client-specific, and which deserve a permanent fix instead of repeat tickets.

**8. Weekly leadership report, saved**
> Rigor: 10 ft deep. Craft: Painting, as a Doc. Build this week's internal report: task movement across all clients (from Askcruz), notable emails and calls, anything from the Eoxs-Teams or Read-only data that moved, and top 5 risks with owners. Then, once I approve it, save it with Threads-Ov save_analysis. Don't save before I say so.

**9. Onboarding gap check for a new client**
> Rigor: 10 ft deep. For [client], check whether we have: a client profile, contacts, assets, a wiki page, repo docs, and implementation tasks in each phase. Compare against our best-documented client and list what's missing. Draft a gap-closing checklist with owners, built as a Tasks list.

**10. Decision memo**
> Rigor: 100 ft staged. Craft: Draft. Question: [should we do X for client Y?]. Per the threads-first rule, check Thread-wiki and published wiki pages for prior discussion, then Askcruz emails, calls, tasks and assets, then the databases for hard numbers. Give an outline first, then deliver the memo in sections, pausing after each for me to say "next". Separate facts, assumptions and unknowns, and argue against my likely preference.

---

Prompts 1, 4 and 7 use the most connectors and give the most value. Prompts 6, 8 and 10 need Thread-wiki and Threads-Ov reconnected. If you tell me which workflows you run weekly, I can tighten these into reusable templates with fixed output formats.

## User (2026-10-12 12:32:55 EDT)

please give prompt related to askcruz and eoxs

## Claude (2026-10-12 12:32:55 EDT)

Two assumptions:
- I haven't inspected the Eoxs-Teams schema, so each prompt tells Claude to check it first.
- I'm treating "EOXS" as both the product (tasks like "EOXS Accounting Review" are on the Askcruz board) and the Eoxs-Teams data.

Rigor levels are pre-set so Claude doesn't pause to ask. Replace the bracketed items.

---

**1. Schema map before anything else**
> Rigor: 5 ft deep. Run list_tables and get_business_schema on Eoxs-Teams. Then run get_index and list_clients on Askcruz. Tell me in a table what each source holds, which fields can join across them (client slug, domain, user, instance), and what questions each one can't answer.

**2. Client status: tasks vs. EOXS data**
> Rigor: 10 ft deep. For [client slug], list their open Askcruz implementation tasks by stage. Then pull the matching records from Eoxs-Teams (users, activity, transactions or whatever the schema supports). Flag where a task says something is fixed or done but the EOXS data still shows the problem, or the reverse. Verify against underlying rows, not summary fields.

**3. Bug verification**
> Rigor: 10 ft deep. Take the open bug tasks for [client] (e.g. duplicate tag numbers, wrong weights, invoice status). For each, query Eoxs-Teams to check whether the bad data exists right now and how many records are affected. Output: task ID, bug, affected record count, example IDs, and whether the task's stage matches the reality.

**4. Ticket-to-feature mapping**
> Rigor: 50 ft deep. Search Askcruz tasks, emails and calls for feature requests from [client]. For each request, check Eoxs-Teams and repo docs to see if EOXS already supports it. Sort into: already possible (needs training), configurable, needs development, and unclear. Cite the source for each.

**5. Adoption and usage check**
> Rigor: 10 ft deep. For [client], compare what they said in calls and emails about how they use EOXS against what Eoxs-Teams shows (active users, modules used, volume over time). List where they underuse or misuse it. Give 5 concrete training or config actions.

**6. Cross-client pattern report**
> Rigor: 50 ft deep. Group all Askcruz implementation tasks across clients by theme (packing, tags, reporting, accounting, integrations). Using Eoxs-Teams, check which themes show up in the data for multiple clients. Separate product defects from client-specific setup problems and rank themes by how many clients and records they hit. Recommend which to fix in the product.

**7. Integration readiness**
> Rigor: 10 ft deep. Using Askcruz tasks, emails and wiki pages, list all integrations requested or in progress for [client] (QuickBooks, Aircall, Klaviyo, bank feeds, email). For each, check Eoxs-Teams for any related tables or records and repo docs for what's built. Output a status table: requested, built, tested, live, blocker.

**8. Go-live checklist**
> Rigor: 10 ft deep. Craft: Draft, as a Tasks list. For [client]'s phase, list every task still before "Can be moved to live". For each, check Eoxs-Teams data for blockers (missing records, bad data, config gaps). Produce a go-live checklist with owner, blocker and who must sign off.

**9. Weekly client update, ready to send**
> Rigor: 10 ft deep. Craft: Draft. Write a status update email for [client contact]. Use Askcruz for completed and in-progress tasks, and Eoxs-Teams for evidence of the impact (before/after numbers). Keep it under 200 words, plain language, no internal stage names, and list any decisions we need from them.

---

Prompts 2, 3 and 6 give the most value because they check the board against actual data. I can't save this turn to Threads-Ov, since that connector is disconnected.
