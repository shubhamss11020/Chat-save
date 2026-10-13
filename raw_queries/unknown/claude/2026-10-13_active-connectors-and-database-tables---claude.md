---
conversation_id: cca394f3-6816-4161-896a-28430acd036c
platform: claude
username: "unknown"
title: "Active connectors and database tables - Claude"
created_at: "2026-10-13 10:37:08 EDT"
updated_at: "2026-10-13 10:37:08 EDT"
---

# Active connectors and database tables - Claude

## Claude (2026-10-13 10:37:08 EDT)

I queried both active database connectors, and “the db” could mean either, so here are both. Neither is 3GM’s ERP. That one is the “3gm odoo” connector, which is off in this chat.

1. Eoxs-Teams: EOXS Team Live (Odoo 13), 776 tables

Database Eoxteams_12Feb24, a steel distribution and operations company, with amounts in USD.

Sales and purchasing
sale_order, sale_order_line, sale_order_template*, sale_order_option
purchase_order, purchase_order_line
product_pricelist*, product_supplierinfo
Accounting
account_move, account_move_line, account_payment, account_journal
account_tax*, account_analytic_*
account_asset_*, account_bank_statement*
Report wizards such as account_aged_trial_balance and account_cash_flow
Inventory and products
stock_picking, stock_move, stock_move_line, stock_quant, stock_production_lot
stock_warehouse, stock_location, stock_valuation_layer
product_template, product_product, product_category
existing_mrp is the only manufacturing-related table.
CRM and partners
res_partner, res_partner_*, crm_lead, crm_stage, crm_team, crm_phonecall*
vrm_* (vendor leads), mailing_*
HR and payroll
hr_employee, hr_contract, hr_attendance, hr_leave*
hr_payslip*, hr_salary_rule*, hr_expense*
hr_applicant, hr_recruitment_*, emp_training_*
Projects and documents
project_project, project_task*
documents_*, survey_*, slide_* (eLearning), blog_*, website_*
Custom and integrations
x_* custom fields: x_business, x_icp, x_erp, x_annual_revenue, x_no_of_employees
eoxs_monitor_config, ringcentral_sync, rest_api*, db_backup, ks_dashboard_ninja_*
System: ir_*, res_*, mail_*, base_* and wizard tables.
2. Read-only: AskCruz (Odoo 13 Community), 546 tables
Core, per its own context note: HR, Project and Training.
res_partner, project_project, project_task, project_task_type
hr_employee, hr_department, hr_job
emp_training_center, emp_training_application*, emp_training_class_room
AskCruz custom
askcruz_li_* is a LinkedIn import set covering post, skill, experience, education, reaction, recommendation and others.
askcruz_job_position*, askcruz_connected_via*
HR extras
hr_approval_*
hr_holdback_* (cycle, entry, settlement review)
hr_offboarding_checklist*, hr_subscription*, hr_document_category
Standard modules
crm_*, account_*, product_*, sale_order*, slide_*, mail_*
res_*, ir_*, utm_*, website_*
Discrepancy
The AskCruz connector’s context note says the sale, purchase and account apps are not installed, with no sale_order, account_move or product_template. The table list does contain sale_order, account_move and product_template. The note may be outdated, or these may be empty leftover tables. I haven’t checked row counts.

I can write both full lists to a file, or describe a specific table (for example sale_order) with its columns.

## User (2026-10-13 10:37:08 EDT)

show me the           sales and purchasing table data of september month

## Claude (2026-10-13 10:37:08 EDT)

Claude responded: I'll pull September 2026 sales and purchase orders from the EOXS Team Live database, starting with the table columns.
Identifying the relevant sales and purchasing data source.
Identifying the relevant sales and purchasing data source.

I’ll pull September 2026 sales and purchase orders from the EOXS Team Live database, starting with the table columns.

Used Eoxs-Teams

Used Eoxs-Teams

September 2026 has 3 sales orders totaling $12,997.85 and no purchase orders. The purchase_order table is empty for all dates, not just September.

Order	Date (Eastern)	Customer	State	Invoice status	Untaxed	Tax	Total
S00208	Sep 4, 8:28 AM	Sabre Alloys	sale	invoiced	$10,452.00	$0.00	$10,452.00
S00212	Sep 7, 4:44 PM	Sabre Alloys	sale	invoiced	$205.85	$0.00	$205.85
S00213	Sep 24, 1:04 PM	Eastern Steel Sales	sale	invoiced	$2,340.00	$0.00	$2,340.00
Total					$12,997.85	$0.00	$12,997.85
The most recent sales order in the database is dated Oct 5, 2026, so September is fully covered.
This is EOXS’s own Team Live database, not 3GM’s ERP. For 3GM orders, enable the “3gm odoo” connector in this chat.

I can pull line items for these orders or check the invoices in account_move.

Sources: Eoxs-Teams DB, sale_order S00208, S00212, S00213; purchase_order (0 rows).

## User (2026-10-13 10:37:08 EDT)

show me every  table exist in eoxss team live

## Claude (2026-10-13 10:37:08 EDT)

Claude responded: I'll write the full list of EOXS Team Live tables to a file, since it's 776 names.
Preparing to deliver the complete table list as a file.
Preparing to deliver the complete table list as a file.

I’ll write the full list of EOXS Team Live tables to a file, since it’s 776 names.

Created a file, shared a file

Created a file, shared a file

The file eoxs_team_live_tables.txt has all 776 tables in the EOXS Team Live database, alphabetical, one per line. I copied the names from the table listing I pulled earlier and did not recount them against it.

It is the same database as the earlier September query, not 3GM’s. I can describe any table’s columns or pull data from it.

Eoxs team live tables
TXT 
Download

## User (2026-10-13 10:37:08 EDT)

do we have currently tiers implemented in our project, and working all properly ? which tier consist what data ?

## Claude (2026-10-13 10:37:08 EDT)

“Tiers” could mean several things here, so I’ll search the project knowledge sources (wiki, repo docs, implementation tasks) for it.

Tiers exist in the system but are not working properly, based on the latest evidence I found (Sep 25, 2026). I’m reading “tiers” as the access tiers in AskCruz, the Second Brain. If you meant the Bronze/Silver/Gold pricing tiers, that is a separate topic.

What is implemented

The documented design uses two vocabularies that the wiki says should not be assumed identical:

Architecture sensitivity labels: General, Company-Confidential (financials, salaries, legal, vendor pricing, investor talks, employee performance) and Raj-Personal.
Product access tags: tier1, tier2, tier2_confidential.

What each connection is documented to see:

Connection	Documented visibility
Raj	Company-Confidential + Raj-Personal
HR	Company-Confidential, with financial-detail restrictions
General staff	General business info, with financial amounts and employee performance stripped
Interns	General info only, with financial amounts stripped

Enforcement has two layers: database-level access control, plus an AI response check as defense in depth.

Which tag holds what (observed, not documented)
tier2_confidential: the Second Brain Initiative page and the Sep 2 team session, where the salary-data leak was flagged.
tier2: AskCruz product and architecture docs, the Aug 18 onboarding training, and the Sep 25 session.
tier1: I saw no page carrying this tag. The only mention is that the repo-docs search is “tier1 only”.
The product feature file says no authoritative list of tier names and permissions exists, and tells the AI not to invent any.
Is it working?

No, per these open problems:

Sep 2, salary leak: AskCruz was still surfacing June 2026 salary-structure data. A connector that should have been hidden was also visible. No fix was confirmed on that call.
Sep 2, contradicting reports: a second user was told she had no access to the same salary data, so the leak may be inconsistent across identities.
Sep 25, tag mismatch: a client-registry record returned tier 2 confidential, which didn’t match the team’s documentation. The team couldn’t tell whether an undocumented HR sub-tier exists or the record is mistagged. A task was opened and nothing was resolved.
Sep 25, no audit process: only two users have 3GM access, and no access-rights audit process exists. The client registry is also out of date, with 2 of 8 clients wrong.
What works
In my own searches, dollar amounts came back redacted as “[restricted: amount]”, so amount-stripping works for this identity.
I can’t confirm whether anything was fixed after Sep 25. The 3GM Vault connector, which would hold newer mail, is disconnected.
I can run a live test by querying salary-related data under this connection, or pull the full Sep 2 and Sep 25 call transcripts, if you want either.

Sources: wiki pages 1893 (System Architecture, Ingestion & Access Control), 1894 (Product Capabilities), 2022 (Sep 2 session), 2226 (Sep 25 session), 32 (Second Brain Initiative), 1808 (Aug 18 onboarding); calls 2426, 2427, 2509.
