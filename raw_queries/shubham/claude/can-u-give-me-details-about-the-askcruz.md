---
conversation_id: df776b51-60bb-4723-9bc0-29cf0c0372c8
platform: claude
username: "shubham"
title: "Brannon steel and Sabre alloy - Claude"
created_at: "2026-10-10T14:56:43.755Z"
updated_at: "2026-10-10 12:28:13 EDT"
---

# Brannon steel and Sabre alloy - Claude

## User (2026-10-10 12:28:13 EDT)

can u give me details about brannon steel

## Claude (2026-10-10 12:28:13 EDT)

Brannon Steel is a customer in the ERP with one open invoice and no active orders. Its sales history is almost entirely cancelled.

Record: Brannon Steel, Brampton (Ontario), active, customer rank 15, no vendor role. Contact: sales@brannonsteel.com, (905) 453-4730. No credit limit set.
Open balance: one posted invoice, INV/2026/0385, dated 9 Sep 2026, for $1,356.00, fully unpaid.
Cancelled orders: S00203 ($1,356, 22 Jul), S00196 ($11,390.40, 21 May), S00189 ($4,881.60, 20 May), S00174 ($10,080, 12 Mar), S00155 ($4,320, 7 Jan). Each has a matching cancelled invoice.
Totals: one posted invoice in the system, first dated 7 Jan 2026 and last 9 Sep 2026.

Things to check:

INV/2026/0385 ($1,356) matches the amount of S00203, which is cancelled. Either the invoice came from a different order or the cancellation didn’t carry through. I couldn’t confirm which from the data I queried.
The vault (email and wiki) isn’t connected in this session, so I have no negotiation history, disputes or contacts beyond the ERP record. I can’t say why the orders were cancelled.
The 3GM navigator skill describes tables such as coil/tag and release documents, which don’t appear in this database. The database I queried is “EOXS Team Live” (Odoo 13), and I can’t confirm from here that it is 3GM’s own system.
A separate partner, David Brannon (Brampton), is also a customer with a $0 credit limit. I haven’t checked whether he’s linked to Brannon Steel.

Sources: ERP res_partner id 502523 (Brannon Steel); ERP res_partner id 502524 (David Brannon); ERP sale_order S00203, S00196, S00189, S00174, S00155 (all cancelled); ERP account_move INV/2026/0385 (posted, unpaid) and cancelled invoices for partner 502523.

## User (2026-10-10 12:28:13 EDT)

can u give me detail about sabre alloy

## Claude (2026-10-10 12:28:13 EDT)

Sabre Alloys is one of your most active customers in the ERP: 78 customer records, orders from January 2024 through October 2026, and about $20,378 open across three invoices.

Record: Sabre Alloys, Houston, TX. Phone 281-405-8580. No email on file and no credit limit set. Active, customer only.
Open balance (all posted, unpaid):
INV/2026/0409, 5 Oct 2026: $9,720.00 (from S00216, which is in “sale” state)
INV/2026/0349, 4 Sep 2026: $10,452.00 (from S00208)
INV/2026/0379, 7 Sep 2026: $205.85 (from S00212)
Recent activity: S00216 was placed on 5 Oct and invoiced the same day. Before that, orders ran at roughly one a month, mostly between $9,400 and $13,000, with a few larger ones (e.g. $22,170 in June 2024, $20,000 in January 2024).
Credit: RINV/2026/0003 (15 Jun 2026, $25,000) is a posted customer refund, fully settled.
Stale drafts: S00134 ($12,230, Sep 2025) and S00077 ($9,610, Feb 2025) are still in draft and were never confirmed or cancelled.
Cancelled: a number of invoices and orders were cancelled, mostly in 2024–2025 (e.g. S00062, $18,200, Oct 2024). Some cancelled invoices have no invoice number, which is common when an invoice is voided before posting.

Things to check:

The three open invoices total $20,377.85. The two largest ($9,720 and $10,452) were issued in the past five weeks, so they may not be due yet, but I haven’t checked payment terms because none are set on these invoices.
Two draft orders have been sitting for over a year. They should probably be confirmed or cancelled.
“Sabre Steel, Inc.” (Farmington, MI) and “Manitex Sabre” are separate partners in the ERP. I’ve only included records under Sabre Alloys.
The vault (email and wiki) still isn’t connected in this session, so I can’t tell you why any orders were cancelled or what was agreed on pricing.

Sources: ERP res_partner id 353530 (Sabre Alloys); ERP sale_order S00216, S00212, S00208, S00134, S00077, S00062; ERP account_move INV/2026/0409, INV/2026/0349, INV/2026/0379, RINV/2026/0003 and related cancelled invoices for partner 353530.
