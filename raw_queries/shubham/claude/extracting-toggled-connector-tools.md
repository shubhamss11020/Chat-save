---
conversation_id: 777a0e35-a5e0-4039-98ca-6320bad15c1a
platform: claude
username: "shubham"
title: "Extracting toggled connector tools"
created_at: "2026-10-06T13:35:40.582661Z"
updated_at: "2026-10-12 12:38:18 EDT"
---

# Extracting toggled connector tools

## User (2026-10-12 12:38:18 EDT)

extract all the tools of toggled on connectors and group them accordingly

## Claude (2026-10-12 12:38:18 EDT)

Here are the tools from the connectors enabled in this chat, grouped by connector.

## Claude Docs (5)
- `create`: create a tab, its contents, a comment, or an upload record
- `read`: read a doc, a tab's contents, or a comment
- `delete`: delete a tab, its contents, a comment, or an upload record
- `export`: export a tab as pdf, docx, html, text, markdown, or notion
- `query`: list a doc's or tab's comment history

## Eoxs-Teams (4): SQL on the EOXS Team Live (Odoo) DB
- `list_tables`
- `describe_table`
- `get_business_schema`
- `query` (read-only SELECT)

## Read-only (4): SQL on the askcruz (Odoo) DB
- `list_tables`
- `describe_table`
- `get_business_schema`
- `query` (read-only SELECT)

## Thread-wiki (5): eoxs_frontend_threads DB
- `list_tables`
- `describe_table`
- `get_business_schema`
- `query`
- `get_full_text` (single row and column)

## Internal-team (23) and Interns-mcp (23)
Both connectors expose the same 23 tools, so I've listed them once.

**Clients and contacts**
- `list_clients`
- `list_contacts`
- `get_client_profile`
- `get_client_file`

**Emails**
- `list_emails`
- `search_emails`
- `get_email`
- `get_attachment_text`

**Calls**
- `list_calls`
- `search_calls`
- `get_call`

**Implementation tasks**
- `list_implementation_tasks`
- `search_implementation_tasks`
- `get_implementation_task`

**Assets (SOPs and reference docs)**
- `list_assets`
- `search_assets`
- `get_asset`

**Repo docs**
- `list_repo_docs`
- `search_repo_docs`
- `get_repo_doc`

**Wiki and index**
- `search_wiki`
- `get_wiki_page`
- `get_index`

## threadvault-local (4)
- `vault_local_find`: search or list saved threads
- `vault_local_stats`: coverage statistics for a thread
- `vault_local_log_turn`: archive a chat turn
- `vault_local_backfill`: add missing earlier user messages

## Notes
- **Total:** 68 deferred connector tools, 46 of them the duplicated Internal-team and Interns-mcp set.
- **Connected, but no tools exposed here:** 3gm odoo, 3gm vault, thread, and Threads-Ov. They're linked to your account, but none of their tools are loaded in this chat.
- **ThreadVault:** your preference names `vault_save_turn` and `vault_backfill`, but this chat has `vault_local_log_turn` and `vault_local_backfill`. Since the names differ, I didn't archive this turn automatically. I can switch to the `vault_local_*` tools if you'd like.
- **Schemas:** these are the tool names and descriptions only. Parameters load when a tool is used.

## User (2026-10-12 12:38:18 EDT)

now tell me more about wiki and index and  what is the work of its tools,

## Claude (2026-10-12 12:38:18 EDT)

```

```

Three tools make up the Wiki and index group in Internal-team and Interns-mcp. The wiki is a layer of synthesized pages built on top of the raw emails, calls, tasks and documents, and these tools let you read it.

## `search_wiki(query)`
This is a full-text search over the synthesized wiki pages. Page types include entities, concepts, analyses, overviews, sources and prospects.

- Each result has an `id` you can pass straight to `get_wiki_page`.
- Each result also has `citations`, which are the raw sources the page was written from. Every citation names the tool and identifier to fetch it, such as `get_email/66376`.
- The tool descriptions say to try it first for almost any content question, even ones that sound like raw lookups ("find the email about X"). The reasoning is that a wiki page's citations point to the right thread, call or task more reliably than a keyword search over raw data, which can miss the thread if it doesn't contain every query word.
- Raw searches (`search_emails`, `search_calls`, `search_assets`, `search_implementation_tasks`) are the fallback when the wiki returns nothing relevant.

## `get_wiki_page(title, max_chars?, offset?)`
This fetches one specific page by title or partial title match. It returns:

- A body preview, the first 1500 characters by default, plus `body_length` and `body_truncated`.
- Outbound links to related pages.
- Flags.
- Citations, in the same format as above.

If `body_truncated` is true, the page isn't incomplete. Pass the returned `next_offset` back in as `offset`, and raise `max_chars` if you want bigger chunks.

## `get_index()`
This takes no parameters and returns row counts across all tables. The description calls it "the DB equivalent of the wiki index". It's useful as a quick check of what's loaded and how much data exists for emails, calls, tasks, wiki pages and so on.

## Typical workflow
1. `search_wiki("topic or client")` to find relevant pages and their citations.
2. `get_wiki_page(title)` to read the full synthesized page, paging with `offset` if it's long.
3. Follow a citation (`get_email`, `get_call`, `get_asset` and so on) when you need the exact original wording.
4. Use `get_index` when you just want to see the size and coverage of the data.

## Related tools
- **`get_client_profile(client)`** is better than chaining searches for a full client overview. It aggregates the client record, contacts, recent tasks, emails, calls and wiki pages in one call.
- **`Thread-wiki`** is a separate connector. It queries the `eoxs_frontend_threads` database, which includes a `wiki.pages` table, directly through SQL, so it works at a different level from these tools.

## User (2026-10-12 12:38:18 EDT)

extend plz

## Claude (2026-10-12 12:38:18 EDT)

```

```

```

```

I ran two read-only calls to ground this in real data: `get_index` on Internal-team and `describe_table` on `wiki.pages` via Thread-wiki.

## What `get_index` returned (Internal-team)

| Table | Rows |
|---|---|
| Wiki pages | 1,558 |
| Email threads | 31,017 |
| Fireflies calls | 2,225 |
| Fathom calls | 149 |
| Implementation tasks | 824 |
| Clients | 8 |

The wiki pages break down by type:

| Page type | Count |
|---|---|
| analysis | 601 |
| entity | 494 |
| source | 277 |
| concept | 138 |
| prospect | 35 |
| overview | 13 |

The type names come from the tool descriptions, and the descriptions of each type below are my reading of the names, not documented definitions. Entity pages are probably about a person, company or client. Concept pages are probably about a topic or process. Analysis pages are probably synthesized write-ups. Source pages are probably summaries of raw documents (the `get_asset` description says the wiki pages under `wiki/sources/assets/` are summaries of the raw text). Prospect pages are probably about potential clients. Overview pages are probably high-level summaries.

So about 1,500 curated pages sit on top of roughly 34,000 raw records. That's why the wiki is the recommended first stop: it's a much smaller, pre-digested layer, and each page points back to its raw sources.

## What a wiki page looks like underneath (`wiki.pages`)

`search_wiki` and `get_wiki_page` read from this table. The notable columns are:

- **`title`** is unique, which is why `get_wiki_page` can look pages up by title or partial title.
- **`page_type`** is the type listed above.
- **`entity_class` and `entity_name`** classify entity pages, and are indexed together.
- **`tags`** is a text array.
- **`body`** is the page text. **`body_tsv`** is a full-text search vector with a GIN index, which is what makes `search_wiki` fast.
- **`access_tier`** is indexed, so pages can be restricted by access level. This probably explains why Internal-team and Interns-mcp could return different results from the same tool, though I haven't tested that.
- **`created_date` and `updated_date`** show when a page was written and last revised.

## Practical tips

- **Start with `get_index`** to check that data is loaded and see how big each source is.
- **Search with entity names** such as a client or person, since those match entity pages and their citations.
- **Use `get_wiki_page` with `max_chars` and `offset`** for long pages. Paging avoids treating a truncated preview as the whole page.
- **Use citations to verify.** A wiki page is a summary, so for exact wording (an SOP step, a figure, a quote), follow its citation to `get_email`, `get_call` or `get_asset`.
- **For bulk analysis, use SQL.** Thread-wiki's `query` can filter `wiki.pages` by `page_type`, `tags`, `entity_class` or date, which `search_wiki` can't do.

## Caveats

- I ran `get_index` only on Internal-team. Interns-mcp has the same tool, but the counts may differ if the two connectors have different access scope.
- I haven't run `search_wiki` or `get_wiki_page` yet. Their behavior above comes from the tool descriptions. If you give me a client or topic, I can run a real search and show you the output format.
