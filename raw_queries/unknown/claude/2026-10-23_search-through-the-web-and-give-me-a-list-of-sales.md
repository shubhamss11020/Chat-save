---
conversation_id: eb3fda21-6cf6-4a24-8617-a398554dabda
platform: claude
username: "unknown"
title: "Sales skill files for research - Claude"
created_at: "2026-10-23 10:58:49 EDT"
updated_at: "2026-10-23 11:06:17 EDT"
---

# Sales skill files for research - Claude

## User (2026-10-23 11:06:17 EDT)

search through the web and give me a list of sales skill files which can be helpful for a client to extract sales strategies, or any sales related questions. make a list of it and provide me the best skill files which can be helpful for a company to research about anything and everything related to sales.

## Claude (2026-10-23 11:06:17 EDT)

Org instructions require reviewing the threads-wiki skill before acting on a new thread

Org instructions require reviewing the threads-wiki skill before acting on a new thread

## Claude (2026-10-23 11:06:17 EDT)

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

## User (2026-10-23 11:06:17 EDT)

next

## Claude (2026-10-23 11:06:17 EDT)

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
