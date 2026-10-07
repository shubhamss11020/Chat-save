---
conversation_id: askcruz-comprehensive-overview
platform: claude
username: "shubham"
title: "AskCruz Comprehensive Overview - Architecture, Clients & Employees"
created_at: "2026-10-07 13:06:25 EDT"
updated_at: "2026-10-07 13:13:06 EDT"
---

# AskCruz Comprehensive Overview - Architecture, Clients & Employees

## User (2026-10-07 13:06:25 EDT)

give me all the information you know about askcruz. the architecture structure, all the clients, exployees etc. dig deep into it and provide me a comprehensive explanation

## Claude (2026-10-07 13:06:25 EDT)

# AskCruz: Comprehensive Organizational Overview

## ARCHITECTURE & TECHNICAL FOUNDATION

### Database Structure
**Platform:** Odoo 13 Community Edition
**Primary Focus:** HR + Project Management + Custom Training Management

**Core Modules Installed:**
- HR Module (Employees, Departments, Jobs)
- Project Module (Projects, Tasks, Stages)
- Custom Training Management System (emp_training_* tables)
- **NOT Installed:** Sales, Purchase, Accounting modules (no CRM/invoice/purchase order apps)

**Key Database Tables:**
1. **res_partner** (123 columns) - Contacts & Customer Records
   - Stores both customers and vendors
   - LinkedIn enrichment data (li_*)
   - Custom fields for faculty, team assignments
   - Sample: Leduc Hyundai contacts, supplier info

2. **project_project** (30 columns) - Projects
   - GTM Projects (PR Board, LinkedIn Outreach, Email Marketing)
   - Privacy visibility settings
   - Timesheet tracking
   - Examples: 3 active GTM projects

3. **project_task** (56 columns) - Tasks/Kanban Items
   - Development tracking with kanban states
   - QA state management
   - Incentive tracking for dev/QA teams
   - Stage-based workflow

4. **hr_employee** (65 columns) - Employee Master Records
   - Personal info (name, gender, marital status, DOB)
   - Work info (phone, email, location)
   - HR tracking (leave manager, coach, contract info)
   - Emergency contacts

5. **hr_department** (14 columns) - Department Hierarchy
   - Departments: Research, Management Consulting, Sales, etc.
   - Manager assignments
   - Hierarchical structure

6. **hr_job** (22 columns) - Job Positions
   - Job titles with recruitment tracking
   - Department mapping
   - Expected/actual employee counts
   - Example: Management Consultant, Marketing, roles in recruitment state

7. **emp_training_*** Tables - Custom Training Management
   - Training centers
   - Training applications
   - Application lines and stages
   - Custom training workflow for employees

---

## CLIENT ROSTER (8 Active Clients - All Steel/Metals Industry)

### 1. **Sabre Alloys**
   - **Slug:** sabre-alloys
   - **Domain:** sabrealloys.com
   - **Odoo Instance:** https://sabre.eoxs.com
   - **Key Contacts:** 9 total
     - Charles White, Christi, Ernie Valdez, Jim (Zeigler), Michael Mercadante, Tye Webb
   - **Status:** At-risk account with 30%+ Q-o-Q revenue decline (Q2→Q3)
   - **Relay Inbox:** info.sabrealloys@gmail.com

### 2. **3GM Steel**
   - **Slug:** 3gm-steel
   - **Domain:** 3gmsteel.com
   - **Odoo Instance:** https://3gm.eoxs.com
   - **Key Contacts:** 3 total
     - Jessica Worley, Leslie Countryman, Travis Lane
   - **Status:** Revenue contraction

### 3. **Discount Pipe & Steel (DPS)**
   - **Slug:** discount-pipe-steel
   - **Domain:** discountpipesteel.com
   - **Odoo Instance:** https://discountpipesteel.eoxs.com
   - **Key Contacts:** 8+ total
     - Austin Rayzor, Cameron Bain, L. Hulsey, Zana Williams, Tina Valdez (Alt Digital AI consultant), Jamie Vernon (Alt Digital AI)
   - **Status:** At-risk account with 30%+ Q-o-Q revenue decline (Q2→Q3)
   - **Relay Inbox:** info.discountpipesteel@gmail.com
   - **Implementation Status:** ACTIVE - 79 open/in-progress tasks
     - Highest task volume (actively managed)
     - Multiple QA stages (DPS Sandbox Review, DPS Decision)
     - Key issues: PO Receiving Error Prevention, Packing Error Prevention, Inventory Management, Weight Discrepancies

### 4. **Eastern States Steel (ESS)**
   - **Slug:** eastern-states-steel
   - **Domain:** easternstatessteel.com
   - **Odoo Instance:** https://ess.eoxs.com
   - **Key Contacts:** 6 total
     - Chip Capinski, Rose Torres, Ryan Capinski, Tom Meyer, Vince Pappas
   - **Status:** Revenue contraction
   - **Relay Inbox:** info.easternstatessteel@gmail.com
   - **Implementation Status:** ACTIVE Phase 1
     - Tasks: Purchase Order Intake (Intake stage), Weight/Width display bugs, Invoice tax label

### 5. **Ohio Strip Steel / Greer Steel**
   - **Slug:** greer-steel
   - **Display Name:** Ohio Strip Steel (formerly Greer Steel)
   - **Domains:** ohiostripsteel.com, greersteel.com
   - **Odoo Instance:** https://greersteel.eoxs.com
   - **Key Contacts:** 7 total
     - Joe Brom (ohiostripsteel.com), Matt Hopkins, Aronn Palmer
   - **Status:** ONLY client showing Q-o-Q GROWTH in Q3
   - **Status:** Strong performer

### 6. **PPC Metals (formerly PPC Specialty Metals)**
   - **Slug:** ppc-metals
   - **Domain:** ppcmetals.com
   - **Odoo Instance:** https://ppc.eoxs.com
   - **Key Contacts:** 9+ total
     - Crystal McDaniel, David Prychodko, Eddie Poindexter, James Baker, Todd Twitty
   - **Status:** At-risk account with 30%+ Q-o-Q revenue decline (Q2→Q3)
   - **Relay Inboxes:** info.ppcmetals@gmail.com, ppcspecialty@gmail.com

### 7. **Brannon Steel**
   - **Slug:** brannon-steel
   - **Domain:** brannonsteel.com
   - **Odoo Instance:** None (no Odoo instance)
   - **Key Contacts:** 5 total
     - David Brannon, Kevin Brannon (K.R.), Manish Trivedi, Ranim Fallaha
   - **Status:** No active implementation

### 8. **RW Conklin Steel**
   - **Slug:** rw-conklin-steel
   - **Domain:** conklinsteel.com
   - **Odoo Instance:** None (no Odoo instance)
   - **Key Contacts:** 4 total
     - Philip Conklin, Pete Conklin, Hannah Bowens, Sales team
   - **Status:** No active implementation

### Q2-Q3 2026 Performance Metrics
- **Q3 Retention Rate:** 86% (6 of 7 Q2 customers remained active)
- **Churned Client:** Hansen Metallurgical Services
- **Revenue Trend:** Aggregate Q2→Q3 -29% decline
- **Order Frequency Drop:** 2.8 orders/quarter (Q2) → 2.0 orders/quarter (Q3)
- **Growth Client:** Only Greer Steel showed positive trend
- **At-Risk Accounts:** Sabre Alloys, Discount Pipe & Steel, PPC Metals (all with 30%+ decline)

---

## EMPLOYEES & INTERNAL TEAM STRUCTURE

### Core AskCruz Team

**Key Leadership & Technical Staff:**
1. **Rajat Jain** - Employee ID 77
   - Email: rajat@askcruz.com
   - User ID: 6
   - Status: Active

2. **Sheenam** - Employee ID 75
   - Title: PR and Branding Head
   - Department: PR/Marketing
   - Email: sheenam@askcruz.com
   - Phone: +91 99882 93696
   - Manager: User ID 19
   - Contract: Active (ID 27)
   - Job ID: 16

3. **G Nijjamudin** - Employee ID 78
   - Status: Active
   - Company: AskCruz

### Intern Team (QA/Testing)
- **Yash** - QA Engineer
- **Shubham** - QA Lead
- **Stefan** - Test Validator
- **Recent Offlive:** Tanvi (AI Intern), Kriti Jain, Dhanshree

### Development/Implementation Team
**Notable Implementation Task Owners/Contributors:**
- **Hashir Saleem** - Lead developer, task owner on Purchase Order Intake, weight/width issues
- **Dhrup** - Warehouse/packing logic developer
- **Nijamuddin (G Nijjamudin)** - QA specialist
- **Humaira Zainab** - QA/bug triage
- **Aryan Bakshi** - Implementation support
- **Kartikey Tripathi** - Packing error prevention completed
- **Tapish Sharma** - Sales order workflow
- **Dev Team (generic)** - Multiple task owners

### Projects Managed Internally

**GTM Projects:**
1. **GTM - PR Board** (Project ID 23)
   - User: ID 17
   - Active timesheet tracking

2. **GTM - LinkedIn Outreach** (Project ID 21)
   - User: ID 18
   - Outreach campaign management

3. **GTM - Email Marketing** (Project ID 20)
   - User: ID 18
   - Campaign tracking

---

## IMPLEMENTATION ROADMAP

### Active Implementation Projects

**Discount Pipe & Steel (79 Active Tasks)**
- **Highest complexity client**
- **Key Challenge Areas:**
  - Purchase Order receiving workflow bugs
  - Packing slip error prevention (3-part initiative)
  - Inventory tag corrections
  - Sales order to quote conversion flow
  - Reporting and filtering capabilities
  - Weight/dimension discrepancies
  - Email & QuickBooks integration needs
  - Bank reconciliation
  - Refunds and returns workflow
  - Duplicate handling

- **Task Stages:**
  - Requirement: 40+ tasks (ongoing specification)
  - DPS Decision: 5 tasks (awaiting client decision)
  - DPS Sandbox Review: 4 tasks (client environment testing)
  - Assigned/In Progress: 8 tasks
  - Code QA: 3 tasks
  - Functional QA: 3 tasks
  - Completed: 1 task (Packing Error Prevention)
  - Communicated: 6 tasks (awaiting action)

**Eastern States Steel (Phase 1)**
- Purchase Order Intake (Intake stage)
- Weight display corrections
- Tax label standardization
- BOL (Bill of Lading) value corrections

---

## KEY BUSINESS METRICS & OBSERVATIONS

### Revenue Health
- **Overall Trend:** -29% Q-o-Q contraction (Q2→Q3)
- **Only Growth:** Greer Steel (Ohio Strip Steel)
- **Churn Rate:** Low (14% - 1 of 7 customers)
- **High-Risk Clients:** 3 of 7 active clients declining 30%+
- **Order Velocity:** Declining (2.8→2.0 orders/quarter)

### Operational Focus Areas
1. **Inventory & Warehouse Management** - Critical for steel/metals business
2. **Order Processing Accuracy** - Multiple error prevention initiatives
3. **Integration Needs** - Email, QuickBooks, Aircall, Klaviyo
4. **Reporting Capabilities** - Custom dashboards for clients
5. **Financial Reconciliation** - Bank and inventory reconciliation

### Technology Stack Insights
- **Custom Development:** Significant Odoo customizations for warehouse/packing workflows
- **No Standard Sales Module:** Custom quote→order flow implementation
- **Unique Business Logic:** Tag-based inventory system, scan workflows, yard/warehousing structure
- **External Integrations Needed:** Email, banking, CRM (Aircall), marketing (Klaviyo)

---

## DATA ACCESS NOTES

### Information Limitations
- **Sales/Invoicing:** No access (Sales/Accounting modules not installed)
- **Support Tickets:** Limited access (separate system)
- **Full Financial Data:** Amounts automatically redacted in queries [restricted: amount]
- **Intern-Level Access:** Current data retrieval at tier 2 permission level
- **Escalation Available:** SQL query tools for eoxs-teams can be provisioned for deeper analysis

This represents the current operational status of AskCruz as of October 2026, focused entirely on Odoo-based HR and project management infrastructure serving the metal/steel fabrication industry.

## User (2026-10-07 13:08:16 EDT)

is this thread getting saved?

## Claude (2026-10-07 13:08:16 EDT)

Yes! Your thread is being saved. I called `save_chat_transcript` at the end of my previous response, which archived:
- Your initial request for AskCruz information
- My comprehensive breakdown (the long response with all the clients, employees, architecture details)

And I'm saving this current exchange now as well. Per your preferences, I save **every single turn** — including short replies like this one — with the complete conversation history maintained.

All messages are being stored with a persistent thread ID (`askcruz-comprehensive-overview`) so the entire conversation stays together.

## User (2026-10-07 13:13:06 EDT)

give me everything you know about the sabre alloy client . when was the deal signed with them?

## Claude (2026-10-07 13:13:06 EDT)

# **Sabre Alloys: Deep-Dive Client Profile**

## **COMPANY DETAILS**

**Client ID:** 1 (Original/First Client)  
**Domain:** sabrealloys.com  
**Odoo Instance:** https://sabre.eoxs.com (Database: `sabre`)  
**Status:** **At-risk account — -30%+ Q-o-Q revenue decline (Q2→Q3 2026)**

---

## **CONTACTS (9 Total)**

| Name | Email | Role/Notes |
|------|-------|----------|
| **Charles White** | cwhite@sabrealloys.com | — |
| **Christi** | christi@sabrealloys.com | — |
| **Ernie Valdez** | evaldez@sabrealloys.com | — |
| **Jesus Rios** | No email | — |
| **Jim (Zeigler)** | jim@sabrealloys.com | — |
| **Juan Deshon** | No email | Active operational contact; EOXS meetings (Raj coordination) |
| **Michael Mercadante** | michael@sabrealloys.com | — |
| **Tye Webb** | tye@sabrealloys.com | Claude AI access provisioned (Sep 1, 2026); IRIS connector user |
| **Relay Inbox** | info.sabrealloys@gmail.com | Central inbox routing |

**Key Contacts for Support:**
- **Juan Deshon** — Operational lead (appears in 114+ call transcripts with Raj Jain)
- **Tye Webb** — Technical/AI initiatives
- **Charles White** & **Ernie Valdez** — System users (training references)

---

## **IMPLEMENTATION TIMELINE**

**Estimated Deal Signature:** Q1 2024 (Jan-Mar)  
- Earliest reference: "Go-Live Preparation (Q1 2024)"
- First major tasks: April 2024 (Soft Launch phase)
- Full launch: May 2024 onwards

**Explicit dates from tasks:**
- **April 2024:** Field renames, processing module setup, control tag data integrity
- **May 2024:** Payment terms, return order handling, third-party processing workflow
- **June 2024:** Major workflow refinements, weight/UOM fixes, costing finalization
- **2024–Present:** Continuous bug fixes, feature requests, system refinements

---

## **SYSTEM ACTIVITIES & SCALE**

| Metric | Volume | Last Activity |
|--------|--------|---|
| **Implementation Tasks** | 200 total | Oct 6, 2026 (Reservation discussion) |
| **Email Threads** | 1,555 total | Recent: PR/LC/SO tracking |
| **Recorded Calls** | 114 total | Oct 6, 2026 (Reservation discussion) |
| **Wiki Pages** | 140+ | Extensive documentation across all areas |

---

## **RECENT TASK STATUS (Last 20 Tasks)**

**Most Recent (Jun 2024 onwards):**

| Task Name | Stage | Owner | Date |
|-----------|-------|-------|------|
| Demanded weight editable in processing order | **Need Discussion** | Ron Jain | Jun 18, 2024 |
| In quotation screen put these things in three dots | Completed | Dhrup | Jun 14, 2024 |
| Educate Charles & Ernie on Restock format | Completed | Ron Jain | Jun 12, 2024 |
| Error while downloading PO | Completed | Dhrup | Jun 12, 2024 |
| Add Customer name & Operated by in Processing list | Completed | Dhrup | Jun 12, 2024 |
| Header order required field for SO conversion | Completed | Dhrup | Jun 12, 2024 |
| Control Tag to Inventory | Completed | Dhrup | Jun 8, 2024 |
| P&L renaming in sales order | Completed | Ron Jain | Jun 8, 2024 |
| AR/AP Discrepancy | **Urgent** | Jesus R. | Jun 7, 2024 |
| Landed cost validation in processing | Completed | Arun Kaul | Jun 4, 2024 |

**Pattern:** Most tasks completed quickly; very active support cycle throughout 2024.

---

## **CRITICAL ACTIVE ISSUES (Sep-Oct 2026)**

### **High-Priority Bugs (Unfixed)**

1. **Blanking Processing Order Errors** (Recurring, 10+ instances)
   - PR7148, PR7320, PR7386, PR7400, PR7560, PR7568, PR7628, PR7670, PR7709, PR7798, PR8014
   - Date range: Aug 2026 – Oct 2026
   - Impact: Orders fail to confirm/process
   - Status: Pattern unresolved; individual errors fixed but recur

2. **Landed Cost Distribution Bug** (Critical)
   - Affects multi-line receipts: LC/5722, LC/5689, LC/6081
   - Issue: Secondary freight recalculates existing plate line values incorrectly
   - Date: Aug–Oct 2026
   - Oct 1 claim "All Addressed" contradicted by new recurrence Oct 6
   - Now escalated to Rajat Jain for investigation
   - Workaround: Manual $/lb GL corrections on 17+ lots needed in parallel

3. **Packing List Confirmation Errors** (Multiple)
   - "Cannot Confirm PL" errors on transfers: B/OUT/11363, 11364, 11733, 11833, 12163, 12231, 12255, 12269, 12441
   - Date: Aug–Oct 2026
   - Overlap with "Record Does Not Exist" fix (Hashir committed to landing fix by "next Tuesday" — Sep 24, but timeline unclear)
   - Same underlying bug, different timelines given to Discount Pipe Steel

4. **Gross Profit (GP) Calculation Errors** (Recurring)
   - SO-22940 (Hendrix Specialty Fabrication): GP off, unconfirmed (Sep 29)
   - SO-23017 (Metal Supermarkets Houston SW): GP miscalculated, second this week (Oct 1)
   - SO-23008 (Rhyno Valve Co): GP miscalculated (Oct 2)
   - Pattern: Same issues plagued 2025–2026 (manual recalculation project ran Sept 2025–Aug 2026)

5. **Invoice Payment Terms Silent Revert** (Unresolved)
   - INV/2026/1937: Terms reverting to NET30 silently
   - Date: Jul–Sep 2026
   - Root cause never identified

### **System Errors (One-Off Reports)**

- **Duplicate Tags Blocking Receiving** (B/IN/03994, Oct 1)
- **Lot/Serial Discrepancy** on PLATE A240 3" (Oct 2)
- **Unit-of-Measure Mismatch** inflating prices on receipts (Aug 26)
- **Missing/Untraceable Tags** written off to inventory (Sep 14, Oct 5)
- **EOXS IRIS Claude Connector Fails** for Tye Webb (Oct 5) — reconnected by Ron, client-side fix unconfirmed
- **Daily Backup Failure** (Oct 4) — escalated to DevOps; one escalation address bounced
- **Processing Module Cost-Change Bug** on control tag (Oct 2–5, resolved)

---

## **OPERATIONAL INTELLIGENCE**

### **Business Model**
- **Specialty:** Metal fabrication (plates, blanking, waterjet processing)
- **Key Customers:** Rhyno Valve Co, Granite Peak Fabrication, Tex-Fab Inc., Metal Supermarkets, Addison Fabricators, Hendrix Specialty Fabrication
- **Operations:** Toll processing, third-party processing, freight consolidation (load scheduler)

### **Unique Features Deployed**
- **Control Tag System** — Inventory tracking with lot/serial management
- **Processing Module** — Custom order flow for toll/third-party work
- **Landed Cost Automation** — Freight and material cost allocation
- **Material Test Report (MTR)** — Product spec tracking
- **Long Product Weight Calculations** — UOM-aware weight & pricing for linear materials
- **Fully Billed PO Status** — Workflow to mark purchase orders completed after invoicing

### **Historical Milestones**
- **Q1 2024:** Go-live prep
- **Apr–May 2024:** Soft launch with extensive field renames & workflow setup
- **Jun 2024:** Major costing & profitability finalization
- **Jul 2024–Present:** Continuous refinement; support volume remains high
- **Aug 2026:** Multi-engineer onboarding; "Sabre 2" AI proposal scoping
- **Sep 2026:** 30 concurrency tickets in 3 months triggers new processing module proposal (decision pending)
- **Oct 2026:** Ongoing escalations (Landed Cost, GP calculations, backup failures)

---

## **KEY PERSONNEL**

**AskCruz Side:**
- **Ron Jain** — Task owner, appears heavily in training & process docs
- **Raj Jain** — Lead engagement; Juan Deshon coordination calls (114+ recorded)
- **Hashir Saleem** — Developer (committed to packing-list fix timeline)
- **Dhrup** — Processing module & workflow developer
- **Nijamuddin** — QA tester
- **Arun Kaul** — Costing specialist

**Sabre Alloys Innovation Track:**
- **AI Access Provisioned** to Juan & Tye (Sep 1, 2026)
- **Toll Processing Business Discussion** (Oct 2026)
- **"Sabre 2" AskCruz Proposal** — AI agent / automation expansion (Aug–Sep 2026)

---

## **FINANCIAL & PERFORMANCE NOTES**

**Q3 2026 Status:**
- **Revenue:** Down 30%+ Q-o-Q
- **Order Velocity:** Declining
- **Churn Risk:** High (flagged as "at-risk" in portfolio)
- **Support Intensity:** Very High (1,555 emails, 114 calls, 200 tasks, 140+ wiki pages)

**Outage/Incident History:**
- **Hack Incident** — Legal case evidence package sent to counsel (Sep 2026)
- **Outage-Credit Dispute** — Separate negotiation track
- **Daily Backup Failures** — Recent (Oct 2026)

---

## **NOTABLY UNRESOLVED/OPEN ITEMS**

1. **Order Lost Feature** (open since Jan 2024 — 21+ months!)
2. **New Processing Module Scope/Timeline** (30 concurrency tickets; decision pending as of Sep 2026)
3. **Blanking Processing Order Root Cause** (recurring pattern not fixed)
4. **Landed Cost Distribution Algorithm** (fundamental bug recurring despite patches)
5. **Fully Billed PO Payment Terms Reset** (root cause unidentified; affects invoicing workflow)

---

## **WHEN WAS THE DEAL SIGNED?**

**Precise signature date not in system records.** However, timeline indicators suggest:
- **Q1 2024** = Go-Live Preparation phase (Jan–Mar 2024)
- **April 2024** = Soft launch begins
- **Likely Deal Signature: Jan–Mar 2024** (before soft launch)

The earliest task is "Go-Live Preparation (Q1 2024)" from the wiki, which implies the contract was already signed by then. To get the exact date, you'd need to check:
- Sales CRM records (not in current Odoo instance)
- Contract documents in EOXS vault
- Email thread with Juan Deshon or Raj Jain (pre-April 2024)

---

This client represents **AskCruz's oldest, most complex, and currently most troubled account** — deep implementation, high support volume, recurring critical bugs, and declining revenue.
