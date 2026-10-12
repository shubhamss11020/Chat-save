---
conversation_id: 1db82ad9-9af6-4360-9d39-309701c280f8
platform: claude
username: "shubham"
title: "Urgent important tasks from Odoo"
created_at: "2026-10-08T13:47:34.471089Z"
updated_at: "2026-10-12 10:41:51 EDT"
---

# Urgent important tasks from Odoo

## User (2026-10-12 10:41:51 EDT)

give me pending task that are urgent and important also from odoo board and how did you concluded how improtant and urgent they are,

## Claude (2026-10-12 10:41:51 EDT)

I'll pull the pending tasks from the Odoo board, then rank them by urgency and importance.
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



Ten tasks are both urgent and important right now. Eight are on the teams-askcruz board and two are on eoxs-teams. This is a ranking across everything open on both boards, not filtered to one person, at "10ft" rigor: I checked the board fields but did not read task descriptions or comments.

## Do first (urgent and important)

| # | Task (board) | Owner | Why |
|---|---|---|---|
| 1 | **#162 EOXS spam emails filter** (askcruz) | Kriti Jain | 37 days past its 1 Sep deadline. It is the longest-overdue open item on the board. |
| 2 | **#208 Onboarding Structure & Process** (askcruz) | Ron | P1, 6 days past its 2 Oct deadline, still in dev. |
| 3 | **#753 Audit Employee Access Rights** (askcruz) | Ron | Due tomorrow (9 Oct) and still in Intake, so not started. |
| 4 | **#733 Teams.EOXS MCP: Remove Employee access** (askcruz) | Ron | Open since 30 Sep. Offboarding tasks #760 and #761 were created on 7 Oct. |
| 5 | **#654 Disable website visitor tracking** (askcruz) | Ron | P1, in dev for 12 days. |
| 6 | **#526 Data Access & Privacy Policy** (askcruz) | Ayan Dutta | P1 and starred, but no deadline. |
| 7 | **#386 AskCruz Security & Compliance** (askcruz) | Ron | P1, already in QA, so it only needs closing out. |
| 8 | **#8078 "AI Mass Spamming has begun"** (eoxs-teams) | Aryan Bakshi | Created 29 Sep and still just "Assigned". It may be linked to #162, but that is my guess. |
| 9 | **#7598 CRA email Raj received** (eoxs-teams) | Ron | Open since 10 Aug and never moved. No deadline is recorded, but government notices usually carry a response date, so check the email. |
| 10 | **#8051, #8031, #7848, #8079 "Need Developer" tickets** (eoxs-teams) | Dev Team and others | Live client tickets waiting for a developer. #7848 has waited since 28 Aug. |

## Important but not urgent (schedule these)

- **Sabre Alloys intake:** about 36 tasks have sat untouched since 28 Sep, most assigned to Ayan Dutta. #671 (staging server) and the unassigned #711 (platform review) block the rest. This looks like a bottleneck on one person.
- **Billing:** #7688 Brannon Monthly Invoicing has been open since 21 Aug, and #7916 Sabre Claude-usage invoice since 7 Sep.
- **Brannon support desk:** #8072 and #8073 have been in QA since 1 Oct.

## How I decided

**Urgency** came from whether a deadline had passed or was within 48 hours, a star priority, a blocked state, and time since the last stage move.

**Importance** came from the P1/P2 level, whether the task touches security, access or compliance, and whether it affects a client or revenue.

Tasks needed a strong signal on both to make the top list. Beyond that, these are my own judgments:

- **#4 (access removal):** the signal is that offboarding tasks were created on 7 Oct. Whether that links to #733 is my inference, not something the board states.
- **#1:** Kriti Jain's offboarding task (#761) means #162, #651 and #650 may need a new owner. This is also inference.
- **#8078:** I ranked it on its title and age, since the task has no priority or deadline.

## Data caveats

- **Sparse fields:** almost every task is priority "0" with no deadline. Only a handful have a P-level, and only about five open tasks on the askcruz board carry a deadline. The ranking leans on judgment more than on hard dates.
- **Stale "overdue" tasks:** Build Team shows about 20 tasks in "Can be released" with deadlines from 2025 to Jan 2026, and EOXS Support has 5 "Ready for Live" tasks due 8 Apr. These are built and waiting for release, so I excluded them from the top list. The CalPal AI agent task is 370 days overdue and blocked, which looks abandoned. Releasing or closing this backlog is a separate cleanup.

I can narrow this to one person's tasks (Ron's and Ayan's are the heaviest) or draft a handoff list for Kriti's open tasks.

Sources: teams-askcruz (askcruz Odoo, `project_task`) and eoxs-teams (EOXS Team Live Odoo, `project_task`), queried live on 8 Oct 2026.
