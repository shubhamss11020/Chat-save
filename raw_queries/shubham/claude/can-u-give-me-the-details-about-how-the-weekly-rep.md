---
conversation_id: 69fd346f-5fb2-40b9-9bff-b42bbfe77c82
platform: claude
username: "shubham"
title: "Weekly employee report in Askcruz"
created_at: "2026-10-12 08:39:18 EDT"
updated_at: "2026-10-12 16:20:12 EDT"
---

# Weekly employee report in Askcruz

## User (2026-10-12 16:20:12 EDT)

can u give me the details about how the weekly report of employeee  generated in askcruz

## Claude (2026-10-12 16:20:12 EDT)

Claude responded: The weekly report is a self-addressed scrum report that Rajat's automation generates from the AskCruz project board in the teams-askcruz Odoo instance.
Using Askcruz: Search emails
Using Askcruz: Search emails
Used Askcruz

Used Askcruz
Figuring out how weekly report generation works for askcruz.
Loaded
Askcruz
Searched Askcruz wiki
weekly report generation askcruz

Searched Askcruz repo docs
weekly report

Fetched Askcruz wiki page
AskCruz Board Scrum Reporting (Daily/Weekly Team Engagement Reports)

Fetched Askcruz wiki page
AskCruz Board Scrum Reporting (Daily/Weekly Team Engagement Reports)

Figuring out how the generated page comes together.
Searched Askcruz emails
Weekly AskCruz Board Scrum Report

The weekly report is a self-addressed scrum report that Rajat’s automation generates from the AskCruz project board in the teams-askcruz Odoo instance. It’s one of two recurring reports (the other is daily). Its last run in the record I can see is August 18, 2026, so I can’t tell from here whether it still runs as of today, October 12.

How it works

Data source: Live Odoo data from the board (project_id=6, 39 active tasks as of Aug 17): task records, stage changes, and chatter (log notes). The report describes itself as pulled from live data, not compiled by hand.
Window: The weekly report covers the previous 7 days. The Aug 18 run covered Aug 11 19:22 to Aug 18 19:22.
Scoring: Each assignee gets a score out of 10. The Aug 17 version used five sub-metrics:
Ack: share of open tasks the assignee personally acknowledged with a note
Movement: weighted stage advances
Completions
Depth: note specificity. The report itself calls this a low-confidence text proxy.
Scope: whether a high-priority task was touched
Delivery: It is sent by email to Rajat’s own address (raj_gmail), so it appears in the mailbox.

Known problems

Two conflicting reports for the same window. On Aug 17 two weekly reports covering Aug 11–17 disagree. One says 6 tasks were completed and the other says 3. Per-person scores also differ, e.g. Ron is 6.4/10 in one and 3/10 in the other. Neither report explains the gap.
Shutdown order not carried out. At 15:17 UTC on Aug 17, Rajat wrote “Shut this automation down, please.” The next day a new weekly report ran with a larger scope: 6 boards and 128 tasks instead of one board. The record has no explanation for this.
Ack metric ignores authorship. Ron scored 100% on Ack even though every note on his tasks was written by others. The metric doesn’t check who wrote the note.
Scores mostly track chasing. Most of the logged activity is Rajat chasing assignees rather than assignees updating their own tasks. The reports say so themselves.

What I couldn’t confirm: the vault has no weekly report after August 18. If it still runs, the September and October reports aren’t in this record. Whether the shutdown order was ever applied is also unresolved.

Sources: wiki page “AskCruz Board Scrum Reporting (Daily/Weekly Team Engagement Reports)” (id 1779). Underlying emails: 66381 (Aug 17 report), 66431 (Aug 17 second report), 66615 (Aug 18 report).
