---
conversation_id: 7e64ca64-2c83-49d3-8821-62700a76e66c
platform: claude
username: "shubham"
title: "Wiki pages analysis"
created_at: "2026-10-12 10:29:38 EDT"
updated_at: "2026-10-12 16:19:36 EDT"
---

# Wiki pages analysis

## User (2026-10-12 16:19:36 EDT)

How many wiki pages do we have on customers, and how many on suppliers?

## Claude (2026-10-12 16:19:36 EDT)

**Customers: 223 wiki pages. Suppliers: 32 wiki pages.**

Several customer pages look like duplicates of the same company, so the number of distinct companies is probably a bit lower. Examples: Longreach Steel Inc (pages 233 and 234), Longhorn Steel Structures (232 and 458), Nova Building Solutions (462 and 463), and Greenfield Metals (298 and 299). Wheeling Nippon appears twice among the suppliers (176 and 628). I haven't checked whether these are true duplicates. The vault holds 675 live wiki pages in total, 410 of them entity pages. The 255 customer and supplier pages are part of those 410.

Sources: wiki list_wiki_pages (entity_class=customer, 223 pages; entity_class=supplier, 32 pages); get_vault_stats (675 live pages, 410 entity). ERP not consulted, since this is a count of wiki pages.

## User (2026-10-12 16:19:36 EDT)

Which people appear in the most wiki pages?

## Claude (2026-10-12 16:19:36 EDT)

I can't give exact wiki-page counts per person with these tools. Travis Lane and Stefan Brown are the most-mentioned people by a wide margin, and that holds in the wiki too: both hit the 50-page cap on every search.

- **Wiki search cap:** `search_wiki` returns at most 50 pages per query, ranked by relevance, so any name with 50 hits is truncated. Travis Lane, Stefan Brown, Matt Inman, Corey McGlothlin and Leslie Countryman all reached the cap. No tool here counts pages directly.
- **Proxy from raw mail:** The search results also report how many raw messages contain each name. Roughly in order:
  - Travis Lane: 8,873 messages
  - Stefan Brown: 8,802
  - Matt Inman: 3,229
  - Leslie Countryman: 1,400
  - Corey McGlothlin: 1,103
  - Matt Wilson: 10 (the name search also matched Matt Inman on "Matt", so the true count is lower)

  These count messages, not wiki pages, so treat them as a proxy.
- **Person pages:** Only 10 wiki pages are classed as people. Stefan Brown and Travis Lane each have their own page, and Corey McGlothlin, Matt Inman, Leslie Countryman and Matt Wilson also do. Most people appear only inside company and deal pages, which is why these ranks don't reflect page counts.

If you need exact page counts, I can search each name in the wiki's fact index, which has a different limit. Tell me if you want that.

Sources: wiki `list_wiki_pages` (entity_class=person, 10 pages: 47, 654, 398, 306, 629, 504, 92, 137, 138, 468); wiki `search_wiki` for "Corey McGlothlin", "Stefan Brown", "Travis Lane", "Matt Inman", "Leslie Countryman" and "Matt Wilson" (each capped at 50 hits; raw-message counts as reported in each result).

## User (2026-10-12 16:19:36 EDT)

What did Stefan send Travis yesterday?

## Claude (2026-10-12 16:19:36 EDT)

I can't answer this right now. The 3GM Vault connector has disconnected, so I can't read Stefan's mail. I haven't guessed at the contents.

Once the Vault is reconnected, I'll look for messages Stefan sent to Travis on Sunday, 11 October 2026, and list them with their subjects and times. Ask again then, or reconnect the Vault and I'll run it straight away.

Sources: none. No vault data was retrieved.
