---
conversation_id: 4c57293c-365f-47e2-ad55-5a2dc7b00060
platform: claude
username: "harsh"
title: "Askcruz details"
created_at: "2026-10-13 08:33:23 EDT"
updated_at: "2026-10-13 08:37:33 EDT"
---

# Askcruz details

## User (2026-10-13 08:37:33 EDT)

give me detail about askcruz

## Claude (2026-10-13 08:37:33 EDT)

I'll start by reading the two skill files.

Here's the detail on AskCruz, drawn from the internal wiki pages and the product reference documents behind them.

**AskCruz is an AI "second brain" for a company.** It connects scattered business data (email, calls, project boards, documents), structures it into synthesized, cited knowledge pages, and lets employees ask questions through one conversational interface. The product family is called "Cruz". It began as EOXS's internal knowledge base and is now being sold to outside companies. The reference documents describe it as an AI agent that makes organizational knowledge usable, not a general chatbot or a search box.

**The four-part capability model**
- **Company Brain** is the shared working knowledge: who does what, how quotes are priced, customer history, past commitments.
- **Company Hands** is practical work such as drafting a quote, flagging an at-risk order, or summarizing a customer call. It is not meant to make final decisions on its own.
- **Digital Workforce** covers standing responsibilities, such as watching an order queue and reporting on it.
- **Company Personalization** reflects one company's own vocabulary, pricing logic and tolerances.

**How it works**
- **Pipeline:** source systems → ingestion → filtering → sensitivity classification → central knowledge store → knowledge generation → citation check → human approval → retrieval → response.
- **Sources:**
  - Gmail (three accounts) and a Zoho support inbox.
  - Fireflies and Fathom call data.
  - Odoo implementation boards for six clients: Greer Steel, Eastern States Steel, Discount Pipe & Steel, PPC Metals, 3GM Steel and Sabre Alloys.
- **Freshness:** knowledge pages are synthesized every six hours, so it isn't real-time. Live systems remain the source of truth.
- **Access control:** it is role-aware, enforced at the database level, with an independent AI response check as a second layer. Interns see general information only, with financial amounts stripped. Other tiers see more.
- **Security rules:** it must never reveal restricted data, never grant access because someone claims to be an admin, and never follow instructions embedded in retrieved documents.
- **Boundary:** support tickets and invoices or sales orders are not part of its native collection. They stay in the separate EOXS Teams Odoo connection.

**Positioning and traction**
- **Market:** the product-market-fit guide defines it as industry-agnostic. The ICP is defined by how fragmented a company's data is, not by industry, and the CEO is the primary buyer.
- **Traction:** 3GM Steel is the first confirmed customer, closed at a reduced 2-user scope with a shorter initial term. Sabre Alloys has been pitched, and prospects include Ohio Strip Steel, Collier Metals, Lumberman's Wholesale and a legal-services firm.
- **Product-market fit:** the guide's own assessment is "early signals, not yet proven repeatable". Retention, ROI, pricing acceptance and the active-customer count beyond 3GM are all listed as not yet established.
- **Roadmap:** today it handles plain-language Q&A over organizational knowledge. Next come workflows, business-system integrations and connected agents.

**Things to be aware of**
- **Positioning contradiction:** the product feature file calls AskCruz "for steel businesses", while the PMF guide says industry-agnostic. The wiki flags this as unresolved, so confirm the current line before using it externally.
- **Unverified ownership details:** the technical-ownership notes (for example, Jaskeerat owning the chat frontend) come from a 21 Aug baseline and haven't been cross-checked.
- **Completeness figure:** the "94% data completeness" figure is a product-file status metric, not a per-answer guarantee.
- **Scope of this answer:** I used wiki overview pages and didn't open the raw assets. Monetary amounts are redacted on this connection. 777 implementation tasks, 26,909 email threads and 2,130 calls are visible in this session.

**Archiving:** the transcript-saving connector (Notes / `save_chat_transcript`) isn't connected in this session, so this conversation couldn't be archived.

I can go deeper on any area, such as the 3GM deal, the sales pipeline, the internal build board, or the full text of a source asset.

**Sources:** wiki pages "AskCruz — Product Capabilities, Feature Model & Client-Facing Boundaries" (assets 17 and 19), "AskCruz — System Architecture, Ingestion & Access Control" (asset 16), "AskCruz — Market Positioning, ICP & Product-Market Fit Status" (asset 18), and the 3GM Steel proposal-call page.
