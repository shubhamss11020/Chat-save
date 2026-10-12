---
conversation_id: b3eedffa-5f19-4b47-be5b-84a13da26096
platform: claude
username: "shubham"
title: "Claude's subagent deployment approach"
created_at: "2026-10-06T13:52:36.624899Z"
updated_at: "2026-10-12 11:01:32 EDT"
---

# Claude's subagent deployment approach

## User (2026-10-12 11:01:32 EDT)

How claude is basically deploy subagents according to the prompts or task basically

## Claude (2026-10-12 11:01:32 EDT)

Subagent deployment is a pattern called **orchestrator-worker**. Claude doesn't have a hidden "spawn" mechanism. It decides to delegate through a **tool call**, the same way it decides to call a search tool.

**How it works**

1. **The main agent receives the task** and reasons about it: is it big, parallelizable, or likely to flood its context with raw material (reading 50 files, searching many sources)?
2. **It calls a delegation tool** (in Claude Code this is the Task/Agent tool). The call includes a short description, a detailed prompt for the subagent, and optionally which subagent type to use.
3. **The subagent runs in a fresh context window** with its own system prompt and its own allowed tools. It knows nothing about the parent conversation except what the prompt tells it.
4. **It returns only a final summary** to the parent. The messy intermediate work (file reads, failed searches) never enters the parent's context.
5. **The parent synthesizes** the results and continues, or spawns more subagents.

**How Claude chooses which subagent to use**

Custom subagents are defined as config (for example a markdown file in Claude Code) with a name, a **description**, a tool list, and a system prompt. The description is what matters most: Claude matches your task against those descriptions, much like tool selection. A description like "Use proactively after code changes to review for security issues" makes Claude delegate automatically. A vague description rarely gets triggered.

**When delegation makes sense**

- **Parallel independent work**, such as researching 5 competitors at once
- **Context isolation**, such as exploring a big codebase and reporting back only the findings
- **Specialization**, such as a reviewer, tester, or debugger with its own instructions and restricted tools

It's a poor fit for small tasks or tightly sequential work, because each subagent adds token cost and loses shared context.

**Where you see this**

- **Claude Code and the Agent SDK:** explicit subagents, which you can define yourself
- **Claude's Research feature:** a lead agent plans, spawns parallel search subagents, then compiles a cited report
- **This chat:** I don't have a subagent tool in this conversation, so I work directly with the tools I have

Since you're building an MCP project, one practical point: subagents can use MCP tools too, as long as their tool list allows it. That's a good way to give a dedicated "email search" subagent only the Gmail tools.

If you'd like, I can show a sample subagent definition file or a minimal orchestrator example with the Agent SDK.

## User (2026-10-12 11:01:32 EDT)

don't u think suppose fetching from each different website one by one gather info from each store locally and then after merge all the website info and llm give enhanced response after that take to much time and have impact user experience but how claude do very fastly

## Claude (2026-10-12 11:01:32 EDT)

Yes, sequential fetch, store, merge, then LLM would be slow. Claude avoids it in a few ways.

**1. It doesn't crawl websites live**
Web search goes through a search engine API that already has the web indexed. One call returns the top results with snippets in about a second. Claude only fetches the full page for a few promising results. The expensive "visit every site" step mostly doesn't exist.

**2. Parallel tool calls**
When the calls are independent, the model can emit several tool calls in a single turn, and the system runs them concurrently. Fetching 5 pages takes roughly as long as the slowest one, not the sum of all five. Subagents in research workflows work the same way: they run in parallel, not one after another.

**3. No local storage or merge step**
Results are fed straight into the model's context as text. There's no "save to DB, then merge" stage. The LLM does the merging while it writes the answer.

**4. Trimmed content**
Pages are cleaned to plain text and truncated before the model sees them. Less input means less latency and cost.

**5. Streaming**
The answer streams token by token, so the user sees output almost immediately instead of waiting for the full response. Perceived speed matters as much as actual speed.

**6. Caching and cheaper models**
Repeated fetches and prompt prefixes can be cached, and subagents that just gather data can use a smaller, faster model while a stronger model writes the final synthesis.

**It's not always fast, though.** A simple search answer takes a few seconds, but deep research with many subagents can take several minutes. That's a deliberate tradeoff, and the UI shows progress so it doesn't feel frozen.

**For your own system, the same principles apply:**
- Use `asyncio.gather` (or `httpx.AsyncClient`) to fetch all sources concurrently
- Set per-request timeouts and return partial results if one source is slow
- Pre-index data that doesn't change often (like your PostgreSQL email sync) instead of fetching live
- Pass trimmed snippets to the LLM, not full pages
- Stream the response to the user

I can sketch a FastAPI example with concurrent fetching and streaming if you'd like.
