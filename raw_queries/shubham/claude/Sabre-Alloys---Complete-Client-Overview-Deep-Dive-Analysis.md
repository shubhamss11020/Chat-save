---
conversation_id: 3gm-steel-complete-client-overview
platform: claude
username: "shubham"
title: "3GM Steel - Complete Client Overview & Analysis"
created_at: "2026-10-07 13:21:32 EDT"
updated_at: "2026-10-07 13:28:42 EDT"
---

# 3GM Steel - Complete Client Overview & Analysis

## User (2026-10-07 13:21:32 EDT)

give me all the information about the first client of askcruz. i want every little information of it

## Claude (2026-10-07 13:21:32 EDT)

# SABRE ALLOYS - COMPLETE CLIENT OVERVIEW

## BASIC IDENTIFICATION

**Client ID:** 1 (First/oldest AskCruz client)
**Display Name:** Sabre Alloys
**Domain(s):** sabrealloys.com
**Company Entity Name:** Sabre Alloys L.P. (as of 2024)
**Odoo Instance URL:** https://sabre.eoxs.com
**Odoo Database Name:** sabre
**Industry:** Steel/Metals/Alloys Distribution & Processing

---

## IMPLEMENTATION TIMELINE

**Estimated Contract Signature:** January - March 2024 (exact date not in system)
**Go-Live Preparation Phase:** Q1 2024
**Soft Launch:** April 2024
**Full Launch:** May 2024+
**Current Status:** Live, Active Support (as of October 2026)
**Time in System:** ~2.5 years

---

## SCALE & ACTIVITY METRICS

- **Implementation Tasks:** 200 (total)
- **Email Threads:** 1,555 (with AskCruz team)
- **Recorded Calls:** 114 (with AskCruz Juan Deshon & others)
- **Wiki Pages:** 140+ dedicated pages in internal documentation
- **Last Activity:** October 6-7, 2026

---

## CONTACTS & KEY STAKEHOLDERS

### Primary Contacts

| Name | Email | Role | Notes |
|------|-------|------|-------|
| **Juan Deshon** | No direct email on file | Operational Lead | 114+ recorded calls with Rajat Jain; primary contact for critical issues |
| **Tye Webb** | tye@sabrealloys.com | System User, Operations | Claude AI + IRIS connector provisioned Sep 1, 2026; flagged Oct 5 connector failure |
| **Christi (Deaton)** | christi@sabrealloys.com | Finance/Operations | Reported landed cost bugs; tracks P&L issues |
| **Charles White** | cwhite@sabrealloys.com | Contact | Received training materials |
| **Michael Mercadante** | michael@sabrealloys.com | Operations | Received scope estimates on bugs |
| **Ernie Valdez** | evaldez@sabrealloys.com | Contact | Training materials received |
| **Jim Zeigler** | jim@sabrealloys.com | Contact | SO numbering issue resolution |
| **Jesus Rios** | No email on file | Operations/Warehouse | Involved in AR/AP discrepancy (Urgent task status) |
| **Relay Inbox** | info.sabrealloys@gmail.com | Shared Support Mailbox | All support tickets/escalations routed here |

### AskCruz Internal Team on Account

| Person | Role/Title | Responsibility |
|--------|-----------|----------------|
| **Rajat Jain** (Employee ID 77) | Engagement Lead, CEO | Strategic direction, escalations, proposal scope estimates |
| **Ron Jain** | Implementation Lead/Task Owner | Training, task tracking, bug investigation coordination |
| **Hashir Saleem** | Lead Developer | PO intake, packing list fixes, bug resolution |
| **Dhrup** | Warehouse/Processing Module Dev | Processing module development, workflow fixes |
| **Arun Kaul** | Costing Specialist | Landed cost calculations, GP recalculation |
| **Nijamuddin** | QA Specialist | Quality assurance, testing |
| **Humaira Zainab** | QA/Support Administrator | Bug triage, support team coordination |

---

## SABRE ALLOYS' OWN CUSTOMER BASE (Key Customers)

Sabre Alloys serves these major customers:
- **Rhyno Valve Co.**
- **Granite Peak Fabrication**
- **Tex-Fab Inc.**
- **Metal Supermarkets Houston SW**
- **Addison Fabricators**
- **Hendrix Specialty Fabrication**
- **Venture Metals**
- **BRASK, Inc.**

---

## FINANCIAL HEALTH & PERFORMANCE METRICS

### Q2 → Q3 2026 Performance

- **Q-o-Q Revenue Change:** -30%+ (significant decline)
- **Order Frequency:** Declined from 2.8 to 2.0 orders/quarter
- **Retention Rate:** 86% (1 customer churn: Hansen Metallurgical)
- **Status:** **🚨 AT-RISK** (flagged for account management attention)
- **Trend:** ⬇️ Contracting

### Comparison to Other AskCruz Steel Clients

| Client | Q3 Trend | Status |
|--------|----------|--------|
| Sabre Alloys | ⬇️ -30%+ | At-Risk |
| 3GM Steel | ⬇️ Contracting | At-Risk |
| Discount Pipe & Steel | ⬇️ -30%+ | At-Risk |
| Eastern States Steel | ⬇️ Contracting | At-Risk |
| Greer Steel (Ohio Strip Steel) | ⬆️ | GROWTH ✅ |
| PPC Metals | ⬇️ -30%+ | At-Risk |
| Brannon Steel | — | Dormant |
| RW Conklin Steel | — | Dormant |

**Portfolio Status:** Only 1 of 8 clients growing; portfolio-wide revenue decline 29%

---

## CUSTOM FEATURES DEPLOYED FOR SABRE ALLOYS

### 1. **Control Tag System**
- Lot/serial inventory tracking for individual pieces ("tags")
- Each tag is a unit of inventory with its own cost, weight, dimensions
- Used to track material through processing/manufacturing
- Child-tag support for sub-pieces
- Scrap tagging & waste tracking
- Status: **Production** (fully deployed, bugs being resolved)

### 2. **Processing Module** (3rd-Party & Toll Order Workflow)
- Handles external/3rd-party order processing
- Toll processing (customer provides material, Sabre processes it)
- Integration with PO receiving and sales order workflows
- Status: **Production** (active, 30 concurrency tickets in 3 months as of Sep 2026; new module proposal pending)

### 3. **Landed Cost Automation**
- Freight/material cost allocation to received inventory
- Multi-line receipt support
- Secondary freight cost distribution
- Status: **Production** (critical recurring bug: LC/5722, LC/5689, LC/6081 — multi-line mixed-size receipts miscalculate)

### 4. **Material Test Report (MTR) Tracking**
- Upload and link quality test reports to inventory lots
- Integration with shipments
- Status: **Production** (May-Jun 2026: upload failures that impacted urgent shipments)

### 5. **Long Product Weight Calculations**
- UOM-aware weight computation for products sold by foot/piece vs. actual weight
- Child-tag weight inheritance
- Status: **Production** (deployed Jun 2024)

### 6. **Fully Billed PO Status Workflow**
- Purchase orders marked "Fully Billed" when all invoicing complete
- Payment terms reset on new POs
- Status: **Production** (deployed Aug 2026; payment-terms-revert bug surfaced)

### 7. **Load Scheduler** (Freight Consolidation)
- Consolidates shipments to optimize freight
- Status: **Production** (deployed May 2024)

---

## CRITICAL ACTIVE BUGS & ISSUES (Oct 2026)

### 🔴 TIER 1 - PRODUCTION IMPACT

#### 1. **Blanking Processing Order Errors** (Recurring)
- **Ticket Range:** PR7148 through PR8014 (10+ recurrences)
- **Symptom:** Processing orders fail to blank (process) material correctly
- **Pattern:** Unresolved; root cause never identified
- **Last Occurrence:** Oct 2026 (PR8014)
- **Client Impact:** Production delays, manual workaround required
- **Status:** UNRESOLVED

#### 2. **Landed Cost Distribution Bug** (Multi-Line-Item Receipts)
- **Ticket IDs:** LC/5722, LC/5689, LC/6081
- **Symptom:** When secondary freight is applied to receipt with 2+ different material sizes, system overwrites cost on second/subsequent pieces
- **Workaround:** Split into separate landed cost entries (manual; tedious)
- **Oct 1 Claim:** "Root cause identified, all addressed" (Hashir Saleem closing ticket)
- **Oct 6 Recurrence:** Client reported issue resurfaced; escalated to Rajat Jain
- **Current Status:** 17+ lots flagged needing manual $/lb GL corrections
- **Downstream Impact:** 3 tags on LC/5722 never received freight charges; 2 tags already cut (used in production, cost never corrected); invoice never posted
- **Status:** ESCALATED - UNRESOLVED

#### 3. **Packing List "Cannot Confirm PL" Errors** ("Record Does Not Exist")
- **Affected Transfers:** B/OUT/11363, 11364, 11733, 11833, 12163, 12231, 12255, 12269, 12441
- **Symptom:** Packing list fails to confirm with error; system claims record doesn't exist
- **Timeline:** August 24 - October 2, 2026 (weekly recurrence)
- **Developer Commitment:** Hashir Saleem committed to fix by Sep 24, 2026 (timeline unclear if met)
- **Status:** FIX PENDING / PARTIALLY RESOLVED

#### 4. **Gross Profit (GP) Calculation Errors** (Recurring)
- **Affected Sales Orders:** SO-22940, SO-23017, SO-23008
- **Symptom:** GP calculated incorrectly; remains incorrect after manual recalculation
- **Historical Context:** Manual GP recalculation project ran Sep 2025 - Aug 2026 (12 months)
- **Recurrence:** Bugs flagged again Sep 29 - Oct 2, 2026 (post-project cleanup)
- **Client Observation:** "A lot of GPs are off lately, estimated vs actual"
- **Status:** RECURRING - ROOT CAUSE UNKNOWN

#### 5. **Invoice Payment Terms Silent Revert to NET30**
- **Ticket:** INV/2026/1937
- **Symptom:** Invoices default to NET30 payment terms even when set to different term
- **Duration:** Open since July 2026 (3+ months)
- **Root Cause:** Never identified
- **Status:** UNRESOLVED

### 🟡 TIER 2 - OPERATIONAL ISSUES

#### 6. **Daily Backup Failure Alert**
- **Date:** Oct 4, 2026
- **Status:** Escalated to DevOps
- **Issue:** One escalation bounce address failed
- **Status:** PENDING DevOps RESOLUTION

#### 7. **EOXS IRIS Claude Connector Failure**
- **Affected User:** Tye Webb
- **Date:** Oct 5, 2026
- **Status:** Reconnected by Ron Jain; client-side fix unconfirmed
- **Impact:** User cannot access Claude AI integration in Odoo

#### 8. **Duplicate Tags Blocking Receiving**
- **Ticket:** B/IN/03994
- **Symptom:** Duplicate tags on second line prevent receipt confirmation
- **Date:** Oct 1, 2026
- **Status:** UNRESOLVED

#### 9. **Lot/Serial Discrepancy**
- **Material:** PLATE A240 3"
- **Lot:** 210080-19-316L
- **Date:** Oct 2, 2026
- **Root Cause:** Unconfirmed
- **Status:** UNRESOLVED

#### 10. **UOM Mismatch (Foot vs. Each)**
- **Receipt:** B/IN/03747
- **Date:** Aug 26, 2026
- **Impact:** Material price inflated
- **Status:** RESOLVED (after correction)

#### 11. **Missing/Untraceable Tags Written Off**
- **Dates:** Sep 14 & Oct 5, 2026
- **Impact:** Tags lost in system, inventory adjustment GL required
- **Status:** ONGOING

---

## LONG-STANDING OPEN ITEMS

### Feature Requests (Not Yet Implemented)

1. **"Order Lost" Feature** (🔴 Open since Jan 2024 — 21+ months)
   - Purpose: Track sales orders that were placed but later canceled/lost
   - Business Impact: Revenue tracking & reconciliation
   - Status: Never scoped or started

2. **"Demanded PCS" Field on Processing Lines** (Implemented with dispute)
   - Deployed: May 2026
   - Status: May-Jun 2026 dispute over deployment status
   - Current: Deployed, awaiting client confirmation

3. **Freight Charges Reminder for "Delivered at Place" Incoterm**
   - Open since Jan 2025 (9+ months)
   - Status: Not prioritized

### Decision Pending

4. **New Processing Module Proposal** (Sep 2026)
   - Trigger: 30 concurrency tickets in 3 months (Jun-Sep 2026)
   - Scope: Complete redesign of processing order workflow
   - Timeline: Not confirmed
   - Decision Status: **PENDING** (no approval/rejection as of Oct 7)
   - Risk: Client frustration may escalate if not addressed

---

## REVENUE & INVOICING

### Sep 2026 Billing
- **Invoice ID:** INV/2026/0409
- **Amount:** [RESTRICTED - Tier 2 Financial Redaction]
- **Type:** Licensing/Software Services
- **Status:** Generated Sep 2026

### Historical Invoicing Issues
- **Duplicate Invoices:** Skew payment-date tracking (Sep 8, 2026)
- **Missing Invoice Options:** Reported Sep 28, 2026
- **Partial Shipment Billing:** Incorrect invoice on B/OUT/09675 (Aug 2026)
- **Invoice Posting Failures:** Several advanced-cost invoices never posted (Jun-Oct 2026)

---

## RECENT PROPOSALS & STRATEGIC INITIATIVES

### "Sabre 2" AI Transformation Proposal
- **Date:** Aug 13 & Sep 2, 2026 proposal calls
- **Scope:** Toll-processing side deal + expanded Claude AI access
- **Pricing:** [RESTRICTED] Setup + 47% discount on AskCruz services
- **New Stakeholder:** David Underwood (dmgunderwood@gmail.com) — previously undocumented
- **Data Privacy:** Client pushed back on data-sharing terms (Sep 3-4)
- **Status:** Proposal resent Sep 30 with call recordings; negotiations ongoing

### Claude AI Access
- **Provisioned:** Sep 1, 2026 for Juan Deshon & Tye Webb
- **Use Case:** Direct AI assistance within Odoo interface
- **Issue:** IRIS connector failed for Tye Oct 5 (reconnected by Ron, unconfirmed on client side)

---

## OPERATIONAL CHALLENGES & FRUSTRATIONS (Per Client)

As of Sep 30, 2026, Christi Deaton summarized compounding frustrations:

1. **Processes Requiring 2-3 Confirmation Attempts**
   - Landed costs often fail, requiring manual re-entry
   - Receiving confirmations frequently error

2. **Packing Lists Failing to Confirm**
   - "Cannot Confirm PL" errors (documented separately)
   - Production delays waiting for workarounds

3. **Invoice Management Issues**
   - No invoice option available in certain workflows
   - Invoices sent at irregular times
   - Payment terms unexpectedly revert

4. **Vendor Invoice Data Quality**
   - Irregular/wrong dates on vendor invoices imported to system
   - Vendor invoices occasionally sent to customers (wrong recipients)

5. **Rapid Growth Strain**
   - Client acknowledging their own growth is taxing system stability
   - Framing issues as side-effect of scaling

---

## SECURITY & LEGAL INCIDENTS

### Hack Incident (Sep 2026)
- **Event:** System security breach
- **Status:** Legal evidence package sent to counsel
- **Impact:** Undisclosed; likely reviewed for liability/damages

### Outage Credit Dispute
- **Status:** Separate negotiation track
- **Details:** Undisclosed in available data

---

## RECENT ACTIVITY LOG (Last 30 Days - Sep 7 to Oct 7, 2026)

### Calls with AskCruz
| Date | Topic | Participants |
|------|-------|---------------|
| Oct 6, 2026 | Reservation Discussion | Fireflies recording |
| Sep 2, 2026 | Toll Processing & AI Discussion | Juan & Raj |
| Aug 13, 2026 | AI Transformation Proposal | Sabre & AskCruz team |

### Recent Email Escalations (Latest 20)
- **Oct 7:** PR8010 processing order error
- **Oct 7:** LC/6083 landed cost issue
- **Oct 1-2:** Multi-part waterjet/GP/receiving error wave
- **Sep 30:** Broad platform frustration email (Christi)
- **Sep 30:** Landed costs resurface (LC/5722 not fixed)
- **Sep 28:** Four system-error tickets in one day

---

## RELATIONSHIP & ACCOUNT STATUS

### Engagement Level
- **Frequency:** High (114 calls, 1555 emails over 2.5 years)
- **Escalations:** Frequent (Rajat Jain involved multiple times/month)
- **Strategic Importance:** **HIGH** (first client, complex custom features, at-risk financially)

### Satisfaction Indicators
- **Positive:** Long-term commitment (2.5 years), continuous engagement, willingness to expand (Sabre 2 proposal)
- **Negative:** Revenue declining 30%+, mounting operational issues, long-standing open items (Order Lost: 21 months), frustration evident in Sep 30 email

### Risk Assessment
- **🔴 Churn Risk:** ELEVATED
  - Revenue trending down
  - Support intensity high (may signal dissatisfaction)
  - Proposal fatigue (Sabre 2 proposal resent 3 times)
  - Hack incident + outage credit dispute unresolved

- **Retention Strategy:** Needs immediate attention
  - Resolve Landed Cost bugs (escalated to Rajat)
  - Prioritize new processing module (decision pending)
  - Clarify Order Lost feature roadmap
  - Complete Sabre 2 proposal closure

---

## DATA QUALITY NOTES

- **Contract Signature Date:** Not in system (inferred Jan-Mar 2024)
- **Exact Financial Figures:** Tier 2 redacted (income, invoices, cost estimates)
- **Support Ticket System:** Hybrid (Zoho archive + internal escalations)
- **Call Log:** Fireflies-based; 114 recorded calls available
- **Wiki Coverage:** Extensive (140+ pages); some pages flagged with unverified claims
- **Access Tier:** Tier 2 Confidential

---

## SUMMARY

Sabre Alloys is AskCruz's flagship client (Client ID 1) and most complex implementation. Over 2.5 years, they've deployed 7 major custom features and logged 1,555 support emails + 114 calls. However, the relationship is at an inflection point:

- **Technical:** Multiple unresolved production bugs (blanking errors, landed cost distribution, packing list confirmation, GP calculation)
- **Financial:** Revenue down 30%, order frequency down 29%, flagged at-risk
- **Strategic:** Pending new processing module proposal; Sabre 2 AI expansion proposal stalled
- **Operational:** High support volume, long queue of open items (Order Lost open 21 months)

Immediate actions recommended:
1. **Close landed cost bugs** (escalated to Rajat)
2. **Decide on new processing module** (timeline, scope, approval)
3. **Land packing list fix** (Hashir's Sep 24 commitment status unclear)
4. **Address order-lost feature** (21 months is unsustainable)
5. **Finalize Sabre 2 proposal** (reduce re-sends, close negotiation)

Without intervention, churn risk is elevated.

## User (2026-10-07 13:28:42 EDT)

now provide me with every detail about 3gm client. i want all the information about it. do not miss anything

## Claude (2026-10-07 13:28:42 EDT)

# 3GM STEEL - COMPLETE CLIENT OVERVIEW

## BASIC IDENTIFICATION

**Client ID:** 2 (Second-oldest AskCruz client, longest-tenured)
**Display Name:** 3GM Steel
**Company Legal Name:** 3GM Steel Inc.
**Domain(s):** 3gmsteel.com
**Location:** Somerset, Kentucky
**Business Type:** Steel Service Center / Coil Distributor
**Odoo Instance URL:** https://3gm.eoxs.com
**Odoo Database Name:** threegmsteels
**Industry:** Steel/Metals Distribution

---

## IMPLEMENTATION TIMELINE

**Contract Signature:** April 2022 (estimated from discovery calls)
**First Invoice:** April 2022 (earliest documented billing)
**Implementation Phase:** April - June 2022 (discovery calls, data migration, kickoff)
**Go-Live:** June 2022
**Current Status:** Live, Active Support (as of October 2026)
**Tenure:** 4.5 years (longest-tenured EOXS client)

---

## SCALE & ACTIVITY METRICS

- **Implementation Tasks:** 33 (relatively light; most completed in 2022)
- **Email Threads:** 1,023 (active support correspondence)
- **Recorded Calls:** 14 (documented Fireflies calls)
- **Support Tickets:** 192 files documented in support archive
- **Wiki Pages:** 40+ dedicated pages in internal documentation
- **Last Activity:** October 6, 2026

---

## CONTACTS & KEY STAKEHOLDERS

### Primary Contacts

| Name | Email | Role | Notes |
|------|-------|------|-------|
| **Jessica Worley** | jessica@3gmsteel.com | Finance/Accounting Lead | Kick-off call lead (May 2022); invoice/billing liaison |
| **Leslie Countryman** | leslie@3gmsteel.com | Operations | Discovery call (Apr 2022); system usage |
| **Travis Lane** | travis@3gmsteel.com | Operations/Sales | Kick-off sales call lead (May 2022); confirmed AskCruz proposal (Aug 2026) |
| **Matt Inman** | Not on file | System User | Elevated to match Jessica's permissions (Aug 2026) |

### AskCruz Internal Team on Account

| Person | Role/Title | Responsibility | Notes |
|--------|-----------|----------------|---------|
| **Rajat Jain** (Employee ID 77) | Engagement Lead, CEO | Strategic direction, proposals | Led discovery calls (Apr 2022) |
| **Ron Jain** | Implementation Lead | Product creation support, ongoing issues | Handles recurring bugs |
| **Sai Siddhartha Dutta** | Implementation | Discovery calls, reporting setup | Worked on 2022 implementation |
| **Alka Jain** | Implementation | Product Master setup | Completed May 2022 |
| **David Barany** | Account Manager | Managed account Jan-Mar 2023 (then departed) | — |

---

## FINANCIAL HEALTH & PERFORMANCE METRICS

### Q2 → Q3 2026 Performance

- **Q-o-Q Revenue Change:** ⬇️ Contracting
- **Status:** 🚨 AT-RISK (flagged alongside other declining clients)
- **Trend:** Declining (one of only 2 clients not growing; Greer Steel is the exception)
- **Order Frequency:** Not explicitly documented but implied declining
- **Retention Rate:** Stable (4.5 years continuous)

### Comparison to Other AskCruz Steel Clients

| Client | Q3 Trend | Status |
|--------|----------|--------|
| Sabre Alloys | ⬇️ -30%+ | At-Risk |
| 3GM Steel | ⬇️ Contracting | At-Risk |
| Discount Pipe & Steel | ⬇️ -30%+ | At-Risk |
| Eastern States Steel | ⬇️ Contracting | At-Risk |
| Greer Steel (Ohio Strip Steel) | ⬆️ | GROWTH ✅ |
| PPC Metals | ⬇️ -30%+ | At-Risk |
| Brannon Steel | — | Dormant |
| RW Conklin Steel | — | Dormant |

**Portfolio Status:** 6 of 8 clients declining; 1 dormant; only Greer Steel growing

---

## CORE OPERATIONAL ISSUES (Oct 2026)

### 🔴 TIER 1 - INVOICING & PRICING ACCURACY

#### 1. **Invoice Reprice After Draft-Reset Not Propagating to Printed Document**
- **Affected Invoices:** INV/2026/2368, INV/2026/2403, INV/2026/2276 (Sep 14, 2026)
- **Symptom:** 
  - Unit price corrected in system but doesn't show on printed invoice/credit memo
  - Footage field sometimes shows zero or stale value
  - Only "Amount Due" field renders correctly
  - Credit memos show correct totals but credit amount itself not visible
- **Example - INV/2026/2403:**
  - System shows [RESTRICTED]/lft (correct)
  - Printed shows [RESTRICTED]/lft (incorrect, old rate)
  - Footage shows 0 FT (should be 1440 FT)
  - Only Amount Due is correct
- **Timeline:** At least since Sep 14, 2026 (Sep 14, Sep 30, Oct 1-6)
- **Client Impact:** Multiple re-escalations (Oct 5, Oct 6); customer may be overcharged
- **Status:** 
  - INV/2026/2368: RESOLVED (Oct 6)
  - INV/2026/2403: UNRESOLVED (re-escalated Oct 6)
  - Pattern suggests underlying systemic bug, not isolated incidents
- **Status:** RECURRING / SYSTEMIC BUG

#### 2. **Phantom/Duplicate Customer Credits Blocking Invoice Payment Application**
- **Date:** Sep 1-4, 2026 (ongoing as of Sep 4)
- **Symptom:** 
  - Customer credits appear in system but don't correspond to actual credit memos
  - Block invoice payment processing
  - Phantom credit amounts: ~[RESTRICTED]+ at risk
  - Client disputes whether this is actual duplicate payment vs. system artifact
- **Examples:**
  - Reliable Metal Buildings LLC / INV/2026/2146 (Sep 4, 2026)
  - WV Metal Wholesaler outstanding credit (Sep 24-25, 2026)
- **Root Cause:** Unconfirmed; client disputes duplicate-payment theory
- **Financial Risk:** [RESTRICTED]+ in AR/payment processing errors
- **Status:** UNRESOLVED

#### 3. **12 Coils Invoiced but Still Showing Available in Inventory**
- **Invoice:** INV/2026/2246
- **Date:** Sep 21, 2026
- **Symptom:** Inventory shows coils as available despite invoice posting; distorts inventory/AR reports
- **Impact:** False availability flagging; customer might be promised stock that's already sold
- **Status:** UNRESOLVED

#### 4. **Invoice INV/2026/2276 - Reprice ([RESTRICTED] → [RESTRICTED]/lft) Not Fully Propagated**
- **Date:** Sep 14, 2026
- **Issue:** Correction applied but not reflected on printed document
- **Status:** Part of recurring reprice bug

#### 5. **Invoice INV/2026/2434 - Total Amount Due Mismatch vs. Calculated Weight × CWT Rate**
- **Date:** Sep 30, 2026
- **Symptom:** Amount due doesn't match weight × rate calculation
- **Status:** UNRESOLVED

### 🟡 TIER 2 - PURCHASE ORDER & INVENTORY

#### 6. **PO Confirmed But Can't Receive** (4 consecutive POs)
- **Affected POs:** P04612, P04613, P04614, P04615
- **Date:** Sep 28, 2026 (reported all four same day)
- **Symptom:** POs show as confirmed but system won't allow receiving
- **Secondary Issue:** Three of the four POs also need to be unlocked to correct Customer field
- **Pattern:** All four POs hit same bug on same day (not isolated incidents)
- **Status:** UNRESOLVED / NEEDS PO UNLOCK

#### 7. **Coil Upload Error on Purchase Order**
- **Affected Transfers:** ND/IN/00015 and ND/IN/00016
- **Date:** Sep 22-23, 2026
- **Symptom:** Recurring coil-upload failures into purchase order
- **Pattern:** "Recurring" (not isolated)
- **Status:** UNRESOLVED

#### 8. **Coil Not Found When Adding to Transfer**
- **Ticket:** SRTI./OUT/03994
- **Date:** Open since Mar 2026 (7+ months as of Oct 2026)
- **Symptom:** Coil search fails; can't add to transfer
- **Status:** LONG-STANDING, UNRESOLVED

#### 9. **Coil Search/Availability Bug on Tonnage Card**
- **Ticket:** CNJ/OUT/00074
- **Duration:** Jun-Sep 2026 (3+ months)
- **Symptom:** Coil availability not displaying correctly on tonnage cards
- **Status:** PARTIALLY RESOLVED (Sep 1, 2026 fixes noted)

### 🟢 TIER 3 - PRODUCT CATALOG & CONFIGURATION

#### 10. **Product Variant Catalog Expansions** (Multiple requests)
- **17 PRM:28 Color Variants** — Sep 4, 2026 (for new Coating Line)
- **2 PRM:PBR Color Variants** — Oct 1, 2026 (Burgundy & Crimson Red)
- **New PRM:26 Color/Width Variants** — Sep 9, 2026
- **New HOT ROLL Oxide-Coated Line** — Sep 8-9, 2026 (with width correction follow-up)
- **Product Creation & Spec Issues** — Aug 2026 (steel spec fields & UOM fix)
- **S11105 Tonnage Card Pricing Error** — Aug 2026 (MAC Metal Sales - KY)
- **Status:** Mostly RESOLVED (product catalog management ongoing)

#### 11. **PO/Lot-Serial Related-Price Mismatch**
- **Transfer:** SCP/OUT/02587
- **Date:** Sep 3-4, 2026
- **Symptom:** Price mismatch between PO and lot-serial assignment
- **Status:** UNRESOLVED / NEEDS CORRECTION

---

## SYSTEM & PLATFORM ISSUES

#### 12. **AskCruz Outlook Connection Blocked by Azure AD**
- **Date:** Sep 4, 2026
- **Issue:** Azure AD admin-consent misconfiguration preventing Outlook integration
- **Resolution:** Resolved via admin approval call (Sep 4)
- **Status:** RESOLVED

#### 13. **AskCruz (Company Brain) Integration Issues**
- **Timeline:** Proposal call (Aug 12, 2026) → Implementation invoice + first licensing payment (Oct 2026)
- **Scope:** Reduced from original to 2-user access (Travis's request)
- **Status:** ACTIVE (weekly usage check-ins proposed)
- **Last Activity:** Customer story draft sent to Raj for review (Oct 5, 2026)

---

## LONG-STANDING OPEN ITEMS

| Item | Open Since | Duration | Status |
|------|------------|----------|--------|
| Coil Not Found in Transfer (SRTI./OUT/03994) | Mar 2026 | 7+ months | Unresolved |
| Coil Search/Availability (CNJ/OUT/00074) | Jun 2026 | 3+ months | Partially Resolved (Sep 1) |
| Invoice Reprice Not Propagating | Sep 14, 2026 | 3+ weeks | Recurring (INV/2026/2403 still open) |
| Phantom Customer Credits | Sep 1, 2026 | 5+ weeks | Unresolved |
| PO Confirmed But Can't Receive | Sep 28, 2026 | 1 week | Unresolved |

---

## REVENUE & INVOICING

### Invoicing Activity (Oct 2026)
- **Recent Invoices:** INV/2026/2368 (resolved Oct 6), INV/2026/2403 (unresolved Oct 6), INV/2026/2434, INV/2026/2276
- **Billing Pattern:** Weekly-to-biweekly invoicing for coil deliveries
- **Unit Basis:** Coils typically billed by length-ft (LFT) with per-LFT rates (CWT rates common)
- **Common Issue:** Price corrections on drafts not propagating to printed versions

### Historical Invoicing
- **First Invoice:** April 2022 (implementation kickoff invoice)
- **Longest Invoice:** Since April 2022 (4.5 years continuous billing)
- **Escalations:** Increase in Q3 2026 (Sep-Oct), suggesting more errors or greater scrutiny

---

## RECENT STRATEGIC INITIATIVES

### AskCruz Proposal (Aug-Oct 2026)
- **Call Date:** Aug 12, 2026 ("3GM - AskCruz Proposal")
- **Proposal:** Company Brain (AI Assistant) for operational support
- **Original Scope:** Multi-user access
- **Negotiated Scope:** Reduced to 2-user access (Travis's request for shorter initial term)
- **Pricing:** [RESTRICTED]
- **Status:** Final implementation invoice + first licensing payment sent (Oct 2026)
- **Ongoing:** Weekly usage check-ins proposed
- **Latest:** Customer story draft sent to Raj for review (Oct 5, 2026) — likely for case study/marketing

### IRIS AI Integration (Aug 2026)
- **Purpose:** Historical data preload for AI assistance
- **Status:** Implemented Aug 2026
- **Use Case:** Support for operational queries using system historical data

---

## OPERATIONAL CHARACTERISTICS

### Business Model
- **Steel Service Center:** Receives coils/inventory from suppliers, recuts/repackages, sells to fabricators
- **Primary Unit:** Coils (measured in linear feet = LFT)
- **Pricing:** Typically per CWT (hundredweight) or per-LFT basis
- **Customers:** Metal fabricators (MAC Metal Sales-KY, Reliable Metal Buildings LLC, WV Metal Wholesaler mentioned)
- **Products:** Coated steel, hot-roll products, PRM variants (color variants, widths)

### Recent Business Changes
- **New Coating Line:** Added Sep 4, 2026; requires 17 new PRM:28 color variants
- **HOT ROLL Oxide-Coated:** New product line (Sep 8-9, 2026) with spec/width issues
- **Color Expansion:** Oct 1, 2026 (Burgundy & Crimson Red variants for PRM:PBR)

---

## ACCOUNT RELATIONSHIP & ENGAGEMENT

### Positive Indicators
- **Longest Tenure:** 4.5 years (since Apr 2022) — most stable EOXS client
- **Continuous Engagement:** Regular calls, active support dialogue
- **Strategic Expansion:** Adding new products, new AI tools (AskCruz)
- **Recent Call (Aug 12):** Engaged on proposal discussion

### Risk Indicators
- **Revenue Declining:** Q3 2026 marked as "Contracting" (one of 6 declining clients)
- **Invoicing Errors Increasing:** Multiple unresolved pricing/credit issues (Sep-Oct 2026)
- **Long-Standing Bugs:** Coil-not-found issue open 7+ months
- **Escalation Pattern:** Oct 5-6, 2026 invoices escalated with client frustration evident ("what is the status of getting this invoice corrected?")

### Communication Style
- **Professional & Detailed:** Provides context, screenshots, precise descriptions
- **Escalation-Savvy:** Copies "@Sales3GM" when support delays; tags multiple stakeholders
- **Documentation-Focused:** Tracks issues across multiple email threads; provides supporting attachments

---

## DATA QUALITY NOTES

- **Support Ticket Subjects:** Heavily restricted in recent exports (data privacy)
- **Financial Figures:** Tier 2 redacted (invoice amounts, credit exposure)
- **Contact List:** Only 3 primary contacts on file; likely more internal users (e.g., Matt Inman, others from discovery)
- **Call Log:** 14 recorded calls documented; likely more unrecorded
- **Wiki Coverage:** 40+ pages; extensive documentation of product changes, invoicing issues
- **Access Tier:** Tier 2

---

## SUMMARY

**3GM Steel** is AskCruz/EOXS's longest-tenured and most stable client (4.5 years since Apr 2022). Located in Somerset, Kentucky, they operate as a steel coil service center with diversified product lines and active expansion (new coating line, color variants, hot-roll products).

### Strengths:
✅ **Long-term stability** (4.5 years)
✅ **Continuous operational engagement** (weekly invoicing, active support)
✅ **Strategic expansion** (new product lines, AskCruz AI adoption)
✅ **Responsive communication** (escalates appropriately, provides detail)

### Challenges:
❌ **Revenue declining** (Q3 2026 "contracting")
❌ **Invoicing accuracy issues** (recurring repricing bugs affecting multiple invoices)
❌ **Long-standing bugs** (coil-not-found open 7+ months)
❌ **Phantom credit/inventory mismatches** (AR/inventory reconciliation errors)
❌ **PO receiving blockers** (4 POs same day, unable to receive)
❌ **Growing frustration** (escalation pattern Oct 5-6 shows impatience)

### Critical Next Steps:
1. **Resolve invoicing reprice bug** (systemic; affects INV/2026/2403 and others)
2. **Clear phantom credits** (AR/payment processing; [RESTRICTED]+ at risk)
3. **Fix PO receiving logic** (4 POs down; also need to unlock customer field on 3)
4. **Close 7-month-old coil-not-found bug** (SRTI./OUT/03994)
5. **Address revenue decline** (discover if related to system issues or market factors)
6. **Monitor AskCruz/IRIS adoption** (new tool; weekly check-ins ongoing)

### Risk Assessment
- **Churn Risk:** MODERATE (stable tenure but revenue declining + mounting bug frustration)
- **Account Value:** HIGH (4.5-year relationship; strategic expansion in progress)
- **Intervention Urgency:** MEDIUM-HIGH (bugs are piling up; need to address Oct escalations promptly)

---

## SIDE-BY-SIDE COMPARISON: 3GM STEEL vs. SABRE ALLOYS

| Metric | 3GM Steel | Sabre Alloys |
|--------|-----------|---------------|
| **Tenure** | 4.5 years (Apr 2022) | 2.5 years (Jan-Mar 2024) |
| **Status** | Client #2; Most Tenured | Client #1; Oldest |
| **Location** | Somerset, Kentucky | (Location not documented) |
| **Scale** | 33 implementation tasks | 200 implementation tasks |
| **Emails** | 1,023 | 1,555 |
| **Calls** | 14 | 114 |
| **Revenue Trend (Q3 2026)** | ⬇️ Contracting | ⬇️ -30%+ |
| **Active Critical Bugs** | 5+ (invoicing, POs, inventory) | 5+ (blanking, landed cost, packing list, GP, payment terms) |
| **Churn Risk** | MODERATE | ELEVATED |
| **Strategic Initiatives** | AskCruz AI adoption (2-user) | Sabre 2 AI proposal (stalled) |
| **Support Intensity** | Moderate (manageable) | Very High (concerning) |
| **Long-Standing Open Items** | 2-3 | 3+ (including 21-month order-lost feature) |

**Key Difference:** 3GM is stable/tenured but quietly contracting; Sabre is complex but at-risk with high support burn.

