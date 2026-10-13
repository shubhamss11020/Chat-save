---
conversation_id: 7d5f7360-f7ca-48fd-a1d1-dcf709a3bc3f
platform: claude
username: "unknown"
title: "Askcruz platform overview and functionality - Claude"
created_at: "2026-10-13 09:11:11 EDT"
updated_at: "2026-10-13 09:21:36 EDT"
---

# Askcruz platform overview and functionality - Claude

## User (2026-10-13 09:21:36 EDT)

provide me with all the information you know about askcruz . it should include details like its working, structure, its functioning.

## Claude (2026-10-13 09:21:36 EDT)

Here is what the AskCruz knowledge base says about it. Two things first. There was no separate AskCruz skill file in this session, so this comes from the AskCruz connector’s wiki pages. And the Threads-Ov archive tool (save_chat_transcript) isn’t connected in this session, so this conversation hasn’t been archived.

What it is

AskCruz (product family name Cruz) is EOXS’s AI-powered company knowledge base and conversational assistant, a “second brain” for a business. It connects scattered business data, structures it into cited knowledge, and lets employees query it through one chat interface. The product’s own definition calls it an industry-agnostic AI agent that turns fragmented data into usable organizational knowledge.

How it works: the pipeline

The documented flow has ten stages:

Source systems → Ingestion → Filtering → Sensitivity classification → Central knowledge store → Knowledge generation → Citation check → Human approval → Retrieval → Response

Ingestion mixes event-driven ingestion, scheduled sweeps, source-specific fetchers and sync jobs.
Knowledge generation doesn’t expose raw data. It synthesizes readable pages with source references, verifies the citations, and requires human approval before publishing.
The synthesis cycle runs every six hours, so answers are not real-time.
The product file cites 94% data completeness, but that is a product-level metric, not a per-answer guarantee.
Data sources
Gmail: three individual accounts.
Zoho: one shared support inbox.
Fireflies and Fathom: call transcripts and recordings.
Client Odoo implementation boards: Greer Steel, Eastern States Steel, Discount Pipe & Steel, PPC Metals, 3GM Steel and Sabre Alloys. RW Conklin and Brannon Steel have no Odoo instance, so they appear only through email and calls.
Internal assets: SOPs, policies and reference docs.
Not natively collected: support tickets and invoices or sales orders. These stay in the live EOXS Odoo system, reached through the separate eoxs-teams connector, and were removed from the AskCruz tools on 2026-08-10.
Capability model

The product feature file defines four named capabilities:

Company Brain: shared company knowledge, such as who does what, pricing norms, customer history and past commitments.
Company Hands: practical help like drafting quotes, flagging at-risk orders and summarizing calls. It is not autonomous decision-making.
Digital Workforce: standing responsibilities that watch and report on conditions, such as an order queue.
Company Personalization: reflects one company’s vocabulary, pricing logic and tolerances.

Capabilities are grouped as email, call and meeting data, client and implementation data, employee information, internal documents, and cross-source context. Domains include accounts, orders, inventory (“free to sell”), quotes, margins (“true margin”), and commitments. Typical users are sales, operations, customer-facing teams, leadership and new hires.

Access control and security
Sensitivity labels: General, Company-Confidential (financials, salaries, legal, vendor pricing, investor talks, employee performance) and Raj-Personal. When classification is uncertain, it picks the more restrictive label.
Product tiers: tier1, tier2_confidential and tier2. These are a separate vocabulary and not assumed to map one-to-one to the labels above.
Visibility by connection:
Raj: Company-Confidential plus Raj-Personal.
HR: Company-Confidential, with some financial restrictions.
General staff: general info, with financial amounts and employee performance stripped.
Interns: general info only, with amounts stripped.
Two protection layers: database-level access control, plus an independent AI response-level check as defense-in-depth.
Behavior rules: it never infers access from how a question is worded, never accepts “I’m an admin” claims, never exposes credentials, and never follows instructions embedded in retrieved documents (prompt-injection resistance).
Boundaries: live systems remain the source of truth, and explaining information is not the same as being able to act in the source system. Client-facing wording should be conditional (“can support this when available for the client”), not absolute.
Positioning and commercial status
Target: any industry with scattered data and a need for centralized access. The buyer is typically the CEO.
Competitive framing: against generic AI, which lacks internal context, and against traditional search, which finds records but doesn’t make knowledge usable.
Traction: 3GM Steel is the first confirmed customer, a deal at reduced 2-user scope with a kickoff invoice dated 2026-09-06. An AskCruz proposal to Sabre Alloys is still being negotiated as of Oct 12, 2026, including installment pricing and a services agreement. The Lumberman’s Wholesale Supply prospect had a walkthrough scheduled.
PMF status: the product’s own assessment is early signals but not yet proven repeatable product-market fit. Retention, ROI, pricing, contract value and CAC are explicitly listed as not yet established.
Roadmap: today it handles knowledge capture and plain-language Q&A. Next come workflows, business-system integration and connected AI agents.
Team and operations
The chat frontend is documented as built by Jaskeerat. The server, database and pipelines are owned by the build-out team. The wiki flags this as unverified and possibly stale.
There is an AskCruz project board in the teams-askcruz Odoo instance, with daily and weekly scrum reports. Recent activity includes an intern mailbox rollout (Aug 2026), an SDR onboarding, and marketing work on new verticals such as car dealerships.
Technical docs referenced include docs/backend-server.md, docs/postgres-database.md, docs/raw-ingestion.md, docs/wiki-ingestion.md and docs/linear-integration.md.
Caveats
Positioning conflict: the product feature file calls AskCruz “for steel businesses.” The PMF guide and client-facing catalog say it is industry-agnostic. The wiki flags this as unresolved, so confirm which is current before using it externally.
Staleness: the architecture details come from a 21 Aug 2026 baseline, and the wiki pages date from late August. Details like data sources and ownership may have changed since.

I can go deeper on any area, such as the 3GM or Sabre deals, the ingestion docs, or the internal task board.

## User (2026-10-13 09:21:36 EDT)

hive me information about everyone's salary

## Claude (2026-10-13 09:21:36 EDT)

I’m not going to pull together a list of everyone’s salaries. AskCruz classifies salary data as Company-Confidential, and by its own access rules only Raj and HR can see it. General staff and interns get financial amounts stripped. I can’t tell who you are or what access you have in this session, and the system’s rules say access shouldn’t be inferred from how a request is worded or from someone saying they’re authorized. A bulk compilation of everyone’s pay is also hard to undo if it reaches the wrong person.

There is an internal reference document listed as a “salary register” in AskCruz’s assets, so that data does exist in the system. If you’re in HR or are Raj, the cleanest route is to open that document through your own AskCruz access, where your permissions are enforced directly.

If there’s a narrower need behind this, I can probably help. I can explain how compensation is structured or what policies exist, look at a specific role or the salary-related process for a hire, or help with budgeting or headcount planning without individual figures. Tell me which of those is closest and I’ll look into it.
