---
conversation_id: 1db3c22e-3d57-4c35-a3aa-c09f7f60aca8
platform: claude
username: "shubham"
title: "Jaskeerat's work logs"
created_at: "2026-10-08T16:54:05.711991Z"
updated_at: "2026-10-12 12:34:13 EDT"
---

# Jaskeerat's work logs

## User (2026-10-12 12:34:13 EDT)

can u tell me last week log note what jaskeerat put in the board

## Claude (2026-10-12 12:34:13 EDT)

```

```

**Routing:** Work-log question → system of record is task-board chatter (log notes in `mail_message`). Checking teams-askcruz and eoxs-teams, last week = Mon 28 Sep – Sun 4 Oct 2026 (IST).
```

```

```

```

Jaskeerat posted **6 log notes last week (28 Sep – 4 Oct)**, all on the **Brannon Support Desk** board, covering 3 tasks about impact-testing logic on MTRs.

**1. #8057: Impact threshold logic wrongly marking MTRs as passing** (notes on 28 Sep, plus 3 on 1 Oct)
- **Cause:** On 23 Jul, "does heat X meet spec Y" questions stopped going through the deterministic spec checker. The AI answered them itself and compared temperatures the wrong way. Heat 3777T6 only looked right because −50 °F really is colder.
- **Fix:** Those questions now go back to the deterministic checker. It picks the plate or tubing branch from the heat and returns "no matched inventory" when nothing is found. The AI also got an explicit temperature-direction rule as a backup.
- **Verified:**
  - Heats 1377T6-02 and 2645T6-04 (both −20 °F) now fail LW0940.
  - 3777T6 still passes.
  - Edge cases behave correctly: −22 passes, −21.9 fails.

**2. #8072: Wrong impact temperature read from spec LW5725** (1 Oct)
- **Cause:** This was a data error, not the AI. The PDF import read "0 °F" as 0 °C and stored 32 °F. As a result, MTRs tested between 0 and 32 °F were wrongly accepted.
- **Fix:** Migration 13.0.2.1.12 corrects the four LW5725 rows to 0 °F. The import now warns when an impact temperature comes out above 0 °F.
- He checked the other 21 specs against their PDFs, and only LW5725 was affected.

**3. #8073: Impact orientation read from the wrong MTR field** (2 notes, 1 Oct)
- The false orientation warning is removed. The field the chatbot was reading is actually the tensile test direction.
- Real orientation checking is pending the client's decision. It can't be applied to MTRs already processed, because impact direction was never stored.
- He verified the change on 12 phrasings with verdicts unchanged.
- **Deploy step he left:** merge `fix/impact-orientation-rule`, restart Odoo (no upgrade needed), and re-run the client's heats.

**Things to check:**
- #8072 was a silent false-accept that sat in production. Ask whether Brannon has been told which MTRs may have been wrongly passed under LW5725.
- #8057 is the same kind of exposure: the regression ran from 23 Jul until the fix.
- Find out whether the #8073 merge and restart actually happened. His note gives the steps but doesn't say they were done.

**Coverage:** I checked only the EOXS Teams board. The askcruz board connector isn't available in this session, so any notes he posted there are not included.

Sources: eoxs-teams (live Odoo), `mail_message` log notes on tasks 8057, 8072, 8073.

## User (2026-10-12 12:34:13 EDT)

can u tell me what jaskeerat work in september month

## Claude (2026-10-12 12:34:13 EDT)

**Routing:** Contribution question → task boards. Only eoxs-teams is reachable this session (askcruz connector not loaded), so I'm checking his assigned tasks there plus his September log notes.
```

```

In September, Jaskeerat worked only on **Brannon** work: **9 tasks** on the EOXS Teams board. **7 are completed and 2 are in QA.**

**Brannon Support Desk (8 tasks)**

| Created | Task | Stage | Notes |
|---|---|---|---|
| 5 Sep | MTRs with matched status not displayed | Completed | 1 |
| 5 Sep | Stop-generation button + scroll during response | Completed | 1 |
| 5 Sep | Chatbot failing to return matched heat | Completed | 1 |
| 10 Sep | New MTRs stuck in Pending | Completed | 2 |
| 15 Sep | AI spec reading for conditional requirements | Completed | 3 |
| 28 Sep | Impact threshold wrongly passing MTRs | Completed | 1 |
| 29 Sep | Wrong impact temp from spec LW5725 | QA | 0 |
| 29 Sep | Impact orientation read from wrong field | QA | 0 |

**EOXS project (1 task)**

| Created | Task | Stage | Notes |
|---|---|---|---|
| 15 Sep | Temporary MTR upload & spec validation for Brannon | Completed | 3 |

The Notes column counts the log notes he posted in September.

**Takeaways:**
- He is effectively the dedicated engineer for Brannon's MTR/spec-validation chatbot. All of his September output went to that one client.
- Most of the work was fixing bugs Brannon reported, not building new features. The only enhancements were spec reading for conditional requirements and the stop-generation button.
- Several of the bugs were silent correctness failures, where the system gave wrong pass verdicts. That points to a missing regression test suite for spec-checking logic, which is worth asking about.

**Caveats:**
- `date_end` is empty on every task, so I can't tell exactly when each one was closed. "Completed" is the current stage, not proof it was finished in September.
- I checked only the EOXS Teams board. The askcruz board connector isn't loaded in this session.

I can pull the full note text for any task if you want the details.

Sources: eoxs-teams (live Odoo): `project_task` assignments and `mail_message` log notes, 1–30 Sep 2026 IST.

## User (2026-10-12 12:34:13 EDT)

can u tell me about leave policy of askcruz

## Claude (2026-10-12 12:34:13 EDT)

**Routing:** This is a reference-document question, so the source is the eoxs-db assets (SOPs/policies). Checking whether that connector is available.
```

```

I can't answer this from this session. The leave policy would be stored as a reference document in eoxs-db assets, and the eoxs-db connector isn't loaded here. The askcruz board connector isn't loaded either.

The only EOXS source I can reach in this chat is the EOXS Teams Odoo database. That holds leave types and allocations for the EOXS team, not a written askcruz policy, so it isn't the source for this.

There are two ways to get the answer:
1. **Enable eoxs-db for this chat** in the connector settings and ask again. I'll then fetch the leave policy document with its exact wording.
2. **Check the EOXS Teams Odoo leave setup** (leave types and allocations) as a stand-in, labelled as EOXS-side configuration rather than the askcruz policy.

Which do you want?
