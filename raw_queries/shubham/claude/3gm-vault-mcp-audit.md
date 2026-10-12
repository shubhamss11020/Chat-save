---
conversation_id: 959043c5-ee4c-470b-bf0b-f525b4888326
platform: claude
username: "shubham"
title: "3GM Vault MCP audit"
created_at: "2026-10-09T21:14:50.489874Z"
updated_at: "2026-10-12 10:34:44 EDT"
---

# 3GM Vault MCP audit

## User (2026-10-12 10:34:44 EDT)

Audit the 3GM Vault MCP for data-integrity problems. Examine record identifiers, references, parent-child relationships, metadata, timestamps, and links between related records wherever these are exposed. Identify orphaned records, invalid references, duplicate identifiers, mismatched relationships, and values that violate apparent data rules. Provide evidence and suggest the safest correction for each confirmed issue.

## Claude (2026-10-12 10:34:44 EDT)

I'll start by reading the 3GM navigator skill, as your preferences require for any 3GM question.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```


The skill is loaded. Next I'll pull the vault's scale and its page inventory so I know what I'm auditing.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```


The corpus is large (659 pages, 31,509 facts), so I'll focus on the places integrity problems usually show up: near-duplicate page titles, cross-page references, and citation integrity. I'll start with the near-duplicate pairs in the inventory, reading only the metadata and first facts to keep output small.
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







The first pass turned up real issues in the Bluestone, Discount Metal Roofing, and C O Building Systems clusters. Next I'll check whether the citation IDs they rely on actually resolve, and look at a few other suspicious pages.
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








The Dongkuk pages are too large to read in full, and the vault's own flags already document the main Dongkuk problem. Before I write up, I want to confirm one specific citation conflict on the Dongkuk International page: the AR balance figure cites two different attachments, one of which is unresolved.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```


Short answer: the vault has real integrity problems, and they cluster in three places. Dongkuk and two other customers each have duplicate live pages that were never merged. Several citations are stored with a null source ID even though the record exists. One attachment is stored under two IDs. I read 11 of 659 live wiki pages and 6 source records, so this is a sampled audit, not a full one.

## Confirmed issues, highest impact first

**1. Dongkuk is split across two live pages, and the merge never ran.**
- Page 166 "Dongkuk International Inc." (309 facts) and page 205 "Dongkuk" (546 facts) are both live. Each names the other as a possible duplicate.
- Both share the contact Roy Jeong (yunkyo.jeong@dongkuk.com) and the PO group P04225, P04227-P04233 / HPL202607002.
- Dozens of staging drafts say they are "deliberately titled to match" so that consolidation will merge them. The flags say no merge capability exists in that layer.
- The pages also disagree on what the entity is. Page 205's flags describe the Busan mill, and page 166 describes the Houston trading house. Page 166 concedes it cannot say which legal entity a given PO belongs to.
- Effect: a Dongkuk query can return two partial answers, and a dollar figure cannot be attributed to the right legal entity.
- Safest fix: do not merge yet. First add a legal-entity key (mill or trading company) to each fact, with a human decision on the split. Then merge into one page and keep the other page ID as a redirect.

**2. Bluestone has two live pages for one account (28 and 574).**
- Page 574 uses "Bluestone Carports and Garages LLC" and page 28 uses "Bluestone Carports & Garages." Both list the same salesperson (Maggie Moore) and the same contacts, and both point to Euler Hermes policy 5124811. Each flags the other as a possible duplicate.
- Fix: merge 28 into 574, which has the fuller legal name and buyer number, and keep 28's ID as an alias.

**3. Page 28 contradicts its own citation on invoice INV/2026/0160.**
- The body says whether that invoice was resolved "is not stated by anything read in this chunk." Yet its fact `wire_received_usd` = 48,385.64 (as of 3 Mar 2026) cites message 70189.
- I opened 70189. It is Stefan Brown's message "Showing a wire of $48,385.64 in today," dated 3 Mar 2026. That shows the wire was received, not that it was applied to the invoice.
- Fix: rewrite the open question to cite 70189, and mark application to INV/2026/0160 as needing ERP confirmation.

**4. Citations with a null source ID, where the ID is present in the raw reference.**
- Page 28 has three such citations (raw "70200", "70189", "18506"). I verified that all three records exist: 70200 and 70189 are Bluestone messages, and 18506 is the "Past Due Invoices 3.3.26" workbook.
- Page 166 has six (raw 63772, 63813, 63839, 70491, 18721, 70507). I verified that 18721 exists.
- These are the citations the skill says must be checkable, and `get_source` cannot resolve them as stored.
- Fix: backfill `source_id` from the raw reference where it is a plain integer, verify the type, and log every change. Leave prose-only references flagged.

**5. One AR confirmation letter is stored under two attachment IDs.**
- Attachments 18721 and 19062 are the same PDF: same filename, same 231,242 bytes, same extracted text. They have different internet message IDs, so they came in on two separate emails.
- Page 166 uses 18721 for the $2,513,284.83 amount and 19062 for the as-of fact. Its citation list also names 18755 as the same letter. I did not open 18755.
- The OCR renders the year inconsistently, and the page already flags that.
- Fix: choose one canonical attachment ID, add a duplicate pointer, and cite that ID for every fact. The two messages stay as separate delivery records.

**6. C O Building Systems has two live pages with conflicting class and legal name.**
- Page 391 (class customer) and page 392 (class prospect) share the same address (320 W 100 N, Ephraim UT) and purchasing contact (Jana Mann). Page 391 holds PO 18025 for $77,035.84 (attachment 45160), so "prospect" on 392 is wrong for the same entity.
- Legal name: 391 says "C O Building Systems and Manufacturing, Inc." (attachment 44721). 392 says "CO Building Systems & Manufacturing" (credit application 44753). Neither is reconciled with the other.
- `engagement_verified` is "unknown" on 391 and "two-way" on 392, despite a placed PO.
- Fix: merge. Set class to customer, check 44721 against the signed credit application, and set engagement to two-way with a citation to the PO thread.

## Smaller issues

7. **Page 52 asserts a role the evidence does not support.** Its fact `role` = customer is marked agent judgement, and its body says nothing shows a trading relationship. The only source is one insurer notification. Fix: set the role to insured buyer with no trade evidenced. Keep it separate from page 345, which has a different buyer number under the same policy.

8. **AkzoNobel (622) links to itself and has zero facts.** Its links out and in both contain 622→622, twice each, labelled "likely duplicate." The page has no facts, even though its price letter gives dated percentages (9% domestic surcharge from 1 Jun 2026, 20% on import volume on top of an earlier 6%, about a 60-day lag). `find_facts` cannot return those numbers. Fix: remove the self-links and record the price terms as cited facts with as_of 2026-04-17.

9. **Facts cite sources missing from the page's citation index (page 9, 3GM Holdings).** `citation_count` is 1 (message 202518), but facts also cite attachments 13976 and 17681 and message 67851. Fix: regenerate the index from fact-level references.

10. **Quote facts have no as-of or expiry (page 384, 3MG Roofing).** The price facts (110.50, 74.85 and 71.30 per cwt) have `as_of` null. The body says the 110.50 offer was valid until 16 Jan 2026. A "current price" query would return an expired quote with no staleness marker. Fix: add as-of and valid-until to every price fact.

11. **Timestamps are empty.** `created_date` and `updated_date` are null on all 11 pages I checked. Freshness can only be guessed from `as_of`, which is often missing too.

12. **Rejected duplicates are stored as ordinary links, and duplicate detection is noisy.** Page 384 has a link to page 203 whose own context says "declined duplicate candidate." Page 384 also carries six "possible duplicate" flags, all triggered by the shared word "Roofing" (title similarity 0.667). Fix: keep rejected candidates in their own table, and exclude generic industry words from title matching.

13. **Lower priority:** page 166's header reads "[Reviewed draft 3019, unknown source]," so provenance is missing. Entity classes are inconsistent ("company," "group-entity," "customer," and null on Eagle Manufacturing). The same email appears in two case variants on page 384. The vault's flags also record two Houston addresses for the Dongkuk entity (#350 and #860); that may be legitimate, but it is worth checking.

**Likely root cause (a hypothesis, not verified):** the consolidation step defers identity decisions to humans, and that queue does not appear to be worked. Live pages then keep accumulating additions that say they will be merged later.

## What checked out

- Page 384's facts match their source. Message 298457 is dated 12 Jan 2026 and says what the page claims.
- The mailbox counts sum correctly: 403 + 42 + 55 + 159 = 659.
- Pages 52 and 345 are correctly kept apart pending evidence. The flags on both are appropriate.
- The Bluestone spreadsheet (attachment 18506) lists INV/2026/0160 for $48,385.64, matching page 28's fact.

## Limits

- `list_wiki_pages` returned 100 of 659 pages and has no offset, so I could not enumerate every page for orphan or duplicate-ID checks.
- I read only excerpts of pages 166 and 205 (146k and 244k characters). Staging pages are not exposed, so I could not check the IDs the flags name.
- I did not cross-check any figure against the ERP, since this audit is of the vault.
- The skill's snapshot (536 pages, 11,728 facts) is out of date against the current stats (659 pages, 31,509 facts). That is the documentation, not the vault.

I can page through the remaining pages in batches if you want fuller coverage, though it will take many calls.

Sources: wiki pages 384, 574, 28, 52, 345, 391, 392, 9, 622, 205, 166 (get_wiki_page) · outlook messages 298457, 70189, 70200 (get_source) · outlook attachments 18506, 18721, 19062 (get_source) · vault stats and page list (get_vault_stats, list_wiki_pages)
