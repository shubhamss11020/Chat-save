---
conversation_id: 59760963-4d17-467d-990d-183cc0bebc20
platform: claude
username: "shubham"
title: "Sabre alloys and Brannon steel - Claude"
created_at: "2026-10-10T17:40:50.789Z"
updated_at: "2026-10-10 13:40:51 EDT"
---

# Sabre alloys and Brannon steel - Claude

## User (2026-10-10 13:40:51 EDT)

can u give me detail about the sabre alloys\

## Claude (2026-10-10 13:40:51 EDT)

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

## User (2026-10-10 13:40:51 EDT)

can u give me details about brannon steel

## Claude (2026-10-10 13:40:51 EDT)

Brannon Steel is not a 3GM customer in the data I could reach. Like Sabre Alloys, it is an EOXS client. The connected vault is EOXS’s AskCruz wiki, not the 3GM Vault, and the 3GM Vault tools weren’t available in this session.

The relationship

It was won as a client in January 2026. The engagement is for MTR AI, EOXS’s material test report product, rather than the core Odoo ERP. The EOXS wiki notes a separate Odoo deployment is also in place.
Domain: brannonsteel.com. Contacts include David Brannon, Kevin Brannon, Manish Trivedi and Ranim Fallaha (the primary tester on the MTR calls).
Kickoff was 21 Jan 2026. The weekly “Implementation Huddle || Brannon Steel” ran from February 2026 and continued through at least 25 Aug 2026 (29 recorded calls).
The wiki describes a three-phase expansion roadmap. A new MTR AI engagement with Algoma Join, with pre-purchase MTR spec verification, was signed and was due to start work on 14 Sep 2026.
Other recent activity: Ayan Dutta was credited with an incentive claim for the Brannon upsell (29 Aug 2026). Manish Trivedi was offered as a reference to Ohio Strip Steel (early Oct 2026).

Open issues

The MTR Inventory Module has a conflict between the escalation and the ticket status. I haven’t checked the details.
The wiki has no implementation tasks logged for this client.

Sales (ERP)

The partner record “Brannon Steel” (id 502523) is flagged as a customer, but it has no confirmed or completed sales orders in EOXS Team Live. The relationship is the MTR AI service, not product sales, so this doesn’t mean the client is inactive.

Caveat: Deal terms and pricing sit on the CRM Record page, which I didn’t open, so I can’t give contract values.

Sources: AskCruz client profile “brannon-steel” (id 8) · wiki pages 1032 (CRM Record), 1036 (Fireflies Call Log), 1033 (MTR AI Huddles Mar–Jun 2026), 1229 (Algoma Join Report), 1283 (MTR Inventory Module) · email thread 215 · email 3051 · ERP res_partner 502523, sale_order (partner 502523, state sale/done)
