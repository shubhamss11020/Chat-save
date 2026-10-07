---
conversation_id: 3gm-impl-analysis-001
platform: claude
username: "shubham"
title: "3GM Steel Implementation — Comprehensive Analysis vs. Sabre Alloys"
created_at: "2026-10-07 14:12:38 EDT"
updated_at: "2026-10-07 14:18:51 EDT"
---

# 3GM Steel Implementation — Comprehensive Analysis vs. Sabre Alloys

## User (2026-10-07 14:12:38 EDT)

now provide me with every detail about 3gm client. i want all the information about it. do not miss anything

## Claude (2026-10-07 14:12:38 EDT)

[Comprehensive 3GM Steel overview provided in narrative format]

## User (2026-10-07 14:12:38 EDT)

why is this data so unorganised? give me proper data with a structure

## Claude (2026-10-07 14:12:38 EDT)

[Created structured database with 12 organized sections: Client Master Registry, Contact Registry, Implementation Metrics, Bug Tracker, Revenue Metrics, Risk Assessment, Timeline, Feature Deployment, Strategic Initiatives, Quick Reference, Portfolio Snapshot, Data Quality Notes]

## User (2026-10-07 14:18:51 EDT)

give me all the information about the 3gm implementation and you need not to create any file for it. just give me comprehensive information about the implementation and how it's different from the implementation of askcruz

## Claude (2026-10-07 14:18:51 EDT)

## **3GM Steel — Comprehensive Implementation Analysis**

---

### **I. IMPLEMENTATION TIMELINE & DURATION**

**3GM Steel (Apr 2022 – Aug 2022):**
- **Duration:** 4.5 months total, with core work compressed into **June–August 2022**
- **Go-Live Date:** July 18, 2022 (originally July 7, but pushed back 2 weeks for inventory count + personnel availability)
- **On-Site Leadership:** Rajat Jain personally attended for ~1 week, starting day one (July 18)
- **Support Window:** 2 weeks on-site support (July 18–Aug 2) + 3 weeks online support (Aug 2–Aug 23), then formal handoff to ticketed support
- **Official Completion:** August 12, 2022 (formal "implementation complete" notice issued)

**Sabre Alloys (Jan–Jun 2024):**
- **Duration:** ~2.5 years since onboarding (Jan–Mar 2024 implementation window start), with **3.5-month dense sprint** (Mar 15–Jun 18, 2024)
- **Go-Live Date:** Late March – Early April 2024 (soft launch, exact date reconstructed from task deadlines, not explicitly documented)
- **Task Volume:** 200 implementation tasks (vs. 33 for 3GM, all completed pre-go-live)
- **Post-Launch Stabilization:** Entire April–May 2024 consumed with stabilization tasks (UI cleanup, workflow bugs, access control)
- **Note:** Implementation tasks existed but did not specify a formal "implementation complete" date in the same way

---

### **II. BUSINESS MODEL & COMPLEXITY DIFFERENCES**

**3GM Steel:**
- **Business Model:** Steel **coil service center** — receives coils from mills, recuts/repackages, sells to fabricators
- **Revenue Basis:** Linear feet (LFT) or hundredweight (CWT)
- **Core Workflow:** Incoming receives → coil recut/repackaging → customer fulfillment → invoicing
- **Inventory Character:** Relatively **homogeneous** — variations are product type/coating/color (e.g., PRM:28 color variants, HOT ROLL oxide-coated)
- **Customer Base:** Limited (3 key customers: MAC Metal Sales-KY, Reliable Metal Buildings LLC, WV Metal Wholesaler)
- **Operational Complexity:** Medium; focused on lot/serial tracking, coil transfers, and LFT/CWT billing

**Sabre Alloys:**
- **Business Model:** Steel/metals **distributor & processor** — buys from mills, applies custom processing (cutting, blanking, toll processing), sells to OEM/fabricators
- **Revenue Basis:** Multi-tier (weight-based, toll charges, freight, processing fees)
- **Core Workflow:** PO receipt → receiving (often damaged/QA) → processing (third-party or in-house) → delivery valuation → invoicing with landed costs
- **Inventory Character:** **Highly heterogeneous** — tagged with control tags, processing order chains, UOM conversions (e.g., coils to pieces, weight to count), long-product weight calculations
- **Customer Base:** Larger (9+ key customers: Rhyno Valve, Granite Peak Fabrication, Tex-Fab Inc., Metal Supermarkets Houston SW, etc.)
- **Operational Complexity:** High; multi-lot delivery valuation, landed cost distribution, processing order chains, third-party processing, control tag system, MTR tracking

**Implication:** 3GM's simpler, transactional model allowed faster go-live. Sabre's complexity demanded 200 tasks just to stabilize.

---

### **III. DISCOVERY & PRE-GO-LIVE APPROACH**

**3GM Steel:**

| Phase | Activity | Participants | Notes |
|-------|----------|--------------|-------|
| **May 2022** | Accounting Kickoff Call | Jessica Worley (lead) | Pre-call discovery checklist: full accounting Phase 1 vs. deferred? Payment terms? Chart of accounts? No transcript captured |
| **May 2022** | Discovery Call Methodology | Rajat Jain | Documented EOXS's general practice: clients screen-share existing system; EOXS walks through workflow; documents current state before mapping to new system |
| **Jun 3** | Weekly Update: Core Customization Complete | Rajat → Travis & Jessica | Product Review phase underway |
| **Jun 22** | First Cut Product Review Done | Rajat → Travis | Rachel, Jessica, Leslie, Adam, Donnie queued for reviews |
| **Jun 29** | Soft-Launch Prep Guide Sent | Rajat → All 3GM | Jessica requests July 18 (instead of July 7) due to staffing |
| **Jul 15** | Data Cut-Off & Inventory Migration | Jessica → EOXS team | Full inventory spreadsheet + AR/AP balances; EOXS migrates over weekend |

**Key Characteristic:** Highly **structured discovery checklist** approach. Jessica Worley drove all scheduling decisions. Minimal surprise elements; timeline was driven by 3GM's operational calendar (inventory count, vacations), not EOXS scope creep.

---

**Sabre Alloys:**

| Phase | Activity | Timeline | Notes |
|-------|----------|----------|-------|
| **2024-03-15** | Pre-Launch Setup | ~1 week | Chart of Accounts migration (from SteelPlus legacy system). Inventory list + database request |
| **Late Mar–Apr 2** | Go-Live Execution | ~2–3 weeks | Soft launch occurs; exact date reconstructed from task deadlines, not formally documented |
| **Apr 2–30** | Post-Launch Stabilization Spike | ~4 weeks | 100+ of 200 tasks: UI/UX cleanup, workflow bugs (multi-lot delivery valuation, COGS sourcing), access control |
| **Late Apr–May** | Feature Build Cluster | ~4 weeks | Planning checkpoint meeting (Apr 29/30): Dashboards, QA Flow, error lists, third-party processing, control tags, buyout workflow |
| **May 24–Jun 7** | Accounting Reconciliation Cluster | ~2 weeks | AR-vs-Trial-Balance gap, Notes Payable verification, AR/AP discrepancy (modest scale, unrelated to 2026 crisis) |

**Key Characteristic:** **Reactive discovery**. No pre-documented discovery checklist visible in tasks. Issues emerged post-launch (UI labeling, COGS sourcing bugs, multi-lot valuation errors). Entire April consumed with firefighting. Feature requests came later (May onward).

---

### **IV. CRITICAL BUGS & POST-GO-LIVE ISSUES**

**3GM Steel — Immediate Post-Go-Live Window (Jul 18–Aug 31, 2022):**

| Issue | Reported By | Date | Resolution Status |
|-------|-------------|------|--------------------|
| Freight Inbound Errors | Leslie Countryman | Jul 19–20 | Addressed during 2-week on-site support |
| Coils Not Transferring After "Delivered" | Leslie | Jul–Aug | Addressed during 2-week on-site support |
| Coil IDs Not Appearing on Transfer Orders (despite showing available) | Leslie | Jul–Aug | Known issue persisting; inventory module crashes on report download |
| 5 Coils Missing from System Entirely (SO0518 incident) | Leslie | Aug 29 | Escalated as data migration error |
| 7,153 Rows Customer-Owned Coil Data Showing "False" | Data audit | Aug–Sep | Structural data gap persisting into Sep/Oct 2022 |
| Inventory Report Download Causing Module Crash | Leslie | Jul–Aug | System stability issue |

**Severity:** Moderate. Focused on **inventory module edge cases** and **data migration gaps**. None caused permanent business interruption; on-site support addressed most within 2 weeks.

---

**Sabre Alloys — Post-Launch Stabilization Window (Apr–May 2024):**

| Issue | Category | Severity | Notes |
|-------|----------|----------|-------|
| COGS Sourced from Product Master Instead of Delivery Valuation | Accounting | **HIGH** | Silent margin misstatement risk; marked Completed but no verification log |
| Multi-Lot Delivery Valuation Keeping Only Last Lot | Accounting | **HIGH** | Inventory value misstatement; marked Completed but unverified |
| Multi-Lot PO Weight Calculation Issues | Workflow | MEDIUM | Third-party processing testing bug list (6 issues) |
| Access Control: Payment Terms Permissions | Access | MEDIUM | Documented call with Tye Webb; access-control work ongoing |
| UI/UX Cleanup (Label Renames, Tab Order) | UI | LOW | Iterative improvements through April |
| AR-vs-Trial-Balance Gap ~[restricted amount] | Accounting | MEDIUM | Escalated as "Urgent" to Jesus Rios |

**Severity:** High. Accounting defects had **silent misstatement risks**. Entire April consumed with bug fixes. Unlike 3GM, no single on-site support week; stabilization was ongoing and less structured.

---

### **V. TEAM & GOVERNANCE STRUCTURE**

**3GM Steel:**

- **Primary On-Site Champion:** Jessica Worley (Office Administrator + scheduler)
- **Business Contacts Engaged:** Travis Lane (sales), Leslie Countryman (operations), Jessica Worley (finance), Rachel Epperson, Donnie Simpson, Adam Buck
- **AskCruz Lead:** Rajat Jain (on-site Jul 18–25, ~1 week)
- **Implementation Team:** Alka Jain (product master), Sai Siddhartha Dutta (2022 lead implementer)
- **Communication Cadence:** Weekly update emails; formal sign-off on Aug 2 by multi-stakeholder group (Rachel, Leslie, Donnie, Jessica); formal "implementation complete" notice Aug 12

**Governance Style:** **Centralized, scheduled, milestone-driven.** Jessica controlled the calendar. Rajat was physically present during go-live week. Clear handoff from implementation to support (Aug 12). No scope creep documented.

---

**Sabre Alloys:**

- **Primary On-Site Champion:** Juan Deshon (operational lead, 114+ calls with Raj)
- **Business Contacts Engaged:** Charles White, Christi Deaton, Ernie Valdez, Jesus Rios, Jim Zeigler, Michael Mercadante (CEO, owned only 1 task), Tye Webb
- **AskCruz Lead:** Rajat Jain (primary escalation contact)
- **Implementation Team:** Ron Jain, Hashir Saleem, Nijamuddin (QA), Humaira Zainab (QA/triage), Dhrup (warehouse), Arun Kaul (costing)
- **Communication Cadence:** No formal weekly update cadence visible; task-driven (chatter logs show reactive task creation)

**Governance Style:** **Reactive, task-heavy, open-ended.** 200 tasks suggest scope was not pre-defined. Stabilization consumed April–May without a formal completion milestone. Juan Deshon became the primary escalation contact (114+ calls), suggesting EOXS relied on client-side escalation rather than proactive checkpoints. No single clear "implementation complete" date in visible records.

---

### **VI. CUSTOM FEATURES DEPLOYED**

**3GM Steel (Minimal, Focused):**
1. **AskCruz Company Brain (AI)** — 2-user scope, provisioned Oct 2026 (4+ years post-go-live, during strategic expansion phase)
2. **IRIS AI Historical Data Preload** — Aug 2026
3. **LFT/CWT Billing Automation** — Core to business model; no major custom builds documented during implementation

**Sabre Alloys (Extensive, Complex):**
1. **Control Tag System** — Custom lot/serial tracking with tag lifecycle management
2. **Processing Module (3rd-party/toll)** — Handles toll processing, vendor workflows, buyout logic
3. **Landed Cost Automation** — Multi-line, multi-size coil distribution (source of active bugs)
4. **MTR (Material Test Report) Tracking** — Custom document attachment system
5. **Long Product Weight Calculations** — UOM conversion + weight standardization
6. **Fully Billed PO Status** — Custom workflow gate
7. **Load Scheduler** — Outbound logistics planning
8. **Dashboards (Unfulfilled in 2024, built later in 2026)** — Profitability, salesperson commission, machine queue depth, aged inventory

**Implication:** 3GM's simpler model required minimal custom work. Sabre's complexity drove 7+ custom features, many of which became sources of bugs post-launch.

---

### **VII. FINANCIAL MODEL & BILLING**

**3GM Steel:**

- **Billing Start:** Apr 2022 (proposal signed ~Jan 2022)
- **Pricing Structure:** 50% kickoff deposit + implementation hours (200 hrs) + post-live customizations + Phase 2 (with 10% referral discount)
- **Recurring Revenue:** Quarterly billing at [RESTRICTED]/user/month
- **Total Implementation Cost:** Documented as multi-invoice series (S00012, S00016, S00023)
- **Contract Span:** Continuous billing from Apr 2022 to present (4.5 years without interruption; longest-tenured client)

**Sabre Alloys:**

- **Billing Start:** ~2024 (post-go-live invoicing begins)
- **Pricing Structure:** No detailed breakdown visible in 2024 implementation tasks; 2026 crisis includes billing dispute + outage-credit negotiation
- **Recurring Revenue:** Continuous, with revenue declining Q2→Q3 2026 (-30%+ q-o-q); order frequency 2.8→2.0/quarter
- **Churn Risk:** Elevated (8.4/10) as of Oct 2026

**Implication:** 3GM's stable, long-term billing reflects successful, low-disruption implementation. Sabre's financial decline mirrors post-launch chaos and unresolved bugs.

---

### **VIII. KEY DIFFERENCES — SIDE-BY-SIDE SUMMARY**

| Dimension | 3GM Steel | Sabre Alloys | Implication |
|-----------|-----------|--------------|------------|
| **Tenure** | 4.5 years (since Apr 2022) | ~2.5 years (since Jan 2024) | 3GM is longest-tenured client |
| **Implementation Duration** | 4 months concentrated (Jun–Aug 2022) | 3.5 months + ongoing (Mar–Jun 2024, extended stabilization) | 3GM was faster, more linear |
| **Pre-Launch Discovery** | Structured checklist; Jessica scheduled everything | Reactive; tasks emerged post-launch | 3GM had clearer scope |
| **Go-Live Approach** | Staged ramp (day 1: SO/Releases/BOLs; day 2+: invoicing/payments) | Soft launch; exact date not documented | 3GM was more deliberate |
| **On-Site Support** | Rajat present 1 week (Jul 18–25); clear 2-week on-site window | No single documented on-site lead week | 3GM had dedicated leadership presence |
| **Post-Launch Issues** | Inventory edge cases (coil transfers, missing records, report crashes); moderate severity | Accounting defects (COGS sourcing, multi-lot valuation); high severity (silent misstatements) | Sabre's bugs were more serious |
| **Task Volume** | 33 tasks (pre-go-live; all completed by Aug 2022) | 200 tasks (mostly post-launch stabilization) | Sabre required 6x more work post-launch |
| **Completion Marker** | Aug 12, 2022 formal "implementation complete" notice | None visible; project appears to close in Jun 2024 but no formal notice | 3GM had clearer closure |
| **Business Model Complexity** | Simple (coil service center; LFT/CWT billing) | Complex (distributor + processor; landed costs, control tags, third-party processing) | Complexity drove implementation differences |
| **Custom Features Deployed** | 2–3 (billing automation; AI add-ons later) | 7+ (control tags, processing module, landed cost, MTR, load scheduler, dashboards) | Sabre required more custom work |
| **Financial Outcome (Oct 2026)** | Stable; 4.5-year continuous billing; churn risk MODERATE (6.0/10) | Declining; revenue -30%+ q-o-q; churn risk ELEVATED (8.4/10) | 3GM's smooth implementation correlates with retention |
| **Escalation Cadence** | Weekly structured updates; no surprise escalations | 114+ calls with Juan Deshon; reactive escalations | 3GM was predictable; Sabre was chaotic |

---

### **IX. ROOT CAUSE ANALYSIS: WHY THE DIFFERENCE?**

**3GM's Success Factors:**

1. **Simpler Business Model:** Coil service center ≈ transactional, homogeneous inventory, no complex multi-lot workflows
2. **Strong Operational Champion:** Jessica Worley; proactive scheduling; clear decision-making
3. **Staged Go-Live:** Day-by-day ramp (SO → Releases → BOLs → Invoicing → Payments) reduced risk
4. **On-Site Leadership:** Rajat's 1-week presence ensured real-time problem resolution
5. **Predictable Timeline:** No external surprises (unlike Sabre, which later faced security breaches, server outages, disputes)
6. **Small Scope:** 33 tasks, pre-defined; no scope creep

**Sabre's Challenges:**

1. **Complex Business Model:** Multi-step processing chains; landed costs; third-party workflows; control tags; UOM conversions
2. **Decentralized Governance:** Juan Deshon as primary contact vs. a structured champion; 114+ calls = reactive, not proactive
3. **Reactive Stabilization:** 100+ of 200 tasks were post-launch fixes, suggesting bugs were discovered live, not pre-tested
4. **Unresolved Pre-Launch Risks:** COGS sourcing bug, multi-lot valuation errors — accounting defects that silently misstate margins
5. **Open-Ended Stabilization:** No formal "implementation complete" milestone; April–May consumed entirely by bug fixes and feature requests
6. **Scope Creep:** 200 tasks suggest requirements were not pre-defined; discovered iteratively post-launch

---

### **X. STRATEGIC INSIGHTS**

**3GM's Implementation as a Baseline:**

3GM Steel represents EOXS's **cleanest, most predictable implementation path** in the current portfolio. The combination of:
- Simple, transactional business model
- Structured discovery & scheduling
- Staged go-live approach
- On-site executive leadership (Rajat)
- Clear completion milestone (Aug 12, 2022 formal notice)

…resulted in **4.5 years of uninterrupted, stable service** with moderate churn risk (6.0/10) and a longest-tenure status.

**Sabre as a Complexity Cautionary Tale:**

Sabre's implementation exposed the risks of:
- **High complexity without pre-defined scope:** 200 post-launch tasks suggest requirements engineering failed pre-go-live
- **Reactive vs. proactive governance:** 114+ Juan Deshon calls = firefighting, not planned execution
- **Silent accounting defects:** COGS/multi-lot bugs went unverified; no formal testing/QA phase visible
- **No clear completion or handoff:** Open-ended "stabilization" dragged April–May 2024; no formal implementation-complete milestone

This complexity, left unresolved, likely contributed to Sabre's later 2026 crisis (Feb outage, settlement disputes, elevated churn risk 8.4/10).
