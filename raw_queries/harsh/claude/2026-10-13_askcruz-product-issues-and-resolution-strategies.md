---
conversation_id: 6a35bf47-17a5-4e47-8078-3db438f2e085
platform: claude
username: "harsh"
title: "Askcruz product issues and resolution strategies"
created_at: "2026-10-13 09:08:18 EDT"
updated_at: "2026-10-13 09:37:34 EDT"
---

# Askcruz product issues and resolution strategies

## User (2026-10-13 09:08:18 EDT)

What are the current problems in the product of the Askcruz that are going on and what are the things that are being done to resolve them explain them in detail and tell me the some problems that are not discussed till now(note them too and explain them) and what can be done to resolve them

## Claude (2026-10-13 09:10:08 EDT)

I'll start by reading the two skill files, then look into the data.

> *Thinking:*
>

I'm going from the AskCruz wiki, the AskCruz asset docs and the implementation tasks visible on this connection. I could not query the full task boards, so this is a partial picture. Wiki pages are synthesized, and many flag their own claims as unverified; I note those below.

One more point: the conversation-archiving tool (`save_chat_transcript`) isn't connected in this session, so this chat was not saved to the archive.

## Part 1: Problems currently documented

**1. The "reasoning extraction" error (Claude Sonnet 5.5), the most urgent one**
- **What it is:** Users hit an error flag that blocked responses outright. A 62-minute internal meeting on Oct 10 diagnosed it as a known Sonnet 5.5 bug. It is triggered when a prompt asks the model to output its internal reasoning in a fixed format.
- **What's being done:**
  - Shubham confirmed the diagnosis through research.
  - Vaibhav found a working workaround: rewrite the prompt so it doesn't ask for the model's internal process.
  - The team tested GPT-4 as an alternative. It avoided the error but took over 14 minutes per complex response, so it was ruled out.
  - Ron is checking whether a low "rigor level" setting explains the slowness.
  - Shubham is sending an authentication/access-rights flow PDF, so the team can test whether user permissions play a role.
- **Still open:** Whether access rights contribute is only a hypothesis. It is also unknown whether client deployments (Sabre Alloys, Ohio Strip Steel) can hit the same bug.

**2. Contradictory product positioning**
- The product feature file calls AskCruz a steel-specific product. The product-market-fit guide says it is industry-agnostic and warns against single-vertical framing. The client-facing catalog is industry-neutral.
- The wiki flags that these can't all be canonical. No page records a decision on which one is, and the current marketing push into verticals such as car dealerships follows the agnostic line.

**3. Product-market fit is unproven**
- The guide's own conclusion is early signals but no proof of repeatable fit. 3GM Steel is the only confirmed customer, and its deal closed at a reduced 2-user scope. Retention, usage depth, ROI, sales-cycle length and customer acquisition cost are all listed as not yet established.
- **Being done:** The doc's stated loop is Refine → Deploy → Acquire → Measure → Learn.

**4. Sabre Alloys deal friction**
- The proposal drew data-privacy pushback. The services agreement went out via DocuSign to Michael and as a PDF to Tye Webb on Oct 12. There is no confirmation yet that it has been signed or reviewed.
- **Being done:** The contract includes an explicit clause that client data stays theirs and isn't used for training. Ron rephased the setup fee into 6 monthly installments.

**5. Search is keyword-only; vector search is roadmap**
- On Oct 2, Rajat described pgvector as an enhancement they *can* add alongside keyword search, not a shipped feature. Keyword search can miss the right thread entirely if it doesn't contain every query word.

**6. Internal task-board hygiene (Sept 5 snapshot, so possibly stale now)**
- No deadlines were set on any of Ron's 9 open tasks. Two follow-ups with Ayan Dutta were stalled for 10 days. The Access Rights task had no activity since Aug 26.
- The board has both a "Complete" and a "Completed" stage, so finished tasks keep reappearing in open-task reports.
- One task's note says "moving to complete" while its stage is still QA.
- **Suggested fix in the report:** Clean up the stage names or widen the exclusion filter.

**7. Freshness and coverage limits**
- Knowledge synthesis runs every 6 hours, so answers aren't real-time. The "94% data completeness" figure is a product-file metric, not a per-answer guarantee.
- Tickets and invoices were removed from the AskCruz tools on Aug 10 and live only in the separate EOXS Teams system. Brannon Steel and RW Conklin have no Odoo implementation instance, so they appear only through email and calls.

**8. Cost and governance**
- A page titled "AskCruz API Cost Pause — Team Moves to a Single Shared Claude Account (Aug 13)" exists, and so does a Git/personal-Gmail governance question. I could only see the titles on this connection, not the contents.

## Part 2: Problems I don't see discussed anywhere

These are my inferences from the documents above, not recorded findings.

1. **A single model dependency with no fallback.** Everything runs on Sonnet 5.5, and the only alternative tested was too slow. The next model bug will block the whole product again.
   - *Fix:* Define a fallback model and test it on your real prompts. Add a prompt linter that catches patterns known to trigger errors before they reach users.
2. **Shared accounts weaken access control.** The architecture says access depends on user identity, but the team moved to a single shared Claude account, and several people use the same login. Per-person permissions, audit trails and the access-rights investigation all get muddier.
   - *Fix:* Use per-user identities at least for any client-facing deployment. For internal use, log the actual person on every request.
3. **No visible accuracy measurement.** Nothing documents a test set or any tracking of wrong answers, citation misses or retrieval failures. Without that, "does it work?" rests on anecdotes, and it is also what the PMF guide says is missing.
   - *Fix:* Build a 50–100 question golden set from real client questions. Score it weekly and after every model or prompt change.
4. **Prompt-injection risk is a stated rule but not a documented test.** AskCruz ingests email and call transcripts, which are untrusted text, and the rule says to ignore embedded instructions. I found no record of anyone testing that.
   - *Fix:* Red-team it with planted instructions in emails and transcripts.
5. **Contradictions aren't resolved by any visible process.** The wiki generates flags for contradictions, but I found no workflow that closes them. Conflicting claims, such as the steel-vs-agnostic framing, persist and get cited.
   - *Fix:* Assign an owner and a weekly review of open flags.
6. **The human-approval step could be a bottleneck.** Pages are drafted every 6 hours but need human approval, and I couldn't confirm how big the unapproved backlog is on this connection.
   - *Fix:* Track the backlog and approval time as metrics, with an SLA.
7. **Key-person dependency.** Ron appears across client escalations, the board and sales, and the chat frontend is documented as owned by one person (an unverified, Aug 21 claim).
   - *Fix:* Add backup owners and documented runbooks for the frontend and pipelines.

## Where my answer is thin

- The reasoning-extraction page rests on a single meeting recap.
- Amounts are redacted on this connection, so pricing and cost problems are invisible to me.
- I did not review the full AskCruz task board or the support tickets.

I can look into any one of these further, for example the tasks and emails behind the Sabre data-privacy pushback.

**Sources:** wiki pages "Claude Sonnet 5.5 Reasoning Extraction Error" (id 2397), "AskCruz — Product Capabilities…" (1894), "…Market Positioning, ICP & PMF Status" (1895), "…System Architecture, Ingestion & Access Control" (1893), "Ron's AskCruz Daily Task Report, Sept 5" (2079), "AskCruz Proposal Resent to Sabre Alloys" (2053), and the "Michael Mercadante" page (586).

## User (2026-10-13 09:21:39 EDT)

-The product feature file calls AskCruz a steel-specific product. The product-market-fit guide says it is   industry-agnostic and warns against single-vertical framing. The client-facing catalog is industry-neutral.
Explain these points in detail and in simple words

## Claude (2026-10-13 09:21:58 EDT)

> *Thinking:*
>

I need to correct my earlier answer first. I went back to the original feature file this time, instead of the wiki summary of it, and the problem I described has mostly already been fixed.

## What I got wrong

I told you the feature file calls AskCruz steel-specific. That was true of an earlier version, and the wiki summary I relied on was written from it. The wiki page was created on Aug 25 at 15:48. The feature file was then updated about an hour later, at 16:58 the same day, to version 1.1.

The change log of version 1.1 says it corrected the industry scoping from steel-only to industry-agnostic, to align with the product-market-fit guide. So the contradiction is resolved in the source document. The wiki page's warning is out of date and should be refreshed.

## The three documents in simple words

Think of them as three descriptions of the same product, written by different people for different readers.

**1. The product feature file (an AI-readable product description)**
- It is written so that an AI can answer questions about AskCruz correctly.
- It describes four capabilities:
  - **Company Brain:** the company's shared knowledge.
  - **Company Hands:** helping do work, such as drafting quotes.
  - **Digital Workforce:** watching conditions over time.
  - **Company Personalization:** reflecting how one company actually works.
- The old version said AskCruz is "for steel businesses." The current version says it is not limited to any one industry. It explains that the internal pilot at EOXS and the first client, 3GM, happen to be steel businesses.
- It even includes a rule for the AI: don't describe AskCruz as limited to any single industry.

**2. The product-market-fit guide (who the product is for)**
- It says the target market is any industry where a business has scattered data that needs to be connected and searched from one place.
- It lists examples like healthcare, retail and logistics, but only as places the product could apply, not as existing customers.
- It warns against pitching AskCruz as a single-industry tool.

**3. The client-facing catalog (what to tell customers)**
- It is organized by type of information, such as email, calls, implementation data, employee info and internal documents.
- It avoids industry words entirely. I know this from the wiki summary, since I didn't re-read this document today.

## Why the confusion happened

The same product was being described two ways at the same time:
- **Early framing:** "a steel tool," because that's where it was built and first used.
- **Later framing:** "any industry," which is the growth plan.

For a few hours on Aug 25, the documents disagreed. The wiki, which is generated automatically, captured that moment and kept the warning after the source was fixed.

## What still matters

- **The wiki page is misleading.** Anyone reading it, or any AI that cites it, may think the confusion still exists. It should be regenerated or have its flag cleared.
- **Reality still leans steel.** Every customer and nearly every prospect so far is steel, and the proof of product-market fit is still thin. The documents now say "any industry," but the evidence doesn't show it yet. That is a business risk, not a document error.
- **I haven't checked other places** like sales decks, the website and outreach emails. They could still use the older steel-only wording.

I can check the other two documents and recent marketing emails to see whether any steel-only wording remains.

## User (2026-10-13 09:34:43 EDT)

Now tell me somethings that I can say to CEO or manager that these are the problems that we are having that we can fix in this amount of time and keep in mind they are people of non-tech background and has only vague understanding of the technical terms. So, explain them in simple words that can be understood by nayone

## Claude (2026-10-13 09:35:04 EDT)

> *Thinking:*
>

Here is a version you can use almost as written. The time estimates are my own rough guesses, not figures from company records, so check them with whoever would do the work before promising anything.

## A short opening to say out loud

"AskCruz is working and we have our first customer. We found several weak spots that could slow growth or embarrass us in front of customers. Most are small and fixable within weeks. I'd like to walk you through them."

## The problems, in plain words

**1. The AI sometimes refuses to answer**
- **What's happening:** Some questions trigger an error and the AI gives no answer. The team traced it to a known bug in the AI model we use, caused by the way certain prompts are worded.
- **Why it matters:** If a customer's employee hits this error, it looks like our product is broken.
- **Fix:** Reword the prompts that trigger it (a working fix already exists) and add a check that catches risky wording before customers see it. We also need to confirm whether customers can hit this problem.
- **Time:** About 1–2 weeks.

**2. We depend on a single AI provider with no backup**
- **What's happening:** We tested another AI as an alternative, but it took over 14 minutes per answer, which is too slow. So if our main AI has a problem, everything stops.
- **Why it matters:** One outside bug can freeze the whole product, and we can't control when the provider fixes things.
- **Fix:** Test one or two backup options on our real questions and keep the best one ready.
- **Time:** About 3–4 weeks.

**3. We can't yet prove how often it's right**
- **What's happening:** We don't have a regular test showing how many answers are correct. Today we mostly rely on stories and impressions.
- **Why it matters:** Customers will ask for proof, and we can't say "it's right 9 times out of 10" with evidence.
- **Fix:** Write 50–100 real questions with correct answers, run them every week, and report the score.
- **Time:** About 2–3 weeks to set up, then ongoing.

**4. Several people share one login**
- **What's happening:** The team moved to a shared account to control costs. We believe this makes it harder to see who asked what and to keep each person's access limited to what they should see.
- **Why it matters:** Customers will ask who can see their data. "Everyone shares a login" isn't a good answer.
- **Fix:** Give each person their own login, starting with anything customer-facing.
- **Time:** About 2–4 weeks. This depends on cost, so it may need your decision.

**5. Our task tracking is messy**
- **What's happening:** As of an early-September check, open tasks had no deadlines, some had been untouched for 10 days, and the board had two stage names ("Complete" and "Completed") that mean the same thing. That made finished tasks look unfinished.
- **Why it matters:** Work can quietly stall and reports can mislead.
- **Fix:** Merge the two stage names, add deadlines to important tasks, and hold a 15-minute weekly review. This snapshot is old, so we should recheck it first.
- **Time:** A day or two, then 15 minutes a week.

**4. Too much depends on a few people**
- **What's happening:** Ron appears in customer problems, task tracking and sales. One person is documented as the owner of the chat screen customers use. If either is unavailable, things slow down.
- **Fix:** Name a backup for each critical area and write short how-to guides.
- **Time:** About 4–6 weeks.

**6. Our own notes are slightly out of date**
- **What's happening:** One internal wiki page still says our product descriptions disagree on whether AskCruz is only for steel. That was fixed in August, but the page wasn't updated.
- **Why it matters:** Staff or the AI could repeat the old, confusing message to customers.
- **Fix:** Refresh the page and check sales materials and the website for steel-only wording.
- **Time:** A few days.

## Things to keep on your radar (longer-term, not quick fixes)

- **Smarter search:** Today the system finds things by exact words, so it can miss a good answer phrased differently. A smarter search was described to Sabre as a possible addition, but it isn't built yet. Realistically this is a one- to two-month project.
- **Proof the product works for customers:** So far 3GM is our only confirmed customer, and we don't yet have data on renewals, usage or savings. Collecting these should start now.
- **Sabre Alloys deal:** The contract was sent on Oct 12. As far as I can see, it hasn't been signed yet, and they raised data-privacy concerns. Our contract already says their data stays theirs and isn't used to train AI. A follow-up call this week would help.

## A simple closing line

"Nothing here is a crisis. Most items can be handled within a month, and a few need a decision from you, mainly on separate logins and the backup AI. I'd suggest we fix the quick ones first and report back in two weeks."

I can turn this into a one-page email or a short slide for the meeting. Tell me which format you'd prefer.
