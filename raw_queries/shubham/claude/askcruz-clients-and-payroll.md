---
conversation_id: 437a730f-1834-4e03-a3a5-ca7367c9f5d5
platform: claude
username: "shubham"
title: "Askcruz clients and payroll"
created_at: "2026-10-08T13:24:01.251200Z"
updated_at: "2026-10-12 10:58:46 EDT"
---

# Askcruz clients and payroll

## User (2026-10-12 10:58:46 EDT)

can u give me detailed description about the askcruz clients

## Claude (2026-10-12 10:58:46 EDT)

I'll pull the client registry from the Askcruz connector and check it against what's already on file.
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








All 8 Askcruz clients are steel/metals companies, and 6 of them run on their own EOXS Odoo instance. Brannon Steel (MTR AI only) and RW Conklin Steel have no instance on record. Contact counts below include relay inboxes.

| Client | Instance | Contacts | Tasks / emails / calls |
|---|---|---|---|
| Sabre Alloys | sabre.eoxs.com | 9 | 200 / 1,561 / 114 |
| 3GM Steel | 3gm.eoxs.com | 3 | 33 / 1,023 / 14 |
| Discount Pipe & Steel (DPS) | discountpipesteel.eoxs.com | 10 | 231 / 692 / 63 |
| Eastern States Steel (ESS) | ess.eoxs.com | 7 | 225 / 411 / 82 |
| Ohio Strip Steel (ex-Greer) | greersteel.eoxs.com | 7 | 106 / 286 / 24 |
| PPC Metals | ppc.eoxs.com | 11 | 29 / 480 / 30 |
| Brannon Steel | none | 5 | 0 / 43 / 29 |
| RW Conklin Steel | none | 4 | 0 / 166 / 19 |

**Sabre Alloys**
- It does plate and alloy processing, including toll and blanking processing. The key contacts are Charles White, Ernie Valdez, Christi Deaton (operations and office manager), Tye Webb, Michael Mercadante and Juan Deshon.
- It is the heaviest support load. Open issues include:
  - A landed-cost distribution bug on multi-line receipts. A fix was verified in staging with a deploy ETA of Oct 8, but Sabre disputes EOXS's "display only" explanation.
  - "Cannot confirm packing list" errors that keep recurring.
  - Gross profit miscalculations on sales orders.
  - A blanking order (PR8010) that went unresolved for 3+ hours on Oct 7 and was escalated.
- On the AskCruz side, the proposal was resent after the Aug 13 and Sep 2 calls. Sabre pushed back on data privacy, and a toll-processing side deal was priced separately.
- A "new Processing module" request is pending after 30 concurrency tickets in 3 months.
- Other wiki items: an outage-credit dispute, Claude access provisioned for Juan and Tye, and a Sep 2026 hack incident with a legal evidence package sent to counsel.

**3GM Steel**
- It is an early adopter, onboarded in 2022. Contacts are Travis Lane, Jessica Worley and Leslie Countryman. Its work is coil-heavy: product variant and colour creation, and tonnage-card pricing.
- Open issues: draft invoices INV/2026/2403 (unresolved after a second escalation) and INV/2026/2368 (confirmed correct Oct 6), plus phantom or duplicate customer credits blocking payment application.
- It is the most advanced AskCruz deal. Travis confirmed it at a reduced 2-user scope. The final implementation invoice and first licensing payment went out in Oct 2026, with weekly usage check-ins proposed. A customer story draft went to Raj on Oct 5.

**Discount Pipe & Steel**
- It sells secondary, surplus and auction steel by the pound, each and the foot. Its main warehouse is Pickton, TX. Austin and Amy Rayzor are the decision-makers. Alt Digital AI consultants (Jamie Vernon, Tina Valdez) sit on the client side.
- It is the highest-friction account. The issues are:
  - Recurring packing-list and tag-reservation errors, including three transfers failing in about 25 minutes on Sep 22.
  - A reservation/double-selling escalation that needed an emergency live push in August.
  - A bank-reconciliation module billing dispute.
  - Stalled Aircall, Stripe and training-video deliverables.
  - ROI concerns raised at the Aug 18 check-in.
- Two earlier tasks, Stripe and AvaTax, were closed in a single sweep on 2026-03-27, so check whether they actually work.

**Eastern States Steel**
- It is a coil and long-products business. Contacts are Ryan and Chip Capinski, Rose Torres, Tom Meyer and Vince Pappas. It soft-launched around Nov to Dec 2025.
- Ongoing work covers warehouse additions (several third-party warehouses in Aug and Sep), the Purchase Order Intake task, control-tag weights, and invoice and BOL weight mapping.
- Ryan said on Oct 1 that ESS expects to run exclusively on EOXS within about 3 months. He wants self-service training because support response is too slow.
- He also flagged that margin follows the sales-order price, not the invoice price, which feeds commissions.
- A competitor (CloudForge AI) approached ESS at the Steel Summit in Aug 2026.
- An inventory valuation investigation is stalled pending a full physical inventory.

**Ohio Strip Steel (formerly Greer Steel)**
- It is a 107-year-old cold-rolled strip mill in Dover, Ohio. It is a CRM-focused account (the wiki snippet was truncated, so "CRM-only" is my reading). It rebranded in June 2026 and is separating from its former parent, Greer Industries.
- Joe Brom is the main contact. Two CRM licenses were added Sep 24.
- Joe has asked for an ERP/AI overview for a new IT hire and a consultant. Ron proposed a 4-way scoping call, and Rajat is connecting Joe with Brannon's Manish Trivedi as an MTR AI reference.
- No live wiki pages are tied to this client in the profile, so the picture comes from the connector's contacts, tasks, emails and calls.

**PPC Metals**
- It is a specialty metals processor (database name "velox"). Go-live was Oct 2025. James Baker, Todd Twitty and Eddie Poindexter are the active contacts.
- Recent issues: system-wide slowness on Oct 6–7 (two contacts, "DELAYS IN EOXS"). Support traced it to accumulated cache files and cleared it. It recurs from a July episode, and client confirmation was due Oct 8.
- Other items: multiple reservations on the same tag, and a weight discrepancy traced to a manual receiving edit.

**Brannon Steel**
- It is in Brampton, Ontario, and is EOXS's first Canadian client and first MTR AI-only engagement. The deal was won Jan 20, 2026 after an introduction at the SMU Steel Summit in Sep 2025.
- Its legacy systems are Microsoft Business Central and a roughly 20-year-old SFA. Contacts are David Brannon, Manish Trivedi (head of operations), Ranim Fallaha (APQP) and Kevin Brannon.
- It has weekly implementation huddles. A pre-purchase MTR–spec verification was signed, with work starting Sep 14.
- There is an open conflict between an MTR inventory module escalation and its ticket status.

**RW Conklin Steel**
- Contacts are Philip and Pete Conklin, Hannah Bowens and a general sales inbox. Activity in the connector runs through about April 2025: the Feb–Mar 2025 software upgrade, product master, processing module, accounting migration, and an accounting-staff transition.
- A "Contract Dispute & Near-Cancellation" page exists. Its details were not in what I pulled.
- Its recent record is thin. I'd treat it as low activity, which is an inference, not a recorded status.

**Limits**
- Dollar amounts and deal sizes are redacted by the connector, so there is no pricing or revenue here.
- Tickets, invoices and CRM pipeline live in eoxs-teams (Odoo), which I haven't queried.
- Emails and calls are live. Wiki pages are promoted-only.
- Business descriptions beyond DPS, Brannon and Ohio Strip Steel are inferred from ticket content.

I can go deeper on any one client, such as the Sabre escalation timeline, the 3GM invoice issues, or the ESS and DPS open-task boards. I can also query eoxs-teams for tickets and invoice counts.

Sources: Askcruz connector (`list_clients`, `list_contacts`, `get_client_profile` for all 8 clients, plus `get_wiki_page` and `search_wiki` for client background and recent items).

## User (2026-10-12 10:58:46 EDT)

can i check the payroll details  of the clients or not

## Claude (2026-10-12 10:58:46 EDT)

```
This block is not supported on your current device yet.
```

Not in any meaningful way. I searched Askcruz for "payroll", and it holds no client payroll records such as employee pay, payroll runs or payroll ledgers.

The only client-related hits are configuration-level:
- **Eastern States Steel** uses a third-party payroll processor, Precise Payroll (added to the wiki 2026-07-22). The soft-launch call also covered payroll mapping. Some bill and journal-entry corrections for that processor appear in support history.
- **Sabre Alloys** has a few accounting-buildout mentions that touch payroll, with no figures.

The remaining hits are EOXS's own internal payroll and HR admin, not client data. Salary and compensation content isn't visible on this connection, and any amounts that do appear are redacted, so there are no figures here for any client.

The clients' payroll would sit inside their own Odoo instances (sabre, 3gm, ess and so on). I have no connector to those, and Askcruz only holds the correspondence, calls and tickets about them. I haven't queried eoxs-teams, which is EOXS's own Teams Odoo, so it is unlikely to hold client payroll.

If you need something specific, I can look into it. For example, I can pull the ESS payroll-processor setup and mapping details, or search the Sabre, 3GM, DPS, PPC and Ohio Strip Steel tickets and calls for payroll-related configuration requests.

Sources: Askcruz `search_wiki("payroll")` (pages: Eastern States Steel — Post-Launch Operations, Precise Payroll, Fathom Eastern States Steel Soft Launch, Sabre Alloys — Accounting & Module Buildout).

## User (2026-10-12 10:58:46 EDT)

i want to ask specifically about brannon steel

## Claude (2026-10-12 10:58:46 EDT)

Go ahead. Here is what I already have on Brannon Steel, so you can tell me what to dig into.

- **Scope:** It is MTR AI only (material test report digitization), not the full ERP. It's in Brampton, Ontario, and is EOXS's first Canadian client.
- **Deal:** It was won Jan 20, 2026. The pricing is redacted on this connection.
- **Roadmap:** The planned phases are MTR AI first, then MRP/SFA replacement, then NLP reporting ("Iris AI").
- **Contacts:** David Brannon, Manish Trivedi (head of operations), Ranim Fallaha (APQP manager) and Kevin Brannon, whose role is unclear.
- **Current state:** Weekly implementation huddles have run through at least Aug 25, 2026. A pre-purchase MTR–spec verification was signed, with work starting Sep 14. An Algoma join report is live.
- **Open item:** The wiki flags a conflict between an escalation and the ticket status on the MTR inventory module.

I can pull call transcripts, email threads, the open escalation, the scope and pricing emails (amounts will be redacted), or the huddle history. What do you want to know?

## User (2026-10-12 10:58:46 EDT)

yeah please try to do

## Claude (2026-10-12 10:58:46 EDT)

I'll take that as "dig into all of it." I'm pulling the open escalation, the MTR AI scope and recent huddles, and the latest calls and emails for Brannon.
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



Brannon is a live MTR AI client with real UAT history, but the record has gaps, and one thing I told you earlier needs correcting.

**Correction:** I said weekly huddles ran through Aug 25. The Aug 18 and Aug 25 "Implementation Huddle || Brannon Steel" recordings are not Brannon meetings. Both have Brannon contacts on the invite, but the content is EOXS internal.
- Aug 18 was the team's Claude and company-brain setup session. Raj left partway through to meet Manish separately.
- Aug 25 was an internal reporting discussion. I'm not summarizing it because that content is restricted on this connection.
- The last verified Brannon-specific huddle content is the June UAT calls (Jun 2–25).

**What's confirmed**
- **Scope:** MTR AI only. Per the CRM page, the deal was won Jan 20, 2026, with a go-live target of 4–6 weeks plus 2–3 months of AI calibration.
- **Billing:** The monthly subscription started May 2026.
- **Cadence:** The Fireflies log shows 14 weekly huddles from Mar 10 to Jun 23, each about 11 minutes. Those recordings contain no usable transcript, so what was discussed in March to May is not recoverable.
- **June UAT (Ranim Fallaha testing, with Ayan and the EOXS team):**
  - 5–6 of 14 flagged issues were resolved by Jun 16.
  - The AI was returning grades from the wrong spec. They agreed to hard-code ASTM-only matching, with a "required grade not found, but these match on chemistry/mechanical" fallback.
  - Batch numbers are 6 digits in the MTR data but 8 digits in the Business Central inventory export, which breaks the join key (certificate, heat and batch numbers). That caused the "MTR does not exist" errors.
  - Other open bugs: the impact-test temperature direction was inverted, a grade was misread from the wrong field, carbon equivalency was missing from compliance output, and the conditional manganese rule was not applied.
  - Her team was logging errors on every interaction. EOXS took accountability and committed to fixes within a day.
- **Later work:** The Algoma join report is live in production. The Pre-Purchase MTR–Spec Verification proposal was signed by Manish on Sep 11, with work starting Sep 14.
- **Reference value:** Rajat connected Ohio Strip Steel's Joe Brom with Manish as an MTR AI reference (Oct 1–7).

**Risks**
1. **Status conflict, unresolved:** An internal escalation (ron_gmail thread 79, around June) said the MTR Inventory Module task had been stalled over 2 months. Ticket T06332 (Ayan, created Feb 4) shows "QA Passed." The wiki flags this as unverified, and the escalation may simply be stale.
2. **Pricing scope gap:** A recovered thread shows the "flat" monthly price was implicitly capped around 200–300 MTRs a month. A backlog of about 3,500 MTRs was treated as out-of-scope bulk work needing a commercial recalibration. That contradicts the "no hidden costs" framing on the CRM page.
3. **Unidentified party:** A Gmail address (deepaksaxena192837) appears on the account with no known role.
4. **Unknown status:** Nothing I pulled shows what happened after the Sep 14 start or whether the June blockers were closed. I haven't checked recent emails and calls beyond the wiki pages.

I can next read the full June huddle page, which was truncated at the cross-spec contamination item. I can also pull email 79, the usage-cap thread, or the latest Brannon emails to see the post-September status.

Sources: Askcruz wiki pages (Brannon Steel CRM Record; MTR AI Implementation Huddles Jun 2026 and Mar–Jun 2026 Call Log; MTR AI Algoma Join Report and Pre-Purchase Verification; MTR Inventory Module escalation conflict; Ohio Strip Steel Oct 1–7 page) and Fireflies calls 2411 and 2395.

## User (2026-10-12 10:58:46 EDT)

No i am asking about the payment details basically

## Claude (2026-10-12 10:58:46 EDT)

You mean what Brannon pays and its billing status, so I'm checking Askcruz for invoice and payment correspondence and looking for the eoxs-teams invoice records.
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


Billing structure and invoice timeline are on record, but the amounts are redacted on this connection and I found no record of any payment actually being received. The eoxs-teams SQL console, where invoice and payment records live, isn't available in this session, so I couldn't check payment status.

| Date | Item | Status in record |
|---|---|---|
| Nov 11, 2025 | Pricing outline from Rajat: one-time implementation fee (CAD), 30% due at kickoff, plus a flat monthly licence (CAD) | Terms only |
| Jan 5–7, 2026 | Manish signed the agreement and struck the "additional user charges" line. EOXS countersigned and sent the SOW and kickoff invoice INV/2026/0043 | Sent |
| Jan 12–15 | Manish asked if the first installment arrived. Ayan said accounting hadn't confirmed receipt but EOXS would start work anyway | Receipt unconfirmed |
| Mar 12 | Phase 1 complete, so invoice INV/2026/0133 for the second installment was sent | Sent, no payment confirmation seen |
| May 2026 | Monthly subscription billing began, per the June huddle page | Started |
| Aug 2026 | Algoma join report enhancement, billed separately | Live, amount redacted |
| Sep 11 | Pre-Purchase MTR–Spec Verification, fixed price, signed | Signed, work started Sep 14 |

- **Currency and pricing model:** The pricing is in CAD. The licence is flat (no per-seat), and cloud hosting is included at no extra cost.
- **Payment terms:** The first installment is 30% at kickoff, and the second is tied to Phase 1 completion. The terms for any further installments weren't in what I pulled.
- **No user charges:** Manish removed the additional-user-charges line and EOXS countersigned the copy. I read that as no extra per-user fees, but I haven't seen the agreement text itself.
- **Usage cap:** A recovered thread suggests the flat price implicitly covers about 200–300 MTRs a month. A backlog of about 3,500 MTRs was treated as separate commercial work.

I can read the extracted text of the two invoice PDFs and the signed agreement. They may show payment terms and due dates, although amounts will still be redacted. For paid or unpaid status and amounts, someone with eoxs-teams access would need to check invoices INV/2026/0043 and 0133 and the monthly licence invoices.

Sources: Askcruz emails 6734 (MTR AI Scope and Pricing Summary) and 14906 (Implementation Invoice), plus the Brannon wiki pages on the MTR AI huddles and the Aug–Sep developments.

## User (2026-10-12 10:58:46 EDT)

i don't have access to the exact payment figures yes or no?

## Claude (2026-10-12 10:58:46 EDT)

Yes, you don't have access to the exact figures. This connection redacts every monetary amount, so the pricing, installments and monthly licence all show as restricted. For the exact numbers, you would need someone with the right access, or the invoices themselves (INV/2026/0043 and INV/2026/0133).

## User (2026-10-12 10:58:46 EDT)

more

## Claude (2026-10-12 10:58:46 EDT)

I'll read the invoice PDFs, the signed agreement and the SOW for payment terms and due dates. Amounts will still be redacted.
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




The invoices and SOW give payment terms but no amounts. Every figure is still redacted, so the answer to your earlier question hasn't changed.

**Both invoices were due on the day they were issued:**
- INV/2026/0043, "Implementation – Kick Off", was dated Jan 7, 2026 and due Jan 7.
- INV/2026/0133, "Implementation Due", was dated Mar 12 and due Mar 12.
- Both were issued by EOXS in CAD to Brannon Steel at 14 Tilbury Court, Brampton.
- Payment is by wire only ("do not send checks"), to Prata Inc.'s Royal Bank of Canada account in Canada. I'm leaving the banking details out here.

**SOW v1.0 (Jan 7, 2026) covers Phase 1 only:**
- **Commercials:** The one-time implementation fee and the monthly licence are both in CAD, with cloud hosting included. The payment schedule is "per proposal," it is a multi-year term, and the exact amounts sit in a separate commercial agreement.
- **Liability:** EOXS's liability is capped at 12 months of fees paid. There is a 30-day cure period for material breach, and Ontario law governs.
- **Support:** Support is Mon–Fri, 9–5 ET, with no 24/7 cover unless contracted separately.
- **Change orders:** Anything outside Phase 1 needs a written change order. That includes direct Business Central API integration, the Phase 2 MRP/SFA work, the Phase 3 Iris reporting and a customer portal.
- **Ownership:** Brannon owns its data and outputs, and EOXS owns the platform and models.

**Gaps and open questions**
1. **Phase 2 coverage:** Ayan's Mar 12 email says Phase 1 is complete and Phase 2 work has started. The SOW lists Phase 2 (MRP/SFA) as out of scope without a change order. I found no change order, so I can't tell whether the second installment covers Phase 2 or whether it's a different phase split.
2. **Add-on billing:** The Algoma join report and the pre-purchase verification look like separately billed items, but I haven't seen their invoices.
3. **Documents not read:** The countersigned agreement file contains only a signature page. I haven't opened Manish's marked-up copy (attachment 25331), which would show the struck user-charges line.
4. **Payment status:** No payment confirmations or later invoices are in the connector, including the monthly licence invoices. That status would be in eoxs-teams.

I can read Manish's marked-up agreement next, or search for the Algoma and verification invoices.

Sources: Askcruz attachments 25334 (INV/2026/0043), 30890 (INV/2026/0133), 25332 (SOW) and 25333 (signature page).
