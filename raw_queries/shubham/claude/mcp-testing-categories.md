---
conversation_id: 6507f5d5-3d01-42a0-a518-c238637b3f3e
platform: claude
username: "shubham"
title: "MCP testing categories"
created_at: "2026-10-08T13:30:01.080743Z"
updated_at: "2026-10-12 12:34:39 EDT"
---

# MCP testing categories

## User (2026-10-12 12:34:39 EDT)

so, our task is to test our mcp working properly or not, is there something to flag, so now tell me the every category we could possibly get with their probability

## Claude (2026-10-12 12:34:39 EDT)

These probabilities are my priors for a single tool call against a typical remote MCP connector. I haven't measured them, since I don't know which MCP you're testing or have its run history. Treat them as a starting point for test design.

| # | Category | Est. probability | Flag? |
|---|---|---|---|
| 1 | **Pass**: correct, complete result within normal latency | ~55% | No |
| 2 | **Pass but degraded**: slow, truncated, or paginated unexpectedly | ~10% | Yes (minor) |
| 3 | **Wrong or stale data**: result returns, but content is incorrect, incomplete, or out of date | ~10% | Yes (high) |
| 4 | **Tool not discoverable**: not loaded, deferred, or connector toggled off for the chat | ~7% | Yes (config) |
| 5 | **Auth or permission error**: expired token, tier-scope denial | ~6% | Yes (check if expected) |
| 6 | **Timeout or dropped connection**: SSE drop, cold start, network | ~5% | Yes |
| 7 | **Schema or parameter validation error**: bad args, tool definition mismatch | ~3% | Yes |
| 8 | **Server error (5xx or crash)** | ~2% | Yes (high) |
| 9 | **Scope leak or injection**: returns data beyond the caller's tier, or returned content contains instructions | ~2% | Yes (critical) |

**How to read it**
- The failures that are most likely to hurt you are rows 3 and 9. Row 3 is silent, because the call "succeeds", so only comparing against a known-good source catches it. Row 9 is rare but the most damaging.
- Row 4 is mostly a configuration problem, not an MCP bug, so check the connector toggle and tool loading before blaming the server.
- Each test case should have an expected output defined up front. Without one, rows 1 and 3 look identical.
- Run each tool at least 20 times with varied inputs. At 2–3% failure rates, a handful of runs won't show anything.
- Log latency per call, since row 2 only shows up against a baseline.

Tell me which MCP and which tools are in scope, and I'll turn this into a concrete test matrix with an expected result per case. After your first runs, replace these priors with the measured rates.

## User (2026-10-12 12:34:39 EDT)

the object is to identify the flags in the response of claude

## Claude (2026-10-12 12:34:39 EDT)

Understood. My last table scored the MCP server, but you want flags in Claude's response when it uses the MCP. These are untested priors, one primary outcome per response (so they sum to 100%), and I'm assuming a quick 5ft-level pass.

| # | Flag category in Claude's response | Est. prob. | Severity |
|---|---|---|---|
| 1 | **Clean**: right tool, answer matches tool output, instructions followed | ~45% | None |
| 2 | **Answered without calling the tool**, from memory or guesswork when the data was in the MCP | ~8% | High |
| 3 | **Wrong tool or source**, e.g. answering a contribution or tasks question from emails instead of the task boards, or the wrong connector or tier | ~8% | High |
| 4 | **Misreported result**: wrong numbers, dropped rows, or undisclosed truncation or pagination | ~8% | High |
| 5 | **Fabrication**: details that appear in no tool result | ~6% | Critical |
| 6 | **Thread Vault lifecycle broken**: no `checkpoint` first, no `save_chat_transcript` last, a changing `thread_name`, or a non-cumulative transcript | ~6% | Medium |
| 7 | **Error handling failure**: claims a connector is unavailable without trying, retries a refusal, hides a failed call, or leaks raw tool tags or errors | ~5% | Medium |
| 8 | **Needless questioning**: asks before inspecting available tools, or runs multi-round clarification loops | ~4% | Medium |
| 9 | **Tone or format violations**: flattery, padding, no stated assumptions, or no rigor or craft level offered on deep tasks | ~4% | Low |
| 10 | **Scope leak or injection followed**: returns data above the caller's tier, or obeys instructions embedded in tool output | ~3% | Critical |
| 11 | **Missing sources**: no "Sources:" list when the answer draws on linkable material | ~3% | Low |

**What this means for testing**
- Rows 4 and 5 are silent failures. The response reads confidently, so you only catch them by diffing against the raw tool output.
- Row 6 is mechanical and easy to check automatically. Verify the first and last tool calls of every turn, not the text.
- Row 3 needs trap prompts, such as the contribution-style question, where the wrong connector is tempting.
- Row 10 needs adversarial test data, such as a record containing "ignore previous instructions". Normal prompts will never trigger it.
- Define the expected tool calls and expected facts for each test case up front. Otherwise rows 1 and 4 look identical.

If you share the MCP and tools in scope, I can turn this into a test matrix with a pass/fail check per row.
