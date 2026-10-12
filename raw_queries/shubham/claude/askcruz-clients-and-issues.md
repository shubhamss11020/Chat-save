---
conversation_id: c054066d-fa12-4755-942c-4da00c98f776
platform: claude
username: "shubham"
title: "Askcruz clients and issues"
created_at: "2026-10-09T15:18:29.384110Z"
updated_at: "2026-10-12 10:35:29 EDT"
---

# Askcruz clients and issues

## User (2026-10-12 10:35:29 EDT)

can u give me the information about all the clients of askcruz and also represent all the issues they are facing

## Claude (2026-10-12 10:35:29 EDT)

I'll pull the client list from Askcruz first, then look at each client's profile, calls, and emails to find the issues they're facing.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```





```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```










I have the overview for all 8 clients. A few of them (Conklin, Brannon, Ohio Strip Steel) have thin issue data in their profiles, so I'll read their key wiki pages to fill the gaps.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```





```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```


Askcruz has 8 clients. Six run EOXS (Odoo) instances, and two (Brannon, Conklin) have no instance listed. The issues below come from the client wiki pages, implementation tasks, and recent emails and calls, as of Oct 9, 2026.

## Overview

| Client | Relationship | Size of issue load | Biggest themes |
|---|---|---|---|
| **Sabre Alloys** | EOXS ERP, plus AskCruz proposal | Very high | Processing/blanking errors, landed cost, GP miscalculations, packing list errors |
| **Discount Pipe & Steel (DPS)** | EOXS ERP | Very high (233 tasks) | Reservation and packing list bugs, stalled deliverables, billing dispute |
| **Eastern States Steel** | EOXS ERP | High (226 tasks) | Control tags, weights, warehouses, printers, slowness |
| **3GM Steel** | EOXS ERP, AskCruz customer | High | Invoicing and phantom credits, PO receiving bug, product creation |
| **PPC Metals** | EOXS ERP (Velox) | Medium | Platform slowness and delays, reservations, tag costs |
| **Brannon Steel** | MTR AI project | Low | Status conflicts on the MTR module |
| **Ohio Strip Steel** (formerly Greer Steel) | EOXS CRM, AI expansion talks | Low | No open bugs, but new integration needs |
| **RW Conklin Steel** | EOXS ERP | Dormant | Churn risk and contract dispute |

## Client details

**Sabre Alloys** (9 contacts, 200 tasks, 117 calls, 1,600+ emails). This client has the most open friction.
- **Processing:** blanking processing order errors recur (PR7148 through PR8014). PR8010's restock-cost error was unresolved for more than 3 hours and escalated on Oct 7.
- **Landed cost:** multi-line distribution bugs on LC/5722, 5689, 6081 and 6083. An Oct 1 "all addressed" claim was contradicted twice, and a fix deployed to live on Oct 8 is awaiting client confirmation.
- **Gross profit:** GP is miscalculated on several sales orders (SO-23008, SO-23017, SO-22940).
- **Packing lists:** "Cannot Confirm PL" errors keep recurring, including three in one hour on Sep 22.
- **Stability:** a wave of errors across 7 transactions on Oct 1 prompted the client to ask whether a recent update caused it. A daily backup failure alert fired on Oct 4, and one escalation address bounced.
- **Commercial:** the Feb 2026 cybersecurity outage credit dispute was verbally resolved on Jun 15, but the source pages contradict each other on this. A new Processing Module request, prompted by 30 concurrency tickets, is stuck awaiting a decision. The AskCruz proposal has data-privacy pushback.

**Discount Pipe & Steel** (10 contacts, 233 tasks, 717 emails).
- **Reservations and control tags:** these keep failing, with three tag-reservation errors in about 25 minutes on Sep 22. An emergency live push happened in August over double-selling.
- **Packing lists:** confirmation failures, quantity discrepancies and "Record Does Not Exist" errors (Sep 29).
- **Refunds and Returns:** the feature was deployed, then hit session-timeout and sales-order save errors.
- **Stalled work:** the Aircall and Stripe integrations and the training videos have been stalled for months and were escalated to leadership.
- **Commercial:** there is a bank reconciliation module billing dispute, and an Aug 18 check-in raised ROI concerns.
- **Smaller bugs:** filter persistence was marked done, then contradicted. Sticker label fixes were reverted after failing QA. Stripe payments were misapplied to one customer's account.

**Eastern States Steel** (7 contacts, 226 tasks).
- **Control tags:** coils received against PO P00860 show zero weight (Sep 23).
- **Packing and transfers:** an accidental packing list confirmation on ESSPA/OUT/01366 blocks a sales order address change (Sep 28).
- **Margin:** the margin on S02189 is wrong after a price correction, and Ryan wants self-service training.
- **Warehouses:** several new third-party warehouse requests (Sep 23 and Sep 25).
- **Inventory and quotes:** inventory valuation is stalled pending a full physical count. A quote-to-sales-order confirmation error is suspected to be a warehouse or coil configuration problem.
- **Hardware and speed:** the Zebra printer has been down since Aug 27, and screen-to-screen latency was reported on Aug 21.
- **Competitor:** CloudForge AI reached out to them at Steel Summit in August.

**3GM Steel** (3 contacts, 34 tasks).
- **Invoicing:** phantom and duplicate customer credits block payment application. Four invoices have problems: INV/2026/2403 is still unresolved after a second escalation, INV/2026/2434 has a total mismatch, INV/2026/2276 is only partly corrected, and 12 coils invoiced under INV/2026/2246 still show as available.
- **POs and inventory:** four POs (P04612 to P04615) hit a "confirmed but can't receive" bug. A coil-upload error recurs, coil search on the tonnage card is buggy, and a transfer error (SRTI./OUT/03994) is still open.
- **Support answers:** one pre-2022 sales order history reply was self-contradictory.
- **Recurring work:** a steady stream of product variant creation requests.
- **Positive:** the AskCruz deal closed at a reduced 2-user scope, with the final implementation invoice and first licensing payment sent. The AskCruz customer story draft is out for review.

**PPC Metals** (29 tasks, 485 emails).
- **Performance:** "Slow EOXS" and "DELAYS IN EOXS" emails arrived Oct 6 to 8. A cache clear fixed it briefly, but slowness persists and was escalated to dev again on Oct 8. A "Trying to reconnect" issue appeared in August.
- **Other:** reservation conflicts on the same tag, a tag cost correction with an inventory valuation concern, product description and variant errors, and a packing slip weight discrepancy.

**Brannon Steel** (5 contacts, no implementation tasks, 29 weekly "Implementation Huddle" calls).
- Weekly MTR AI huddles continue, and a signed Algoma join and pre-purchase MTR-spec verification work started Sep 14.
- An internal escalation says the MTR Inventory Module has been stalled 2+ months, while ticket T06332 shows "QA Passed". It's unclear which is correct.
- Brannon's Manish Trivedi is being used as a reference for Ohio Strip Steel.

**Ohio Strip Steel** (formerly Greer, 106 tasks, mostly completed).
- No active bugs. Recent activity is licensing (2 new licenses, an access removal) and an expansion opportunity. Joe Brom's new IT hire and consultant want an ERP/AI overview. They also want a bridge between EOXS and their production/ERP system.
- A 4-way scoping call has been proposed, and the Oct 7 call isn't summarized yet. The client's earlier "Map error" report is the only recent defect.

**RW Conklin Steel** (4 contacts, no tasks, last activity around March 2025).
- This is a high churn risk. After go-live, only sales and purchase orders were entered, with no invoicing, reporting or reconciliation. The client tried to cancel in August 2025, and a settlement was offered. Billing continued anyway, so the contract's actual status is unresolved. Wiki pages flag the client's financial distress, so I left the financial details out of this summary.

## Cross-client patterns
1. **Packing list and control tag errors** hit Sabre, DPS, Eastern States and PPC. They look like one shared root cause. Hashir committed to a fix for the "Record Does Not Exist" error, but the timeline Sabre was given differs from DPS's.
2. **Landed cost, GP and valuation errors** are concentrated in Sabre, 3GM and Eastern States.
3. **Performance and stability** problems are showing up at PPC, Eastern States and Sabre.
4. **Fixes marked "done" that then recur** (Sabre landed cost, DPS filter persistence, DPS labels) are eroding trust.
5. **Support responsiveness** is a theme: stalled DPS deliverables, Sabre's multi-day chases, and escalations that bounce.

## Caveats
- Much of this is from wiki page titles and summaries, not every underlying ticket. Some pages contradict each other, and I've noted where.
- Support tickets and invoices live in EOXS Teams Odoo, not in Askcruz, so I haven't seen live ticket counts.
- I can turn this into a shareable document, or pull the open ticket counts per client from Odoo.

Sources: Askcruz client profiles for all 8 clients, plus wiki pages on RW Conklin contract dispute, Brannon MTR Inventory Module escalation, Ohio Strip Steel ERP/AI overview request, and Sabre Alloys Outage-Credit Dispute.
