---
conversation_id: ccd65019-6c90-486b-ba7a-d1e64e9702dc
platform: claude
username: "unknown"
title: "Testing AskCruz information retrieval - Claude"
created_at: "2026-10-13 09:21:07 EDT"
updated_at: "2026-10-13 09:21:38 EDT"
---

# Testing AskCruz information retrieval - Claude

## User (2026-10-13 09:21:38 EDT)

give me some ideas on which i can query claude about askcruz and perform some research to see whether its fetching information properly or not

## Claude (2026-10-13 09:21:38 EDT)

Here are test ideas for checking whether AskCruz fetches information correctly. They’re based on the AskCruz tools in this session: calls, emails, attachments, clients, contacts, implementation tasks, reference docs, repo docs, and the wiki.

A note first: I looked for an askcruz skill file and found only thread-wiki, so I’m working from the tool list alone. Also, save_chat_transcript isn’t connected in this session, so this conversation isn’t being archived.

1. Ground-truth checks (you know the answer)

Ask about things you already know, then compare:

“Tell me everything about [client you know well].” Check the profile against what you remember: contacts, domains, Odoo instance, recent activity.
“List all clients” and “How many contacts does [client] have?” Compare against your actual client registry.
“What did we discuss on the call with [client] last [month]?” Check it against what you remember from that call.
“What are the open implementation tasks for [client]?” Compare against the Kanban board.
2. Count and completeness checks
“How many calls do we have in [YYYY-MM]?” Check the number against Fireflies and Fathom directly.
“List only Fathom calls” versus “only Fireflies calls.” This tests the source filter.
“Give me the index/row counts across all tables.” Look for tables that are empty or implausibly small.
3. Search accuracy (precision and recall)
Search a distinctive phrase you know was said in a call and see whether the right call comes back.
Search a misspelling or abbreviation (e.g. “toll processing” vs. “toll proc”) to test fuzzy matching.
Search for something that shouldn’t exist, like a fake client name. A good system says “nothing found” instead of making something up.
Search the same topic across emails, calls, and the wiki, and see whether the answers agree.
4. Hallucination and faithfulness
Ask for a specific detail from a long transcript, like a decision or a name, then open the full transcript with get_call and verify it.
Ask for exact figures such as prices, dates, or quantities and verify them at the source.
Ask “Who said X in the call?” to test speaker attribution.
Ask for the source behind every claim, then check that the cited call, email, or page actually says it.
5. Cross-source consistency
Pick a client with calls, emails, and tasks. Ask for a timeline and check the order of events.
Ask “What’s the current status of [project]?” and compare the wiki’s answer with the latest emails and tasks. Does it flag conflicts, or pick one silently?
Ask about a policy or SOP and compare the answer with the raw reference document (get_asset).
6. Freshness
Ask for “the latest call” or “the most recent email from [client]” and check that it really is the newest one.
After a call you just finished, see how long it takes to appear. Live ingestion lag is a common failure point.
7. Edge cases
Ambiguous names (two clients with similar names) and contacts who appear under several domains.
Date handling, such as “last week” or calls near month boundaries.
Long transcripts and attachments, to test truncation and whether attachment text is extracted.

If you pick one or two of these, I can run them live against AskCruz and give you a side-by-side of what it returned and whether it checks out. A good first test is a client you know well, combined with a count check on one month of calls.
