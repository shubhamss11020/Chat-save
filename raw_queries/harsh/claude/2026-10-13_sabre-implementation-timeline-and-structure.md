---
conversation_id: 7641babe-0e8f-48c7-ac04-ddec9b33dab6
platform: claude
username: "harsh"
title: "Sabre implementation timeline and structure"
created_at: "2026-10-13 09:38:30 EDT"
updated_at: "2026-10-13 10:46:56 EDT"
---

# Sabre implementation timeline and structure

## User (2026-10-13 09:15:15 EDT)

i want to understand the implementation timeline for sabre, and what would be the right structure to get started on it. Take reference from the 3GM board, understand the implementation timeline we took, consider the user difference, and proposed timeline to sabre. Also take in consideration of hurdles that we faced for 3GM that we can mitigate this time to improve the efficiency, and how to strucuture this implementation properly. Use askcruz and teamaskcruz mcp for this

## Claude (2026-10-13 09:18:09 EDT)

Now let me gather the data. I'll start by getting the index and then searching for 3GM and Sabre implementation data.

Now let me pull the full implementation data for both 3GM and Sabre from the task boards:

Now let me get the full implementation kanban pages for both 3GM and Sabre:

Now I have enough depth. Let me pull the Teams boards for a quick look at Sabre's current task stage distribution:

Now I have everything I need. Let me save the transcript and then write the full response.

The save_chat_transcript tool isn't coming up via tool_search — it must be on a connector that needs a different search term. Let me try:

The Threads-OV vault connector isn't resolving via tool_search — it appears it's not available in this session. I'll proceed with delivering the full response and note the save couldn't complete.

---

Here's the full analysis, grounded in what's actually in the boards and wiki.

---

## Sabre Alloys — Implementation Timeline, Structure & Lessons from 3GM

### Part 1: What the 3GM Board Actually Tells Us

**The honest 3GM timeline was ~7 months, not the 2–3 months pitched.**

The kickoff announcement email explicitly told 3GM to expect "2–3 months." The actual go-live was July 18, 2022 — roughly 12 weeks past that commitment. Here's how the phases broke down:

| Phase | Dates | What Happened |
|---|---|---|
| Sales & Proposal | Early April 2022 | Formal proposal sent Apr 14, ownership meeting, Travis confirmed |
| Kickoff Day | Apr 26, 2022 | 13 tasks created same day — announcement email, org chart, data requests, payment tracking |
| Discovery Interviews | Apr 27, 2022 | 7 per-stakeholder discovery calls (Travis, Jessica, Adam Buck, Leslie, Donnie, Rachel, Rajat) |
| Data Gathering | May 3–5, 2022 | Access rights, login credentials issued, sales history, accounting scoping, ports info |
| Internal Housekeeping | May 17, 2022 | Internal cleanup tasks |
| Master Data Import | May 25, 2022 | Product master, coil inventory export (`tblcoilinventory0.xls`) loaded |
| Soft Launch Target | June 13–17, 2022 | **Missed** — internal update pushed target to this week, didn't hit |
| Pre-Soft-Launch Call | July 14, 2022 | "Pre Soft Launch Requisites" call recorded |
| **Actual Go-Live** | **July 18, 2022** | Confirmed go-live |
| Post-Launch Stabilization | July–Nov 2022 | Invoicing (July 27–28), Claims (July 22), Dashboard Review (Sept 26), Tonnage Review (Nov 28) |

**Key structural observation:** 3GM had ~6 stakeholders interviewed in individual discovery calls before a single line of data was entered. That thoroughness was good — the Rachel Epperson call alone produced the full inbound-freight workflow spec that drove module design. The problem was no hard deadlines were held accountable after that.

**3GM's board today (teams-askcruz):** 28 Complete, 10 Intake, 2 In-Dev, 2 Tabled, 1 Requirements, 1 Recurring. They're a fully mature client operating steadily — which is what a successful implementation eventually looks like.

---

### Part 2: What Actually Happened with Sabre — The Real Timeline

Sabre's situation was fundamentally different from 3GM in two ways: **they migrated from an existing system (SteelPlus)** and **they had already been an EOXS client** in some partial capacity before the 2024 soft launch. The "implementation" was really a full-system migration and go-live sprint.

| Phase | Dates | What Happened |
|---|---|---|
| Pre-Launch Setup | Jan–Mar 15, 2024 | Fresh database provisioned, Chart of Accounts (COA migrated from SteelPlus), inventory count, logo/branding assets |
| Server Migration | Feb 5, 2024 | Migrated to `sa.eoxs.com` — caused same-day login failures for multiple users, one data file had to be moved manually (30-min pause) |
| Product Master & Gap Analysis | Feb–Mar 2024 | Sessions with Ernie & Ron on product master structure; formal Gap Analysis (Mar 11); inventory cost review (Mar 13) |
| Sprint I – Data Entry | Apr 2, 2024 | Structured sprint — Sid, Faraz, Herik + Ernie uploading open orders, inventory, freight vendors daily via Zoom |
| **Actual Soft Go-Live** | **~Late Mar/Apr 2, 2024** | Task "Front end and back end cleanup after soft launch" created Apr 4, confirming go-live had already happened |
| Post-Launch Stabilization | April 2024 (~100 tasks) | UI cleanup (label renames), workflow bugs (lot valuation, COGS sourcing), access-control work with Tye Webb |
| Feature Buildout | Late April–May 2024 | Dashboards, QA flow, third-party processing, buyout workflow, control-tag/lot-serial features |
| Accounting Reconciliation | May 24–June 7, 2024 | AR/AP discrepancy cluster (Jesus Rios lead), Notes Payable balance issue, accounting sessions May 30–31 |
| Project Archival | June 18, 2024 | Last task created — "Demanded weight editable in processing order" left as "Need discussion" |

**Sabre's board today (teams-askcruz):** 36 Intake, 1 Assigned — meaning they are now operating as a live client with ongoing ticket flow, not in active implementation. The 200-task implementation board is closed.

---

### Part 3: The Hurdles We Faced (and What They Cost)

These are the documented problems, not hypothetical ones:

**1. Server migration caused immediate disruption (Sabre's biggest early failure)**
The Feb 5 migration to `sa.eoxs.com` broke logins for multiple users on day one. One file failed to migrate entirely. This cost credibility right at the start of the relationship. The fix was Rajat jumping on Zoom in real time — reactive, not planned.

**Mitigation for next time:** Run a pre-migration user login test in a staging window. Have a 24-hour "migration war room" protocol. Don't announce go-live until logins are verified.

**2. Product master not complete before go-live (blocked inventory import)**
A restricted inventory block couldn't be imported during Sprint I because the product master had unresolved issues. Ernie was left holding live orders while the EOXS team worked around an incomplete foundation.

**Mitigation:** Product master sign-off as a hard gate before any inventory data entry begins. No exceptions.

**3. The 2–3 month timeline promise is a fiction**
3GM was told "2–3 months" — it took 7. Sabre wasn't told an explicit timeline in the preserved records, but the sprint-then-stabilize-then-feature-buildout-then-accounting arc naturally ran 3+ months just for stabilization. The real pattern across both clients is: **kickoff → ~2 months data/setup → go-live → 2–3 months stabilization → then feature work begins.** Promising anything shorter sets up client frustration.

**Mitigation:** Commit to a milestone-based timeline, not a duration. "We go live when Product Master is approved, data sprint is complete, and UAT passes" — not "in 8 weeks."

**4. Accounting was treated as an afterthought**
Both 3GM and Sabre had accounting scope questions unresolved at kickoff. 3GM's kickoff explicitly flagged "does full accounting go live in Phase 1, or wait for a CFO?" — meaning the scope was never locked. Sabre's accounting reconciliation became its own crisis cluster in May–June 2024, with AR/AP discrepancies and a Notes Payable balance issue that required dedicated sessions with Jesus Rios.

**Mitigation:** Accounting discovery call must happen in Week 1, not Month 3. Chart of Accounts needs to be finalized and signed off before any transaction data is entered.

**5. Access rights were not scoped upfront**
Both clients had access-rights issues surface mid-implementation. At 3GM, an explicit task tracked access rights as a standalone workstream. At Sabre, Tye Webb raised concerns about sales staff creating their own part numbers — discovered during the go-live sprint, not before. Rajat had to redirect to a controlled item-creation model on the fly.

**Mitigation:** Access rights matrix should be a deliverable in Week 2, reviewed with the VP/decision-maker, and locked before any user credentials are issued.

**6. No formal UAT process — bugs discovered in production**
Sabre's stabilization phase had ~100 tasks just in April 2024. Many were genuine workflow bugs (lot valuation keeping only the last lot, COGS sourced from product master instead of delivery valuation — an actual margin-misstatement risk). These were caught post-go-live, not in testing.

**Mitigation:** A formal UAT checklist (PO → Receipt → Inventory → SO → Delivery → Invoice cycle), run in sandbox by the client before go-live sign-off.

**7. Onsite training visibility was ambiguous**
The wiki flagged a direct contradiction: one source says the Sabre team visited the EOXS office (Apr 11, 2024), but email evidence plus invoiced travel expenses confirm Rajat traveled to Sabre's Houston facility — not the other way around. The fact that this was unclear internally suggests training logistics weren't documented with a clear plan.

**Mitigation:** Training plan as a formal document — who travels where, when, covering what modules, with which Sabre stakeholders.

---

### Part 4: Proposed Sabre 2.0 (AskCruz) Implementation Timeline & Structure

This is specifically for the **AskCruz (Company Brain)** layer Sabre is moving toward — not a fresh ERP implementation, since Sabre is already live. The structure should reflect that.

**Key context:** Sabre has 37 open tasks in the AskCruz project board (36 Intake, 1 Assigned). Claude access was provisioned to Juan Deshon and Tye Webb in Sep 2026. The AskCruz proposal has been through multiple iterations — the latest email chain is "Updated AskCruz Proposal - Sabre Alloys" (Oct 2026). The Toll Processing side deal is separately scoped. A "Sabre 2" AskCruz scope review call happened Sep 2, 2026.

**Proposed phased structure:**

**Week 1–2 — Discovery & Scoping Lock**
- Discovery call with each power user (Juan Deshon, Tye Webb, Ernie Valdez, Charles White)
- Map which workflows/data sources AskCruz will ingest (emails, Odoo, calls, docs)
- Define access tiers: who sees what
- Lock the scope document before any connector setup

**Week 3–4 — Data Connection & Configuration**
- Connect Sabre Odoo instance, email accounts, and call sources to AskCruz
- Verify data ingestion is clean — test with a known historical email/call/task
- Set up the relay inbox and confirm routing
- No user access granted until verified

**Week 5–6 — Internal UAT (EOXS-side)**
- EOXS team runs queries against the connected Sabre data
- Identify gaps (missing records, ingestion failures, domain mismatches)
- Fix ingestion issues before client sees the product

**Week 7–8 — Client UAT with Juan & Tye**
- Guided sessions: Juan and Tye run their own real queries
- Identify training gaps and UX friction
- Build the question library ("what should you be asking AskCruz instead of emailing support?")

**Week 9–10 — Training & Rollout**
- Train remaining stakeholders (Ernie, Charles, etc.)
- Document the use cases that replace existing manual processes
- Set up the weekly check-in cadence (modeled on 3GM's Thursday ~2pm structure)

**Week 11–12 — Stabilization & Handoff**
- Monitor usage, address edge cases
- Deliver a "what to ask, how to ask it" guide
- Formal handoff to ongoing support tier

**Ongoing:** Monthly usage review, like 3GM's AskCruz weekly check-in model.

---

### Part 5: The Structural Difference Worth Noting — Sabre vs 3GM as Users

The user difference matters significantly. 3GM went from zero-to-live with Travis Lane as a hands-on GM who engaged directly. Sabre's primary power users are Juan Deshon and Tye Webb (VP/Partner level) — both have shown they engage through operational questions (Juan has been on weekly calls with Raj for over a year), but there's documented friction around data privacy pushback and scope negotiation. Ernie Valdez is the operational backbone but isn't a decision-maker. Charles White owns IT/systems but isn't the primary user.

This means the AskCruz rollout needs a **champion inside Sabre who drives adoption** — Juan is the most likely candidate given call frequency. Without an internal champion who actively uses it and advocates to the rest of the team, AskCruz will stall at the "Juan and Tye have access" stage, same as any software tool that's provisioned but not embedded in workflows.

The 3GM model worked because Travis Lane became a genuine user of the system. Sabre's implementation structure needs to explicitly plan for that handoff.

---

*Sources: 3GM Steel — Implementation Kanban (Odoo) [wiki]; Sabre Alloys — Implementation Kanban (Odoo, Soft Launch 2024) [wiki]; Sabre Alloys — Data Entry & Gap Analysis [wiki]; Sabre Alloys — Go-Live Preparation (Q1 2024) [wiki]; teams-askcruz project boards (Customer 2 - 3GM, Customer 3 - Sabre Alloys); Sabre Alloys client profile [AskCruz]; 3GM Steel client profile [AskCruz].*

## User (2026-10-13 09:23:57 EDT)

I think we got on the wrong page here, i am talking about Askcruz implementation

## Claude (2026-10-13 09:26:29 EDT)

Got it — you're asking about AskCruz as the **product being implemented for Sabre**, using 3GM's AskCruz implementation as the reference. Let me pull the right data now.

Now let me also check what the Sabre AskCruz proposal actually specifies as the rollout plan:

I now have a complete picture. Let me save and respond.

The Threads-OV vault connector isn't resolving through tool_search in this session — I'll note that and proceed with the full response.

---

Good catch, let me redo this properly — focused entirely on **AskCruz as the product being implemented for Sabre**, using **3GM's AskCruz implementation** as the reference.

---

## AskCruz Implementation for Sabre — Timeline, Structure & Lessons from 3GM

### What the 3GM AskCruz Implementation Actually Looked Like

**The full arc from pitch to active use ran about 7 weeks, but had a meaningful gap in the middle.**

| Milestone | Date | What Happened |
|---|---|---|
| IRIS trial access granted | Late July 2026 | 3GM gets early access to IRIS ahead of formal deal |
| Historical data preload offer | Aug 4, 2026 | Raj offers to bulk-ingest 3GM's sales/purchase/invoice history into IRIS so Travis doesn't have to re-upload per thread |
| Pitch call | Aug 12, 2026 | 27-min Fireflies call — Raj pitches Company Brain to Travis Lane |
| Proposals sent (both rounds) | Aug 13–14, 2026 | Two proposal versions sent with pricing inconsistencies — Travis caught them and flagged to Stefan (CFO) before proceeding |
| Travis confirms deal | Aug 19, 2026 | 2-user scope, 6-month initial term requested |
| Contract signed | Aug 20, 2026 | Same day Raj agreed to shorter term |
| Term auto-renew question resolved in writing | Aug 24, 2026 | Travis's final condition before releasing payment |
| 50% kickoff invoice sent | Sep 7, 2026 | INV/2026/0367 |
| **Kickoff/setup call** | **Oct 1, 2026** | **Actual walkthrough — Travis + Stefan** |
| Outlook connection attempt | Early Sep 2026 | OAuth links sent to Travis and Stefan |
| **Azure AD blocker hit** | **Sep 4, 2026** | Travis's link looped on admin-consent screen — required a 15-min call with Dave Ledford and Ayan to fix (Azure AD "Assignment required" setting misconfigured) |
| Browser issue (Edge vs Chrome) | Sep 4, 2026 post-fix | Travis hit the same-looking error in Edge; copying link to Chrome fixed it |
| 2nd invoice + first month licensing | Oct 5, 2026 | INV/2026/0380 — remaining 50% implementation + October licensing |
| Weekly check-ins confirmed | Oct 12, 2026 | Thursdays ~2pm ET — took 3 emails to pin down due to MetalCon travel |

So the **real elapsed time from signed contract (Aug 20) to kickoff call (Oct 1) was ~6 weeks**, and from kickoff call to weekly check-ins, another 2 weeks. The proposal-to-kickoff stage itself took about 6 weeks longer than it should have because of: the contract back-and-forth on terms, the invoice timing, and then the Azure AD blocker eating a meaningful chunk of the "setup" phase.

---

### Hurdles from 3GM — What to Mitigate for Sabre

**1. Proposal document errors damaged trust before implementation even started**
Travis independently caught pricing inconsistencies between two proposal versions sent the same day. He involved his CFO (Stefan) before agreeing to proceed, and required a point-by-point written reconciliation before signing. This added at least a week of friction.

**Mitigation for Sabre:** One proposal, one sender, one attachment — reconciled internally before it goes out. The Sabre AskCruz proposal has already had multiple rounds (Aug 13 pitch → Sep 3 resend with call transcripts → Oct 12 Services Agreement via DocuSign to Michael + PDF to Tye). The Services Agreement going to two different people via two different channels (DocuSign vs. plain PDF) mirrors the same fragmentation risk. Confirm Michael has signed before proceeding as if it's closed.

**2. The Azure AD / Outlook connection will almost certainly be a friction point with Sabre too**
At 3GM, connecting Outlook required: a dedicated 15-minute call with their IT contact (Dave Ledford), an Azure AD configuration change ("Assignment required" set from Yes → No on the parent app), and still had a residual browser issue (Edge vs Chrome). This wasn't a one-click setup — it required their admin's cooperation.

Sabre's situation is different in a key way: **Sabre already had a documented data privacy pushback** in the AskCruz proposal discussions. Tye Webb and Michael Mercadante both flagged data-ownership concerns — the proposal explicitly addressed this with "Client retains ownership of all data ingested. Ask Cruz does not use client data for training." That pushback will likely resurface when you ask for email access. You need to proactively address this before sending OAuth links, not after.

**Mitigation:** Before the kickoff call, send Sabre a one-pager specifically on what the email connection does and doesn't do — what data gets ingested, how it's stored, who can see it, and the data-ownership clause. Get their IT/admin contact name in advance. Schedule a dedicated 15-min "connection call" with that person on standby, rather than assuming it's self-serve.

**3. A 6-week gap between contract and kickoff is too long**
3GM signed Aug 20, kickoff was Oct 1 — 6 weeks. Part of that was invoice back-and-forth, part was scheduling. That's dead time where client enthusiasm cools and internal urgency fades.

**Mitigation:** At signing, confirm the kickoff date in the same email. Don't let the invoice process block the calendar invite.

**4. Check-in cadence took 3 emails to confirm**
After the kickoff call, it took from Oct 3 → Oct 12 (almost 10 days) just to confirm "Thursdays at 2pm" for weekly check-ins — partly MetalCon, but partly because the ask wasn't specific enough in the first email.

**Mitigation:** Propose a specific day/time in the kickoff call itself — "We'll do Thursday 2pm for the next 4 weeks, I'll send the invite right now." Don't leave it as an open ask to respond to later.

---

### Proposed AskCruz Implementation Structure for Sabre

The proposal already specifies a 6-week rollout: Weeks 1–2 account/email setup, Weeks 3–4 historical ingestion + Company Brain population, Weeks 5–6 prompt history + go-live/training. That structure is sound. Here's how to actually execute it with the lessons applied:

**Pre-kickoff (before Week 1)**
- Confirm Michael Mercadante has signed the DocuSign Services Agreement
- Get the name of Sabre's IT/Microsoft 365 admin — likely someone in Charles White's orbit
- Send the data-privacy one-pager proactively (what connects, what doesn't, ownership clause)
- Set the kickoff date and 4-week check-in cadence in the same email that sends the 50% kickoff invoice
- Identify Sabre's internal champion — Juan Deshon is the strongest candidate given his weekly call cadence with Raj; Tye Webb is the decision-maker but less operationally engaged

**Week 1 — Account Setup & Connections**
- Kickoff call: walk through what will connect (email, Odoo, calls), what the ingestion covers, and set expectations on timeline
- Have the Microsoft 365 admin on the call or immediately available
- Send individual OAuth links to Juan and Tye (start with 2 users as the deal likely scopes to a small initial set — confirm the final user count from the signed agreement)
- Do not declare Week 1 complete until at least one email account is successfully pulling

**Week 2 — Connection Verification**
- Verify ingestion is clean — test with a known email thread (e.g., a recent support ticket)
- Address any OAuth/browser/Azure AD issues before moving to historical ingestion
- Identify the historical data sources: emails back to what date? Which Odoo records? Calls?

**Week 3–4 — Historical Ingestion + Company Brain Population**
- Bulk ingest historical data (the same preload Raj offered 3GM on Aug 4)
- For Sabre this is particularly valuable given their 200-task implementation history, 115 recorded calls, and 1,575 email threads — a lot of institutional memory
- Weekly check-in during this phase: what's ingested, what's missing, any data quality issues
- Run internal QA before showing Sabre — don't surface the Company Brain until you're confident the data is accurate

**Week 5 — Prompt History + Guided UAT**
- First live session where Juan and Tye run real queries against their own Company Brain
- Focus on the use cases that replace what they currently do manually (checking order status, reviewing pricing history, finding old call notes)
- Identify gaps and feed them back as configuration items

**Week 6 — Training + Go-Live**
- Train the broader user set
- Deliver the "what to ask, how to ask it" guide — mirroring what Ron built into the 3GM weekly check-in structure
- Confirm the ongoing support cadence (Thursday 2pm model from 3GM works; adapt to Sabre's schedule)

**Ongoing (post-Week 6)**
- Weekly check-ins for 4 weeks minimum, then monthly
- Track which use cases are getting adopted vs. which are stalling — that signals where more training is needed
- Toll processing side deal (separately scoped at a restricted amount) should be tracked as a Phase 2 item, not bundled into the initial 6 weeks

---

**The key structural difference between 3GM and Sabre as AskCruz users:** 3GM's deal closed cleanly (Travis brought Stefan in early and required written clarity before signing — healthy). Sabre's deal is still technically unsigned as of Oct 12 (DocuSign unconfirmed). Before structuring any timeline, the first step is making sure the contract is actually closed.

*Sources: 3GM Steel — AskCruz Proposal Call (Aug 2026) [wiki]; 3GM Steel — AskCruz Final Invoice + Check-ins (Oct 2026) [wiki]; 3GM Steel — AskCruz Outlook Connection / Azure AD Blocker (Sep 2026) [wiki]; 3GM Steel — IRIS Historical Data Preload (Aug 2026) [wiki]; AskCruz Sales Push to Sabre Alloys (Aug 2026) [wiki]; AskCruz Proposal Resent to Sabre + Services Agreement (Sep–Oct 2026) [wiki]; Sabre Alloys — "Sabre 2" Scope Review Call (Sep 2, 2026) [wiki]. Note: Threads-OV vault connector unavailable in this session — transcript save could not complete.*

## User (2026-10-13 09:30:21 EDT)

Ok we only take care of the aspects post proposal sign off, when we start technical. Only consider that part, take reference of all the tasks created on EOXS and 3GM board on Askcruz, understand the entire product development and go through all the log notes. And make a list of tasks we need to create for sabre with timeline for each of them, this is a heavy task, requires utmost attention, and precision. Do not half ass it. Take as much time as you need. It is the output quality i am looking for.

## Claude (2026-10-13 09:38:30 EDT)

> *Thinking:*
>

Now the full 3GM board (project 14), with stages, owners, dates, and parent links:

Now the 3GM task descriptions:

Now the log notes (chatter) on the 3GM tasks. Let me check volume first:

Substantial — 338 log notes on 3GM (~256K chars) and 912 on EOXS (~511K). I'll read them task by task. First, distribution on 3GM:

Reading the setup-phase log notes first (onboarding, approval, servers, DNS, DB structure):

Now the Outlook integration and inbox-access unblock (the biggest friction point):

Critical finding: the real root cause was a `prompt=consent` code bug, not Azure config — that's now fixed in the codebase. Next, historical ingestion + attachments:

Now the wiki pipeline (285), full historical data ingestion (580), and Linear board setup (414):

Now the Claude account/plan issues, custom instructions, logs, audit, and the redesign outcome:

3GM board fully read. Now the **existing Sabre board** (project 18) — 37 tasks already exist, so I need to know what's there before proposing anything:

Now system visibility, retrieval discrepancies, spam filtering and model-safeguard issues from EOXS:

Last reference: the AskCruz product board (project 6) — checking for anything about client templating, Sabre, or deployment playbooks:

# AskCruz for Sabre — technical implementation task list (post sign-off)

**Bottom line:** Sabre can go live in 6 weeks from kickoff, which matches the proposal's six-week plan and leaves about 6 weeks of buffer inside the contractual **90-day delivery commitment**. That only holds if three things are true:

1. **The infrastructure work 3GM did reactively is done before kickoff (Phase 0).** Most of it needs no client data, so it can start this week.
2. **The wiki backfill is resourced for 15 mailboxes, not 2.** At 3GM's real throughput, 15 mailboxes would take roughly 4 weeks of drafting on one Claude account. That alone breaks the plan.
3. **Multi-user access tiers are designed in Week 1.** 3GM never needed them. Sabre does, and EOXS's own tier bugs show how easily this goes wrong.

The current Sabre board (37 tasks) is mostly a copy of 3GM's task names. It has no sequencing and no dates, contains one duplicate, and carries over obsolete scope. It also has no task at all for **Prompt History**, which is a priced line item in the contract.

---

## 1. What 3GM actually took (from board dates and log notes)

| Workstream | 3GM actual | Sabre target |
|---|---|---|
| Signature → onboarding email | Aug 20 → Aug 26 (needed approval round) | Pre-drafted, sent D1 |
| Servers / DNS / DB | Aug 31–Sep 1. Later found: schema never applied, no certbot, Nginx misrouted, box OOM'd at 458 MB RAM | Phase 0, from a runbook |
| Inbox access | One-pager Sep 1 → connected Sep 9 (8 days) | D2–D10 for 15 users |
| Raw email backfill | Sep 9–11 (~2 days, 2 mailboxes) | D4–D12 |
| Attachment extraction fixes + 2 QA rounds | Sep 11–24 | D11–D15 (fixes already in code) |
| Wiki taxonomy + backfill | Sep 14 → drafting done Sep 24; reject backlog cleared Oct 9 | D6–D27 |
| Query QA | Sep 23 → Oct 5, ~500 queries, 3 rounds | D16–D25 |
| Monitoring / logging | Sep 30 → Oct 12 (built after handoff) | Phase 0 |
| Client walkthrough | Oct 1 (~6 weeks after signature, 2 users) | Go-live D30, 15 users |

*D = business days from kickoff (D1 = kickoff call).*

---

## 2. Lessons from the log notes that change the plan

**1. The inbox-access blocker was our bug, and it is fixed.** Over 8 days the team chased Azure "Assignment required", Conditional Access, and Edge-vs-Chrome. Nidhi's Sep 9 root cause was in our own code: `prompt=consent` forced a consent screen that non-admin users cannot pass. It is now `prompt=select_account`, committed. The remaining risk for Sabre is admin availability, so book a 30-minute call with their M365 admin instead of working it over email.

**2. Servers were built fast and missed steps.**
- The schema was never applied to production.
- Systemd units, certbot, and `postgresql-client` were not installed.
- Tesseract was missing, which silently broke image OCR.
- The 458 MB droplet was OOM-killed on the first real sync.
- Open security items were left: root SSH (S-3, left open on purpose), no verified backup or restore, and the Flask dev server running in production.
- Migrations 0011–0012 reached production only, so staging and production schemas drifted.

**3. Claude quota was the real bottleneck, not compute.**
- 20 of 44 backfill cycles hit the usage ceiling.
- Runs died silently whenever a terminal session closed, because nothing supervised them.
- The dedicated $100 pipeline account was lost to identity verification. The refund was denied and the account was deleted.

**4. Multi-user access is new territory.** 3GM's taxonomy explicitly chose "one access tier, nothing withheld" for its two execs. On EOXS:
- The tier classifier ran with `max_tokens=8`. That truncated `TIER2_CONFIDENTIAL_HR` to plain "confidential", so HR content was visible to the internal team for a month.
- OAuth QA later found 557 leave/health emails visible to the intern tier.
- Sabre has 15 users and sensitive content, including the Sep 2026 security-incident legal package and partner-level financials.

**5. Byte budgeting is now billable.**
- 3GM used one shared 3 GB cap across both mailboxes. Sabre's contract is 3 GB **per user**, with a per-GB excess charge.
- 3GM has an unresolved measurement discrepancy: the budget counts raw base64 at fetch time, while the logs count stored bytea.
- Michael explicitly asked what is measured.

**6. A third of QA "failures" were test design.** Testers graded against stale answer keys. Their `qa_travis` / `qa_stefan` tokens were never added to Nginx, so they had no user identity. Some follow-up questions ran without their setup question.

**7. Don't build a separate staging environment that runs its own ingestion.** 3GM ran duplicate ingestion, duplicate AI drafting, and duplicate Linear boards. The redesign (#485) concluded:
- Staging should be decommissioned.
- A read-only mirror plus local sandboxes replaces it.
- The reason is that the AI writes non-identical content even from identical input, so two pipelines can never match.

**8. The contract has a clock.** The 90-day commitment is extended by client-caused delays ("late access to email accounts, or key staff"). That only protects us if every client ask is logged with the date it was requested and the date it was received.

---

## 3. Current Sabre board: keep, rewrite, or close

| Existing task | Action | Reason |
|---|---|---|
| #671, #708, #702 (staging server, staging DB, redesign) | **Close** | Adopt the #485 target architecture from day one. Replaced by S-39, after go-live. |
| #691 | **Close** | Exact duplicate of #706. |
| #688 Real-time email plugin | **Close** | The 60 s Graph poll plus the 6 h wiki pipeline already covers this. 3GM never built it. |
| #681, #682, #683, #685, #687 | **Merge** | Into S-27, S-19, S-26, and S-17. |
| #699 Outlook integration | **Rewrite** | The description wrongly describes a Gmail/Zoho approval-link flow. This is clone-and-configure plus a per-mailbox budget change, not a build. |
| #712 ERP skill file | **Rewrite** | The description is 3GM's *completion* note pasted in ("verified 16 module files"). Nothing has been done for Sabre. |
| #703 Email approval file | **Rewrite** | References the Gmail version, which was obsolete at 3GM within a day. |
| #692 Requirements section | **Move to change order** | Not in the scope of the signed proposal (Section 03). |
| #689 SOP ingestion | **Hold** | Tabled at 3GM. Michael asked whether "assistants from training materials" are included. Follow SSA Section 2. |
| All others | **Keep** | Re-scoped and dated below. |

---

## 4. The task list

### Phase 0 — Readiness (internal, start now, done by D0, ~5–7 business days)

Owners are suggested, mapped to the 3GM roles.

| Task | When | Owner | Done when |
|---|---|---|---|
| **S-01** Fork the 3GM repo into a parameterized Sabre repo (#690) | P0, 3d | Nidhi | All 3GM fixes are carried over (see list below). The shared 3 GB cap is replaced by a per-mailbox budget, with one byte-measurement definition matching the SSA. A migration tracker exists (master list plus a per-DB applied record). A deploy runbook is written. |
| **S-02** Production server, managed Postgres, DNS/TLS (#709, #704, #697) | P0, 3d, after S-01 starts | Nidhi | Sized for 15 mailboxes: ≥4 vCPU, 8 GB plus swap (the guard needs 1.9 GB free; 8 workers × ~500 MB). Disk sized for up to 45 GB raw. DB connection headroom (3GM's guard failed against 25 connections). `sabre.askcruz.com` live. Gunicorn, not the Flask dev server. Systemd with `Restart=always`. All migrations applied and recorded. OCR, LibreOffice, and Whisper installed. End-to-end smoke test passes with a test mailbox. |
| **S-03** Security and backup gate (#684) | P0, 2d | Nidhi, reviewed by Ayan | Root SSH off, UFW on, Flask bound to loopback, no secrets in URLs or `ps` output, least-privilege DB roles. Backup **and a test restore** verified. EOXS staff access is logged (#526). **Hard gate: no Sabre mailbox connects before this passes.** |
| **S-04** Entra app registration | P0, 0.5d | Nidhi | "Cruz – Sabre Outlook Ingestion" registered: Mail.Read + User.Read delegated, multitenant. Redirect URI registered (avoids AADSTS50011). `prompt=select_account` verified in code. |
| **S-05** Pipeline Claude capacity (#694) | Now → D0 | Ayan / Sheenam | At least 2 dedicated accounts, **identity-verified before kickoff**, separate from the EOXS and 3GM pipelines. Usage-limit pause and retry confirmed working. A written decision on subscription vs API key for the unattended pipeline (the 3GM log records subscription as a known risk accepted at 2-user scale). |
| **S-06** Linear team and monitoring clones (#695 + new) | P0, 2d | Nidhi / Harsh | Linear lanes and label taxonomy (including "no-activity"); webhook points at production only. Airflow DAGs cloned: mail monitoring 4×/day, system health 4×/day, MCP query monitoring daily. Alert email works (DigitalOcean blocks SMTP port 587, so use an API sender or request an unblock). |
| **S-07** IT approval and data-privacy pack (#703) | P0, 2d | Ayan / Ron | Admin one-pager: client ID, scopes, what the app does *not* do, the admin-consent URL plus manual Entra steps, the "Assignment required" note, and "use Chrome". Privacy statement: who at EOXS can see Sabre data, access logging, ZDR, the data-ownership clause. Reviewed by Raj. |
| **S-08** Onboarding pack and access-matrix template (#707) | P0, 1d | Ron | Asks Sabre for: the named point of contact (required by contract), the final 15-user roster (role, email, whether the mailbox is on Sabre's tenant), the M365 admin, the Claude plan choice, history depth, and a filled access matrix. |
| **S-09** Sabre ERP platform review and skill v0 (#711) | Now, 5d | Ron / Ayan | Head start: we already have ERP access, the "Sabre Odoo Master Reference" page, and 1,575 support threads. Covers processing and blanking orders, control and child tags, landed cost, GP and estimated margin, toll processing, and long-product UOM / weight-per-ft. Includes a landmine list drawn from the support history. |
| **S-10** Access-tier and mailbox-visibility design (new) | P0, 3d | Ayan / Jaskeerat | Options documented for decision at kickoff (see Section 6). Classifier fails closed. Per-user OAuth identity (#747 pattern). A wiki page inherits the most restrictive tier among the sources it cites. |

**3GM fixes S-01 must carry into the Sabre repo:**
- `prompt=select_account` in the OAuth connect route
- NUL-byte stripping before insert
- Two-pass OCR (72 then 144 DPI)
- DOCX table and text-box extraction, XLSX stylesheet patch, PDF magic-byte detection
- `logging.basicConfig()` in the app, so INFO logs are not dropped
- Shared fail-closed `tier_parse` module (the `max_tokens` fix)
- `decision='failed'` rows written to `wiki_ingest_seen`
- The corrected DB-connection guard (#797)
- Unique-title adoption in promote, resolver wired into both drivers, the typed logging tools

### Phase 1 — Accounts, access, integrations (Weeks 1–2, D1–D10)

| Task | When | Owner | Done when |
|---|---|---|---|
| **S-11** Kickoff call (#707) | D1 | Ron / Ayan | Roster, access matrix, admin contact, point of contact, Claude plan, and history depth confirmed in writing. |
| **S-12** Client-dependency and 90-day clock log (new) | D1 → ongoing | Ron | Every client ask logged with date requested and date received. Weekly status email to the point of contact. |
| **S-13** Admin consent call (#706, part 1) | D2–D4 | Nidhi + Ron | Tenant-wide consent granted. One user connected and a test pull succeeds. Test data purged. |
| **S-14** Mailbox connects in two waves (#706) | Wave A (partners + CFO) D4–D6; Wave B (sales) D6–D10 | Ron (chasing), Nidhi | 15 accounts connected with refresh tokens. Links reissued on expiry (they are valid for 5 days). Failures documented with screenshots. |
| **S-15** Mailbox volume census (new) | Runs on each connect; report D10 | Nidhi | Per-mailbox counts and size, projected coverage within 3 GB, projected excess. Sent to Michael for written approval **before** any import beyond 3 GB. |
| **S-16** Raw backfill and attachments (#710, #714) | D4–D12, per mailbox as it connects | Nidhi | Per-mailbox cap and SSA date floor honored. Newest-first, resume points saved, per-message error isolation. Extraction yield reported (3GM reached 66%, with 0 truncated files). |
| **S-17** Claude Team org and 15 seats (new; absorbs #687) | D2–D10 | Jaskeerat / Priyanshu | Client-paid org created. Org-level read-only connectors for Sabre Vault and Sabre ERP. One compiled navigator skill. The 3GM onboarding video fixed per Ayan's three review notes, then sent. |
| **S-18** ERP MCP hardening (#698) | D1–D8 | Jaskeerat / Nidhi | Per-user auth (the 3GM ERP MCP had no bearer auth). Read-only confirmed. Field exposure set per tier (GP, accounting). Michael's "one shared connection or one per user?" question answered in writing. |
| **S-19** ERP navigator skill v1 (#712; absorbs #682, #683) | D3–D10 | Ayan | 150-question pilot answered against the live DB. Guardrails for UOM, join fan-out, and the "data went stale" fabrication seen at 3GM. Vault-vs-ERP routing included (vault = why and with whom; ERP = what happened). |
| **S-20** Access tiers built (from S-10) | D3–D10 | Jaskeerat / Nidhi | Tier assigned on insert, failing closed. Mailbox scoping enforced in the query MCP. Leakage QA run across every identity. |
| **S-21** Sabre wiki taxonomy (new) | D6–D10 | Nidhi / Ayan | Built from a survey of the Wave A corpus. Entity classes (customers, mills and vendors, toll-processing customers, carriers, related parties). Inclusion, materiality, and identity-merge rules. Sensitivity mapped to tiers, not just labels. Coverage-boundary statement. |

**Milestone M1 (end of Week 2):** all mailboxes connected, or the delay is logged as client-caused. ERP live with auth. Seats configured. Raw email searchable.

### Phase 2 — Ingest, summarize, populate, test (Weeks 3–4, D11–D20, spilling to D27)

| Task | When | Owner | Done when |
|---|---|---|---|
| **S-22** Wiki backfill (#701) | D11–D25, Wave A first | Nidhi | 0 unseen messages. Runs as a supervised systemd service. Daily month-by-month coverage card. |
| **S-23** Noise pre-filter (new, efficiency) | D8–D11 | Nidhi | 144 of 3GM's first 275 decisions were noise, yet each still cost a drafting call. Done when the measured drafting load drops and a 200-message human-checked sample shows zero false skips. |
| **S-24** Attachment QA (#686) | D11–D15 | Interns | 30 files per type sampled and fixed. |
| **S-25** Historical email logs (#705) | D13 | Nidhi | Per-mailbox counts, bytes (by the SSA definition), date ranges, skipped and failed messages. This is the evidence for the 3 GB allowance. |
| **S-26** Multi-user query MCP (#680; absorbs #685) | D11–D16 | Nidhi / Jaskeerat | OAuth sign-in and `whoami`. Wiki-first, then citations, then thread expansion, then trigram fallback. Full-text indexes. Exact email-address filter, subject conversation grouping, duplicate-page flag. Every call logged with user, tool, and latency. EOXS reviewer access is **logged** (3GM chose not to log Raj; Sabre's privacy concerns argue the other way). |
| **S-27** Steady-state pipeline (#696; absorbs #681) | Starts when S-22 reaches 0 unseen | Nidhi | New mail is raw-searchable within about a minute and in the wiki within 6 h. The monitoring sheet distinguishes "pending next run" from "failed". |
| **S-28** Persona QA bank (new) | D11–D17 | Ayan + interns | 8–10 Sabre personas: CEO, partner, fractional CFO, accounting, sales, purchasing, processing, IT. About 300 questions, including real pain points (GP, landed cost, control tags). Answer keys verified against sources and versioned. |
| **S-29** Query testing round 1 (#700) | D16–D20 | Interns | `qa_<persona>` identity tokens provisioned **first**. Each defect classified as system, skill, or test-design. |
| **S-30** Review backlog and rejected-page recovery (new) | D18–D27 | Nidhi + 1 reviewer | Rejected pages reduced to a handful. Client-clarifying questions documented. (3GM's reject rate was about 40%.) |

### Phase 3 — Prompt History, go-live, hand-off (Weeks 5–6, D21–D30)

| Task | When | Owner | Done when |
|---|---|---|---|
| **S-31** Prompt History database (new; contract line) | Build D14–D24; connect D25 | Jaskeerat / Harsh | Reuses Threads-OV capture, identity taken from the sign-in token (#747), and MCP query logs (#765). Every prompt and response is captured per user and searchable. Management view, retention, and export per SSA Sections 2 and 6. Confirm whether Sabre bought it, since Michael asked if it is optional. |
| **S-32** Custom instructions by role (#693, expanded) | D21–D23 | Nidhi | Four role templates plus a per-user identity line. Derived from the Travis/Stefan instructions. QA'd. |
| **S-33** Query testing round 2 on real identities (#700) | D21–D25 | Interns | All fixes from round 1 verified. |
| **S-34** Client UAT | D24–D28 | Ron | Point of contact plus 2 power users test against each line of proposal Section 03. Evidence pack assembled. |
| **S-35** Go-live and role-based training | D27–D30 | Ron / Ayan | 3–4 recorded sessions. Quick reference covering "how to ask" and "how to check sources". |
| **S-36** Acceptance sign-off and hand-off pack | D30 | Ron | Signed acceptance per line item, which also starts the monthly subscription. |
| **S-37** Training materials (#679) | Recurring | Ayan | — |

### Phase 4 — Hypercare and after go-live (Weeks 7–10)

- **S-38 Weekly check-ins (4 weeks).** Book them at go-live; at 3GM it took three emails and 10 days just to fix the slot. Review usage from the query logs.
- **S-39 Read-only mirror and dev sandboxes.** Non-blocking; replaces the closed staging tasks.
- **S-40 Change-order backlog.** Requirements section (#692), SOP and training-material ingestion (#689), and Michael's automation list. Each is quoted at the hourly rate and needs written approval first.

---

## 5. Critical path, calendar, and backfill capacity

**Critical path:** S-03 → S-13 → S-14 → S-16 → S-22 → S-30 → S-34 → S-36.

**Example calendar if kickoff is Monday Oct 19:**

| Milestone | Business day | Date |
|---|---|---|
| M1 (accounts, access, integrations) | D10 | Oct 30 |
| Backfill and first QA round complete | D20 | Nov 13 |
| Go-live and training week | D26–D30 | Nov 30–Dec 4 |
| 90-day contractual backstop | — | Jan 17, 2027 |

- Thanksgiving (Nov 26–27) falls in Week 6, so go-live slides one week to Nov 30–Dec 4.
- Avoid letting slippage run into Dec 21–Jan 1, when client availability drops.

**Why the backfill needs extra capacity:**
- 3GM drafted 21,599 messages in 7.7 days of wall-clock time, about 2,800 messages a day, with quota pauses.
- Assume Sabre's 15 mailboxes average half of a 3GM exec's volume. That is roughly 80k messages before cross-mailbox de-duplication. This is an assumption; S-15 replaces it with real numbers by D10.
- On one account, that is about 4 weeks of drafting and misses the plan.
- With two or more accounts (S-05) and the noise pre-filter (S-23), it is roughly 1.5–2 weeks, which fits D11–D25.
- Raw email is fully searchable as soon as it lands. 3GM was 100% raw-queryable while only 57% of the curated layer existed, so users get value before the wiki finishes.

---

## 6. Decisions needed at or before kickoff

1. **Mailbox visibility.** Does each user see only their own mail, or do partners see everyone's?
2. **Tier set.** What counts as partner-confidential (legal, security incident, financials, payroll), and who holds that tier.
3. **ERP exposure per tier.** For example, whether sales staff can see GP, margins, and accounting.
4. **Roster.** Which users have mailboxes on Sabre's tenant. The board lists Juan Deshon (fractional CFO) and David Underwood. Juan may sit on an external domain. David is also tied to the 2026 settlement matter, so his tier needs an explicit decision.
5. **Import terms.** History depth and the byte-measurement definition, per the SSA.
6. **Pipeline capacity.** Subscription accounts or an API key (S-05).
7. **Prompt History.** Whether it was purchased, and what management can see.
8. **Staging architecture.** Formally adopt the #485 mirror-plus-sandbox model. It is still marked Tabled, so Ayan needs to sign off.

One check before kickoff: #800 shows the SSA as sent through DocuSign, but no signature is on record yet. Confirm it is signed before D1.

*Sources: teams-askcruz boards — Customer 2 - 3GM (44 tasks, all 338 log notes read), Customer 1 - EOXS (task list plus access, tier, OAuth, retrieval, and onboarding notes), AskCruz product board (#526, #552, #717, #718, #790, #800), Customer 3 - Sabre Alloys (37 tasks); AskCruz email 70584 and the revised Oct 9 proposal (90-day terms). The Threads-OV save tool still isn't available in this session, so this transcript wasn't archived.*

I can turn this into a Claude Doc or an Odoo-importable task sheet if that would help with setting up the board.
