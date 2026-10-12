---
conversation_id: dfde6caf-6961-43ba-b284-b76b265de78f
platform: claude
username: "shubham"
title: "Claude instructions"
created_at: "2026-10-08T18:22:51.961240Z"
updated_at: "2026-10-12 12:33:42 EDT"
---

# Claude instructions

## User (2026-10-12 12:33:42 EDT)

what exactly does instruction do in the claude? and what can and should we add over there ?, don't use any connector or tools calling ,

## Claude (2026-10-12 12:33:42 EDT)

# Instructions in Claude: What They Are & What EOXS Should Add

## What Instructions Do

**Instructions** (Custom Instructions in Claude.ai) are persistent, user-level guidelines that shape how Claude behaves across *every conversation*. They're not system prompts—they're your standing preferences that Claude applies automatically.

What they affect:
- **Communication style** — tone, formality, brevity
- **Output format** — how Claude structures answers (bullet points, prose, tables)
- **Depth preferences** — level of detail, technical complexity
- **Behavioral defaults** — what Claude assumes you want without asking
- **Domain expertise** — Claude treats you as having relevant background
- **Workflow preferences** — when to use tools, when to ask first

**Key difference:** Instructions are *additive*—they layer onto Claude's base behavior. They don't override safety or ethical constraints. They're about efficiency, not capability.

---

## What EOXS Should Add (Right Now)

Based on your role and context, these instructions would save time and clarify intent:

### 1. **Role & Context (Non-Negotiable)**
```
I'm Rajat Jain, CEO of EOXS (a compliance automation platform) and founder of AskCruz (AI recruitment platform). Assume deep familiarity with the business, clients, team, and operational metrics. Don't explain basics.
```
This prevents Claude from over-explaining and assumes you know your own business.

### 2. **Communication Style**
```
Be direct, concise, and factual. Avoid flattery, emotional padding, and hedging. Prioritize truth over agreement. If I'm overlooking something, missing a risk, or wasting time, say it directly. Be a strategic advisor and sounding board, not a subordinate.
```
Shifts Claude from "assistant mode" to "advisor mode."

### 3. **Decision Rigor Framework**
```
Before starting research, analysis, or strategic work, present depth options (Quick/5ft, Verified/10ft, Deep/50ft, Staged/100ft) unless I specify. Also ask for craft level (Sketch/Draft/Painting/Commissioned) for deliverables.
```
Gives you control over time-to-answer and quality tradeoff upfront.

### 4. **Evidence & Sourcing**
```
Back every material claim with sourcing. Flag uncertainty. Separate facts from assumptions. When data conflicts, name each source and flag the conflict. Show the reasoning, not just the conclusion.
```
Ensures accountability and helps you spot weak reasoning.

### 5. **Goal-Focused Filtering**
```
Primary objectives: (1) Keep EOXS stable and growing inbound-only. (2) Grow AskCruz to $1,000,000 ARR within 12 months. When evaluating opportunities, decisions, or time allocation, ask: "Does this move the needle?" Flag distractions or low-leverage work.
```
Makes Claude your accountability partner on focus.

### 6. **Clarification Before Depth**
```
Before diving into analysis or building, take a step back and ask clarifying questions until you reach 95% certainty. Examples: "Are you asking because you're considering X, or because you want to understand Y?" "Is this for immediate action or exploratory?" Better to ask 2 questions upfront than answer the wrong question.
```
Prevents wasted work on misunderstood problems.

---

## What *Not* to Add

- **Specific data or metrics** — Instructions can't be updated instantly. Put those in memory or as query preambles instead.
- **Time-sensitive details** — "Current priorities are X, Y, Z" changes weekly; reference memory or tell Claude in the moment.
- **Names, passwords, or secrets** — Never. Instructions are visible in settings.
- **Task lists or to-dos** — Use task management tools; instructions aren't a project tracker.

---

## How It Stacks With What You Already Have

Your preferences file (/userPreferences) is *already* doing what instructions would do—but stronger, because they load per-conversation and can trigger skills. Instructions are a *secondary* layer:

- **Preferences** = Baked into every turn (auto-loaded, deep).
- **Instructions** = Visible to you in settings, can be edited anytime, apply across your whole account.

You'd use Instructions for the **stable, universal stuff** that should be your standard across all use cases (role, tone, evidence standards). You'd use Preferences for the **EOXS-specific routing logic** (which connectors, which skills, which rigor frameworks).

**Recommendation:** Set instructions for 1-2-3-4 above (role, tone, evidence, clarification discipline). Keep the routing and skill logic in preferences where it's already working.

---

## Where to Set Them

**Claude.ai or Claude app:**
Settings → Profile → Custom Instructions

Add your top 3-4 principles, keep it under 200 words. Claude will apply them by default.

---

**What should EOXS add first?** Start with role + tone + evidence standards. That unlocks the most value. The rest can follow as you refine your interaction pattern with Claude.

## User (2026-10-12 12:33:42 EDT)

does instructions manipulate mcp ? by how much ? and what can be handled by instructions about a mcp or thier tools ?

## Claude (2026-10-12 12:33:42 EDT)

# Instructions & MCPs: No Direct Manipulation, High Indirect Influence

## The Short Answer

**Instructions do NOT manipulate MCPs themselves.** They influence *how Claude decides to use* MCPs. The difference is critical.

- **MCPs** = External tools that run independently, return data on their own terms
- **Instructions** = Guidance for Claude's decision-making about *when and how* to call those tools

**Impact: Zero direct, High indirect.**

---

## What Instructions CANNOT Do (No MCP Manipulation)

| What | Why |
|------|-----|
| Change how an MCP works internally | Instructions are Claude's guidance layer, not the MCP's code |
| Alter data the MCP returns | MCP data comes from the system of record, not instructions |
| Modify MCP authentication/scope | Permissions are set at the connector level, not via instructions |
| Add new MCP capabilities | Instructions can't invent new queries or features the MCP doesn't support |
| Override MCP security rules | MCPs enforce their own access controls independently |
| Change which MCPs are available | That's a connector/account setting, not an instruction effect |
| Make an MCP "faster" or "more accurate" | The underlying service determines that, not Claude's instructions |

---

## What Instructions CAN Do (Influence Claude's Tool Use)

### 1. **Routing & Prioritization**
```
"When a question touches EOXS data (emails, clients, tasks), use askcruz first. 
If askcruz lacks data, cross-check with eoxs-teams."
```
Claude reads this and *decides* which MCP to call. The MCP itself doesn't change—Claude's strategy does.

### 2. **Conditional Tool Calling**
```
"Don't call MCPs for basic factual questions you already know. 
Only call askcruz if the question requires current data."
```
Claude becomes more selective about *when* to invoke tools, reducing unnecessary calls.

### 3. **Verification Strategy**
```
"Always cross-check material claims with at least one additional source 
before stating something as fact."
```
Claude uses multiple MCPs sequentially and compares results. The MCPs work unchanged; Claude's interrogation strategy shifts.

### 4. **Transparency About Tool Use**
```
"Always state which connector you're calling and why."
```
Doesn't change the MCP—just changes Claude's reporting of what it's doing.

### 5. **Freshness & Recency Awareness**
```
"Flag when data from an MCP is stale (>7 days old). 
If stale, note that in the answer."
```
Claude adds *context* about data age. The MCP returns what it returns; Claude adds the caveat.

### 6. **Error Handling**
```
"If an MCP returns no results, don't assume the answer is 'no data exists.' 
State the query limit and suggest a different approach."
```
Claude becomes smarter about interpreting empty results, doesn't blame the MCP.

---

## The Technical Reality

**Flow:**
1. User asks a question
2. Claude reads instructions
3. Claude *decides* which MCP to call (or not)
4. Claude calls the MCP with a query
5. MCP executes independently and returns data
6. Claude formats/interprets the result per instructions
7. Claude presents the answer

**Instructions affect steps 3, 4, and 6.** Steps 5 is the MCP's job—instructions don't touch it.

---

## Quantifying the Effect

| Dimension | Impact | Why |
|-----------|--------|-----|
| **Which MCP gets called** | High (instructions can prioritize) | Claude decides based on instructions |
| **When MCPs are called** | High (instructions set thresholds) | Claude decides based on conditions in instructions |
| **Query sent to MCP** | Low (query is implied by the user) | MCP schema determines what queries are valid |
| **Data returned by MCP** | Zero (MCP owns this) | Data comes from the system of record |
| **How Claude interprets results** | High (instructions guide framing) | Claude can add context, caveats, or re-order results |
| **Accuracy of MCP data** | Zero | That's determined by the underlying system, not instructions |

---

## What EOXS Can Control With Instructions About MCPs

### ✅ DO This

**1. Specify routing priority:**
```
"For contribution/work questions, query teams-askcruz and eoxs-teams. 
Cross-reference both before answering."
```

**2. Set freshness expectations:**
```
"Always flag data older than 48 hours. Refresh if available."
```

**3. Define fallback logic:**
```
"If askcruz returns no results, try searching wiki (search_wiki) 
before concluding 'no data.'"
```

**4. Control uncertainty communication:**
```
"If data is incomplete, say so. Don't extrapolate."
```

**5. Set verification thresholds:**
```
"For high-stakes claims (revenue, client status, headcount), 
verify against two independent sources."
```

### ❌ DON'T Try This

- "Make askcruz return data 10x faster" (can't; that's the connector's performance)
- "Make MCPs return real-time data if they don't support it" (can't; depends on the MCP's design)
- "Add new fields to MCP queries" (can't; limited by MCP schema)
- "Make an MCP return data it doesn't have access to" (can't; limited by permissions)

---

## How This Stacks With Your Preferences

Your preferences file already has detailed MCP routing logic:
```
"State which connector you're using and why. Never silently pick a wrong connector."
```

That's **Instructions-level thinking**, but implemented in preferences because it's EOXS-specific and needs to trigger skills.

**Recommendation:**
- **Use Instructions** for universal MCP principles (always cross-check, always state source, flag staleness)
- **Use Preferences** for EOXS-specific routing (which connector for which question type, skill stacking order)

---

## Bottom Line

**Instructions influence Claude's *decision-making* about MCPs, not the MCPs themselves.** They're a lens through which Claude views tool use, not a control mechanism for the tools.

The value isn't in manipulating the connector—it's in making Claude smarter about *which connector to use, when, and how to interpret the results.*
