---
conversation_id: bc548d03-47b1-4a67-a777-c60de58c68a2
platform: claude
username: "shubham"
title: "Last week log notes"
created_at: "2026-10-08T16:54:05.711991Z"
updated_at: "2026-10-12 12:34:16 EDT"
---

# Last week log notes

## User (2026-10-12 12:34:16 EDT)

can u tell me last week log note what jaskeerat put in the board

## Claude (2026-10-12 12:34:16 EDT)

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

## User (2026-10-12 12:34:16 EDT)

can u tell me last week log note what jaskeerat put in the board

## Claude (2026-10-12 12:34:16 EDT)

**Routing:** Same as before, log notes live on the board chatter. The askcruz board connector (Read-only SQL) has disconnected since the last query, so I can only check **eoxs-teams** right now.
```

```

On EOXS Teams, Jaskeerat posted **6 log notes across 3 tasks last week, all on 28 Sep and 1 Oct**. This is incomplete: the askcruz board couldn't be checked because that connector disconnected. Ayan tagged him on four askcruz tasks on 5 Oct (DO servers, System Visibility, OAuth, ChatGPT MCP), so any replies would be there.

**Task 8057, "heat X meets spec Y" check (28 Sep, re-posted in full 1 Oct)**
- **Cause:** On 23 Jul the route to the deterministic spec checker was removed. Since then the AI answered these questions itself and compared temperatures the wrong way round. Heat 3777T6 only looked right because −50 °F really is colder.
- **Fix:** These questions go back to the deterministic checker, which decides pass or fail in code. The AI also has an explicit temperature-direction rule as a backup.
- **Verified:** Heats 1377T6-02 and 2645T6-04 (−20 °F) now fail LW0940, and 3777T6 still passes. The boundary is correct: −22 passes, −21.9 fails.

**Task 8072, LW5725 wrong spec limit (1 Oct)**
- **Cause:** The data was wrong, not the AI. On PDF import, "0 °F" was read as 0 °C and stored as 32 °F, so MTRs tested between 0 and 32 °F were wrongly accepted.
- **Fix:** A migration (v13.0.2.1.12) corrects the 4 impact rows to 0 °F. The importer now warns when an impact temperature comes out above 0 °F.
- **Checked:** He compared the other 21 specs against their PDFs; only LW5725 was affected.

**Task 8073, impact orientation (1 Oct)**
- **Fix:** The false orientation warning is removed. The stored direction is actually the tensile test direction, not impact.
- **Pending:** Real orientation checking needs the client's decision, and can't apply to MTRs already processed.
- **Verified:** Tested on 12 phrasings with no change in verdicts. His next step: merge `fix/impact-orientation-rule`, restart Odoo, and re-run the client's heats.

**What stands out**
- **The work quality is strong.** Each note gives root cause, fix and boundary tests.
- **The LW5725 bug is a real compliance exposure.** MTRs between 0 and 32 °F were accepted when they should have failed. It's worth confirming whether past MTRs or shipments certified against LW5725 were re-checked; the note doesn't say.
- **Nothing on EOXS Teams after 1 Oct.** Combined with Ayan's 5 Oct chasers, his askcruz notes are the open question.

Sources: eoxs-teams (`mail_message` comment notes, 28 Sep–8 Oct). teams-askcruz was not queried because the connector was disconnected. Reconnect it and I'll pull his askcruz notes.

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
