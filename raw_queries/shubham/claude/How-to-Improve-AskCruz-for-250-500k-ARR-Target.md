---
conversation_id: askcruz-improvement-strategy-oct7-2026
platform: claude
username: "shubham"
title: "How to Improve AskCruz for $250–500k ARR Target"
created_at: "2026-10-07 11:18:50 EDT"
updated_at: "2026-10-07 11:21:55 EDT"
---

# How to Improve AskCruz for $250–500k ARR Target

## User (2026-10-07 11:18:50 EDT)

what do you know about askcruz. give me all the information about that from the connectors

## Claude (2026-10-07 11:18:50 EDT)

## Here's Everything About AskCruz From the Connectors

I've pulled complete documentation on AskCruz from the system. Here's the consolidated picture:

### **Product Fundamentals**

**AskCruz is an industry-agnostic AI-powered company knowledge platform and assistant.** It's not limited to steel, manufacturing, or any single vertical—that's a critical point. EOXS is the parent company (internal pilot), and 3GM Steel is the first and currently only external client, mid-implementation. The fact that 3GM is in steel doesn't define the product's scope.

**Core problem solved:** Companies have scattered information across email, conversations, documents, systems, spreadsheets, calls, and operational tools. Employees waste time searching multiple places to reconstruct context. AskCruz centralizes that knowledge into one searchable, AI-assisted layer.

---

### **The Four Core Capabilities (Product Model)**

1. **Company Brain** — The company's shared working knowledge. Users ask business questions (Who handled this? What were we promised? What's our pricing logic?) and get answers grounded in available company context.

2. **Company Hands** — Practical work AskCruz helps execute: drafting quotes using company terms, flagging orders at risk of missing promise dates, summarizing customer calls against accounts, preparing account briefings.

3. **Digital Workforce** — Standing responsibilities that watch, follow, and report. Watch an order queue. Follow a defined exception. Report when a condition needs attention. Reduces manual checking.

4. **Company Personalization** — AskCruz reflects how a specific company actually operates: their vocabulary, pricing logic, customer expectations, operational exceptions, and practices—not generic industry assumptions.

---

### **Documented Functional Scope**

- **Customers & Accounts:** Review history, identify open threads, find commitments, understand expectations, prepare for interactions
- **Orders & Delivery:** Flag orders at risk, review exceptions, understand customer commitments, prioritize follow-up
- **Inventory & Availability:** Determine what material is genuinely "free to sell" (available after commitments/context)
- **Quotes & Pricing:** Draft quotes using company pricing logic, account for exceptions
- **Calls & Conversations:** Summarize calls, connect to account context
- **Commitments:** Identify what was promised, who promised it, surrounding context
- **Margins:** Understand customer margin, investigate why margin changed, calculate "true margin" after freight/processing
- **Operational Issues:** Identify risks, understand context, flag what needs attention

---

### **Data Sources & Architecture**

AskCruz connects to:
- Gmail (three business accounts)
- Zoho (shared support inbox)
- Fireflies (call transcripts)
- Fathom (call recordings)
- Client implementation/onboarding boards (Odoo instances)

**Critical distinction:** For EOXS specifically, support tickets and invoices/sales orders are pulled *live* from the operational Odoo system rather than ingested into the vault. This is a **configurable choice per client**, not a fixed limitation—other clients may ingest this data if live retrieval isn't reliable.

---

### **How It Works (Pipeline)**

**Sources → Ingestion → Filtering & Sensitivity Classification → Central Knowledge Store → Knowledge Generation (6-hour cycle) → Citation Verification → Human Approval → Retrieval & Response**

The knowledge-generation process is not automatic; human approval is a control step before published knowledge reaches users.

---

### **Access & Security**

Three access tiers map to information sensitivity:
- **tier1** → Raj-Personal (most restricted, personal information about Raj only)
- **tier2_confidential** → Company-Confidential (salaries, financials, legal, vendor pricing, investor conversations, employee performance)
- **tier2** → General (broad internal visibility; monetary amounts stripped for intern access)

Every user does not see the same information. Access is role and clearance aware.

---

### **Critical Boundaries (What It's NOT)**

- Not an unrestricted database browser
- Not a replacement for formal authorization
- Not real-time necessarily (ingestion cycles vary; knowledge synthesis runs every 6 hours)
- Not a guarantor of correctness—freshness, evidence quality, access, and conflicting information still matter
- Not autonomous in making final commercial/operational decisions
- Not limited to steel or EOXS's client roster (only 3GM is currently an AskCruz client)

---

### **Current Status**

- **Internal pilot:** Running at EOXS with 94% data completeness (product metadata)
- **First external client:** 3GM, mid-implementation
- **Product-market fit assessment:** Early signals are credible (problem clear, solution coherent, working product, first customer acquired), but broad PMF is NOT yet proven. Still need evidence on: customer retention, repeated usage, measurable time savings, pricing acceptance, expansion, referrals, and business outcomes.

---

### **Immediate Priorities (Per Leadership)**

1. Product refinement (using real customer needs)
2. Customer readiness and deployment repeatability
3. Customer acquisition + disciplined measurement

---

**The bottom line:** AskCruz is a horizontal, cross-industry business knowledge layer. Its market is any company with fragmented data needing centralized, searchable access. The product exists, it's being deployed, and the next stage is proving that customers will repeatedly use it, derive measurable value, and expand/renew.

## User (2026-10-07 11:18:50 EDT)

how can we make askcruz better

## Claude (2026-10-07 11:18:50 EDT)

Before I outline improvements, I need clarity on what you're optimizing for and at what depth.

Your stated objective is **$250–500k ARR by Sept 2027** with EOXS stable. That's 12 months away. The constraints and leverage points are different depending on whether you're bottlenecked by:

1. **Product capability** — does AskCruz lack features customers need?
2. **Deployment/readiness** — is onboarding, configuration, or time-to-first-value the blocker?
3. **Customer acquisition** — can you even find and close customers fast enough?
4. **Unit economics** — does the pricing/cost structure support the growth target?
5. **Customer retention/usage** — do customers stick around and use it?

**What I can tell you directly:** You have one customer mid-implementation. You don't yet have evidence on retention, usage depth, time savings, pricing acceptance, or churn. That means the leverage is asymmetric:

- **High leverage:** Finish 3GM onboarding, measure what they actually use, measure their ROI, listen to what they say they need, then use that to calibrate the next 5–10 customers.
- **Medium leverage:** Harden deployment repeatability so you're not rebuilding for each customer.
- **Lower leverage:** Building features you think customers want without customer-validation feedback.

**My recommendation:** Pick a rigor level and I'll map what "better" means given the growth objective.

## User (2026-10-07 11:18:50 EDT)

5ft deep (quick pass using available data)

## Claude (2026-10-07 11:18:50 EDT)

**Quick Answer: Where to Focus for $250–500k ARR Growth**

### **1. Finish 3GM & Instrument It (Highest Leverage)**
You need usage data *now*. Measure:
- How many users are active
- What questions they're actually asking
- Time saved vs. manual searching
- Which features drive the most queries

This will tell you what to double down on for customer 2–5. Without it, you're guessing.

---

### **2. Reduce Deployment Time**
The current documented timeline is **6 weeks for 3GM**. That's custom work. You need:
- A standard onboarding playbook
- Pre-built integrations (Gmail, Odoo, Fireflies are documented—automate these)
- A config template for "first customer" setup

This directly reduces sales cycle and increases repeatability.

---

### **3. Focus Company Hands Over Company Brain**
The strongest near-term value is probably **practical work**, not just knowledge discovery:
- Draft quotes using company pricing
- Flag orders at risk
- Summarize calls against accounts
- Prepare customer briefings

These are friction-reducing workflows that sales/ops teams will use daily. Knowledge discovery is harder to measure and stickier.

---

### **4. Pricing & Packaging**
The supplied materials don't document pricing, ACV, or packaging. You need:
- A clear pricing model (per user? per deployment? per month?)
- A minimum commitment length that de-risks churn
- An expansion motion (add users, add sources, add workflows)

This unlocks the $250–500k math. Without it, you can't model whether 5 customers or 50 customers gets you there.

---

### **5. Sales Motion / ICP Clarity**
You have one customer. You don't know yet:
- Who the champion was / why they bought
- What their specific problem was
- How to find 4 more like them

After 3GM, capture: industry, company size, data-fragmentation score, primary buyer role, what convinced them, what they're measuring as success.

---

### **What NOT to Do (Yet)**
- Don't build Digital Workforce broadly until a customer asks for it
- Don't chase steel-industry-specific features (product is horizontal; stick to horizontal)
- Don't over-engineer before you have usage patterns
- Don't build features without customer validation

**Bottom line:** Your constraint isn't the product. It's customer traction + measurement. Get 3GM live, measure hard, use that to land customer 2. Then iterate.

## User (2026-10-07 11:21:55 EDT)

give me the list of employees working in askcruz team

## Claude (2026-10-07 11:21:55 EDT)

Based on the connectors, here's the **AskCruz team** that I can identify:

### **Core Team**

| Person | Role | Notes |
|--------|------|-------|
| **Ron** | Product/Implementation Lead | Manages daily task board, escalations, customer implementation. Critical operational bottleneck for deliverables. |
| **Ayan Dutta** | Engineering/Technical Lead | Manages team access rollout, technical architecture discussions, email ingestion/citation-review pipeline design. |
| **Jaskeerat** | Frontend Engineer | Owns the Cruz chat interface/frontend codebase (mentioned in self-knowledge doc as internal ownership). |
| **Sebastian Roa Viertel** | Sales Development Representative (SDR) | Engaged starting 2026-08-27, working through his own company (SRV Consulting) as independent contractor. |

### **Supporting/Involved**

| Person | Role | Context |
|--------|------|----------|
| **Aryan Bakshi** | (role unclear) | Involved in administrative/payment flow setup, participated in Claude/MCP rollout. |
| **Build-out team** | Backend/Database/Pipelines | Owns server, database, automated pipelines (mentioned in architecture but no individual names documented). |
| **Lawrence Tabachnick** | Advisor/Content Strategy | External advisor, not employee—led content/marketing strategy session on messaging. |

---

### **What's Missing**

The documentation doesn't have a formal org chart. Based on the evidence:
- **No dedicated product manager** explicitly named
- **No dedicated sales lead** (Sebastian is SDR, but no AE/sales director visible)
- **No dedicated ops/customer success** manager identified
- The "build-out team" for backend/DB/pipelines isn't broken down by individual ownership

### **Key Bottleneck**

**Ron** is a single point of failure—he's handling product, implementation, escalations, and customer readiness across all work. This was flagged in your profile as a structural constraint for EOXS broadly, and it applies directly to AskCruz.

---

Do you want me to dig deeper on any of these people or map out the missing roles you need to fill to hit the $250–500k ARR target?
