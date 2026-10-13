---
conversation_id: b7245a72-1b57-4dfe-9185-85e0235cc87d
platform: claude
username: "harsh"
title: "3gm steel detail - Claude"
created_at: "2026-10-13 06:55:22 EDT"
updated_at: "2026-10-13 06:55:24 EDT"
---

# 3gm steel detail - Claude

## User (2026-10-13 06:55:24 EDT)

3gm steel detail

## Claude (2026-10-13 06:55:24 EDT)

3GM Steel is an active EOXS client that closed an AskCruz (Company Brain) deal at reduced scope in 2026, and its current day-to-day work is mostly Odoo support issues around invoices, coils and product variants.

Account basics

Odoo instance: 3gm.eoxs.com (db threegmsteels), domain 3gmsteel.com.
Contacts: Jessica Worley, Leslie Countryman, Travis Lane.
The original Odoo implementation ran from April to May 2022, with discovery and kickoff calls led by Rajat Jain and Sai Siddhartha Dutta. The Product Master import was completed by Alka Jain. 28 implementation tasks are on record, mostly completed, with a few internal sub-tasks still open.

AskCruz deal

On the Aug 12, 2026 proposal call, Travis confirmed the deal at a reduced 2-user scope and asked for a shorter initial term.
In Oct 2026 the final implementation invoice and first licensing payment were sent, and weekly usage check-ins were proposed. The latest emails are “AskCruz - 3GM Steel Weekly Check-ins”.
A customer story draft went to Raj for review on Oct 5.
Earlier in the rollout, an Outlook connection was blocked by an Azure AD admin-consent issue (resolved Sep 4), and historical data was preloaded for IRIS AI in Aug.

Open and recent support issues (Aug to Oct 2026)

Invoicing: INV/2026/2368 was confirmed correct. INV/2026/2403 is still unresolved after a second escalation (Oct 6). INV/2026/2434 shows a total-due mismatch against weight × CWT rate (Sep 30). Twelve coils invoiced under INV/2026/2246 still show as available, which distorts inventory and AR reports (Sep 21).
Purchase orders: Four POs (P04612 to P04615) hit the same “confirmed but can’t receive” bug, and three also need unlocking to fix the customer field (Sep 28). There is a recurring coil-upload error into POs (ND/IN/00015 and 00016) and a lot/serial related-price mismatch on SCP/OUT/02587.
Coil and inventory bugs: The coil search/availability bug on the tonnage card (CNJ/OUT/00074) has been open since June. SRTI./OUT/03994, where a coil is not found when added to a transfer, has been open since March.
Pricing: S11105 had a tonnage card and line-item pricing error (Aug).
Product setup: Many PRM color and width variant requests, including PRM:28, PRM:26, a hot-roll oxide-coated line and the Burgundy/Crimson Red variants (Aug to Oct).
Access: Matt Inman’s permissions were raised to match Jessica Worley’s (Aug).
Possible duplicate payment: An investigation into Reliable Metal Buildings LLC on INV/2026/2146 (Sep 4).

Call history: 13 calls on record, from 2023 dashboard and PO reviews through the 2024 server migration and open-ticket reviews, to the Jul 29, 2026 Travis Lane call and the Aug 12 proposal call.

Gaps

This connection doesn’t surface monetary amounts, so deal and invoice values aren’t available.
Three wiki pages for this client are restricted and not visible here.
Support tickets and invoice records live in EOXS Teams Odoo, which this connection doesn’t cover. The issue list above comes from wiki summaries and email subjects, not the tickets themselves.
I haven’t opened individual emails or call transcripts. I can drill into any of them, such as the proposal call or the INV/2026/2403 thread.

Note: The Notes connector with save_chat_transcript isn’t connected in this session, so this conversation wasn’t archived. Reconnect it in Settings → Connectors if you want it saved.

Sources: AskCruz client profile for 3gm-steel; live wiki page titles, emails and calls listed there.
