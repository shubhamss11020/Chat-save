---
conversation_id: d52930c3-32e2-40ba-a746-e2f6c56f50e6
platform: claude
username: "shubham"
title: "Finding askcruz client data"
created_at: "2026-10-13 05:40:00 EDT"
updated_at: "2026-10-13 05:40:24 EDT"
---

# Finding askcruz client data

## User (2026-10-13 05:40:24 EDT)

How can we find data related to askcruz clients

## Claude (2026-10-13 05:40:24 EDT)

I'll start by reading the relevant skill files.

The fastest route is `get_client_profile`, which you call with a client's slug or a name fragment (e.g. `sabre-alloys`). It returns the client record, contacts, implementation tasks, recent emails, recent calls and related wiki pages in one call. If you're not sure of the slug, run `list_clients()` first. 8 clients are visible in this session.

| If you need... | Use |
|---|---|
| Everything on one client | `get_client_profile` |
| A topic, person or "what's the story with X" | `search_wiki`, then follow the citations to the underlying email or call |
| Exact wording of an SOP or reference doc | `get_asset` |
| Onboarding and dev work (Odoo Kanban) | `list_implementation_tasks` or `search_implementation_tasks`, filtered by client or stage |
| Raw email or call detail | `search_emails` / `list_emails` and `search_calls` / `list_calls`, then `get_email` / `get_call` with the `id` |
| Contacts | `list_contacts` |

- **Search order:** Start narrow with the wiki. Only fall back to raw email and call search if the wiki comes back thin.
- **Use the `id`:** Always pass the `id` from a search result to the matching `get_*` tool. Don't guess file paths.
- **Filters:** `client`, `stage`, `source` (fireflies or fathom) and `account` save extra calls.
- **Past Claude conversations:** If you're looking for previous Claude chats about a client rather than the client's own data, use the Threads-Wiki connector. It reads the conversation archive with SQL.

On this connection, monetary amounts show as `[restricted]`. It has no access to support tickets, invoices, sales orders or CRM data. It also can't see the full task boards. Those live in the EOXS Teams Odoo database, which needs a broader connection than this one.

I couldn't archive this conversation. The conversation-saving tool isn't connected in this session (only the read-only Threads-Wiki is), so nothing from this chat was saved.

If you tell me which client you're interested in, I can pull its profile now.
