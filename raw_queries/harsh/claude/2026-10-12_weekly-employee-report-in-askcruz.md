---
conversation_id: 69fd346f-5fb2-40b9-9bff-b42bbfe77c82
platform: claude
username: "harsh"
title: "Weekly employee report in Askcruz"
created_at: "2026-10-12 08:48:42 EDT"
updated_at: "2026-10-13 11:17:05 EDT"
---

# Weekly employee report in Askcruz

## User (2026-10-12 08:48:05 EDT)

can u give me the details about how the weekly report of employeee  generated in askcruz

## Claude (2026-10-12 08:48:42 EDT)

> *Thinking:*
>

The weekly report is an automated HR email built on top of Cattr, the time-tracking tool EOXS uses. Kriti Jain built the automation. The wiki doesn't include the exact technical setup (schedule, code, or data fields), so this comes from the email-based summaries.

**How it works, as far as the records show:**
- **Data source:** Cattr logs each employee's tracked time and activity. The automation compares that against each person's expected weekly hours.
- **Output:** A "Weekly Team Report" table with worked vs. expected hours for each employee, plus individual "Work Hours Reminder" and flagged-performance emails to the employees concerned.
- **Recipients:** HR (Isha Bisht) and leadership (Rajat Jain) receive the report.
- **Hand-off:** On 1 Sept 2026, Kriti delivered a "Final Employee Report Card" and said a "Cowork automation" would email it to Rajat every Monday. The same day, an automated "EOXS HR Automation" sent a Monthly Performance Summary for August covering 49 employees. The wiki flags as unverified whether these are one pipeline or two.

**Known problems in the record:**
- The reminder emails count only Monday to Saturday, so Sunday work is invisible unless the employee reports it.
- The same notices were sent 3–4 times within a second or two.
- The personal reminder and the master report have shown different hour totals for the same person and week.
- Cattr has intermittently lost or hidden tracked time for several employees.

**Current status:** Kriti is offboarding (7–8 Oct 2026). She handed over an SOP for setting up Cattr automation again and a zip of rule sheets and supporting files for the report card automation. HR has asked for full video knowledge-transfer sessions on the LinkedIn process and the report card automation before her exit formalities proceed. The wiki doesn't show whether she has provided them.

Sources: wiki pages 1241 (Attendance Tracking: Cattr Automation & Weekly Team Reports, Aug 2026), 2000 (Employee Report Card handoff, Sep 2026), 2365 (Kriti Jain offboarding, Oct 2026), 50 (Cattr Automation); emails 62187, 66070, 67562, 68052, 70514.
