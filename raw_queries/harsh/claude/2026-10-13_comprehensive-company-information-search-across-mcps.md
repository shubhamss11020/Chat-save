---
conversation_id: 0c67f02a-b82e-428b-9cb8-fc16124c8831
platform: claude
username: "harsh"
title: "Comprehensive company information search across MCPs"
created_at: "2026-10-13 09:32:22 EDT"
updated_at: "2026-10-13 09:32:31 EDT"
---

# Comprehensive company information search across MCPs

## User (2026-10-13 09:32:22 EDT)

Perform a comprehensive search across the company information available through the connected MCPs and their associated skills.
Start by identifying the relevant data sources and tools available to the current user. Then retrieve and cross-reference information from the following categories wherever supported:

* Employees and organizational structure.
* Projects and project ownership.
* Tasks, deadlines, and task statuses.
* Customers and business relationships.
* Sales activities and opportunities.
* Meetings, transcripts, and documented decisions.
* Invoices and other financial records, if authorized.
* Internal documentation and company knowledge.

For each category, retrieve actual records and identify relationships with records from other categories.
For example, connect employees to projects, projects to tasks, meetings to documented commitments, and customers to their associated projects and account activities.
Use the relevant skills to organize the retrieved data and validate the relationships. Where possible, include record identifiers, source names, timestamps, and other available references.
Do not assume that every MCP contains the same information. Report which sources were successfully queried, which returned no matching records, and which were inaccessible.
Respect all tier-based permissions. Do not attempt to bypass access restrictions, and do not expose restricted information in the final report.
Return a structured report of the accessible company information, with evidence supporting each major finding. Do not make any changes to the database.
