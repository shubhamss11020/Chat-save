---
conversation_id: 08827e0c-a543-46bb-81bd-2689828f2ea5
platform: claude
username: "shubham"
title: "Shubham Srivastava information"
created_at: "2026-10-08T13:29:27.848809Z"
updated_at: "2026-10-12 12:34:42 EDT"
---

# Shubham Srivastava information

## User (2026-10-12 12:34:42 EDT)

can u tell me who is shubham srivastava

## Claude (2026-10-12 12:34:42 EDT)

```

```

Here's what I have on a Shubham, though the surname "Srivastava" isn't confirmed anywhere in my notes.

- He's listed as QA Lead on the intern team, alongside Yash (QA Engineer) and Stefan (Test Validator).
- That team has been running the MCP testing rounds, including the Travis and Stefan Round 3 projects.

I don't have his role at EOXS beyond that, his contact details, or confirmation that this is the same Shubham Srivastava you mean. I can check the EOXS task boards and contacts for his full name, current assignments and output if you'd like.

## User (2026-10-12 12:34:42 EDT)

try to fetch from the askcruz project board

## Claude (2026-10-12 12:34:42 EDT)

Checking the Askcruz task boards for Shubham Srivastava now.
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

I couldn't pull Shubham Srivastava from the project board, because the teams-askcruz and eoxs-teams SQL connectors aren't available in this session. Those two are where per-person task data lives, and nothing in this chat can load them. I can't tell you whether he has tasks or contributions on those boards.

The only Askcruz hit for "Shubham" is a 2022 Library task for the 3GM Steel client, owned by Rajat Jain. It mentions a "Shubham" in a note about a Customer Claims item. That's a name in a note rather than an assignment, and it doesn't identify which Shubham or tie it to Srivastava, so I'd treat it as unrelated until confirmed.

Askcruz also has no employee directory, so his role or department isn't retrievable from here either.

To get a real answer, either:
1. Enable the teams-askcruz and eoxs-teams connectors in this chat, and I'll run the per-person task query.
2. Tell me which project or board he's on, and I'll search the Askcruz implementation tasks for it.

Sources: Askcruz `search_implementation_tasks` (task 30663).

## User (2026-10-12 12:34:42 EDT)

try again

## Claude (2026-10-12 12:34:42 EDT)

```

```

This is the askcruz Odoo DB, so I'll run the per-person task query from the skill.
```

```

```

```

Shubham Srivastava is on the Askcruz board, in the **Ai Interns** stage of the **Daily Snippets** project. That matches your notes placing him on the intern team.

- **Board record:** one task, titled with his own name and created 2026-08-25, with no end date or deadline. It looks like a placeholder card for tracking him, not a work item, though that's my reading.
- **What the board can't tell me:** his role, department, or any delivered work. Askcruz has no employee directory, so "QA Lead" comes from your notes, not the board.
- **Possible mix-up:** the search also returned a **Shubham Sharma**, who has one task in "GTM - LinkedIn Outreach" (created 2026-08-17). That's a different person, so make sure it's not the one you meant.

I only checked the teams-askcruz board. I haven't looked at eoxs-teams, which holds the Teams tickets and CRM work, so I can't say whether he has activity there.

Sources: askcruz Odoo DB (`project_task`, `project_project`, `project_task_type`), read-only connector; live as of this query.

## User (2026-10-12 12:34:42 EDT)

can u tell me about harsh yadav

## Claude (2026-10-12 12:34:42 EDT)

```

```

```

```

Harsh Yadav is an EOXS team member who takes part in the team's Claude/MCP rollout and "Study Time" sessions. I couldn't find his role, title or department. I also couldn't check his tasks on the project board, because the board connector wasn't available this turn.

- **Aug 27 Study Time (connector setup and practice):** he was present and helped coordinate the attendance and skill-file logistics.
- **Sep 3 Study Time:** he said he still didn't fully understand how to implement one particular concept, and the question was deferred.
- **Session reports (Aug 28 to Sep 5):** his name is on the distribution list of the hourly session productivity reports, alongside Kriti Jain and several others. Any activity or performance detail in those reports is restricted on this connection, so I haven't read them.

Askcruz has no employee directory, and no wiki page exists for him, so there is no profile to draw on beyond those mentions.

Retry and I'll run the per-person task query on the askcruz board, as I did for Shubham. If you tell me which project he's on, I can also search the implementation tasks for it.

Sources: Askcruz wiki pages 1814, 1965 and 2059 (calls 2416 and 2429, Aug 27 and Sep 3, plus the Sep 5 report emails); the board query failed to run.
