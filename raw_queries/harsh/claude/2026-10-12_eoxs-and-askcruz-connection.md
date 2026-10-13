---
conversation_id: 4d63e652-9b89-401f-ac3c-94883126cc1d
platform: claude
username: "harsh"
title: "EOXS and AskCruz connection"
created_at: "2026-10-12 16:25:22 EDT"
updated_at: "2026-10-13 07:15:31 EDT"
---

# EOXS and AskCruz connection

## User (2026-10-13 07:15:31 EDT)

what about eoxs and askcruz how they are linked to each other on what aspects

## Claude (2026-10-13 07:15:31 EDT)

I'll start by reading the two skill files, then look into how EOXS and AskCruz relate.

EOXS is the steel ERP company, and AskCruz is the AI knowledge product that grew out of it. They share the same people, customers and sales motion, but AskCruz is now being aimed beyond steel.

| Aspect | How they connect |
|---|---|
| **Product lineage** | EOXS (legal entity Prata Inc.) sells a steel-specific ERP plus a suite of "AI Workers". AskCruz appears in the wiki as the "Second Brain Initiative" product, which is the AI layer now pitched to prospects. |
| **Same team** | Rajat Jain leads sales for both. Ron J does EOXS implementation and also runs AskCruz marketing. AskCruz walkthroughs are booked through the "External Calls EOXS" calendar. |
| **Same customer base** | 3GM Steel is an EOXS client that also bought AskCruz (Company Brain) at a reduced 2-user scope. |
| **Upsell path** | Collier Metals is being worked as an AskCruz relationship first, with the full EOXS platform as a possible later step. |
| **Technical link** | AskCruz connects to a client's ERP data and syncs email. The 3GM proposal separated an "ERP connection only" option from Company Brain, which adds training on the client's own terminology and ongoing email sync. |
| **Billing** | They are invoiced separately: EOXS licensing invoices for ERP (for example Sabre Alloys) and a separate AskCruz kickoff invoice for 3GM. |
| **Where they diverge** | EOXS is steel-only. AskCruz's marketing now starts with car dealerships, then steel. |

- **Inference:** the wiki has no clean statement of how the two are structured legally or organisationally. One wiki page even says AskCruz's relationship to the internal "Cruz" second-brain system is unclear. I'm reading them as one team running two product lines.
- **Redacted amounts:** pricing and invoice amounts are hidden in this session, so I can't compare what each side earns.
- **Not saved:** the Threads-OV save tool isn't connected in this session, so this conversation wasn't archived.

I can go deeper on any one angle, such as the 3GM deal or the vertical rollout.

Sources: EOXS Company Overview (asset); wiki pages "3GM Steel — Invoice History", "3GM Steel — AskCruz (Company Brain) Proposal Call", "Collier Metals", "Three D Metals", "Sabre Alloys — Invoice History", "AskCruz Marketing — Ron's Priorities Through Oct 12, 2026"; "AskCruz Mailbox Rollout — August 2026 Intern Cohort".

## User (2026-10-13 07:15:31 EDT)

ok give me detail about brannon steel

## Claude (2026-10-13 07:15:31 EDT)

Brannon Steel is EOXS's first Canadian client and its first standalone AI-only engagement (MTR AI, not the full ERP). The deal was won on January 20, 2026, and the account is still active with a new add-on signed in September.

**Who they are**
- Brannon Steel is based in Brampton, Ontario, and uses Microsoft Business Central as its legacy ERP, plus a roughly 20-year-old sales force automation (SFA) system.
- It handles prime steel only, with full traceability by plate ID.
- Contacts:
  - David Brannon: owner-level contact who met Raj.
  - Kevin Brannon: Vice President, but his role in the account is unknown.
  - Manish Trivedi: Head of Operations and technical lead, signs the proposals.
  - Ranim Fallaha: APQP Manager, ex-Gerdau, oversees MTR compliance.

**How the deal happened**
- Raj met David at the SMU Steel Summit in September 2025.
- An in-person meeting on Oct 15, 2025 set a three-phase roadmap: MTR AI digitization first, then MRP/SFA replacement, then "Iris AI" natural-language reporting.
- A 55-minute scoping call on Nov 11, 2025 agreed the architecture: an MTR database, an inventory database and an AI search layer, with the heat number as the shared key and manual CSV/Excel upload to start.
- Manish's confidence was helped by a Gerdau mentor connection and by his watching 3–4 hours of EOXSplore videos.
- A Dec 8 call settled his IP concern: Brannon owns its data and AI training, and EOXS owns the core platform.
- The formal proposal went out Dec 9, and the kickoff was Jan 21, 2026.

**Delivery since then**
- Weekly "Implementation Huddle" calls ran from March 2026, with 26 on record through Aug 18. The call log only holds metadata and no transcript content, so what was discussed is unknown.
- The Algoma Join Report enhancement (matching heat/batch mismatches on Algoma MTRs) is live in production and was billed on invoice INV/2026/0295.
- A pre-purchase MTR–spec verification add-on was signed on Sep 11, 2026, with work starting Sep 14.
- Brannon is now a reference account. Rajat connected Manish with Ohio Strip Steel as an MTR AI reference in early October 2026.

**Open issues**
- **Status conflict:** an internal escalation says the MTR Inventory Module task was stalled for over 2 months (around June), while ticket T06332 shows "QA Passed". It's unresolved which is right, and the ticket may have drifted from the task tracker.
- **Pricing scope contradiction:** earlier pages describe the pricing as flat with no hidden costs. A recovered thread implies a cap of about 200–300 MTRs a month, with a roughly 3,500-MTR backlog treated as out of scope. That could become a commercial friction point.
- **Gaps in the record:**
  - Go-live confirmation isn't documented.
  - Phase 2 (MRP) and Phase 3 (Iris) status is unknown.
  - Whether "Iris AI" here overlaps with EOXS's own IRIS product is unclear.

All dollar amounts are hidden in this session. No implementation tasks appear for Brannon on the task board, and support tickets aren't reachable from this connection, so the ticket detail comes only from wiki pages. The save tool for archiving this conversation still isn't connected in this session.

Sources: client profile (brannon-steel); wiki pages "Brannon Steel — CRM Record", "MTR AI: Algoma Join Report & Pre-Purchase MTR–Spec Verification" (email 215), "MTR Inventory Module: Escalation vs. Ticket Status Conflict" (email 79), "MTR AI Implementation Huddles Mar–Jun 2026 (Call Log)", and the Ohio Strip Steel page.

## User (2026-10-13 07:15:31 EDT)

give for 3gm

## Claude (2026-10-13 07:15:31 EDT)

3GM Steel has been an EOXS ERP client since 2022, and in 2026 it also became an AskCruz (Company Brain) customer at a reduced scope. Its ERP support load is currently heavy, mostly recurring invoice and inventory bugs.

**Account basics**
- 3GM runs on its own EOXS Odoo instance (3gm.eoxs.com).
- Onboarding started in April 2022 with discovery calls across the team, kickoff calls on reports, access rights and company details, and a product master import. The task board shows 28 implementation tasks, nearly all from 2022.
- The archive holds 964 emails and 13 calls, most of them support threads.
- Contacts: Jessica Worley, Leslie Countryman and Travis Lane. Stefan Brown is the second AskCruz user, and Matt Inman's access was raised to match Jessica's in August.

**AskCruz (Company Brain)**
- **Proposal call, Aug 12, 2026:** Travis confirmed the deal at a reduced 2-user scope and asked for a shorter initial term.
- **Outlook connection blocked, Sep 4:** an Azure AD admin-consent misconfiguration stopped the connection, and it was resolved through an admin approval call.
- **Kickoff, Oct 1:** a setup walkthrough took place, and an IRIS AI historical data preload was done in August.
- **Billing:**
  - The implementation fee is split 50/50 across two invoices: INV/2026/0367, then INV/2026/0380 on Oct 5.
  - INV/2026/0380 also covers the first month of licensing, which is monthly per user.
  - There is no evidence that either invoice has been paid.
- **Check-ins:** on Oct 3 Ron proposed 30-minute weekly check-ins for 4 weeks, starting either the MetalCon week or the week of Oct 12. No reply from Travis or Stefan is on file.
- **Customer story:** a draft was sent to Raj for review on Oct 5.

**ERP issues, Aug–Oct 2026**
- **Invoice correction bug, recurring:**
  - On INV/2026/2368 and INV/2026/2403, corrections show in the data but not on the printed invoice or credit memo.
  - 2368 was confirmed correct by 3GM on Oct 6. 2403 is still open after two escalations, with 3GM now tagging Sales as well as Support.
  - INV/2026/2276 (Sep 14) showed the same symptom, so this may be a systemic reprice-after-draft gap. That's a hypothesis, not a confirmed root cause.
  - INV/2026/2434 also has a total-due mismatch against the calculated weight × CWT rate.
- **Inventory and receiving:**
  - Four POs (P04612–P04615) hit a "confirmed but can't receive" bug on Sep 28.
  - 12 coils invoiced under INV/2026/2246 still show as available, which distorts inventory and AR reports.
  - Coil search and availability errors on the tonnage card ran June–September, and a recurring coil-upload error hit purchase orders in September.
- **Pricing and payments:** S11105 had tonnage-card pricing errors in August, and a suspected duplicate payment (Reliable Metal Buildings, INV/2026/2146) was investigated on Sep 4. A related page flags duplicate-payment phantom credits across invoices, but its exposure amount is restricted.
- **Routine requests:** a steady stream of product variant creations (PRM:26, PRM:28, color variants for a new coating line).

**Gaps**
- Dollar amounts are hidden in this session, so I can't give deal size or pricing.
- Support tickets aren't reachable from this connection, so the ERP issue status comes from wiki pages and emails only. Whether INV/2026/2403 has been fixed since Oct 6 isn't known.
- The wiki gives no confirmed AskCruz payment status or usage data yet.

Sources: client profile (3gm-steel); wiki pages "AskCruz (Company Brain) Final Implementation Invoice + First Licensing Payment Sent; Weekly Usage Check-Ins Proposed (Oct 2026)", "INV/2026/2368 Confirmed Correct, INV/2026/2403 Still Unresolved (Oct 6, 2026)", and the 3GM live-page list (Proposal Call, Outlook Connection, Four POs, 12 Coils, Duplicate Payment).
