---
conversation_id: ccd65019-6c90-486b-ba7a-d1e64e9702dc
platform: claude
username: "unknown"
title: "Testing AskCruz information retrieval - Claude"
created_at: "2026-10-13 09:21:07 EDT"
updated_at: "2026-10-13 09:31:23 EDT"
---

# Testing AskCruz information retrieval - Claude

## User (2026-10-13 09:31:23 EDT)

give me some ideas on which i can query claude about askcruz and perform some research to see whether its fetching information properly or not

## Claude (2026-10-13 09:31:23 EDT)

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

## User (2026-10-13 09:31:23 EDT)

give me more questions

## Claude (2026-10-13 09:31:23 EDT)

Here are more questions to try, grouped by what they test. Swap the bracketed parts for real clients, people, and dates.

Client and contact lookups

Who is the main contact at [client], and what’s their email?
Which clients use the same Odoo instance or share a domain?
Which clients have no contacts on file?
What’s the history with [client] from the first call to now?
Which clients haven’t had any call or email in the last 60 days?

Calls and transcripts

What action items came out of the most recent call with [client]?
Who spoke the most in [call]? Who joined late or left early?
Which calls mention [feature or module, e.g. inventory, manufacturing, toll processing]?
Summarize the three most recent Fathom calls.
What objections or concerns did [client] raise across all their calls?
Did anyone commit to a deadline on a call, and was it met according to later emails?

Emails and attachments

What was the last email thread with [client] about?
Find the email where [name] mentioned [topic], and show who replied.
What’s in the attachment on the [subject] email? Pull the key numbers.
Which email threads have attachments but no reply?
Find every email mentioning an invoice, quote, or contract.

Implementation tasks

What tasks are blocked right now, and who owns them?
Which tasks for [client] are high priority and still open?
What does the task chatter say about [problem]? Does it match what was said on calls?
Which tasks have no owner or no stage?

Wiki, assets, and SOPs

What does our SOP say about [process]? Quote the source document.
What’s in the company overview and ICP documents? Does the wiki summary match them?
Which wiki pages cover [client], and which sources back each claim?
What’s our position on [pricing, onboarding, or support policy]?

Trap questions (the right answer is “I don’t know”)

What did [real client] say about [topic never discussed]?
What’s the phone number for [real contact who has none on file]?
What happened on the [date with no calls]?
Compare [client A] and [fake client B].
What did [client] agree to on the call? Ask this about a call where nothing was agreed, to see whether it invents a commitment.

Reasoning across sources

Does what [client] said on a call match what they wrote afterward in email?
Build a timeline for [project] from calls, emails, and tasks. Are there gaps or contradictions?
What risks do you see for [client] based on everything on file? Cite the evidence for each.
What did we promise [client] that isn’t tracked as a task yet?

Reproducibility

Ask the same question twice, in different wording, and compare the answers.
Ask for the same list sorted two ways. Do the counts match?
Ask something, then ask “What sources did you use?” and check that each one exists and says what it claims.

I can run any of these live and show you what AskCruz returns next to the underlying source. The trap questions and the “promised but not tracked” question tend to expose problems fastest.
