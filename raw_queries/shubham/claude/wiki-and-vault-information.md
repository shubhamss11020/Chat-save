---
conversation_id: 1e7c88e7-ab73-478d-8cc9-567fc7b21513
platform: claude
username: "shubham"
title: "Wiki and vault information"
created_at: "2026-10-12T14:28:04.972164Z"
updated_at: "2026-10-12 10:28:16 EDT"
---

# Wiki and vault information

## User (2026-10-12 10:28:16 EDT)

What are the three most recent analysis pages in the wiki?

## Claude (2026-10-12 10:28:16 EDT)

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





The three most recent analysis pages, by the dates their content records, are:

1. **Seametal 400MT Acrylic-Coated Offer (October 2026)**: Travis Lane, Stefan Brown, Tadd Sapone and Matt Inman worked a 400 MT offer from Seametal on 2026-10-06. The deal was still under negotiation, and the offer price was valid through 2026-10-07.
2. **Fraudulent "Blanchard" Consulting Invoice (BEC Attempt, October 2026)**: a business-email-compromise attempt impersonating Corey McGlothlin was received by Stefan Brown on 2026-10-05. The page flags that the archive doesn't show whether any payment was made.
3. **Mac Metal Sales — unnamed manufacturing acquisition, first seen 2026-09-28**: an asset purchase of a roughly 70-employee manufacturer, expected to close in 2–4 weeks. The target is never named.

The wiki's list view doesn't expose creation or update timestamps, so I ranked these by the event dates in each page's content. If you want ranking by when a page was added or last edited, that metadata isn't available through these tools. Also, the "October 2026" in some titles, such as ASTA October 2026 PT Order, refers to the order's delivery timing; the activity itself happened in July.

Sources: wiki pages 558 (outlook_message 301133, 301144), 546 (outlook_message 301027, outlook_attachment 49411), 536 (outlook_message 277303, 277332); list_wiki_pages(page_type=analysis), 163 pages total.

## User (2026-10-12 10:28:16 EDT)

What’s the newest email in the vault, and who sent it?

## Claude (2026-10-12 10:28:16 EDT)

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

The newest email in the vault is "CMT Insurance," sent by Stefan Brown (stefan@3gmsteel.com) to Calvin Nissley (calvin@cmtcomponents.com) on 2026-10-12 at 08:53 ET. It has no attachments. In the excerpt, Stefan asks Calvin for his latest insurance policy on the real estate, and says the attorneys are still working through the redline reply on the PA and the noncompetes.

It appears only in Stefan's Sent Items, so it's an outgoing message from his mailbox.

Sources: msg 301455 (list_emails, newest first)

## User (2026-10-12 10:28:16 EDT)

What’s the difference between an analysis page and an entity page, per the vault’s own structure?

## Claude (2026-10-12 10:28:16 EDT)

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

In the vault, an **entity page** describes a standing thing: a company, person or place. An **analysis page** describes a bounded deal or matter, such as a single order, claim, negotiation or acquisition.

Examples from the wiki:
- **Entity:** "POSCO International America" (page 256) and "3GM Steel, Inc." (page 191, classed as a group-entity). Each records a counterparty or company across all its dealings.
- **Analysis:** "ASTA October 2026 PT Order" (page 20), which covers one mill order, and "Mac Metal Sales — unnamed manufacturing acquisition" (page 536), which covers one acquisition.

Entity pages carry an `entity_class` such as customer, supplier, prospect, or group-entity. Analysis pages almost always have none, which is consistent with their being about a matter rather than a party. Both page types hold cited facts.

The vault doesn't have a page that defines the types. The overview pages I checked (3GM Group Structure, Active Matters, Obligations Register) don't cover this, and the only definition I found is in the 3gm-navigator skill: entity (company/person/place), analysis (a bounded deal or matter), source (a recurring report template, one page per template), and concept (a process or standing arrangement). The examples above come from the page listings, not from a rulebook. If you want the full rules, that would be the taxonomy document, which I couldn't locate in the vault.

Sources: wiki pages 191, 256 (search_wiki "page types entity analysis…"), 20, 536 (list_wiki_pages); overview pages 666, 667, 670 (list_wiki_pages page_type=overview); 3gm-navigator skill, "Page anatomy" section.

## User (2026-10-12 10:28:16 EDT)

Which emails from the last week have “urgent” in the subject?

## Claude (2026-10-12 10:28:16 EDT)

I can't answer this right now. The 3GM Vault connector is disconnected, so I can't search email subjects, and I'm not going to guess at results.

Once the connector is back, I'll search for "urgent" in subject lines from 2026-10-05 through today, 2026-10-12, both mailboxes unless you want one. I'll list each match with sender, recipients, time in ET, and message IDs.
