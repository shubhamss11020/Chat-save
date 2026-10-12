---
conversation_id: 10fedaa8-a6f8-4c4c-b33e-d5444d3c3284
platform: claude
username: "shubham"
title: "3GM client details and billing disputes"
created_at: "2026-10-08T13:45:35.793438Z"
updated_at: "2026-10-12 12:34:35 EDT"
---

# 3GM client details and billing disputes

## User (2026-10-12 12:34:35 EDT)

I want to have full details about the 3gm clients from start and what the services we have provided to them and also all the flagged issues they are facing all details

## Claude (2026-10-12 12:34:35 EDT)

I'll pull the 3GM client records, the services delivered, and the flagged issues from the EOXS data connectors.
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

```

```

```

```

```

```

```

```

3GM Steel is EOXS's longest-tenured client, live since July 18, 2022, and it has chronic invoicing and coil-data defects that keep recurring. Several are open right now. This is built from the Askcruz wiki, which synthesizes emails, calls and tasks. I did not open the raw threads. All dollar amounts are redacted on this connection.

## Who they are
- Steel service center in Somerset, KY. The instance is `3gm.eoxs.com`, and MAC Metal Sales is a sister company on the same system.
- **Client contacts:**
  - Travis Lane: General Manager, then Chief Commercial Officer from March 2026. He signed the original deal.
  - Jessica Worley: day-to-day power user since May 2022.
  - Leslie Countryman: inventory and logistics.
  - Brittany Meece: COO.
  - Stefan Brown: CFO.

## Timeline from the start

| Date | Event |
|---|---|
| Mar–Apr 2022 | Discovery call Mar 25. Proposal Apr 14. Signed Apr 19, about 25 days from first call. Contract has 3-year renewals with a 6% cap on increases. |
| Apr–May 2022 | Kickoff Apr 26. About 34 discovery and data tasks, including a custom inbound steel-import logistics workflow. |
| Jul 18, 2022 | Go-live, with Rajat on-site for about a week. Sign-off Aug 2. It slipped from the "2–3 months" pitched to roughly 7 months. |
| Late 2022 | Sales KPI and profit dashboard, P&L reporting, and a tonnage-order invoicing fix. |
| 2023 | Phase 2 live in July: vendor bills, monthly quoting module, account statements. MAC Metal Sales onboarded. |
| 2024 | Server migration to `3gm.eoxs.com` in January. A late-June performance crisis and a November storage/CPU escalation. |
| Aug 2025 | 3-year renewal for 2025–2028 at 6% per year. |
| Dec 2025 | Performance crisis. Rajat authorized a free Tier 3 server upgrade. |
| Mar 2026 | Travis became CCO and asked for a full dashboard redesign. |
| Aug–Oct 2026 | AskCruz "Company Brain" upsell. The first invoice and the kickoff call (Oct 1) are done. The second invoice, covering the remaining 50% of implementation plus the first month of licensing, went out Oct 5. Weekly check-ins were proposed Oct 3. |

## Services delivered
- **Implementation:** ERP build, master data import, access rights, BPF sign-off, and go-live support.
- **Core modules in use:** inventory and coil tracking, tonnage orders and releases, bill of lading, purchasing, invoicing, CRM pipeline, price guidelines and accounting.
- **Added builds:** P&L and profit reporting, the MT-goal sales dashboard, the Phase 2 modules above, the Processing Module (spin-down coil invoicing, confirmed live Feb 24, 2025), and server upgrades.
- **Ongoing:** product and variant creation requests, user access changes and account archives, and ticket support.
- **Ticket volume:** the July 2025–July 2026 export shows 192 tickets, mostly order and invoice reference requests.
- **AskCruz:** Company Brain, scoped down to 2 users with a 6-month initial term. The 3-year term does not auto-renew. It runs on Claude, and the Outlook OAuth blocker on Sep 4 was fixed.

## Flagged issues

**Open or unresolved as of the latest records**
1. **INV/2026/2403 (Oct 1–6):** the amount due is correct, but unit price, footage (should be 1,440 ft) and credit memo are wrong. 3GM has re-escalated twice, tagging Sales. INV/2026/2368 was confirmed fixed Oct 6.
2. **INV/2026/2434 (Sep 30):** the amount-due field doesn't match the invoice's own total. No EOXS reply is captured.
3. **P04612–P04615 (Sep 28):** four POs are confirmed but can't be received. Three also need the PO unlocked to fix the Customer field. No reply is captured.
4. **ND/IN/00015 and 00016 (Sep 22–23):** a recurring error when uploading coils into a PO. No fix is recorded.
5. **12 coils invoiced under INV/2026/2246 (Sep 21):** they still show "available" and distort inventory and AR reports. No fix is recorded.
6. **Reliable Metal Buildings (Sep 4):** a suspected duplicate payment, CUST.IN/2024/1826. EOXS was waiting on Leslie's confirmation before cancelling.
7. **T06692 (Mar 31):** a coil can't be added to transfer SRTI./OUT/03994. It sits in "Need Developer" and is unassigned.
8. **CNJ/OUT/00074 (Jun–Sep):** coil search and sales-order change bug. EOXS found no root cause and was about to close it pending Leslie's reply.

**Chronic defects (never root-caused)**
- **Invoice weight and footage:** invoices pull footage instead of net weight. Seen in Jul 2025, Oct 2025, Nov 2025 and Apr 2026.
- **Amount due vs. total:** the amount-due line disagrees with the total.
- **Price reprice:** a price correction doesn't carry to the printed invoice or credit memo. INV/2026/2276 on Sep 14 and INV/2026/2403 are the same symptom.
- **Coil zero values:** weight, footage and cost zero out after transfers or returns. It recurred through 2025.
- **Coil availability:** shipped or invoiced coils still show "Available." This dates back to 2022.
- **Self-service coil edits:** the coil-weight edit failed again about a week after a fix, in Oct 2025. Jessica asked about it again in May 2026.
- **Footage tax calculation:** 3GM's Shanan Shaver declined the permanent fix on Aug 13, 2024 as not cost-justified, so it was knowingly left open.
- **Payment terms:** terms silently changed on unrelated customers in Nov and Dec 2024, from duplicate payment-term records.
- **Performance:** slow loading in Mar–Apr 2026 and again on Jun 29, 2026 (T07384).

**Account risks**
- **Churn signal:** the COO wrote on Jul 17, 2024, during the "0.00 values" crisis, that cheaper systems exist and EOXS's value was being reassessed.
- **Billing disputes:** INV/2022/0014 and the MAC licensing charge in 2022–23 strained the relationship.
- **Backups:** backups silently stopped from Jul 11, 2024 and were caught by 3GM's own IT contact. A second halt, from Apr 13, 2025, was flagged by their IT and fixed in 3 days.
- **Support continuity:** staff turnover, including Yash's departure in Feb 2026, pushed 3GM to the shared "EOXS Support" tag.
- **AI pitches:** Jessica declined in Jun 2025. Travis didn't respond to the May 2026 pitch but did sign Company Brain in August.
- **AskCruz payments:** nothing confirms INV/2026/0367 or INV/2026/0380 was paid.

## Gaps
- The `eoxs-teams` SQL connector (live tickets, invoices, CRM) wasn't available in this session, so the open-ticket picture comes from emails and wiki pages. The ticket export wiki page ends Jul 16, 2026.
- Several wiki entries say "no reply captured." That means no reply in the ingested emails, not necessarily no fix. Confirm against the live ticket board before escalating.
- Four 3GM wiki pages are redacted, and I could not find a "Duplicate-Payment Phantom Credits" page that another page links to.
- I can pull the raw threads for the open items next. Say which ones.

Sources (all Askcruz wiki): 3GM Steel — Support Tickets; Ongoing Operations; Invoicing & Billing; Server & Platform Maintenance; Feature Expansion & Reporting; Data Integration & Inventory Setup; Sales & Onboarding; Implementation Kanban (Odoo); the INV/2026/2368 and 2403 page (Oct 6); the INV/2026/2434 page; the P04612–P04615 page; the coil-upload page; the 12-coil page; the Reliable Metal Buildings page; the CNJ/OUT/00074 page; the SRTI./OUT/03994 page; and the AskCruz proposal, invoice and Outlook pages.

## User (2026-10-12 12:34:35 EDT)

Billing disputes: INV/2022/0014 and the MAC licensing charge in 2022–23 strained the relationship. can u give me more details about in depth

## Claude (2026-10-12 12:34:35 EDT)

I'll pull the rest of the billing pages and the original email threads for the INV/2022/0014 dispute.
```

```

```

```

```

```

```

```

Pulling the three key raw threads: the Dec 2022 dispute, the March 2023 "3GM and Mac Invoices" thread, and the Aug 2022 licensing-waiver email.
```

```

```

```

```

```

Both disputes come down to charges 3GM's management says they never approved, and EOXS had no written approval trail. The Dec 2022 dispute was about the tonnage order and dashboard work (INV/2022/0014). The Mar 2023 dispute was about the monthly license for MAC Metal Sales. This is from the raw threads, with amounts redacted. Whether either dispute was formally settled is not recorded.

## 1. INV/2022/0014: tonnage orders and dashboards (Dec 20–28, 2022)

**3GM's position (Jessica Worley):**
- On Dec 20 she wrote that her understanding from a prior Zoom call was that 3GM would never be charged for tonnage orders or user dashboards.
- She argued both were "must have" items from the original discovery calls. Tonnage orders are 70% of 3GM's business.
- She cited the contract line "EOXS-Dashboard Reports for Office Users 15" to argue Travis Lane's dashboard, built while he was General Manager, was included.
- She also said 3GM's customers would never accept being told work was free and then billed for it.
- She resubmitted the invoice to management for review.
- She said 3GM was willing to pay the MAC invoice, since MAC wasn't discussed in discovery.

**EOXS's position (Rajat, Dec 20):**
- Standard terms apply. Invoices cover licensing, implementation, customizations, investigations, data cleanse, migration and special project fees.
- Customizations bill at the standard hourly rate, and some dashboards were given free in Q3 2022 in good faith.
- He conceded he had said Peyton's dashboard (Peyton is 3GM's Logistics Manager) and the tonnage order would not be charged.
- Tonnage orders were scoped as 8–10 hours of no-code configuration. After 2 weeks of an unstable code environment, he found extra requirements that needed code-level customization. The full dev team spent almost 4 weeks on it.
- He said engagement terms were set before the discovery calls, and all open invoices were reviewed and believed correct.
- He promised standardized project estimate forms going forward.

**Outcome:**
- Rajat proposed a Zoom call on Dec 27. Jessica said she would get back to him on availability.
- Rajat agreed it could wait. The thread ends there with no resolution.
- The wiki says the dispute ran into April 2023. I did not open the intervening threads.

**What this shows:** Rajat's own reply admits a verbal waiver for the tonnage order, and EOXS billed it anyway. That is a weak position on a client that calls tonnage orders 70% of its business.

## 2. MAC Metal Sales licensing charge (Mar 30–31, 2023)

**Background:**
- MAC is 3GM's sister company. Its COO and General Manager is Brittany Meece, who is also 3GM's COO.
- On Aug 29, 2022 Rajat offered MAC a discounted package, after what he said was a Board conversation:
  - MAC's license fee would be waived for every user already paying the 3GM license.
  - That cut the user package from 20 to 15.
  - The offer also cancelled the implementation discount.
- On Oct 18, 2022 Brittany declined: "the cost doesn't make sense" for MAC's growth.
- On Dec 12, 2022 Rajat said that was the bare minimum EOXS could do.
- The Oct–Dec 2022 emails don't explain how MAC ended up as a billed instance by March 2023.

**The March 2023 thread (14 messages):**
- Alka Jain sent revised invoices for both companies:
  - INV/2023/0001 is 3GM's monthly license.
  - INV/2023/0002 is MAC's monthly license.
  - She told Brittany to ignore a charge on INV/2022/0013, which was an error.
- Brittany asked EOXS to explain MAC's license, then who approved it. Rajat said the requirement came from Jessica and Rachel Epperson, and asked Alka to find the call recording.
- Brittany replied that this was "another cost that management had no idea about." She said ownership and management were never told of a monthly license, and called it "way too much assuming and lack of communication."
- Rajat's defense:
  - MAC was quoted for the full software, then said it wanted only the Purchasing Module.
  - There is always a setup fee plus monthly licensing, and EOXS makes its money on licensing.
  - EOXS doesn't normally create instances for fewer than 3 users. MAC was an exception because of the 3GM relationship. The license covers 1 user.
- Rajat committed that any future work with a real cost would get a formal quote and written confirmation first.
- He asked 3GM to pay all other invoices and left MAC's license for a call the following week.

## Policy changes that came out of it
- Written quotes and written approval before billable work (Dec 2022 and again Mar 2023).
- Standardized project estimate forms for customizations (Dec 2022).
- Rajat took over billing conversations himself. The wiki says the account manager David Barany handed the relationship over in early 2023, and that Rajat blamed him on Mar 29 for saying two months earlier that all invoices were approved.

## What explains the friction
- **Leadership change:** 3GM restructured in Jan 2023. Travis Lane's general-manager role went to Brittany (COO), Stefan Brown (CFO) and Cole Wolford (Sales Manager). The people who agreed to the original scope (Travis, Jessica) were no longer the people approving invoices.
- **Verbal scope:** the "free" tonnage-order and dashboard work was a spoken understanding, and the MAC license wasn't clearly communicated to 3GM's management.
- **Cash:** the wiki says invoices were more than 120 days past due as of Mar 29, 2023, so this was also a collections problem.

## Related
The commercial relationship recovered after this. 3GM did the Phase II project in 2023, EOXS gave a referral discount in May 2023, and the 3-year renewal was signed in Aug 2025.

## Unknowns
- How INV/2022/0014 was finally settled, and whether MAC's license was paid or waived.
- How MAC went from declining in Oct 2022 to being invoiced by Mar 2023.
- The restricted portions of the emails, which hid some of Rajat's reasoning.

I can pull the April 2023 threads and the Phase II quote to find out how these were settled.

Sources (Askcruz): raj_gmail threads "RE: Eoxs Invoice (Ref INV/2022/0014)" (id 1432), "3GM and Mac Invoices" (id 5034) and "Happy Monday!" (id 9818); wiki pages 3GM Steel — Invoicing & Billing and 3GM Steel — Feature Expansion & Reporting.

## User (2026-10-12 12:34:35 EDT)

Aug–Oct 2026	AskCruz "Company Brain" upsell. The first invoice and the kickoff call (Oct 1) are done. The second invoice, covering the remaining 50% of implementation plus the first month of licensing, went out Oct 5. Weekly check-ins were proposed Oct 3.

## Claude (2026-10-12 12:34:35 EDT)

You pasted the AskCruz line without a question, so I'm assuming you want the full detail on that deal. I'm pulling the rest of the proposal thread and the Oct 1 kickoff call.
```

```

```

```

3GM's AskCruz "Company Brain" deal is signed and live, but the proposal EOXS sent was wrong in several places and payment on both invoices is unconfirmed. This comes from the wiki pages plus the Oct 1 kickoff transcript. Amounts are redacted throughout.

## What was sold
- **Product:** Claude as the front end, connected to 3GM's email and the EOXS ERP, plus a searchable log of every question the team asks ("Prompt History"). The EOXS integration is a separate one-time fee.
- **Original proposal (Aug 14):** 3 users, a 6-week rollout, a 12-month initial term, a 3-year term after that, and 50% due at kickoff. It also quoted AI agents and automation.
- **Signed deal (Aug 20):** reduced to 2 users, Travis Lane and Stefan Brown. The initial term is 6 months.
- **Front end:** Ron told Travis that EOXS is using Claude as the only front end for this deal, not AskCruz, and keeps developing AskCruz internally. The wiki flags that no internal record confirms this decision.

## Timeline

| Date | Event |
|---|---|
| Aug 12 | 27-minute pitch call, Rajat to Travis |
| Aug 14 | Two proposals went out with different line-item prices. Travis replied with five reconciliation questions and copied Stefan. Rajat admitted the sent version was wrong. |
| Aug 17 | Ron answered all five points. Rajat sent a corrected proposal about 30 minutes later. |
| Aug 19 | Travis confirmed 3GM is moving forward at a reduced scope. |
| Aug 20 | Rajat agreed to a 6-month initial term. Travis signed a 2-user proposal the same day. |
| Aug 24 | Rajat confirmed in writing that the 3-year term does not auto-renew, with a decision point at month 6. This was Travis's condition for releasing the 50% payment. |
| Sep 4 | Outlook OAuth was blocked for Travis. Root cause was an Azure AD setting on the parent app, "Mac Metal Sales", requiring user assignment. Setting it to No fixed it. Travis then hit the same prompt in Edge and used Chrome. |
| Sep 7 | Kickoff invoice INV/2026/0367 (50% of implementation) sent. |
| Oct 1 | Kickoff and setup call, 56 minutes. |
| Oct 3 | Ron proposed 30-minute weekly check-ins for 4 weeks. Travis and Stefan may be at MetalCon the week of Oct 5. |
| Oct 5 | Invoice INV/2026/0380 sent, covering the other 50% of implementation plus October's license. |

## Travis's five objections on Aug 14
1. What the EOXS integration fee actually covers, and confirmation it is one-time.
2. The Claude subscription line didn't add up (3 users × the per-user price didn't match the total).
3. The monthly total didn't equal the sum of its lines.
4. Email integration pricing: written terms were per user for 3GB, but he recalled a per-5GB quote.
5. The proposal described "your salespeople and your four partners," which doesn't match 3GM, so he asked whether it was a reused template.

Ron's answers on Aug 17:
- **Integration fee:** one-time, with no recurring charges. Any user added later carries a further one-time charge.
- **Claude subscription:** it runs on 3GM's own Anthropic account, not billed by EOXS.
- **Missing platform fee:** he admitted a monthly platform fee should have been in the draft.
- **Email integration:** priced per GB, and the rate Travis recalled was correct.
- **Template and total errors:** acknowledged as mistakes and cleaned up in the new version.

## The Oct 1 kickoff
- **Attendees:** Travis and Stefan, plus Ron, Ayan Dutta (AskCruz product lead), Nidhi Rana (developer) and Rajat for a moment. Ayan said they are AskCruz's first customer.
- **How they use Claude today:** Travis has used Claude on a personal account for about five months, mainly to analyze monthly mill pricing in about 30 seconds instead of hours. He wants fast yes/no deal decisions while traveling: account health, stock on hand, average cost and incoming material. He also wants to turn inventory faster. Stefan uses it for approving pre-sold offshore deals, return on capital, QuickBooks reports and 5–6 month cash forecasting.
- **How EOXS set it up:**
  - Nidhi logged into their Claude accounts using emailed verification codes to add the custom instructions and skill files, then logged out. Those files include a "3GM Navigator" skill.
  - Ayan said not to edit the instructions and to ask him for changes.
  - Email data runs from Sep 1, 2025 and refreshes every 6 hours. ERP data is queryable in real time.
  - Ron's model guidance was to use Sonnet 5.5 day to day and Opus for complex analysis, and that better models use more of 3GM's token allowance.
- **Reaction:** Travis said it would help with opportunities lost in his email. Stefan said it returned the data he wanted. Both ran test queries live, and Travis's email query was slow on the heavier engine.

## Risks and open questions
- **Proposal errors reached the client.** The wrong figures went to the CCO and CFO, and Travis caught them himself. He said he needed a reconciled version before taking it to 3GM's CEO.
- **Payment unconfirmed.** Nothing in the record shows either INV/2026/0367 or INV/2026/0380 was paid.
- **No term lock-in.** Travis negotiated a short initial term and a written decision point at month 6. Renewal depends on the 4 weekly check-ins going well.
- **History of billing disputes.** In 2022–23 3GM's management pushed back on charges they said they hadn't approved. The Aug 2026 discussion shows the same pattern of reconciling pricing before the CEO signs off.
- **Customer story.** A wiki page records a customer story draft sent to Raj on Oct 5. I only saw its title.
- **Unknowns:** the Sep 9 follow-up on the Outlook issue, which check-in start date they chose, and whether either invoice has been paid.

Sources (Askcruz): wiki pages on the AskCruz proposal call, the Company Brain invoice and weekly check-ins, and the Outlook OAuth issue; Fathom call 2516 ("AskCruz Kickoff | 3GM Steel", Oct 1, 2026).

## User (2026-10-12 12:34:35 EDT)

can we have payroll details or discussion whatever happened related to that

## Claude (2026-10-12 12:34:35 EDT)

I'll check the wiki, emails and calls for anything on payroll.
```

```

```

```

```

```

Two hits look relevant: a 3GM stakeholder tied to payroll, and an ICP note on payroll as a product gap. I'll read both.
```

```

```

```

I found no payroll discussion for 3GM in the wiki, emails or calls. The only mention is that a 3GM finance contact, Gerri, pays the bills and manages payroll. She had low expected involvement in the system during the 2022 go-live. Payroll was never raised as a feature request, a ticket or a dispute for this account.

- **Searches run:** the wiki, email and call transcripts for 3GM and payroll.
- **Other payroll hits:** they were about other clients or EOXS's own internal operations, not 3GM, so I left them out. One example is Sabre Alloys, where payroll cost during downtime came up in a damages claim.
- **Why this is likely complete:** the 3GM scope was ERP, inventory, tonnage orders, invoicing, dashboards and accounting. There was an open scope question in 2022 about whether full accounting would go live in Phase 1 or wait until 3GM hired a CFO. Nothing records payroll being part of it.

Did you mean something else? For example, payroll processing inside the EOXS ERP, payroll at EOXS, or another client such as Sabre? Tell me which, and I'll search for that.

Sources (Askcruz): wiki page 3GM Steel — Data Integration & Inventory Setup, plus wiki, email and call searches on "payroll".

## User (2026-10-12 12:34:35 EDT)

overall it means not able to access due to access tier?

## Claude (2026-10-12 12:34:35 EDT)

I can't tell. What I know is that the data connections have access levels and content restrictions. Dollar amounts and some other content are redacted, and I can't confirm or deny whether anything specific, payroll included, sits behind a restriction. Searches for restricted material return the same "not found" as material that doesn't exist.

- **What I can say:** my searches returned no 3GM payroll content apart from the Gerri mention.
- **What I can't say:** whether that is because nothing exists or because something isn't visible to this account. I shouldn't have called my earlier answer "likely complete," because I can't establish that.
- **If you need a definitive answer:** ask whoever administers EOXS data access, which per the account notes is Raj. They can check payroll-related records at the right access level or point you to the system that holds them.

I can also look for payroll in other places, such as the 3GM Odoo task boards, if that connector is available to you.
