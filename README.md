# Chat-Save

Automatic, save-only backup of Claude conversations to Git. No retrieval, no MCP:
the model never has to remember to save anything.

```
Claude Code session files (read-only)
        │   Stop hook  +  periodic/startup reconciliation
        ▼
  CaptureController  → full transcript → SHA-256 → skip if unchanged
        ▼
  SQLite outbox (storage/capture.db): pending → processing → completed
        ▼  background worker, retries with backoff
  Git writer → raw_queries/<user>/claude/<conversation-id>.md → commit → push
```

- **Idempotent**: same transcript = same hash = nothing queued, no duplicate commits.
- **Git failures don't lose chats**: items stay `pending` with `last_error` and retry.
- **Crash-safe**: `processing` items are reset on start; startup reconciliation re-scans
  everything that changed while the agent was down.
- **Read-only** toward Claude's files.

## Run

```
python -m venv .venv && .venv\Scripts\pip install -r requirements.txt
copy .env.example .env      # set CHATSAVE_GIT_URL
.venv\Scripts\python -m uvicorn app.main:app --port 8000
```

`GET /status` shows outbox counts and the latest errors. `POST /reconcile` forces a scan.
`POST /conversations` is a manual fallback for a full transcript.

## Optional: instant capture with a Claude Code Stop hook

Reconciliation already catches everything within ~10 s. For immediate capture add to
`~/.claude/settings.json`:

```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command",
  "command": "python C:\\Users\\shubh\\OneDrive\\Desktop\\Chat-Save\\scripts\\claude_stop_hook.py" } ] } ] } }
```

The hook fails open: it never blocks Claude if the agent is down.

## Limits

Only **Claude Code** sessions (`~/.claude/projects`) are readable locally. Chats in the
Claude Desktop chat tab and ChatGPT are stored server-side, so no local source exists for
them yet; `ConversationSource` in `app/sources/base.py` is where one would plug in.
