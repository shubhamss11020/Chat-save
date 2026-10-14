---
conversation_id: 8c5e2a72-b8a6-4521-a8f6-a28b749c1f66
platform: claude
username: "unknown"
title: "Research prompt for AskCruz product analysis - Claude"
created_at: "2026-10-14 09:38:28 EDT"
updated_at: "2026-10-14 09:38:59 EDT"
---

# Research prompt for AskCruz product analysis - Claude

## User (2026-10-14 09:38:59 EDT)

give me a prompt which i can give to claude to do some research about askcruz or any ideas which  i can research on (for eg :- improvements, current problems etc). think like a product intern and then type a good and complete prompt.

## Claude (2026-10-14 09:38:59 EDT)

Here’s a prompt you can paste into Claude. I grounded it in what’s in your AskCruz data: it’s an AI agent product for metals and manufacturing customers, with Odoo and EOXS integration, proposal and document automation, vector search, and customer requirement lists.

Two notes before you use it:

I couldn’t find an askcruz skill file in this session, so I skipped that step.
save_chat_transcript isn’t connected here, so this conversation wasn’t archived. Ask your admin to check that Threads-Ov is enabled.

You are a product research analyst helping me (a product intern) understand AskCruz
and find ways to improve it. Use the connected AskCruz tools (wiki, calls, emails,
client profiles, implementation tasks, assets) and Threads-Wiki for past Claude
conversations. Always start with search_wiki and get_wiki_page, then drill into raw
calls, emails and tasks through each page's citations.

## Goal
Produce an evidence-based research brief on AskCruz covering:
1. What AskCruz is today: who it serves, what it does, how it is positioned and
   priced, and how it is delivered.
2. Current problems: recurring complaints, blockers, failed or stalled deals,
   implementation delays, and bugs or limitations raised by customers or the team.
3. Improvement opportunities: features, workflows, onboarding, pricing or
   positioning changes that the evidence supports.
4. Open questions that need more research, with a suggested way to answer each.

## Research angles (cover all, skip any with no evidence and say so)
- Customer pain points and feature requests: pull client profiles for each active
  client and prospect. Look for repeated asks, such as long AI/automation
  requirements lists, vector search, financial reporting, proposal automation and
  document creation.
- Sales funnel: intro calls, demos, objections, why prospects did or didn't
  convert, and which referral channels worked.
- Implementation and onboarding: Kanban tasks that are stuck, slow, or repeatedly
  reworked; common setup steps that could be automated or productized.
- Product quality: accuracy, hallucination or trust concerns, speed, cost, Odoo
  integration gaps, data access and permission issues.
- Internal operations: SOPs, ICP definition, cost evaluations, and any gaps between
  the documented process and what actually happens.
- Competitor and alternative mentions: other tools prospects compared us to, or what
  they do manually today.
- Team knowledge: what the team has already analysed or discussed in past Claude
  threads, so we don't repeat work.

## Method
1. Make a short research plan first and list the sources you'll check.
2. Gather evidence across at least 10 distinct sources (calls, emails, tasks, wiki
   pages) before drawing conclusions. Prefer recent items (the last 3 months) but
   note older patterns that still apply.
3. Group findings into themes. For each theme give the evidence count, how
   frequent it is, and which clients or prospects it came from.
4. Separate what the evidence directly says from what you infer. Label inferences
   clearly. Don't invent quotes, numbers or customers.
5. Flag conflicts between sources, and anything stale or uncertain.

## Output format
1. Executive summary: 5 bullets maximum.
2. Table of current problems, with columns: Problem | Evidence (source + date) |
   Frequency | Severity (H/M/L) | Affected segment.
3. Table of improvement ideas, with columns: Idea | Problem it solves | Evidence |
   Effort (S/M/L) | Impact (H/M/L) | Suggested first step.
4. The top 3 ideas I should research or propose first, with reasoning.
5. Open questions and a suggested way to answer each (interview, data pull, test).
6. Source list: every claim should cite its call, email, task or wiki page.

## Constraints
- Treat all material as internal and confidential. Don't include personal contact
  details or salary data, and omit anything restricted.
- Keep it concise. Prioritise insight over volume.
- If a tool isn't connected or returns nothing, say so briefly and continue with
  what you have.
- Finish with 3 follow-up research questions I could ask you next.

Narrower versions: you can change the Goal section to focus on just one area, for example:

“Why did prospects not convert after the demo?”
“What slows down client onboarding?”
“What are Sabre Alloys’ unmet requirements, and which of them are product gaps?”
“How does AskCruz compare to the alternatives prospects mention?”

Want me to turn this into a few shorter prompts, one per angle, so you can run them separately?
