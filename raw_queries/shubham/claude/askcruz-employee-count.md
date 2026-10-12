---
conversation_id: 280cb7be-de6b-438b-b6d4-af494e6929a4
platform: claude
username: "shubham"
title: "Askcruz employee count and functionality - Claude"
created_at: "2026-10-12T18:07:08.567362Z"
updated_at: "2026-10-12 14:14:24 EDT"
---

# Askcruz employee count and functionality - Claude

## User (2026-10-12 14:14:24 EDT)

How many employees work in askcruz?

## User (2026-10-12 14:14:24 EDT)

How many employees work in askcruz?

## Claude (2026-10-12 14:14:24 EDT)

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

The wiki doesn't give a total headcount for AskCruz. The closest figure is **45 people**, the number scored in the weekly report for the 2026-08-31 to 2026-09-06 week, across five departments: HR, Support and Functional & Implementation, AI & Innovation, AI & Innovation (Intern Cohort), and PR & Branding. That count leaves out 8 people with no Cattr data and three standing exclusions, so the true headcount is probably higher.

I also searched the client registry, and AskCruz isn't listed as a client, so this appears to be an EOXS-side internal tool rather than a company. If you meant a different count, such as total EOXS staff or people on a specific team, tell me which and I'll check.

Sources: email threads 68439, 68440, 68441 and 68455 (EOXS Weekly Scored Report and Weekly Scores DATA, 2026-08-31 to 2026-09-06). Wiki page 2090, "EOXS Weekly Scored Report — Aug 31–Sep 6, 2026: DATA Correction and Three Resends." That page is marked tier2 confidential HR.

## Claude (2026-10-12 14:14:24 EDT)

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

The wiki doesn't give a total headcount for AskCruz. The closest figure is **45 people**, the number scored in the weekly report for the 2026-08-31 to 2026-09-06 week, across five departments: HR, Support and Functional & Implementation, AI & Innovation, AI & Innovation (Intern Cohort), and PR & Branding. That count leaves out 8 people with no Cattr data and three standing exclusions, so the true headcount is probably higher.

I also searched the client registry, and AskCruz isn't listed as a client, so this appears to be an EOXS-side internal tool rather than a company. If you meant a different count, such as total EOXS staff or people on a specific team, tell me which and I'll check.

Sources: email threads 68439, 68440, 68441 and 68455 (EOXS Weekly Scored Report and Weekly Scores DATA, 2026-08-31 to 2026-09-06). Wiki page 2090, "EOXS Weekly Scored Report — Aug 31–Sep 6, 2026: DATA Correction and Three Resends." That page is marked tier2 confidential HR.

## User (2026-10-12 14:14:24 EDT)

Make a pdf on the working of askcruz and it's overall functionality

## Claude (2026-10-12 14:14:24 EDT)

Claude responded: The PDF is ready: AskCruz_Overview.pdf.
Created a file, shared a file, and 8 more steps

Created a file, shared a file, and 8 more steps

The PDF is ready: AskCruz_Overview.pdf. It covers what AskCruz is, the size of its knowledge base, how the pipeline works (capture, raw storage, wiki synthesis, query), how citations and contradictions are handled, access tiers, the tools the agent exposes, and known issues.

Some of the content is provisional. Several source pages are marked unverified because their call transcripts were garbled or partly unreadable. The document says so in its caveats section. The exact citation-automation change and the contradiction routing should be confirmed with Ron J and Ayan Dutta before anyone relies on them.

I kept individual names out of the document, and I left out the HR scoring details because that material is restricted.

Askcruz overview
Document·PDF 
Download

## User (2026-10-12 14:14:24 EDT)

How many clients do we have?

## Claude (2026-10-12 14:14:24 EDT)

You have 8 clients in the AskCruz registry, and the index count agrees:

3GM Steel
Brannon Steel
Discount Pipe & Steel
Eastern States Steel
Ohio Strip Steel (formerly Greer Steel)
PPC Metals
RW Conklin Steel
Sabre Alloys

Brannon Steel and RW Conklin Steel have no Odoo instance listed. The other six each have one.

Source: AskCruz client registry (list_clients) and index totals (get_index).

## User (2026-10-12 14:14:24 EDT)

What is 3gm?

## Claude (2026-10-12 14:14:24 EDT)

3GM Steel, Inc. (also written “Three G M Steel”, doing business as 3GM Steel) is a Kentucky corporation that trades, distributes and manufactures steel, based at 1650 W. Highway 80 in Somerset, KY. In October 2026 Travis said its primary inventory is in Kentucky and Indiana.

Some context from the vault:

Group: The wiki’s group overview treats 3GM Steel as the hub of a small group of related companies, including Mac Metal Sales (same Somerset address, administered by the same CFO). The legal link between 3GM and Mac Metal is not established in any source, so the wiki marks it unverified.
Financials (dated, unaudited): A December 31, 2025 tax-basis compilation by an outside CPA firm shows total assets of about $107.6M, sales of about $152.4M for the year, and net income of about $6.5M. The accountants gave no assurance on these figures. For current numbers, the ERP is the authority.
Corporate activity: In early October 2026 the company’s lawyers circulated draft documents for an asset purchase from CMT Financial LLC, with Stefan Brown as CFO signing for the buyer. This is in progress, not complete.

I haven’t queried the ERP for current figures, so I can do that if you want live numbers alongside these.

Sources: page 191 (3GM Steel, Inc.: aliases, Dec 2025 compilation facts, att 18170); page 666 (3GM Group Structure, as of 2026-10-12); msg 292031 (Travis Lane, “RE: ISS Expo - 3GM Steel Follow-Up”, 2026-10-02); att 49576 and att 49578 (msg 301353, “RE: 3GM / CMT - Asset Purchase Agreement”, 2026-10-09).

## User (2026-10-12 14:14:24 EDT)

Show me every available information about the Mac Metal saled invoice, and identify which sources you searched

## Claude (2026-10-12 14:14:24 EDT)

The only invoice I can find matching “Mac Metal Sales invoice” is MID-SHIP Logistics invoice #62279773, dated September 24, 2026. It bills Mac Metal Sales $15,600.00 in barge demurrage for five barges on the Royal Orion / July ‘26 project. I couldn’t check it against the ERP because the ERP tools didn’t load in this session.

I read “saled” as “sales,” since no record matched the literal spelling.

Invoice details (from the PDF attachment)

Issuer: MID-SHIP Logistics, LLC (a Watco company), MidShip NY, Port Washington, NY
Bill to: Mac Metal Sales, 1650 West Highway 80, Somerset, KY 42503
Project: Royal Orion / Mac Metal Sales / July ‘26, Project ID 52321
Terms: Net 30, so due about October 24, 2026
Line items: five barges, all loaded at Avondale, LA and discharged at Jeffersonville, IN, each charged at $400/day after six free days:
IN-075244: 7 billable days, $2,800
IN-165496: 8 days, $3,200
IN-176009: 6 days, $2,400
SCF-26121B: 7 days, $2,800
T-13938: 11 days, $4,400
Two other barges (IN-165469, SCF-28100B) incurred no demurrage.
Remittance: the PDF lists MID-SHIP’s account, but the cover email gives a new remittance address, SCSAR@watco.com.

Correspondence

Sep 24, 2026, 12:27 PM: MID-SHIP’s LogInvoices mailbox (Mike O’Connell) sent the invoice to Jessica Worley and Matt Inman, with the new remittance email.
Sep 24, 2:56 PM: Jessica forwarded it to Stefan Brown with “ARE YOU KIDDING ME?!? Ouch.” She noted the delay was at the port loading the barges, not MID-SHIP’s fault.
Sep 24, 3:15 PM: Stefan replied, “Yea feels like they are leaving them there on purpose.”

Flag: The remittance address changed in a cover email. Confirm it directly with MID-SHIP through a known contact before paying.

Not found: Any mention of this invoice in the wiki, any wiki fact, or any ERP record. The Mac Metal Sales wiki page had no invoice facts matching these terms. I haven’t checked whether the invoice was paid, or whether Mac Metal Sales or 3GM booked it.

Sources searched

Vault wiki search “Mac Metal Sales invoice” (returned the Mac Metal Sales, Inc. page 307 and related pages; none contained this invoice)
Vault raw mail search “Mac Metal invoice” (returned 364 raw matches; I scanned subjects and attachment names and found the invoice threads)
Vault raw mail search “62279773” (2 messages, 1 attachment, 1 thread, complete)
Vault attachment text, att 46001
Vault thread expansion from msg 262337 (2 messages, complete)
Vault fact search on Mac Metal Sales, Inc. for invoice, demurrage, barge, MidShip terms (no matches)
ERP: not queried. The ERP tools weren’t loaded after two ToolSearch attempts.

Sources: msg 262337 (FW: Mac Metal Sales -Invoice # 62279773, 2026-09-24 14:56 ET) · msg 262385 (Re: Mac Metal Sales -Invoice # 62279773, 2026-09-24 15:15 ET) · att 46001 (62279773.pdf, msg 262337) · page 307 (Mac Metal Sales, Inc., searched, no invoice facts)

## User (2026-10-12 14:14:24 EDT)

What did we agree to with our top supplier and has it been followed through?
