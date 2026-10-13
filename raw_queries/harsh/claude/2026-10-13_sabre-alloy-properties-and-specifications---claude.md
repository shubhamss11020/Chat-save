---
conversation_id: 4d575173-b1c9-4e67-b1a1-5b830a58ce22
platform: claude
username: "harsh"
title: "Sabre alloy properties and specifications"
created_at: "2026-10-13 07:07:06 EDT"
updated_at: "2026-10-13 08:33:30 EDT"
---

# Sabre alloy properties and specifications

## User (2026-10-13 08:33:30 EDT)

Give me details about sabre alloy

## Claude (2026-10-13 08:33:30 EDT)

I'll start by reading the two skill files.

> *Thinking:*
>

Sabre Alloys is one of EOXS's eight active ERP clients, a steel and alloy distributor and processor running on the EOXS Odoo build. It is a heavy user of the support desk, and the account currently has a new-entity expansion deal in play.

**Account basics**
- Legal entity: Sabre Alloys L.P., acquired in 2023 (formerly Optimal Alloys). That acquisition left a contract-entity mismatch that has already caused friction once.
- The Odoo instance is sabre.eoxs.com. Sabre is billed for about 27–28 users at the full rate with no discount.
- Visible in this session: 190 implementation tasks, 1,430 emails and 88 calls tied to the account.

**Key people at Sabre**
| Person | Role |
|---|---|
| Michael Mercadante | CEO/Owner. He does real technical due diligence and wrote a 20-category AI requirements doc. |
| Jim Zeigler | Senior Sales Director |
| Jesus Rios / Juan Deshon | Finance. The wiki lists Jesus as CFO and Juan as CFO/financial analyst, so I'd confirm who holds the title. |
| Christi | High-volume accounting and operations contact. She sends most support escalations. |
| Charles White | Accounts payable |
| Tye Webb | Owns the production pricing matrix and requests features |
| James Carter | Quality Manager |

**Product usage**
- Core areas are control tags and lot tracking, processing orders (including blanking), sales order gross profit, landed cost, and packing lists and transfers.
- It is also the main user of toll processing and has a long list of finance and reporting fixes.

**What's live right now (Aug–Oct 2026)**
- **Recurring errors:** "Cannot Confirm PL" errors on packing lists, blanking processing-order errors, and gross-profit miscalculations on several sales orders.
- **Landed cost:** a distribution error on multi-line receipts (LC/5722, 5689, 6081, 6083). A fix was deployed to live on Oct 8, but Sabre hasn't confirmed it works.
- **PR8010:** a restock-cost error on this processing order was unresolved for over 3 hours on Oct 7 and escalated.
- **Overnight automation:** a 3am invoice for an already-paid invoice went to a customer, and 3am internal notifications went to staff. Both were still unresolved as of Oct 1.
- **Concurrency tickets:** 30 tickets from Jun 1 to Sep 10, peaking in late July. A possible new processing module is still undecided because Rajat wants scope, time, risk and client list first.
- **Reservation functionality:** a call was held Oct 6, with Hashir Saleem named as task owner.
- **Claude access:** Juan and Tye were given Claude AI access in Sep 2026. Tye's "EOXS IRIS Sabre" connector failed on Oct 5 and Ron reconnected it.

**Expansion deal (the strategic piece)**
- EOXS has proposed a second Sabre-affiliated company for laser cutting and toll processing, inside the same Odoo database. It has a 12-month term, a 5-week setup and a 47% relationship discount that Sabre's own account doesn't get.
- Michael pressed for automated PO generation and pricing driven by Tye's matrix. Raj said it was possible but deferred it, and it is not in the proposal.
- Both "Not included" sections were removed from the final PDF, so the document sets no scope boundaries.
- The entity name and EIN are still TBD, and the signature block is blank.
- Michael also asked what database AskCruz uses and whether it supports vector data. That reply was waiting on Ayan's answer about pgvector.

**Caveats**
- I can't see monetary amounts on this connection, so I haven't given any deal or invoice figures.
- I couldn't query the support-ticket or invoice systems from here, so ticket counts come from wiki summaries, not a live check.
- Several deal details reach the wiki secondhand through Ron's and Raj's sessions.
- The latest material is from Oct 8, so check for anything newer.

**Sources:** AskCruz client profile (sabre-alloys) and wiki pages "Landed Cost Display Issue on LC/6083" (email 70520), "New Processing Module Proposed… Concurrency Tickets" (email 62413) and the Sabre contact entity pages. Threads-Wiki page 187, "Sabre Alloys — New-Entity Proposal, Live-Account Escalations, and AskCruz Due Diligence (Sep–Oct 2026)".

One note on archiving: the conversation-saving tool (`save_chat_transcript`) isn't connected in this session, so this conversation was not archived. If it should be, reconnect the Notes connector in Settings → Connectors.
