---
conversation_id: 59760963-4d17-467d-990d-183cc0bebc20
platform: claude
username: "shubham"
title: "Sabre alloys details - Claude"
created_at: "2026-10-10T14:56:43.755Z"
updated_at: "2026-10-10 12:24:33 EDT"
---

# Sabre alloys details - Claude

## User (2026-10-10 12:24:33 EDT)

can u give me detail about the sabre alloys\

## Claude (2026-10-10 12:24:33 EDT)

Sabre Alloys is not a 3GM customer in the data I could reach. It is an EOXS Team client that runs on EOXS’s Odoo system, and the connected vault is EOXS’s AskCruz wiki, not the 3GM Vault. The 3GM Vault tools (whoami, find_facts, search_raw) weren’t available in this session, so I used AskCruz. If you meant a 3GM relationship, tell me and I’ll look again.

Who they are

Company domain: sabrealloys.com. Main contacts include Charles White, Ernie Valdez, Tye Webb, Michael Mercadante, Jim Zeigler and Juan Deshon.
Their EOXS implementation dates from April 2024 (soft launch). It has about 200 implementation tasks, 1,614 emails and 117 recorded calls.

Sales (ERP, USD, including tax)

35 confirmed or completed sales orders, from 9 Jan 2024 to 5 Oct 2026, totalling about $404,265.
The ERP partner record is “Sabre Alloys” (id 353530). A separate “Sabre Steel, Inc.” and “Manitex Sabre” also exist and are not the same company.

Main work on their system

Processing module (blanking/processing orders), control tags, costing and gross-profit calculations, landed-cost allocation, freight, and purchase-order “fully billed” status.

Open issues as of early October 2026

Blanking processing order PR8010 has a restock-cost error, unresolved for over three hours and escalated on 7 Oct.
Repeated “Cannot Confirm PL” errors on packing-list transfers.
A landed-cost distribution bug on LC/6081 and LC/6083. A fix was claimed deployed on 8 Oct but is pending client confirmation.
Gross-profit miscalculations on several sales orders (SO-23008, SO-23017, SO-22940).
A daily backup failure alert on 4 Oct.
Claude connector access problems for one of their users (5 Oct).
A reservation call on 6 Oct, with Hashir Saleem named as task owner.
A proposal for a further AskCruz engagement, with installments scheduled 3 Sep to 7 Oct 2026. Amounts are restricted in the wiki, so I haven’t quoted them.

Caveat: The ERP query ran against EOXS Team Live (database Eoxteams_12Feb24). The client profile lists a different Odoo database (“sabre” on sabre.eoxs.com), so the sales figures may not reflect the full client record.

Sources: AskCruz client profile “sabre-alloys” (id 1) · wiki pages 77 (Sabre Alloys), 774 (Invoice History), 2302 (Negative Unit Cost, Process 7839), 2053 (AskCruz Proposal) · email thread 70119, 70584 · call 2521 (6 Oct 2026) · ERP res_partner 353530, sale_order (partner 353530, state sale/done)
