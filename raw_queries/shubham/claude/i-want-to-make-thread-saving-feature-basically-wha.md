---
conversation_id: f06d0175-b231-489e-95f5-136f72101130
platform: claude
username: "shubham"
title: "Thread saving MCP server feature - Claude"
created_at: "2026-10-12T13:46:12.732Z"
updated_at: "2026-10-12 09:46:32 EDT"
---

# Thread saving MCP server feature - Claude

## User (2026-10-12 09:46:32 EDT)

i want to make thread saving feature basically what the user did prompt in claude basically it should have mcp server basically connected to claude desktop which basically saves each and every what user prompting whenever the connector toggle on it should commit in repo github ok each turn should be saved because i know llm is not determinstic if we rely on llm to do tool call of mcp every time it might miss the save tool call and one thing i found add in project instruction every time save the chat tool call told the instruction to do before any prompt but i want it should don't dependent on this ok how supermemory have done basically the saving one only

## Claude (2026-10-12 09:46:32 EDT)

The core problem is that an MCP server only runs when the model decides to call it. Claude Desktop has no per-turn hook it can fire on your behalf, so the “connector toggle” can’t trigger saves. Any design that depends on the model calling a save tool will miss turns, and project instructions have the same flaw. Deterministic capture has to happen outside the model, in code that runs on every turn.

What’s possible on each surface
Surface	Deterministic per-turn capture?	How
Claude Code (CLI)	Yes	UserPromptSubmit and Stop hooks run shell commands on every prompt and every completed response.
Claude Desktop / claude.ai chat	Not natively	No hook API. Options are a browser extension that reads the DOM on each turn, or a periodic export-and-sync job (near-real-time, not per-turn).
Your own API client	Yes	Wrap the Messages API calls in your own app and write every request and response to git.

As far as I know, tools like Supermemory get reliable capture mostly by working outside the model: hooks in coding tools, browser extensions for chat sites, or their own client. The MCP server is mainly used for retrieval. I can’t confirm their internals, so treat that as my understanding rather than a verified fact.

Recommended approach: Claude Code hooks

Hook scripts run whether or not the model “remembers” anything. Add this to ~/.claude/settings.json:


json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "python3 ~/thread-saver/save_turn.py prompt" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "python3 ~/thread-saver/save_turn.py response" } ] }
    ]
  }
}

Hooks receive JSON on stdin that includes session_id, transcript_path, cwd, and (for UserPromptSubmit) the prompt text. For Stop, read the latest assistant message from the transcript file. Check the transcript format on your machine before relying on the parsing.

A minimal save_turn.py:


python
import sys, json, subprocess, fcntl, datetime, pathlib

REPO = pathlib.Path.home() / "chat-threads"          # local clone of your GitHub repo
mode = sys.argv[1]                                    # "prompt" or "response"
event = json.load(sys.stdin)
session = event["session_id"]

if mode == "response" and event.get("stop_hook_active"):
    sys.exit(0)                                       # avoid loops

if mode == "prompt":
    record = {"ts": datetime.datetime.utcnow().isoformat(), "role": "user",
              "text": event.get("prompt", "")}
else:
    # Read the last assistant message from the transcript (verify format first)
    last = None
    with open(event["transcript_path"]) as f:
        for line in f:
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("type") == "assistant" or e.get("message", {}).get("role") == "assistant":
                last = e
    text = json.dumps(last)[:200000] if last else ""  # refine extraction once you see the shape
    record = {"ts": datetime.datetime.utcnow().isoformat(), "role": "assistant", "raw": text}

out = REPO / "threads" / f"{session}.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)

with open(REPO / ".lock", "w") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)                  # serialize concurrent sessions

    with open(out, "a") as f:
        f.write(json.dumps(record) + "\n")
    subprocess.run(["git", "-C", str(REPO), "add", str(out)], check=True)
    subprocess.run(["git", "-C", str(REPO), "commit", "-m",
                    f"turn: {session[:8]} {record['role']}"], check=False)
    subprocess.run(["git", "-C", str(REPO), "push"], check=False, timeout=30)

Design points:

One file per session avoids merge conflicts between concurrent chats.
The lock prevents two hooks from committing at the same time.
check=False on commit and push means a network failure doesn’t block your prompt. Commits stay local and push on the next turn. Add a retry queue if you need stronger guarantees.
Exit 0 always. A failing hook can interfere with the session, so keep the script defensive.
If you need Claude Desktop chat specifically
Browser extension: capture each turn from the DOM on claude.ai and POST it to a small local service that commits to git. This is the closest to real-time, but it depends on the page structure and your own extension.
Export sync: Anthropic lets you export conversation data. A scheduled job can pull the export and commit the diff. It’s reliable but delayed, and not every turn is saved as it happens.
Your own client: if you’re comfortable calling the API directly, route your conversations through a thin client that logs every request and response. Nothing is left to the model.
Why the project-instruction approach fails

Instructions are read by the model, so compliance depends on the model. Hooks and extensions run as code, so they can’t skip a turn. That’s the distinction you’re after.

If you tell me whether you mainly use Claude Code or Claude Desktop chat, I can help you pick one path and write the full setup, including the GitHub repo layout and transcript parsing.
