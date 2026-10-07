---
conversation_id: askcruz-comprehensive-overview
platform: claude
username: "shubham"
title: "AskCruz Comprehensive Overview - Architecture, Clients & Employees"
created_at: "2026-10-07 13:06:25 EDT"
updated_at: "2026-10-07 13:06:25 EDT"
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
