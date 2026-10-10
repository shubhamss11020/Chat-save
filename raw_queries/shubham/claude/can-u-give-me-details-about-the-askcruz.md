---
conversation_id: df776b51-60bb-4723-9bc0-29cf0c0372c8
platform: claude
username: "shubham"
title: "Brannon Steel details - Claude"
created_at: "2026-10-10T14:56:43.755Z"
updated_at: "2026-10-10 12:27:32 EDT"
---

# Brannon Steel details - Claude

## User (2026-10-10 12:27:32 EDT)

can u give me details about brannon steel

## Claude (2026-10-10 12:27:32 EDT)

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
