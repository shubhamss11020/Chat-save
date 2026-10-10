---
conversation_id: 6f5a8eb7-7793-42f4-9c95-181c831015a8
platform: claude
username: "shubham"
title: "Askcruz details - Claude"
created_at: "2026-10-10T14:56:43.755Z"
updated_at: "2026-10-10 11:55:48 EDT"
---

# Askcruz details - Claude

## User (2026-10-10 11:55:48 EDT)

can u give me details about the askcruz

## Claude (2026-10-10 11:55:48 EDT)

AskCruz is an AI “company brain” product built by EOXS, the company that also runs the Odoo ERP that 3GM uses. It connects a company’s scattered business data (email, calls, spreadsheets, operational systems) and lets employees ask questions across it in one conversational interface.

What it does

Company Brain: shared working knowledge, such as who handles what, how quotes are priced, customer history, and past commitments.
Company Hands: practical help like drafting a quote, flagging an at-risk order, or summarizing a customer call. It is explicitly not meant to make final decisions.
Digital Workforce: standing watch-and-report duties on defined business conditions, such as monitoring an order queue.
Company Personalization: tuned to one company’s vocabulary, pricing logic, and customer expectations.

Positioning (conflicting)
The internal docs disagree. One says AskCruz is a steel-industry product for service centers, processors, and tube mills. Another says it is industry-agnostic. The wiki flags this as unresolved and says the current positioning should be confirmed before external use.

Traction and sales

3GM Steel is the first confirmed customer. Travis agreed to a deal at a reduced 2-user scope and asked for a shorter initial term (August 2026). The wiki notes that usage, ROI, and retention for 3GM are not yet verified.
The Sabre Alloys proposal was sent on August 13 and revised after September calls. The setup fee is being paid in six monthly installments from September 3 to October 7, 2026.
Commerce Steel is a prospect that saw a demo.
On October 7, EOXS proposed a reseller partnership with Invera for AskCruz.

Limits
Its client-facing docs say live systems stay authoritative for current state, and that the product explains information but does not perform actions in source systems. Data syncs on about a six-hour lag.

If you meant something else by “askcruz,” such as a specific deal, the internal team’s board, or a particular 3GM question, tell me and I’ll dig in.

Sources:

Wiki: “AskCruz — Product Capabilities, Feature Model & Client-Facing Boundaries” (id 1894), assets 17 and 19
Wiki: “AskCruz — Market Positioning, ICP & Product-Market Fit Status” (id 1895), asset 18
Wiki: “3GM Steel — AskCruz (Company Brain) Proposal Call…” (id 1730), email thread 68402
Wiki: “AskCruz Sales Push Extends to Sabre Alloys…” (id 1733), email threads 66154, 66156, 66150, 66151, call 2393
Wiki: “Sabre Alloys — ‘Sabre 2’ AskCruz Proposal Scope Review Call” (id 2034), call 2428
Wiki: “AskCruz Proposal Resent to Sabre Alloys…” (id 2053), email thread 70584
Wiki: “Commerce Steel (Prospect)” (id 2035), email thread 68548
Wiki: “EOXS Pitches Invera a Reseller Partnership for AskCruz…” (id 2368), email thread 70579
Wiki: “3GM Steel — Invoice History” (id 808), email thread 68407

## User (2026-10-10 11:55:48 EDT)

can u give me detail about the sabre alloys\

## Claude (2026-10-10 11:55:48 EDT)

Sabre Alloys is a steel processor and an EOXS ERP customer (Odoo instance at sabre.eoxs.com). It is also the second AskCruz prospect, after 3GM, and it has been a difficult account since a major outage in February 2026.

Who’s involved

Michael Mercadante: CEO and owner
Tye Webb: COO
David Underwood: investor and advisor, and the sharpest critic in the account record
Rajat Jain: EOXS president, the main contact on the EOXS side
Ron J: EOXS-side account and proposal owner

The February 2026 outage and data loss

On February 11, 2026, EOXS’s server infrastructure failed and took the Sabre instance offline for about 48 hours. EOXS later called it a “breach,” which suggests a possible security compromise.
Sabre lost about three weeks of transactions (roughly January 20 to February 11). Staff rebuilt 218 missing transactions by hand.
One order (SO18263) was re-entered incorrectly during rebuilding. It caused a plate cutting error with a hard cash loss that was accepted into the June settlement. The wiki now flags documentary evidence that undermines Sabre’s account of the dimension dispute.

Settlement

Underwood escalated in April, demanding about eight months of licensing credits. Negotiations ran through May and June.
On June 15, 2026, Rajat sent a settlement: an immediate credit against Sabre’s outstanding balance, plus a monthly service credit for 25 months. Amounts are restricted in the vault.

Open operational issues

Ticket T06021 (a bug where unit values revert during processing) is still unresolved after months of ignored automated escalations. The wiki says it is a valuation-corruption cause the April analysis missed.
A September 30 ticket reports a negative unit cost on plate tags (process 7839), linked to inventory valuation discrepancies.
A September 6 invoice (INV/2026/0349) contradicts the invoice history on the account.

AskCruz proposal

Scope: 15 users, a six-week rollout, a one-time setup fee plus a monthly fee, a 12-month initial term, and a 3-year ongoing contract. Payment was 50% at kickoff, Net 7 billing.
Terms included a clause saying Sabre’s data stays Sabre’s and is not used to train shared models.
The proposal was resent on September 3 with call recaps from August 13 and September 2. The wiki notes that David Underwood joined the thread at that point.
On the September 2 call, Underwood pushed back on data ownership and asked for a separate written data privacy agreement. Rajat agreed.
A separate toll-processing side proposal was discussed. The wiki says it is priced at a 47% discount on setup, but the amounts are restricted.
As of October 7, the main proposal’s setup fee was rephased into six monthly installments (September 3 to October 7). The wiki doesn’t confirm whether this replaces the original 50% kickoff payment.
Status: no signed deal is recorded in the vault. The most recent step was the rephased terms.

Caveats

The September 2 call transcript was too large to read in full, so its details come from partial excerpts.
Several wiki pages are flagged as unverified, including the payment terms and the settlement’s coverage of James Carter’s NCR data loss.

Sources:

Wiki: “Sabre Alloys” entity (id 77)
Wiki: “Sabre Alloys — Post-Crisis Operations” (id 786), calls 2081, 2123, 2062
Wiki: “Sabre Alloys — Invoice History” (id 774), email thread 70369
Wiki: “Sabre Alloys — Negative Unit Cost on Plate Tags, Process 7839” (id 2302), email thread 70119
Wiki: “AskCruz Proposal Resent to Sabre Alloys…” (id 2053), email thread 70584
Wiki: “Sabre Alloys — ‘Sabre 2’ AskCruz Proposal Scope Review Call” (id 2034), call 2428
Wiki: “Sabre Alloys — Accounting & Module Buildout” (id 782)
Wiki: “Sabre Alloys — Support Tickets” (id 775)
