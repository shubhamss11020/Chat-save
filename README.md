# Chat-Save

Automatic backup of Claude conversations to Git, through an MCP server. The model never
has to remember to save: a local capture agent calls the MCP tool for it.

```
Claude Code session files (read-only)
   │  Stop hook  +  periodic/startup reconciliation        ── capture agent (your PC)
   ▼
CaptureController → full transcript → SHA-256 → skip if unchanged
   ▼
SQLite outbox (storage/capture.db): pending → processing → completed, retry w/ backoff
   │  automatic MCP call: save_chat_transcript
   ▼
MCP server (/mcp, token-protected)                        ── e.g. Render
   ▼
Git writer → raw_queries/<user>/claude/<conversation-id>.md → commit → push
```

One codebase, two roles:

| Role | Where | Env |
|---|---|---|
| Capture agent | your PC | `CHATSAVE_MCP_URL`, `MCP_AUTH_TOKEN`, `CHATSAVE_USER` |
| MCP server | Render | `CHATSAVE_CAPTURE=0`, `CHATSAVE_GIT_URL`, `MCP_AUTH_TOKEN`, `CHATSAVE_REPO_DIR` (see render.yaml) |

If `CHATSAVE_MCP_URL` is empty the agent skips MCP and writes Git directly (set `CHATSAVE_GIT_URL`).

- **Idempotent**: unchanged transcript = same hash = nothing sent; the server also makes no commit.
- **Nothing lost on outage**: MCP/Git down → items stay `pending` with `last_error`, retried with backoff.
- **Crash-safe**: `processing` items reset on start; startup reconciliation re-scans everything.
- **Read-only** toward Claude's files.

## Run the agent

```
python -m venv .venv && .venv\Scripts\pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python -m uvicorn app.main:app --port 8000
```

`GET /status` shows outbox counts and errors (add `?key=<token>` if a token is set).
`POST /reconcile` forces a scan. `POST /conversations` is a manual full-transcript fallback.

## Optional: instant capture with a Claude Code Stop hook

Reconciliation catches everything within ~10 s. For immediate capture add to
`~/.claude/settings.json`:

```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command",
  "command": "python C:\\Users\\shubh\\OneDrive\\Desktop\\Chat-Save\\scripts\\claude_stop_hook.py" } ] } ] } }
```

The hook reads `MCP_AUTH_TOKEN` from `.env` and fails open: if the agent is down or
rejects it, reconciliation still covers the conversation.

## Limits

- Only **Claude Code** sessions (`~/.claude/projects`) are readable locally. Chats in the Claude
  Desktop chat tab and ChatGPT are stored server-side, so no local source exists for them;
  `ConversationSource` (`app/sources/base.py`) is where one would plug in.
- The MCP server must be able to **push to GitHub**. That needs a credential on the server
  (token in `CHATSAVE_GIT_URL` or a deploy key); a public repo can be cloned without one but not pushed to.
