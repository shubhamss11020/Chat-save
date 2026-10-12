---
conversation_id: 86ef6ced-aaaa-4542-831a-93037223fe65
platform: claude
username: "shubham"
title: "3GM Vault MCP search testing"
created_at: "2026-10-09T21:14:35.054198Z"
updated_at: "2026-10-12 10:33:53 EDT"
---

# 3GM Vault MCP search testing

## User (2026-10-12 10:33:53 EDT)

Test the search and retrieval capabilities of the 3GM Vault MCP using different search terms, partial names, exact matches, similar terms, and available filters. Check for relevant records that are missed, irrelevant records that are returned, inconsistent results for equivalent queries, and failures to retrieve information that is demonstrably available. Document reproducible examples and explain the likely cause of each issue.

## Claude (2026-10-12 10:33:53 EDT)

I'll start by loading the navigator skill and the vault tool schemas.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```


The skill is loaded and the tools are available. I'll start with baseline checks: identity, corpus size, and a known counterparty searched several ways.
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






The first batch shows a few things worth checking further: the connection isn't signed in, the stats differ from the skill's snapshot, and "Dongkuk Steel" pulls in unrelated "Steel" pages. The raw-mail counts also differ between spellings ("Dongkuk" 879–951 vs "Dong Kuk" and "Dongkok" 0). Next I'll test the raw mail search directly.
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






The raw search does spelling correction ("Dongkok" → "Dongkuk", 951 hits), but "Dong Kuk" matches nothing, and the wiki's raw-count disagrees with the raw search. Next I'll test people resolution and sender filters, where the skill makes specific claims.
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








Sender-name resolution works for the exact name, and a misspelling still resolves. Two things to probe further: surname-only "Worley" also pulls in a different person (madyson.worley@kloeckner.com), and the Jessie Choi display name carries literal quote marks. Next I'll run the same sender query with and without a date window, plus the duplicate-page and fact checks.
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









Both wiki page reads returned far more than the requested limits, which I'll note. The "Dongkuk Intl" lookup also resolved to the "Dongkuk" page rather than "Dongkuk International Inc.", so I'll check how facts split across the two duplicate pages and whether a cited source resolves cleanly.
```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```

```
This block is not supported on your current device yet.
```



The vault's search is strong on misspellings, exact phrases, sender resolution, and date windows. It is weak on company-name variants, on duplicate entity pages, and on payload control. Every finding below comes from the calls I ran in this session. The causes are inferred from the outputs, not confirmed against the code.

**Connection:** `whoami` returned `signed_in: false`, so `mailbox="mine"` is unavailable here. The call failed cleanly with the expected message. I used `travis`, `stefan`, or no mailbox filter.

**What works**

- **Typo correction (raw search and subject search):** `search_raw "Dongkok"` was corrected to "dongkuk" and returned 951 matches, the same as the correct spelling. `list_emails subject="Bluscope contract prce build sheet"` corrected both words and found the thread.
- **Sender resolution:** `list_emails sender="Jessca Worley"` resolved to Jessica Worley and returned the same 19 messages as the exact name.
- **Exact phrases:** `search_raw "DK Inventory Shipment"` matched the phrase in 19 messages across 4 conversations.
- **Conversation grouping:** the subject "BlueScope Contract Price Build Sheet" correctly split into a 7-message exact-subject conversation and a separate 2-message "RE:" conversation, and flagged both.
- **Filters:** Eastern date windows are inclusive and counts are consistent (19 messages from Jessica, Oct 1–10). `human_only=true` removed all newsletters from the result.
- **Retrieval by id:** `get_source` returned msg 301284 with full headers and quoted thread.
- **Invalid parameters:** passing `date=` was rejected with the valid parameter list.

**Issues, with reproducible calls**

1. **Spaced company name finds nothing in mail.** `search_raw "Dong Kuk"` returns 0 messages, 0 threads, with `matched_as` falling back to "dong" AND "kuk". `search_raw "Dongkuk"` returns 951. `search_wiki "Dong Kuk"` still returns the Dongkuk pages (page 205 score 0.545), with `raw_mail_matches: 0`. Likely cause: the raw index treats "Dongkuk" as one token, and spelling correction only handles edit distance, not word splits. The wiki search matches the title by fuzzy trigram, so it finds the company while the mail search cannot.

2. **The wiki count ignores the spelling correction.** `search_raw "Dongkok"` is corrected to "dongkuk" (951 matches), but `search_wiki "Dongkok"` reports `raw_mail_matches: 0`. Likely cause: correction is applied only in the raw path.

3. **Common-word noise in wiki search.** `search_wiki "Dongkuk Steel"` returns Gideon Steel Panel (score 0.324), Steel Dynamics (0.318), Real Steel (0.316), and Leggett Steel (0.273) alongside the Dongkuk pages. Only the Dongkuk pages are relevant. The phrase is not required, so the shared word "Steel" drives the ranking.

4. **Two live pages for one counterparty, and the ranking flips.** Page 205 "Dongkuk" and page 166 "Dongkuk International Inc." describe the same company. Their own flags say "identity unproven". The top hit changes with the query:
   - `search_wiki "Dongkuk"` (entity filter): 205 first (score 1.1), 166 second (0.433).
   - `search_wiki "Dongkuk Steel"`: 166 first (0.938), 205 second (0.757).

   Facts are split as well. `find_facts page="Dongkuk" key_words="price per mt"` returns only page 205 facts (SW RMP price per MT, P04224 prices). The same query on page 166 returns different facts (net-30 and net-60 prices, prior price). A "what did we quote Dongkuk" question sees only part of the record unless both pages are queried.

5. **Abbreviated title resolves to the wrong duplicate.** `get_wiki_page title="Dongkuk Intl"` returned page 205 "Dongkuk" with `title_match: closest`, listing 166 only as "other close title", even though "Intl" abbreviates 166's title. Likely cause: fuzzy title matching favours the shorter stem.

6. **Surname-only sender pulls in a second person.** `list_emails sender="Worley"` (mailbox travis, Oct 1–10) lists `madyson.worley@kloeckner.com` in `senders_used` and marks him `used: true`. The counts and `by_person` show only Jessica (19 messages). The "used" list and the counts disagree. In the no-date version the total is 1,449, again Jessica only. Anyone reading `senders_used` would think two people were matched.

7. **Display names carry literal quote marks.** `find_people "Jessie Choi"` returns the name as `'Jessie Choi'`, with the apostrophes. Matching still works, but the quotes show in every name that is printed.

8. **Requested limits are not honoured on wiki pages.** `get_wiki_page title="Dongkuk" facts_limit=5 body_chars=800` returned 10 facts and a 1,000-character body. The response exceeded the transport limit and was truncated twice (once for each DK page call). Citations and links are returned without any cap.

9. **Search excerpts show drafting metadata, not content.** `search_wiki "Dongkuk"` leads with "[Merged from a draft by outlook_3gm_stefan_outlook] This draft is an addition to the existing Dongkuk drafts (staging 63, 64, 471…)". The page-166 excerpt begins "[Reviewed draft 3019, unknown source]". The excerpt is taken from the drafting preamble, so it is useless for triage.

10. **A pre-archive window looks like "no mail".** `list_emails since=2025-08-01 until=2025-08-31` returns 0 messages with `coverage.complete: true` and no archive-start notice. The archive starts 2025-09-01. A user would reasonably read this as "nothing happened".

11. **Navigator skill figures are out of date.** The skill's snapshot (2026-09-30) gives 536 pages, 11,728 facts, 22,026 messages, and 10,781 attachments. Live stats today are 659 pages, 31,509 facts, 25,178 messages, and 14,226 attachments. The skill says to check `get_vault_stats`, so this is staleness rather than a retrieval fault.

**Not tested:** `find_thread`, `top_correspondents`, `list_attachments`, paging with `offset`, `get_attachment_text` pagination, `find_facts` with `value_contains`, and `human_only` on wiki search.

Sources: msg 301284 · msg 301391 · msg 301313 · msg 67328 · msg 65277 · msg 65263 · att 49397 (msg 301017) · att 46274 (msg 291481) · wiki page 205 "Dongkuk" · wiki page 166 "Dongkuk International Inc." · wiki page 81 "KG Steel USA, Inc." · wiki page 424 "Korea CORE Antidumping Duty Review" · wiki page 449 "3GM Steel 101" · ERP: none queried
