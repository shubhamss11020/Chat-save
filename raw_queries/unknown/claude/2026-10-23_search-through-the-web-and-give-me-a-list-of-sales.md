---
conversation_id: eb3fda21-6cf6-4a24-8617-a398554dabda
platform: claude
username: "unknown"
title: "Sales skill files for research - Claude"
created_at: "2026-10-23 10:58:49 EDT"
updated_at: "2026-10-23 11:34:48 EDT"
---

# Sales skill files for research - Claude

## User (2026-10-23 11:34:48 EDT)

search through the web and give me a list of sales skill files which can be helpful for a client to extract sales strategies, or any sales related questions. make a list of it and provide me the best skill files which can be helpful for a company to research about anything and everything related to sales.

## Claude (2026-10-23 11:34:48 EDT)

Section 2: Outbound and prospecting skill packs
Pack	What’s in it	Fit for outbound
ColdIQ GTM Skills (sachacoldiq / cold-iq)	7 master skills (Clay, Cold Email, LinkedIn Ads, LinkedIn Content, List Building, n8n, Signal Sourcer) that route to 52 sub-skills, plus 33 standalone skills. The standalone skills cover cold call scripts, buying signals, email templates and SDR playbooks.	Highest. Deepest outbound library found.
marketingskills (coreyhaines31)	A prospecting skill that finds, qualifies and scores prospects. It hands off to cold-email, customer-research, competitor-profiling, revops and sales-enablement.	High. Well structured, and the skills cross-reference each other. Broader than sales.
ai-sales-team-claude (zubair-trabzada)	A main orchestrator plus 13 sub-skills: research, contacts, outreach, follow-up, meeting prep, proposal, objections, competitors, report.	Medium-high. Covers the whole sales flow in one install.
explorium-ai/gtm-skills	Account research, personalized cold email, competitor research and meeting prep.	Medium. Built around Explorium’s data. I haven’t confirmed whether it needs a paid account.
louisblythe/Sales-Skills	Playbooks, scripts, ICP and sales-call analysis. Categories include 22 sales process and strategy skills and 80 AI SDR and bot skills.	Medium. Broad, but 80 bot skills is more than a normal sales team needs.
northrn/claude-sales-skills	Four skills: account research, meeting prep, email writer and competitor intel.	Low-medium. Small and basic.
borghei/Claude-Skills cold-email	A single skill covering personalization, follow-up cadence, deliverability and compliance.	Useful as a standalone if you want one email skill.
gtm-skills/gtm	Prompt library and MCP server covering MEDDPICC, SPIN, Challenger, Gap Selling, Value Selling and Sandler.	Methodology reference only. It appears to be prompts, not native SKILL.md files. I haven’t verified that. 
ColdIQ GTM Skills
 +8

What stands out:

ColdIQ is the strongest outbound pack.
It covers signal-based selling: funding, hiring, job changes and tech changes. 
vibeindex

It includes 34 email templates organized by use case and persona. 
vibeprospecting

It comes from an agency that reports running campaigns at scale. That claim is self-reported and I haven’t verified it.
ColdIQ has a vendor bias. The list-building skill text tells Claude to build lists with ColdIQ first instead of hand-building them from separate providers. That is a sales funnel built into the instructions. Edit it before using it with a client. 
skills

The counts conflict. Different directories list 39, 87 or “7 + 52 + 33” skills for the same repo. Treat the numbers as unreliable and count the folders yourself.
The packs overlap. Composio’s roundup warns that several packs ship a cold email skill and compete for the same trigger. Keep one and remove the rest. Installing several at once makes Claude’s routing worse. 
composio

Outbound has legal risk. The cold-email skills mention CAN-SPAM, GDPR and deliverability, but a skill is not legal advice. Have the client’s counsel review it, especially for EU targets.

Section 2 verdict: For outbound, use ColdIQ (trimmed to the master skills you need) + the Anthropic sales plugin. Use the coreyhaines31 prospecting skill if you want something lighter. Skip the others unless a gap shows up.

Preview of Section 3: account research and competitive intelligence. I’ll compare the Anthropic account-research and competitive-intelligence skills against competitor-profiling, the Explorium skills, and any dedicated market or competitor research packs I can find.

Say “next” to continue.

## Claude (2026-10-23 11:34:48 EDT)

Staged outline
#	Section	Status
1	Official foundation: Anthropic’s sales plugin	Below
2	Outbound and prospecting skill packs	Next
3	Account research and competitive intelligence	Pending
4	Deal coaching, objections, retention and account growth	Pending
5	Ranked list and recommended stack for a client	Pending
Section 1: Anthropic’s official sales plugin

What it is. It is a sales plugin designed mainly for Cowork, Anthropic’s desktop app, and it also works in Claude Code. It covers call prep, summaries and follow-up, account research, deal work, pipeline review and the forecast. It sits in the anthropics/knowledge-work-plugins repo. One write-up reports 15,500+ GitHub stars. 
knowledge-work-plugins/sales at main · anthropics/knowledge-work-plugins · GitHub
 +2

Skills confirmed so far:

Skill	Use case it serves
account-research	Strategy and research
competitive-intelligence	Strategy and research (builds an HTML battlecard)
draft-outreach	Outbound
call-prep, call-summary	Deal coaching
handle-objection	Deal coaching (uses responses and proof points from your own history)
pipeline-review, forecast, daily-briefing, create-an-asset	Pipeline management and reporting 
jaymountconsulting

github

Connectors. Every skill works without connectors. The listed connectors are Slack, HubSpot, Close, Clay, ZoomInfo, Notion, Jira, Fireflies and Microsoft 365. Your org already has HubSpot, Apollo, Notion and Fathom connected, so there is overlap. 
github

github

Install (Claude Code): claude plugin marketplace add anthropics/knowledge-work-plugins, then claude plugin install sales@knowledge-work-plugins. In Cowork, install from the Plugins sidebar. 
github

Related plugins in the same repo. A Codex fork of the repo lists apollo, common-room and slack-by-salesforce alongside sales. They may be relevant to your Apollo setup. I haven’t confirmed what they contain. 
github

Assessment:

Strength: It is the only first-party option, it is maintained, and it covers the full sales day. It is the best base layer.
Weakness: It is generic. One review says you must add your own ICP, discovery questions, house voice and CRM fields before relying on it. That is plausible but comes from a single source.
Gap: I have not found a retention or account-expansion skill in it. That is unconfirmed.

Limits of this section:

GitHub blocked direct page fetches, so the skill list comes from search snippets and secondary sources.
One blog says version 2.0 has 36 skills, but I have only confirmed about 10 by name. Check the repo’s skills/ folder for the full list. 
jaymountconsulting

Review any third-party skill’s contents before installing it. Skills are instructions Claude follows, and they may be bundled with scripts.

Preview of Section 2: outbound and prospecting packs, including explorium-ai/gtm-skills, ColdIQ GTM Skills, zubair-trabzada/ai-sales-team-claude, louisblythe/Sales-Skills and coreyhaines31/marketingskills. I’ll compare them on overlap, depth and risk.

Say “next” to continue, or tell me to adjust the scope.

## User (2026-10-23 11:34:48 EDT)

next

## Claude (2026-10-23 11:34:48 EDT)

Section 2: Outbound and prospecting skill packs
Pack	What’s in it	Fit for outbound
ColdIQ GTM Skills (sachacoldiq / cold-iq)	7 master skills (Clay, Cold Email, LinkedIn Ads, LinkedIn Content, List Building, n8n, Signal Sourcer) that route to 52 sub-skills, plus 33 standalone skills. The standalone skills cover cold call scripts, buying signals, email templates and SDR playbooks.	Highest. Deepest outbound library found.
marketingskills (coreyhaines31)	A prospecting skill that finds, qualifies and scores prospects. It hands off to cold-email, customer-research, competitor-profiling, revops and sales-enablement.	High. Well structured, and the skills cross-reference each other. Broader than sales.
ai-sales-team-claude (zubair-trabzada)	A main orchestrator plus 13 sub-skills: research, contacts, outreach, follow-up, meeting prep, proposal, objections, competitors, report.	Medium-high. Covers the whole sales flow in one install.
explorium-ai/gtm-skills	Account research, personalized cold email, competitor research and meeting prep.	Medium. Built around Explorium’s data. I haven’t confirmed whether it needs a paid account.
louisblythe/Sales-Skills	Playbooks, scripts, ICP and sales-call analysis. Categories include 22 sales process and strategy skills and 80 AI SDR and bot skills.	Medium. Broad, but 80 bot skills is more than a normal sales team needs.
northrn/claude-sales-skills	Four skills: account research, meeting prep, email writer and competitor intel.	Low-medium. Small and basic.
borghei/Claude-Skills cold-email	A single skill covering personalization, follow-up cadence, deliverability and compliance.	Useful as a standalone if you want one email skill.
gtm-skills/gtm	Prompt library and MCP server covering MEDDPICC, SPIN, Challenger, Gap Selling, Value Selling and Sandler.	Methodology reference only. It appears to be prompts, not native SKILL.md files. I haven’t verified that. 
ColdIQ GTM Skills
 +8

What stands out:

ColdIQ is the strongest outbound pack.
It covers signal-based selling: funding, hiring, job changes and tech changes. 
vibeindex

It includes 34 email templates organized by use case and persona. 
vibeprospecting

It comes from an agency that reports running campaigns at scale. That claim is self-reported and I haven’t verified it.
ColdIQ has a vendor bias. The list-building skill text tells Claude to build lists with ColdIQ first instead of hand-building them from separate providers. That is a sales funnel built into the instructions. Edit it before using it with a client. 
skills

The counts conflict. Different directories list 39, 87 or “7 + 52 + 33” skills for the same repo. Treat the numbers as unreliable and count the folders yourself.
The packs overlap. Composio’s roundup warns that several packs ship a cold email skill and compete for the same trigger. Keep one and remove the rest. Installing several at once makes Claude’s routing worse. 
composio

Outbound has legal risk. The cold-email skills mention CAN-SPAM, GDPR and deliverability, but a skill is not legal advice. Have the client’s counsel review it, especially for EU targets.

Section 2 verdict: For outbound, use ColdIQ (trimmed to the master skills you need) + the Anthropic sales plugin. Use the coreyhaines31 prospecting skill if you want something lighter. Skip the others unless a gap shows up.

Preview of Section 3: account research and competitive intelligence. I’ll compare the Anthropic account-research and competitive-intelligence skills against competitor-profiling, the Explorium skills, and any dedicated market or competitor research packs I can find.

Say “next” to continue.

## Claude (2026-10-23 11:34:48 EDT)

Org instructions require reviewing the threads-wiki skill before acting on a new thread

Org instructions require reviewing the threads-wiki skill before acting on a new thread

## User (2026-10-23 11:34:48 EDT)

this is the repo which I want you to read and understand. give me the entire findings and do an analysis on what are the limitations of it, what can be improved and what are the things that can be ignored. think as a company who want to search about everything and anything about sales in Claude and want answers which match their expectations.

## Claude (2026-10-23 11:34:48 EDT)

I read all 428 lines. I’m treating the 100 ft rigor you picked earlier as still in force. Your “entire findings” request overrides the section-by-section staging, so everything is below.

Scope of what I read: you uploaded one file, not the repo. This is sales-enablement v2.4.0, and it matches the coreyhaines31/marketingskills family. It points to six reference files (deck-frameworks, one-pager-templates, objection-library, win-loss-analysis, demo-scripts, cold-call-scripts) that I haven’t seen. Anything that depends on them is marked unverified. Section 2 of the sales list research is paused until you say “next”.

1. What it is

A sales collateral generator. It is 3,285 words with 17 sections. Its job is to produce assets that help reps close, not to answer sales questions in general.

Area	What it provides
Intake	Asks for value prop, sales motion, collateral needs and current state. Reads .agents/product-marketing.md first if it exists.
Principles	Five rules, the strongest being “Claims Reps Can Defend.”
Assets	Pitch deck (11 slides), one-pager, objection doc, live-deal objection, battle card (8 parts), win-loss (6-step workflow), ROI calculator, demo script, case study brief, proposal, playbook, persona card
Output	A table of deliverable formats per asset
Routing	The description routes out to competitors, customer-research, copywriting, cold-email and offers

The description is 1,012 characters, close to the 1,024 limit I believe applies to skill descriptions. I haven’t re-checked that limit.

2. What is strong (keep it)
Evidence discipline. Competitor claims must be dated and sourced, “not listed on their site” replaces “they don’t have it,” and the doc must say where you lose. Most sales skills lack this, and it is the main reason to use this one.
Live Deal Objection. It gives one response the rep can say as written, with assumptions stated and a rule against inventing stats. It also says “when not to fight.” This is the most useful part for a rep mid-deal.
Win-loss method. It includes wins, segments before counting, uses one primary reason per deal, reports n every time, and treats fewer than about 5 deals as a signal, not a finding. This is more rigorous than most analyst write-ups.
Asks which competitor before drafting a battle card, so it can’t produce a polished card about the wrong company.
Clean boundaries with sibling skills, which reduces overlap.
3. Limitations

Coverage gaps (the biggest issue for an “everything sales” company)

This skill covers roughly one slice of sales: collateral. It has little or nothing on:

Missing	Why it matters
Discovery methodology (MEDDICC, SPIN, Challenger)	Only name-dropped as “BANT, MEDDIC, or your framework”
Pipeline, forecasting, deal reviews	Delegated to revops, which isn’t included
Prospecting and account research	Delegated or absent
Negotiation, procurement, legal and security reviews	No guidance
RFP and security questionnaire responses	A core enterprise sales task, absent
Multi-threading, mutual action plans	A single vendor link (Introw) stands in for it
Renewal, expansion, churn	Zero coverage
Sales coaching and call review	Absent
Metrics and KPIs (conversion, cycle time, ACV)	Absent
Pricing strategy	Delegated to pricing, not included

Dependency problems

Unresolved references. Related Skills lists pricing, product-marketing, revops and competitor-profiling. The description names offers, which Related Skills doesn’t list. If those aren’t installed, Claude points to skills that don’t exist.
Six reference files not supplied. The deck, one-pager, objection-library, demo, cold-call and win-loss depth lives there. In the main file, cold calls are one pointer line with no body.
Cold calls are a trigger without a section. The description fires on “cold call script” and “voicemail script,” but the body only links out.

Internal inconsistencies

The Output Format table omits battle cards, case study briefs and cold call scripts, which are three of its own asset types.
“10-12 slide framework” lists 11 slides.
Reps need information “in 3 seconds” (principles) but one-pagers must be “scannable in 30 seconds.”
It tells reps to defend every claim, yet states unsourced numbers itself: “Playbooks cut ramp time significantly,” proposals over 10 pages “won’t get read,” aim for 5-7 pages.

Quality risks

ROI calculator is the riskiest section. It has inputs, formulas and outputs, and gives no rules on labeling assumptions, using conservative inputs, sensitivity ranges or discounting. The output spec includes “sample data,” so invented numbers can reach a buyer. This contradicts the file’s own evidence principle.
Pricing advice is one-size-fits-all. “Transparent pricing in the deck” is wrong for many enterprise deals, where price depends on scope. The intake collects sales motion and deal size but nothing changes based on them.
Narrow assumptions. It assumes B2B software with AE/SDR roles. There is nothing for SMB or self-serve, channel and partner sales, services or manufacturing, regulated industries, or non-US markets.
No data access. Win-loss and battle cards need CRM, call recordings and competitor data. The file doesn’t say how to get them, so the user has to paste everything.
Description is nearly at its limit with 12 characters of headroom. Adding triggers would break it.
Broad triggers. “Help my sales team” and “what should I give my sales reps” will pull in requests this skill can’t answer well.
Unverified claim of use. The skill assumes .agents/product-marketing.md exists but doesn’t say what happens when it contains stale information.
4. What to improve (ordered by impact)
Add an ROI guardrail. Require every input to be labeled as customer-provided, benchmark (with source) or assumption. Add conservative, base and upside cases, and ban sample numbers in buyer-facing output.
Make intake change the output. A short branch table: self-serve, inside sales, enterprise, channel. Each should change deck length, pricing guidance, proposal depth and which assets to build.
Add a company-context file. The playbook only works with the client’s own ICP, win/loss history, proof points, banned claims and competitor list. Make it a required pre-read, not an optional “check for.”
Fix routing and output tables. Add the missing assets, resolve the dangling skill references, and add a “not installed” fallback.
Add missing high-value modules: discovery frameworks, mutual action plans, RFP and security questionnaire responses, and renewal/expansion. Or ship separate skills and link them.
Add data connectors. Instruct it to use CRM, call-recording and email connectors when available. Your org already has HubSpot, Fathom and Apollo connected.
Add a quality check. One pass before delivery that flags unsourced numbers and any claim a buyer could disprove in a minute. The file’s own principle, applied to itself.
Add test prompts (evals) for the live-objection, battle-card and win-loss paths so changes don’t silently break them.
Trim the description and move trigger phrases into the body.
5. What can be ignored
The Introw “tool integration.” It’s one partner-sales vendor and irrelevant unless the client sells through partners.
Persona cards, case study briefs and proposal structure if the client already has CRM or sales-enablement tooling that holds them. These sections are generic and any model can produce them.
Deck slide structure and one-pager “design principles.” They are reasonable but standard, and nothing here beats the client’s own brand deck. Keep only the “claims reps can defend” rule.
Output Format table, once fixed. It’s formatting preference, not substance.
Quarterly review advice (“Keeping it Living”). Sound, but it’s process, not skill content.
6. Does it meet “ask Claude anything about sales” expectations?

No, not alone. It would answer about 10-15% of what a sales team asks, mainly asset requests, objections and win-loss. It would not handle:

“What does my pipeline look like?”
“Who should I target next?”
“How do I run this negotiation?”
“Why are we churning?”

What the company actually needs is a stack:

Layer	Source
Collateral and evidence rules	This skill, after fixes 1-4
Daily sales workflow, forecasting, pipeline review	Anthropic’s sales plugin
Outbound and signals	ColdIQ (trimmed)
Company knowledge	An internal context file plus CRM and call connectors
What I need to go further

If you want me to produce an improved version of this SKILL.md, tell me the craft level (Sketch, Draft, Painting or Commissioned). It would help to have the six reference files and a short description of the client’s sales motion (self-serve, inside, enterprise or partner, with typical deal size).

Say “next” to resume Section 2 of the sales skill list research.

## User (2026-10-23 11:34:48 EDT)

this is the repo which I want you to read and understand. give me the entire findings and do an analysis on what are the limitations of it, what can be improved and what are the things that can be ignored. think as a company who want to search about everything and anything about sales in Claude and want answers which match their expectations.

## Claude (2026-10-23 11:34:48 EDT)

I read all 428 lines. I’m treating the 100 ft rigor you picked earlier as still in force. Your “entire findings” request overrides the section-by-section staging, so everything is below.

Scope of what I read: you uploaded one file, not the repo. This is sales-enablement v2.4.0, and it matches the coreyhaines31/marketingskills family. It points to six reference files (deck-frameworks, one-pager-templates, objection-library, win-loss-analysis, demo-scripts, cold-call-scripts) that I haven’t seen. Anything that depends on them is marked unverified. Section 2 of the sales list research is paused until you say “next”.

1. What it is

A sales collateral generator. It is 3,285 words with 17 sections. Its job is to produce assets that help reps close, not to answer sales questions in general.

Area	What it provides
Intake	Asks for value prop, sales motion, collateral needs and current state. Reads .agents/product-marketing.md first if it exists.
Principles	Five rules, the strongest being “Claims Reps Can Defend.”
Assets	Pitch deck (11 slides), one-pager, objection doc, live-deal objection, battle card (8 parts), win-loss (6-step workflow), ROI calculator, demo script, case study brief, proposal, playbook, persona card
Output	A table of deliverable formats per asset
Routing	The description routes out to competitors, customer-research, copywriting, cold-email and offers

The description is 1,012 characters, close to the 1,024 limit I believe applies to skill descriptions. I haven’t re-checked that limit.

2. What is strong (keep it)
Evidence discipline. Competitor claims must be dated and sourced, “not listed on their site” replaces “they don’t have it,” and the doc must say where you lose. Most sales skills lack this, and it is the main reason to use this one.
Live Deal Objection. It gives one response the rep can say as written, with assumptions stated and a rule against inventing stats. It also says “when not to fight.” This is the most useful part for a rep mid-deal.
Win-loss method. It includes wins, segments before counting, uses one primary reason per deal, reports n every time, and treats fewer than about 5 deals as a signal, not a finding. This is more rigorous than most analyst write-ups.
Asks which competitor before drafting a battle card, so it can’t produce a polished card about the wrong company.
Clean boundaries with sibling skills, which reduces overlap.
3. Limitations

Coverage gaps (the biggest issue for an “everything sales” company)

This skill covers roughly one slice of sales: collateral. It has little or nothing on:

Missing	Why it matters
Discovery methodology (MEDDICC, SPIN, Challenger)	Only name-dropped as “BANT, MEDDIC, or your framework”
Pipeline, forecasting, deal reviews	Delegated to revops, which isn’t included
Prospecting and account research	Delegated or absent
Negotiation, procurement, legal and security reviews	No guidance
RFP and security questionnaire responses	A core enterprise sales task, absent
Multi-threading, mutual action plans	A single vendor link (Introw) stands in for it
Renewal, expansion, churn	Zero coverage
Sales coaching and call review	Absent
Metrics and KPIs (conversion, cycle time, ACV)	Absent
Pricing strategy	Delegated to pricing, not included

Dependency problems

Unresolved references. Related Skills lists pricing, product-marketing, revops and competitor-profiling. The description names offers, which Related Skills doesn’t list. If those aren’t installed, Claude points to skills that don’t exist.
Six reference files not supplied. The deck, one-pager, objection-library, demo, cold-call and win-loss depth lives there. In the main file, cold calls are one pointer line with no body.
Cold calls are a trigger without a section. The description fires on “cold call script” and “voicemail script,” but the body only links out.

Internal inconsistencies

The Output Format table omits battle cards, case study briefs and cold call scripts, which are three of its own asset types.
“10-12 slide framework” lists 11 slides.
Reps need information “in 3 seconds” (principles) but one-pagers must be “scannable in 30 seconds.”
It tells reps to defend every claim, yet states unsourced numbers itself: “Playbooks cut ramp time significantly,” proposals over 10 pages “won’t get read,” aim for 5-7 pages.

Quality risks

ROI calculator is the riskiest section. It has inputs, formulas and outputs, and gives no rules on labeling assumptions, using conservative inputs, sensitivity ranges or discounting. The output spec includes “sample data,” so invented numbers can reach a buyer. This contradicts the file’s own evidence principle.
Pricing advice is one-size-fits-all. “Transparent pricing in the deck” is wrong for many enterprise deals, where price depends on scope. The intake collects sales motion and deal size but nothing changes based on them.
Narrow assumptions. It assumes B2B software with AE/SDR roles. There is nothing for SMB or self-serve, channel and partner sales, services or manufacturing, regulated industries, or non-US markets.
No data access. Win-loss and battle cards need CRM, call recordings and competitor data. The file doesn’t say how to get them, so the user has to paste everything.
Description is nearly at its limit with 12 characters of headroom. Adding triggers would break it.
Broad triggers. “Help my sales team” and “what should I give my sales reps” will pull in requests this skill can’t answer well.
Unverified claim of use. The skill assumes .agents/product-marketing.md exists but doesn’t say what happens when it contains stale information.
4. What to improve (ordered by impact)
Add an ROI guardrail. Require every input to be labeled as customer-provided, benchmark (with source) or assumption. Add conservative, base and upside cases, and ban sample numbers in buyer-facing output.
Make intake change the output. A short branch table: self-serve, inside sales, enterprise, channel. Each should change deck length, pricing guidance, proposal depth and which assets to build.
Add a company-context file. The playbook only works with the client’s own ICP, win/loss history, proof points, banned claims and competitor list. Make it a required pre-read, not an optional “check for.”
Fix routing and output tables. Add the missing assets, resolve the dangling skill references, and add a “not installed” fallback.
Add missing high-value modules: discovery frameworks, mutual action plans, RFP and security questionnaire responses, and renewal/expansion. Or ship separate skills and link them.
Add data connectors. Instruct it to use CRM, call-recording and email connectors when available. Your org already has HubSpot, Fathom and Apollo connected.
Add a quality check. One pass before delivery that flags unsourced numbers and any claim a buyer could disprove in a minute. The file’s own principle, applied to itself.
Add test prompts (evals) for the live-objection, battle-card and win-loss paths so changes don’t silently break them.
Trim the description and move trigger phrases into the body.
5. What can be ignored
The Introw “tool integration.” It’s one partner-sales vendor and irrelevant unless the client sells through partners.
Persona cards, case study briefs and proposal structure if the client already has CRM or sales-enablement tooling that holds them. These sections are generic and any model can produce them.
Deck slide structure and one-pager “design principles.” They are reasonable but standard, and nothing here beats the client’s own brand deck. Keep only the “claims reps can defend” rule.
Output Format table, once fixed. It’s formatting preference, not substance.
Quarterly review advice (“Keeping it Living”). Sound, but it’s process, not skill content.
6. Does it meet “ask Claude anything about sales” expectations?

No, not alone. It would answer about 10-15% of what a sales team asks, mainly asset requests, objections and win-loss. It would not handle:

“What does my pipeline look like?”
“Who should I target next?”
“How do I run this negotiation?”
“Why are we churning?”

What the company actually needs is a stack:

Layer	Source
Collateral and evidence rules	This skill, after fixes 1-4
Daily sales workflow, forecasting, pipeline review	Anthropic’s sales plugin
Outbound and signals	ColdIQ (trimmed)
Company knowledge	An internal context file plus CRM and call connectors
What I need to go further

If you want me to produce an improved version of this SKILL.md, tell me the craft level (Sketch, Draft, Painting or Commissioned). It would help to have the six reference files and a short description of the client’s sales motion (self-serve, inside, enterprise or partner, with typical deal size).

Say “next” to resume Section 2 of the sales skill list research.
