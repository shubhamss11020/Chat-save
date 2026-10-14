---
conversation_id: 5cc933b2-b2dd-424b-b286-3f9fd9a5ae21
platform: claude
username: "unknown"
title: "Information about askcruz - Claude"
created_at: "2026-10-14 09:05:43 EDT"
updated_at: "2026-10-14 09:06:32 EDT"
---

# Information about askcruz - Claude

## User (2026-10-14 09:06:32 EDT)

give me all the information you know about askcruz

## Claude (2026-10-14 09:06:32 EDT)

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
