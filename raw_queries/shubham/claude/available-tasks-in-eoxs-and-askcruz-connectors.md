---
conversation_id: 771b4a49-1522-49d8-a56b-9893b79bc57e
platform: claude
username: "shubham"
title: "Available tasks in EOXS and AskCruz connectors"
created_at: "2026-10-06T16:37:07.924342Z"
updated_at: "2026-10-12 12:38:04 EDT"
---

# Available tasks in EOXS and AskCruz connectors

## User (2026-10-12 12:38:04 EDT)

list me all the tasks available currently use the eoxs or askcruz connectors

## Claude (2026-10-12 12:38:04 EDT)

I need to read the required skill files first before querying data. Let me pull those in.
```

```

```

```

Before I query for tasks, I need clarity on what you want:

1. **Scope** — All implementation tasks across all clients, or just specific ones (e.g., askcruz, EOXS clients)?

2. **Stage filter** — All statuses, or just open/active tasks?

3. **Output** — Simple list (name, owner, stage) or detailed (including description, dates, priority)?

With current access, I can pull `list_implementation_tasks` from Interns-mcp (covers onboarding/implementation work across clients). For full askcruz project tasks + stages via SQL, that requires teams-askcruz SQL access, which isn't available yet.

What's the intent here — checking overall project load, finding who's working on what, or something else?

## User (2026-10-12 12:38:04 EDT)

ok

## Claude (2026-10-12 12:38:04 EDT)

Pulling all tasks now.
```

```

```

```

Active tasks: 120 total across 2 EOXS clients.

**Discount-Pipe-Steel** (105 tasks)
- Majority in Requirement stage (45) — backlog of feature requests and spec questions
- Active development: Code QA (5), Functional QA (5), In Developer Review (3)
- Blocked/waiting: DPS Sandbox Review (3), DPS Decision (5), Need Discussion (2)
- High priority: 8 tasks (mostly blocking fixes)
- Completed: 1 task
- One stalled task (Tabled): Filter Delivery Address Dropdown

**Eastern-States-Steel** (13 tasks)
- Mostly Intake (3) and newly assigned stages
- Code QA (2) active work
- Phase 1 implementation focus
- Mostly Normal priority; one On Live

**By Stage (Active vs. Stalled)**
- Requirement: 52 (spec/backlog)
- Intake: 6 (early intake phase)
- Code QA: 7 (development testing)
- Functional QA: 4 (user testing)
- In Developer Review: 4 (code review phase)
- DPS Sandbox Review: 4 (sandbox testing)
- DPS Decision: 5 (awaiting client decision)
- Assigned: 7 (assigned but not started)
- Completed: 2
- Other states (Communicated, Can be moved to live, Need Discussion, On Live, Tabled): 18

**Ownership spread:** Distributed across team — Hashir Saleem (12 tasks), Amy Rayzor (50), Tina Valdez (25), Nijamuddin (5), Dhrup (5), others lighter.

**Quick read:** Discount-Pipe-Steel has significant feature backlog in Requirement (45 tasks). Bottleneck is in DPS decision/sandbox stages — 9 tasks waiting for client sign-off or sandbox approval. Eastern-States is early in intake.

What's the priority — volume reduction, workflow unblocking, or something specific?
