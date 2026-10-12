---
conversation_id: 9175cc2e-288a-4296-8583-cae03999e664
platform: claude
username: "shubham"
title: "Invoice data availability"
created_at: "2026-10-08T12:26:12.876689Z"
updated_at: "2026-10-12 12:35:03 EDT"
---

# Invoice data availability

## User (2026-10-12 12:35:03 EDT)

what invoice related data  can you show me

## Claude (2026-10-12 12:35:03 EDT)

```

```

```

```

```

```

```

```

```

```

No `eoxs-teams` connector tools are present in this conversation — only the Askcruz tool set loaded. Askcruz itself has no invoice data (that moved out in 2026-08); invoices/sales orders live only on the `eoxs-teams` live Odoo connector, which isn't connected here.

**What I can actually show you right now:**
- Nothing invoice-specific — Askcruz has no invoice/billing tools.
- I can check Askcruz for any invoice-related *correspondence* (emails/calls mentioning an invoice, a client's billing discussion) if you want.

**What you'd need for real invoice/sales-order data:** the `eoxs-teams` connector (Odoo). It's not showing up in my tool list for this session.

Want me to:
1. Search Askcruz emails/calls for invoice mentions on a specific client, or
2. Have you check/enable the eoxs-teams connector so I can query actual invoice records?

## User (2026-10-12 12:35:03 EDT)

dont you have any invoices related data present in the Ask cruz mcp you can find me ?

## Claude (2026-10-12 12:35:03 EDT)

```

```

Yes — Askcruz does have invoice-related material, just not through a dedicated "invoice" tool. It's synthesized into per-client wiki pages (correspondence/support-ticket history, not live Odoo sales-order data). Found dedicated **"Invoice History"** pages for several clients:

| Client | Page | Notes |
|---|---|---|
| Sabre Alloys | Invoice History | Monthly licensing invoices; Settlement Credit from Feb'26 outage (amounts restricted) |
| PPC Metals | Invoice History | Register incl. INV/2026/0157, INV/2026/0397 |
| Discount Pipe & Steel | Invoice History | Register, account-manager transition noted |
| RW Conklin Steel | Invoice History | Register table: Invoice #, Date, Amount, Line Items, Status |
| 3GM Steel | Invoicing & Billing | Includes example invoice INV/2022/0739 w/ attachment |

Plus related pages: **support-ticket invoice bugs** (3GM Steel, PPC Metals, Discount Pipe & Steel, Sabre Alloys — recurring defects like weight/footage mismatches, aging-report decimal bugs, draft invoices that won't re-post) and **internal finance email archives** (EOXS's own outbound customer invoicing cadence, vendor invoice disputes).

Note: all dollar amounts come back as `[restricted: amount]` — that's a fixed redaction on this connection, not something I can lift.

Want me to pull a specific client's full Invoice History page (e.g. RW Conklin Steel's register), or dig into the recurring invoice bugs on one of these accounts?

## User (2026-10-12 12:35:03 EDT)

okay , do you find any monthly license related data and you dont need to give me any full ammount let me know if you have any per person or per seat data on you.

## Claude (2026-10-12 12:35:03 EDT)

```

```

Yes — per-seat/per-user licensing structure (not dollar figures) shows up for several clients:

| Client | Seat structure |
|---|---|
| **PPC Metals** | 5 licensed users — one seat (part-time employee) fully waived/free. Described as the highest per-seat rate in the EOXS six-client portfolio. |
| **Discount Pipe & Steel** | 7–10 users, licensing billed per-user starting Aug 2025; a user swap recorded (Lacee Hulsey added mid-2026). |
| **3GM Steel** | 15 base users at a flat per-user/month rate, with additional seats layered on top; users added in increments of 5; license price tier changed Aug 2025 (old rate 2022–mid-2025, new rate after). |
| **Eastern States Steel** | 6 licensed seats, confirmed across 3 invoices (Jan '26, and two from 2025). |
| **Brannon Steel** | Per-seat charge + separate one-time implementation fee, scoped against a 32-engineer / 8-month deployment. |
| **Sabre Alloys** | Monthly licensing invoices referencing per-seat rows (S00168/S00179) — tied into a Settlement Credit after a Feb 2026 outage. |

Structural notes (no amounts):
- 3GM Steel's contract has a **3-year term with a 6% annual renewal-increase cap** and an hourly overage rate for extra work.
- PPC Metals' free seat was a verbal waiver from Rajat Jain, not standard policy.

Want me to pull the full seat-count/rate history for one specific client (e.g., 3GM Steel's old-vs-new per-user rate timeline, still redacted on amounts), or the support-ticket side of any of these (billing bugs tied to seat counts)?
