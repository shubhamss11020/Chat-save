---
conversation_id: 90108a71-eff8-4a3e-96d8-cf0bad3ebdce
platform: claude
username: "harsh"
title: "Finding EOXS client details in connectors - Claude"
created_at: "2026-10-13 06:55:27 EDT"
updated_at: "2026-10-13 06:55:29 EDT"
---

# Finding EOXS client details in connectors - Claude

## User (2026-10-13 06:55:29 EDT)

How we can find eoxs client detail in which connector

## Claude (2026-10-13 06:55:29 EDT)

For EOXS client details, use the AskCruz connector.

list_clients shows every client with its slug, display name, domains and Odoo instance. Use it first if you aren’t sure of the exact name.
get_client_profile is the main tool. Pass a slug (e.g. sabre-alloys) or part of the display name. It returns the client record, contacts, recent implementation tasks, emails, calls and wiki pages in one call.
list_contacts gives contact names and emails for one client, or for all clients if you leave the client blank.
list_implementation_tasks and search_implementation_tasks cover onboarding and development work per client.

You can open any item the profile returns with get_email, get_call or get_implementation_task, using the id from the profile.

This connector doesn’t cover support tickets, invoices, sales orders or CRM data. Those sit in the EOXS Teams Odoo, which isn’t reachable from this connection. Claude conversations about a client are a separate system, Threads-Wiki.

The conversation-saving connector (the one with save_chat_transcript) isn’t connected in this session, so this chat hasn’t been archived. To fix that, reconnect it in Settings → Connectors.

If you tell me which client you’re after, I can pull the profile now.

## User (2026-10-13 06:55:29 EDT)

find about brannon steel

## Claude (2026-10-13 06:55:29 EDT)

Brannon Steel (slug brannon-steel, domain brannonsteel.com) is an EOXS client whose main work is “MTR AI”. That is AI matching of mill test reports (MTRs) against specs and heat/batch data. This is based on the client profile and one wiki page.

Contacts

David Brannon
Kevin (K.R.) Brannon
Manish Trivedi (P.Eng., the signer on the latest proposal)
Ranim Fallaha (APQP Manager)

Timeline

Nov 2025: MTR and AI discussions begin.
Jan 21, 2026: MTR AI project kickoff.
Feb 2026: Weekly Tuesday “Implementation Huddle” calls start.
Mar 3 to Aug 18, 2026: 19 of the 26 calls on record are Implementation Huddles. The most recent is Aug 18.
Aug 2026: The Algoma Join Report enhancement went live in production. It resolves heat/batch number mismatches on Algoma MTRs and is billed on invoice INV/2026/0295.
Sep 10–11, 2026: The Pre-Purchase MTR–Spec Verification proposal was signed. It checks MTRs against spec before purchase, without storing the MTRs in the system. Work was due to start Sep 14, 2026.

Other items in the record

There is a wiki page on an “MTR Inventory Module: Escalation vs. Ticket Status Conflict”, which I haven’t read.
Rajat has offered Manish as an MTR AI reference for Ohio Strip Steel (Oct 2026).
The profile shows no implementation tasks in the Kanban for this client.

Limits

Dollar amounts are not visible on this connection.
Tickets, invoices and CRM data aren’t in this system. They’re in EOXS Teams Odoo.
I haven’t read the call transcripts or individual emails, so detail on the huddles is missing.
The latest huddle on record is Aug 18, so anything after that, including whether work started on Sep 14, isn’t confirmed.

Sources: client profile brannon-steel; wiki page “Brannon Steel — MTR AI: Algoma Join Report (Live) & Pre-Purchase MTR–Spec Verification” (citing email thread 215).

I can read the “Escalation vs. Ticket Status Conflict” page or the latest huddle transcript (call 2395) if you want more detail.

The conversation-saving connector still isn’t connected in this session, so this chat isn’t being archived. Reconnect it in Settings → Connectors.
