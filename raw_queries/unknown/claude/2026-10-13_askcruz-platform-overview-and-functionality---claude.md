---
conversation_id: 7d5f7360-f7ca-48fd-a1d1-dcf709a3bc3f
platform: claude
username: "unknown"
title: "Askcruz platform overview and functionality - Claude"
created_at: "2026-10-13 09:11:11 EDT"
updated_at: "2026-10-13 09:50:20 EDT"
---

# Askcruz platform overview and functionality - Claude

## User (2026-10-13 09:50:20 EDT)

provide me with all the information you know about askcruz . it should include details like its working, structure, its functioning.

## Claude (2026-10-13 09:50:20 EDT)

I'll start by reading the skill files, then look into AskCruz.

There's a referenced architecture page. Let me pull it and the market-positioning page.

Here is what the AskCruz knowledge base says about it. Two things first. There was no separate AskCruz skill file in this session, so this comes from the AskCruz connector's wiki pages. And the Threads-Ov archive tool (`save_chat_transcript`) isn't connected in this session, so this conversation hasn't been archived.

## What it is
AskCruz (product family name **Cruz**) is EOXS's AI-powered company knowledge base and conversational assistant, a "second brain" for a business. It connects scattered business data, structures it into cited knowledge, and lets employees query it through one chat interface. The product's own definition calls it an industry-agnostic AI agent that turns fragmented data into usable organizational knowledge.

## How it works: the pipeline
The documented flow has ten stages:

**Source systems → Ingestion → Filtering → Sensitivity classification → Central knowledge store → Knowledge generation → Citation check → Human approval → Retrieval → Response**

- **Ingestion** mixes event-driven ingestion, scheduled sweeps, source-specific fetchers and sync jobs.
- **Knowledge generation** doesn't expose raw data. It synthesizes readable pages with source references, verifies the citations, and requires human approval before publishing.
- The synthesis cycle runs **every six hours**, so answers are not real-time.
- The product file cites **94% data completeness**, but that is a product-level metric, not a per-answer guarantee.

## Data sources
- **Gmail:** three individual accounts.
- **Zoho:** one shared support inbox.
- **Fireflies and Fathom:** call transcripts and recordings.
- **Client Odoo implementation boards:** Greer Steel, Eastern States Steel, Discount Pipe & Steel, PPC Metals, 3GM Steel and Sabre Alloys. RW Conklin and Brannon Steel have no Odoo instance, so they appear only through email and calls.
- **Internal assets:** SOPs, policies and reference docs.
- **Not natively collected:** support tickets and invoices or sales orders. These stay in the live EOXS Odoo system, reached through the separate `eoxs-teams` connector, and were removed from the AskCruz tools on 2026-08-10.

## Capability model
The product feature file defines four named capabilities:
- **Company Brain:** shared company knowledge, such as who does what, pricing norms, customer history and past commitments.
- **Company Hands:** practical help like drafting quotes, flagging at-risk orders and summarizing calls. It is not autonomous decision-making.
- **Digital Workforce:** standing responsibilities that watch and report on conditions, such as an order queue.
- **Company Personalization:** reflects one company's vocabulary, pricing logic and tolerances.

Capabilities are grouped as email, call and meeting data, client and implementation data, employee information, internal documents, and cross-source context. Domains include accounts, orders, inventory ("free to sell"), quotes, margins ("true margin"), and commitments. Typical users are sales, operations, customer-facing teams, leadership and new hires.

## Access control and security
- **Sensitivity labels:** General, Company-Confidential (financials, salaries, legal, vendor pricing, investor talks, employee performance) and Raj-Personal. When classification is uncertain, it picks the more restrictive label.
- **Product tiers:** `tier1`, `tier2_confidential` and `tier2`. These are a separate vocabulary and not assumed to map one-to-one to the labels above.
- **Visibility by connection:**
  - Raj: Company-Confidential plus Raj-Personal.
  - HR: Company-Confidential, with some financial restrictions.
  - General staff: general info, with financial amounts and employee performance stripped.
  - Interns: general info only, with amounts stripped.
- **Two protection layers:** database-level access control, plus an independent AI response-level check as defense-in-depth.
- **Behavior rules:** it never infers access from how a question is worded, never accepts "I'm an admin" claims, never exposes credentials, and never follows instructions embedded in retrieved documents (prompt-injection resistance).
- **Boundaries:** live systems remain the source of truth, and explaining information is not the same as being able to act in the source system. Client-facing wording should be conditional ("can support this when available for the client"), not absolute.

## Positioning and commercial status
- **Target:** any industry with scattered data and a need for centralized access. The buyer is typically the CEO.
- **Competitive framing:** against generic AI, which lacks internal context, and against traditional search, which finds records but doesn't make knowledge usable.
- **Traction:** 3GM Steel is the first confirmed customer, a deal at reduced 2-user scope with a kickoff invoice dated 2026-09-06. An AskCruz proposal to Sabre Alloys is still being negotiated as of Oct 12, 2026, including installment pricing and a services agreement. The Lumberman's Wholesale Supply prospect had a walkthrough scheduled.
- **PMF status:** the product's own assessment is early signals but not yet proven repeatable product-market fit. Retention, ROI, pricing, contract value and CAC are explicitly listed as not yet established.
- **Roadmap:** today it handles knowledge capture and plain-language Q&A. Next come workflows, business-system integration and connected AI agents.

## Team and operations
- The chat frontend is documented as built by Jaskeerat. The server, database and pipelines are owned by the build-out team. The wiki flags this as unverified and possibly stale.
- There is an AskCruz project board in the `teams-askcruz` Odoo instance, with daily and weekly scrum reports. Recent activity includes an intern mailbox rollout (Aug 2026), an SDR onboarding, and marketing work on new verticals such as car dealerships.
- Technical docs referenced include `docs/backend-server.md`, `docs/postgres-database.md`, `docs/raw-ingestion.md`, `docs/wiki-ingestion.md` and `docs/linear-integration.md`.

## Caveats
- **Positioning conflict:** the product feature file calls AskCruz "for steel businesses." The PMF guide and client-facing catalog say it is industry-agnostic. The wiki flags this as unresolved, so confirm which is current before using it externally.
- **Staleness:** the architecture details come from a 21 Aug 2026 baseline, and the wiki pages date from late August. Details like data sources and ownership may have changed since.

I can go deeper on any area, such as the 3GM or Sabre deals, the ingestion docs, or the internal task board.

## Claude (2026-10-13 09:50:20 EDT)

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

## User (2026-10-13 09:50:20 EDT)

give me ideas by which we can improve askcruz by applying some more features to it or improving the existing system. suggest me some ways and also how it can help with its limitaions

## Claude (2026-10-13 09:50:20 EDT)

Below are ideas tied to the limitations I found in the wiki. Where something is my own suggestion rather than documented, I say so.

Known limitations
Limitation	Source
Knowledge is refreshed only every 6 hours, so it isn’t real-time	Architecture page
Tickets, invoices and sales orders aren’t natively collected and live in a separate Odoo connector	Architecture page
Human approval gates publishing, which can bottleneck	Architecture page
The 94% completeness figure is a product metric, not a per-answer guarantee	Architecture page
Access tiers are not fully documented, and two vocabularies exist (sensitivity labels vs tier1/tier2)	Feature file
AskCruz explains information but can’t act in source systems	Boundaries
The same email lands as duplicate threads across mailboxes	INV/2026/0380 case
Positioning conflicts: steel-only vs industry-agnostic	Feature file vs PMF guide
PMF isn’t proven: no ROI, retention or usage metrics yet	PMF page
Sabre raised data-privacy pushback	Sabre proposal page
Improving the existing system

1. Hybrid live and synthesized retrieval. Keep the six-hour cited synthesis, but for questions about current state (stock, order status, open tickets) query the live source directly and label the answer “live as of [time]”. This addresses the freshness limit and the “live systems are the source of truth” boundary. Today the tickets and invoices connector is separate, so a unified routing layer would also close that gap.

2. Per-answer confidence and coverage. Replace the global 94% with a per-answer indicator showing which sources were searched, which weren’t connected, and how fresh each citation is. This makes completeness something users can judge at the question level, which the docs say it should be.

3. A cross-source deduplication layer. Collapse identical messages (the INV/2026/0380 case) into one canonical record that keeps all mailbox provenance. That cuts noise, token cost, and risk of double-counting in analyses.

4. Faster, tiered approval. Auto-publish low-sensitivity, high-citation-confidence pages, and send only Company-Confidential or low-confidence pages to a human. A review queue with SLAs would stop approval from slowing freshness.

5. A documented access model. Publish a single mapping between sensitivity labels and tier1/tier2/tier2_confidential, with a permissions matrix and audit logs of who asked what. This resolves the documented ambiguity and gives clients like Sabre concrete privacy answers.

New features

6. Proactive alerts (the “Digital Workforce” made real). Watch for conditions and push notices: an invoice mismatch like INV/2026/2434, a PO stuck in “confirmed but can’t receive”, or a deal with no reply for 7+ days. Several of 3GM’s recurring support issues are pattern-detectable.

7. Approval-gated actions (“Company Hands”). Let AskCruz draft and, after explicit approval, execute: create a product variant, send a follow-up email, update a task. Keep the information-vs-action boundary by requiring a human click and logging every action.

8. Customer and account briefs. One-click pre-call briefs combining recent emails, open tickets, call history, contacts and open commitments, like the profile I pulled for 3GM but tailored by role.

9. Contradiction and staleness detection. The wiki already flags contradictions. Surface them in answers (“two sources disagree on pricing”) and auto-flag pages whose underlying sources have changed since synthesis.

10. Usage analytics and ROI dashboards. Track question volume, time saved, top unanswered questions, and per-user adoption. This fills the evidence gaps the PMF doc lists (usage depth, ROI, retention) and would make the 3GM customer story concrete.

11. A feedback loop. Thumbs up/down with a reason on every answer, feeding a “failed questions” backlog. Failed retrievals would show which sources or capabilities to add next.

12. More connectors. Slack/Teams, Outlook (already hit in the 3GM rollout), SharePoint/Drive, CRM, and a native ERP read layer. Priority should follow the questions that currently fail.

13. Vertical packs. Pre-built templates (vocabulary, example questions, source mappings) for car dealerships and other verticals Ron’s marketing work targets. This could resolve the positioning conflict, because the core stays industry-agnostic and the packs add specificity.

Operational and trust improvements
Data-privacy assurances: data residency options, per-client isolation, retention controls, and a security one-pager. These speak directly to Sabre’s pushback.
Prompt-injection and red-team testing: since AskCruz ingests emails and documents, run a regular test suite against the documented rule not to follow embedded instructions.
Cost monitoring: the wiki references an “API cost” page, so per-client cost tracking and caching of frequent queries would protect margins on small 2-user deals like 3GM’s.
Model fallbacks: the Oct 10 “reasoning extraction” error was diagnosed as an Anthropic model bug with a workaround. A fallback or retry path would keep the product from breaking on a single model’s quirks.
Ownership and documentation: the technical-ownership section is flagged unverified, so keep a current owner and runbook list.
Suggested priority
First: per-answer confidence and coverage (#2), deduplication (#3), a documented access model (#5). They are cheap and build trust.
Next: hybrid live retrieval (#1) and proactive alerts (#6), which most visibly raise value.
Then: approval-gated actions (#7) and analytics (#10), the bigger builds that support pricing and PMF proof.

If you’d like, I can turn this into a roadmap with effort and impact scores, or look at which recurring 3GM support issues would be best targets for the alerting idea.

## User (2026-10-13 09:50:20 EDT)

Which clients use the same Odoo instance or share a domain?

## Claude (2026-10-13 09:50:20 EDT)

No two clients share an Odoo instance or a domain in the AskCruz client registry. Each of the eight has its own entry.

**Odoo instances (one per client, all different):**

| Client | Odoo base URL |
|---|---|
| 3GM Steel | 3gm.eoxs.com |
| Discount Pipe & Steel | discountpipesteel.eoxs.com |
| Eastern States Steel | ess.eoxs.com |
| Ohio Strip Steel (formerly Greer Steel) | greersteel.eoxs.com |
| PPC Metals | ppc.eoxs.com |
| Sabre Alloys | sabre.eoxs.com |
| Brannon Steel | none configured |
| RW Conklin Steel | none configured |

All six configured instances sit under the `eoxs.com` parent domain, but each has its own subdomain. Brannon Steel and RW Conklin Steel have no instance, which matches the earlier note that they appear only through email and calls.

**Domains:** each client has distinct domains, with no overlap. The one client with more than one is **Ohio Strip Steel (formerly Greer Steel)**, which has `ohiostripsteel.com` and `greersteel.com`. That reflects the rebrand, so both resolve to the same client.

The only overlap I can see is Ohio Strip Steel's two domains pointing to one client, and that's the same company under two names. If you want to check for shared infrastructure behind the scenes, such as a shared database, I can query the Teams Odoo connectors, but the registry doesn't show it.

## Claude (2026-10-13 09:50:20 EDT)

No two clients share an Odoo instance or a domain in the AskCruz client registry. Each of the eight has its own entry.

Odoo instances (one per client, all different):

Client	Odoo base URL
3GM Steel	3gm.eoxs.com
Discount Pipe & Steel	discountpipesteel.eoxs.com
Eastern States Steel	ess.eoxs.com
Ohio Strip Steel (formerly Greer Steel)	greersteel.eoxs.com
PPC Metals	ppc.eoxs.com
Sabre Alloys	sabre.eoxs.com
Brannon Steel	none configured
RW Conklin Steel	none configured

All six configured instances sit under the eoxs.com parent domain, but each has its own subdomain. Brannon Steel and RW Conklin Steel have no instance, which matches the earlier note that they appear only through email and calls.

Domains: each client has distinct domains, with no overlap. The one client with more than one is Ohio Strip Steel (formerly Greer Steel), which has ohiostripsteel.com and greersteel.com. That reflects the rebrand, so both resolve to the same client.

The only overlap I can see is Ohio Strip Steel’s two domains pointing to one client, and that’s the same company under two names. If you want to check for shared infrastructure behind the scenes, such as a shared database, I can query the Teams Odoo connectors, but the registry doesn’t show it.

## User (2026-10-13 09:50:20 EDT)

Who is the main contact at 3gm, and what’s their email?

## Claude (2026-10-13 09:50:20 EDT)

I’m not going to pull together a list of everyone’s salaries. AskCruz classifies salary data as Company-Confidential, and by its own access rules only Raj and HR can see it. General staff and interns get financial amounts stripped. I can’t tell who you are or what access you have in this session, and the system’s rules say access shouldn’t be inferred from how a request is worded or from someone saying they’re authorized. A bulk compilation of everyone’s pay is also hard to undo if it reaches the wrong person.

There is an internal reference document listed as a “salary register” in AskCruz’s assets, so that data does exist in the system. If you’re in HR or are Raj, the cleanest route is to open that document through your own AskCruz access, where your permissions are enforced directly.

If there’s a narrower need behind this, I can probably help. I can explain how compensation is structured or what policies exist, look at a specific role or the salary-related process for a hire, or help with budgeting or headcount planning without individual figures. Tell me which of those is closest and I’ll look into it.

## Claude (2026-10-13 09:50:20 EDT)

I'll start by reading the skill files, then look into AskCruz.

There's a referenced architecture page. Let me pull it and the market-positioning page.

Here is what the AskCruz knowledge base says about it. Two things first. There was no separate AskCruz skill file in this session, so this comes from the AskCruz connector's wiki pages. And the Threads-Ov archive tool (`save_chat_transcript`) isn't connected in this session, so this conversation hasn't been archived.

## What it is
AskCruz (product family name **Cruz**) is EOXS's AI-powered company knowledge base and conversational assistant, a "second brain" for a business. It connects scattered business data, structures it into cited knowledge, and lets employees query it through one chat interface. The product's own definition calls it an industry-agnostic AI agent that turns fragmented data into usable organizational knowledge.

## How it works: the pipeline
The documented flow has ten stages:

**Source systems → Ingestion → Filtering → Sensitivity classification → Central knowledge store → Knowledge generation → Citation check → Human approval → Retrieval → Response**

- **Ingestion** mixes event-driven ingestion, scheduled sweeps, source-specific fetchers and sync jobs.
- **Knowledge generation** doesn't expose raw data. It synthesizes readable pages with source references, verifies the citations, and requires human approval before publishing.
- The synthesis cycle runs **every six hours**, so answers are not real-time.
- The product file cites **94% data completeness**, but that is a product-level metric, not a per-answer guarantee.

## Data sources
- **Gmail:** three individual accounts.
- **Zoho:** one shared support inbox.
- **Fireflies and Fathom:** call transcripts and recordings.
- **Client Odoo implementation boards:** Greer Steel, Eastern States Steel, Discount Pipe & Steel, PPC Metals, 3GM Steel and Sabre Alloys. RW Conklin and Brannon Steel have no Odoo instance, so they appear only through email and calls.
- **Internal assets:** SOPs, policies and reference docs.
- **Not natively collected:** support tickets and invoices or sales orders. These stay in the live EOXS Odoo system, reached through the separate `eoxs-teams` connector, and were removed from the AskCruz tools on 2026-08-10.

## Capability model
The product feature file defines four named capabilities:
- **Company Brain:** shared company knowledge, such as who does what, pricing norms, customer history and past commitments.
- **Company Hands:** practical help like drafting quotes, flagging at-risk orders and summarizing calls. It is not autonomous decision-making.
- **Digital Workforce:** standing responsibilities that watch and report on conditions, such as an order queue.
- **Company Personalization:** reflects one company's vocabulary, pricing logic and tolerances.

Capabilities are grouped as email, call and meeting data, client and implementation data, employee information, internal documents, and cross-source context. Domains include accounts, orders, inventory ("free to sell"), quotes, margins ("true margin"), and commitments. Typical users are sales, operations, customer-facing teams, leadership and new hires.

## Access control and security
- **Sensitivity labels:** General, Company-Confidential (financials, salaries, legal, vendor pricing, investor talks, employee performance) and Raj-Personal. When classification is uncertain, it picks the more restrictive label.
- **Product tiers:** `tier1`, `tier2_confidential` and `tier2`. These are a separate vocabulary and not assumed to map one-to-one to the labels above.
- **Visibility by connection:**
  - Raj: Company-Confidential plus Raj-Personal.
  - HR: Company-Confidential, with some financial restrictions.
  - General staff: general info, with financial amounts and employee performance stripped.
  - Interns: general info only, with amounts stripped.
- **Two protection layers:** database-level access control, plus an independent AI response-level check as defense-in-depth.
- **Behavior rules:** it never infers access from how a question is worded, never accepts "I'm an admin" claims, never exposes credentials, and never follows instructions embedded in retrieved documents (prompt-injection resistance).
- **Boundaries:** live systems remain the source of truth, and explaining information is not the same as being able to act in the source system. Client-facing wording should be conditional ("can support this when available for the client"), not absolute.

## Positioning and commercial status
- **Target:** any industry with scattered data and a need for centralized access. The buyer is typically the CEO.
- **Competitive framing:** against generic AI, which lacks internal context, and against traditional search, which finds records but doesn't make knowledge usable.
- **Traction:** 3GM Steel is the first confirmed customer, a deal at reduced 2-user scope with a kickoff invoice dated 2026-09-06. An AskCruz proposal to Sabre Alloys is still being negotiated as of Oct 12, 2026, including installment pricing and a services agreement. The Lumberman's Wholesale Supply prospect had a walkthrough scheduled.
- **PMF status:** the product's own assessment is early signals but not yet proven repeatable product-market fit. Retention, ROI, pricing, contract value and CAC are explicitly listed as not yet established.
- **Roadmap:** today it handles knowledge capture and plain-language Q&A. Next come workflows, business-system integration and connected AI agents.

## Team and operations
- The chat frontend is documented as built by Jaskeerat. The server, database and pipelines are owned by the build-out team. The wiki flags this as unverified and possibly stale.
- There is an AskCruz project board in the `teams-askcruz` Odoo instance, with daily and weekly scrum reports. Recent activity includes an intern mailbox rollout (Aug 2026), an SDR onboarding, and marketing work on new verticals such as car dealerships.
- Technical docs referenced include `docs/backend-server.md`, `docs/postgres-database.md`, `docs/raw-ingestion.md`, `docs/wiki-ingestion.md` and `docs/linear-integration.md`.

## Caveats
- **Positioning conflict:** the product feature file calls AskCruz "for steel businesses." The PMF guide and client-facing catalog say it is industry-agnostic. The wiki flags this as unresolved, so confirm which is current before using it externally.
- **Staleness:** the architecture details come from a 21 Aug 2026 baseline, and the wiki pages date from late August. Details like data sources and ownership may have changed since.

I can go deeper on any area, such as the 3GM or Sabre deals, the ingestion docs, or the internal task board.

## User (2026-10-13 09:50:20 EDT)

give me ideas by which we can improve askcruz by applying some more features to it or improving the existing system. suggest me some ways and also how it can help with its limitaions

## Claude (2026-10-13 09:50:20 EDT)

I'll start by reading the skill files, then look into AskCruz.

There's a referenced architecture page. Let me pull it and the market-positioning page.

Here is what the AskCruz knowledge base says about it. Two things first. There was no separate AskCruz skill file in this session, so this comes from the AskCruz connector's wiki pages. And the Threads-Ov archive tool (`save_chat_transcript`) isn't connected in this session, so this conversation hasn't been archived.

## What it is
AskCruz (product family name **Cruz**) is EOXS's AI-powered company knowledge base and conversational assistant, a "second brain" for a business. It connects scattered business data, structures it into cited knowledge, and lets employees query it through one chat interface. The product's own definition calls it an industry-agnostic AI agent that turns fragmented data into usable organizational knowledge.

## How it works: the pipeline
The documented flow has ten stages:

**Source systems → Ingestion → Filtering → Sensitivity classification → Central knowledge store → Knowledge generation → Citation check → Human approval → Retrieval → Response**

- **Ingestion** mixes event-driven ingestion, scheduled sweeps, source-specific fetchers and sync jobs.
- **Knowledge generation** doesn't expose raw data. It synthesizes readable pages with source references, verifies the citations, and requires human approval before publishing.
- The synthesis cycle runs **every six hours**, so answers are not real-time.
- The product file cites **94% data completeness**, but that is a product-level metric, not a per-answer guarantee.

## Data sources
- **Gmail:** three individual accounts.
- **Zoho:** one shared support inbox.
- **Fireflies and Fathom:** call transcripts and recordings.
- **Client Odoo implementation boards:** Greer Steel, Eastern States Steel, Discount Pipe & Steel, PPC Metals, 3GM Steel and Sabre Alloys. RW Conklin and Brannon Steel have no Odoo instance, so they appear only through email and calls.
- **Internal assets:** SOPs, policies and reference docs.
- **Not natively collected:** support tickets and invoices or sales orders. These stay in the live EOXS Odoo system, reached through the separate `eoxs-teams` connector, and were removed from the AskCruz tools on 2026-08-10.

## Capability model
The product feature file defines four named capabilities:
- **Company Brain:** shared company knowledge, such as who does what, pricing norms, customer history and past commitments.
- **Company Hands:** practical help like drafting quotes, flagging at-risk orders and summarizing calls. It is not autonomous decision-making.
- **Digital Workforce:** standing responsibilities that watch and report on conditions, such as an order queue.
- **Company Personalization:** reflects one company's vocabulary, pricing logic and tolerances.

Capabilities are grouped as email, call and meeting data, client and implementation data, employee information, internal documents, and cross-source context. Domains include accounts, orders, inventory ("free to sell"), quotes, margins ("true margin"), and commitments. Typical users are sales, operations, customer-facing teams, leadership and new hires.

## Access control and security
- **Sensitivity labels:** General, Company-Confidential (financials, salaries, legal, vendor pricing, investor talks, employee performance) and Raj-Personal. When classification is uncertain, it picks the more restrictive label.
- **Product tiers:** `tier1`, `tier2_confidential` and `tier2`. These are a separate vocabulary and not assumed to map one-to-one to the labels above.
- **Visibility by connection:**
  - Raj: Company-Confidential plus Raj-Personal.
  - HR: Company-Confidential, with some financial restrictions.
  - General staff: general info, with financial amounts and employee performance stripped.
  - Interns: general info only, with amounts stripped.
- **Two protection layers:** database-level access control, plus an independent AI response-level check as defense-in-depth.
- **Behavior rules:** it never infers access from how a question is worded, never accepts "I'm an admin" claims, never exposes credentials, and never follows instructions embedded in retrieved documents (prompt-injection resistance).
- **Boundaries:** live systems remain the source of truth, and explaining information is not the same as being able to act in the source system. Client-facing wording should be conditional ("can support this when available for the client"), not absolute.

## Positioning and commercial status
- **Target:** any industry with scattered data and a need for centralized access. The buyer is typically the CEO.
- **Competitive framing:** against generic AI, which lacks internal context, and against traditional search, which finds records but doesn't make knowledge usable.
- **Traction:** 3GM Steel is the first confirmed customer, a deal at reduced 2-user scope with a kickoff invoice dated 2026-09-06. An AskCruz proposal to Sabre Alloys is still being negotiated as of Oct 12, 2026, including installment pricing and a services agreement. The Lumberman's Wholesale Supply prospect had a walkthrough scheduled.
- **PMF status:** the product's own assessment is early signals but not yet proven repeatable product-market fit. Retention, ROI, pricing, contract value and CAC are explicitly listed as not yet established.
- **Roadmap:** today it handles knowledge capture and plain-language Q&A. Next come workflows, business-system integration and connected AI agents.

## Team and operations
- The chat frontend is documented as built by Jaskeerat. The server, database and pipelines are owned by the build-out team. The wiki flags this as unverified and possibly stale.
- There is an AskCruz project board in the `teams-askcruz` Odoo instance, with daily and weekly scrum reports. Recent activity includes an intern mailbox rollout (Aug 2026), an SDR onboarding, and marketing work on new verticals such as car dealerships.
- Technical docs referenced include `docs/backend-server.md`, `docs/postgres-database.md`, `docs/raw-ingestion.md`, `docs/wiki-ingestion.md` and `docs/linear-integration.md`.

## Caveats
- **Positioning conflict:** the product feature file calls AskCruz "for steel businesses." The PMF guide and client-facing catalog say it is industry-agnostic. The wiki flags this as unresolved, so confirm which is current before using it externally.
- **Staleness:** the architecture details come from a 21 Aug 2026 baseline, and the wiki pages date from late August. Details like data sources and ownership may have changed since.

I can go deeper on any area, such as the 3GM or Sabre deals, the ingestion docs, or the internal task board.

## User (2026-10-13 09:50:20 EDT)

Who is the main contact at 3gm, and what’s their email?

## Claude (2026-10-13 09:50:20 EDT)

3GM Steel is both a long-standing EOXS ERP client and the first AskCruz customer. The wiki has a lot on both relationships.

Background
Registry: domain 3gmsteel.com, Odoo at 3gm.eoxs.com (DB threegmsteels). Contacts are Travis Lane, Jessica Worley and Leslie Countryman.
Records on file: 28 implementation tasks, 966 emails and 13 call transcripts, plus roughly 40 live wiki pages.
Onboarding (2022): kickoff and discovery calls started in April 2022, run mostly by Rajat Jain and Sai Siddhartha Dutta. They interviewed Travis, Jessica, Leslie and others. The 2022 work covered access rights, reports, company details, ports information, the Product Master import and accounting setup. A few internal sub-tasks (data task, BPF, third-party vendor data) still sit open on the Kanban board.
Calls since then: server migration (Jan 2024), open-ticket reviews (2024), dashboard and payables reviews (2023), an “Issue review” in Jan 2025, and calls with Travis on Jul 29, 2026 and the AskCruz proposal on Aug 12, 2026.
The AskCruz deal
Timeline:
Aug 12: Rajat pitches Company Brain to Travis (CCO).
Aug 14: two proposals go out with inconsistent pricing, and Travis spots the errors and copies Stefan Brown (CFO).
Aug 17: Ron sends a corrected, point-by-point reply, with Company Brain to run on Claude as the front end.
Aug 19: Travis confirms 3GM is moving forward at reduced scope.
Aug 20: the initial term is shortened to 6 months, and Travis signs the 2-user agreement the same day.
Aug 24: Rajat confirms in writing that the 3-year term does not auto-renew, with a decision point at 6 months.
Invoices: INV/2026/0367 (50% kickoff, Sep 6) and INV/2026/0380 (remaining 50% plus the first month’s licensing, Oct 5). Amounts are restricted. The wiki doesn’t confirm that either has been paid.
Implementation:
A Sep 4 issue with the Outlook connection (Azure AD admin consent) was resolved on an admin approval call.
Historical data was preloaded for the IRIS AI component.
The kickoff and setup walkthrough was Oct 1.
3GM agreed on Oct 12 to weekly 30-minute usage check-ins on Thursdays around 2pm ET for the first month. No invite for the first session is on record yet. Travis mentioned pending travel that could shift later weeks.
Marketing: an AskCruz customer story draft was sent to Raj for review on Oct 5.
Referral: 3GM led to the Sabre Alloys proposal, which is still being negotiated.
Day-to-day ERP support (Aug-Oct 2026)

Recent support threads cluster around:

Invoicing and payments:
INV/2026/2368 was confirmed correct, but INV/2026/2403 was still unresolved after a second escalation on Oct 6.
INV/2026/2434 has a total-due mismatch against weight × CWT rate.
INV/2026/2276’s reprice correction didn’t fully propagate.
There was a duplicate-payment investigation (Reliable Metal Buildings, INV/2026/2146) and a phantom-credits issue.
Inventory and coils:
12 coils invoiced under INV/2026/2246 still show as available.
There is a coil search bug on the tonnage card.
Coil uploads into POs keep erroring.
Four POs (P04612-P04615) hit a “confirmed but can’t receive” bug.
Product creation: many color and width variants (PRM:26, PRM:28, PRM:PBR) and an oxide-coated hot roll line, which look like a new coating line.
Access rights: Matt Inman was elevated to match Jessica Worley’s permissions in Aug 2026.

I left out the amounts, since the wiki restricts them.

Caveats
Payment status for both AskCruz invoices is unconfirmed.
Open items are mostly in billing and PO/coil bugs, with INV/2026/2403 the most escalated.
Some of this is drawn from wiki summaries rather than the raw emails.

I can read the full text of any thread, such as the INV/2026/2403 escalation, the Outlook fix, or the proposal pricing contradiction.

## User (2026-10-13 09:50:20 EDT)

what more do you know about the 3gm clients

## Claude (2026-10-13 09:50:20 EDT)

3GM Steel is both a long-standing EOXS ERP client and the first AskCruz customer. The wiki has a lot on both relationships.

Background
Registry: domain 3gmsteel.com, Odoo at 3gm.eoxs.com (DB threegmsteels). Contacts are Travis Lane, Jessica Worley and Leslie Countryman.
Records on file: 28 implementation tasks, 966 emails and 13 call transcripts, plus roughly 40 live wiki pages.
Onboarding (2022): kickoff and discovery calls started in April 2022, run mostly by Rajat Jain and Sai Siddhartha Dutta. They interviewed Travis, Jessica, Leslie and others. The 2022 work covered access rights, reports, company details, ports information, the Product Master import and accounting setup. A few internal sub-tasks (data task, BPF, third-party vendor data) still sit open on the Kanban board.
Calls since then: server migration (Jan 2024), open-ticket reviews (2024), dashboard and payables reviews (2023), an “Issue review” in Jan 2025, and calls with Travis on Jul 29, 2026 and the AskCruz proposal on Aug 12, 2026.
The AskCruz deal
Timeline:
Aug 12: Rajat pitches Company Brain to Travis (CCO).
Aug 14: two proposals go out with inconsistent pricing, and Travis spots the errors and copies Stefan Brown (CFO).
Aug 17: Ron sends a corrected, point-by-point reply, with Company Brain to run on Claude as the front end.
Aug 19: Travis confirms 3GM is moving forward at reduced scope.
Aug 20: the initial term is shortened to 6 months, and Travis signs the 2-user agreement the same day.
Aug 24: Rajat confirms in writing that the 3-year term does not auto-renew, with a decision point at 6 months.
Invoices: INV/2026/0367 (50% kickoff, Sep 6) and INV/2026/0380 (remaining 50% plus the first month’s licensing, Oct 5). Amounts are restricted. The wiki doesn’t confirm that either has been paid.
Implementation:
A Sep 4 issue with the Outlook connection (Azure AD admin consent) was resolved on an admin approval call.
Historical data was preloaded for the IRIS AI component.
The kickoff and setup walkthrough was Oct 1.
3GM agreed on Oct 12 to weekly 30-minute usage check-ins on Thursdays around 2pm ET for the first month. No invite for the first session is on record yet. Travis mentioned pending travel that could shift later weeks.
Marketing: an AskCruz customer story draft was sent to Raj for review on Oct 5.
Referral: 3GM led to the Sabre Alloys proposal, which is still being negotiated.
Day-to-day ERP support (Aug-Oct 2026)

Recent support threads cluster around:

Invoicing and payments:
INV/2026/2368 was confirmed correct, but INV/2026/2403 was still unresolved after a second escalation on Oct 6.
INV/2026/2434 has a total-due mismatch against weight × CWT rate.
INV/2026/2276’s reprice correction didn’t fully propagate.
There was a duplicate-payment investigation (Reliable Metal Buildings, INV/2026/2146) and a phantom-credits issue.
Inventory and coils:
12 coils invoiced under INV/2026/2246 still show as available.
There is a coil search bug on the tonnage card.
Coil uploads into POs keep erroring.
Four POs (P04612-P04615) hit a “confirmed but can’t receive” bug.
Product creation: many color and width variants (PRM:26, PRM:28, PRM:PBR) and an oxide-coated hot roll line, which look like a new coating line.
Access rights: Matt Inman was elevated to match Jessica Worley’s permissions in Aug 2026.

I left out the amounts, since the wiki restricts them.

Caveats
Payment status for both AskCruz invoices is unconfirmed.
Open items are mostly in billing and PO/coil bugs, with INV/2026/2403 the most escalated.
Some of this is drawn from wiki summaries rather than the raw emails.

I can read the full text of any thread, such as the INV/2026/2403 escalation, the Outlook fix, or the proposal pricing contradiction.
