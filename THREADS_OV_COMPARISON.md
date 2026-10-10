# Chat-Save vs Claude Notes Vault: Thread Saving Approaches

## Executive Summary

| Aspect | Chat-Save | Claude Notes Vault |
|--------|-----------|-------------------|
| **Capture Origin** | Local client (Claude Code files) | Remote server (MCP middleware) |
| **Storage Backend** | SQLite outbox queue → Git | Direct Markdown → Git |
| **Reliability Model** | Durable queue with backoff | Middleware auto-capture with reminder |
| **Idempotency** | Content hash deduplication | File-level locking + session tracking |
| **Concurrency Handling** | SQLite serialization + atomic claims | Per-file mutexes + context vars |
| **Multi-User Support** | Via `CHATSAVE_USER` env var | Via URL secrets + context vars |
| **Error Recovery** | Startup reset of stuck items | Git rebase/reset/replay recovery |
| **Crash Safety** | Full ACID transaction guarantee | Middleware auto-save catch-all |
| **Deployment** | Local agent + remote server | Single MCP server instance |
| **Data Loss Risk** | Minimal (durable queue) | Low (middleware redundancy) |

---

## 1. Capture Architecture

### Chat-Save: Client-Side Pull-Based Capture

**Architecture**:
```
Local Files (Claude Code project dir)
    ↓ (read-only polling)
Capture Controller (your PC)
    ↓ (file signature detection: mtime:size)
SQLite (capture.db on your PC)
    ↓ (SHA-256 dedup check)
MCP Call: save_chat_transcript()
    ↓
Remote MCP Server (Render)
    ↓
Git → GitHub
```

**Capture Triggers**:
1. **Periodic reconciliation** (~10s): Scan source directories, detect file changes via signature
2. **Stop hook** (instant): Claude Code `Stop` button triggers `claude_stop_hook.py`
3. **Manual fallback**: `POST /reconcile` or `POST /conversations` endpoints

**Key Characteristics**:
- ✅ **Read-only** toward source files (non-invasive)
- ✅ **Completely automatic** even if LLM never calls a save tool
- ✅ **Redundancy**: Both periodic + hook ensure capture
- ⚠️ **Limited to Claude Code**: `~/.claude/projects` only; Claude Desktop/Web not accessible locally
- ⚠️ **Polling latency**: 10s reconciliation cycle before save appears on server

---

### Claude Notes Vault: Server-Side Push-Based Capture

**Architecture**:
```
MCP Client (Claude)
    ↓ (calls any MCP tool)
_IdentityMiddleware (URL secret → username)
    ↓
Tool Handler
    ↓ (returns result)
Outgoing MCP Response
    ↓
_auto_save_turn() middleware (unconditional)
    ↓ (appends timestamped block)
Local Markdown backup file
    ↓ (per-file lock + git push)
GitHub

ALSO: save_chat_transcript() (explicit full-transcript save)
    ↓
Complete rewrite of thread file
    ↓
GitHub
```

**Capture Triggers**:
1. **Auto-save middleware** (unconditional): Every tool response appends to `<user>_<date>_<session>.md`
2. **Mandatory save_chat_transcript()** (explicit): LLM calls this at end of turn with full transcript
3. **Auto-reminder injection**: Every tool result includes reminder to call save_chat_transcript

**Key Characteristics**:
- ✅ **Works for all Claude interfaces** (Desktop, Code, Web, API)
- ✅ **Automatic + explicit dual paths** (redundancy)
- ✅ **Mandatory reminder system** prevents accidental misses
- ✅ **Server-side capture** (no client-side agent needed)
- ⚠️ **Requires MCP integration** (LLM must call tools, or at least see reminder)
- ⚠️ **Two-stage save** (auto-capture backup ≠ authoritative transcript)

---

## 2. Persistence & Storage Strategy

### Chat-Save: Outbox Queue Pattern

**Storage Layers**:

**Layer 1: Local SQLite (Capture PC)**
```sql
-- conversations, messages, source_state tables
-- UNIQUE constraint: (conversation_id, external_message_id)
-- Deduplication: content_hash for mutation detection
```

**Layer 2: Outbox Queue (Capture PC)**
```sql
-- outbox: id, event_type, conversation_id, status, attempts, next_attempt_at, ...
-- Status transitions: pending → processing → completed (or failed → pending after backoff)
```

**Layer 3: Remote Git (GitHub)**
```
raw_queries/<user>/claude/<conversation-id>.md
```

**Write Path**:
```
Event captured
    ↓ (BEGIN TRANSACTION)
INSERT INTO messages (with dedup constraint)
INSERT INTO outbox (status = 'pending')
    ↓ (COMMIT)
Immediate response to caller
    ↓ (background worker)
Atomic claim: UPDATE outbox SET status='processing' WHERE status='pending'
    ↓
Render Markdown from SQLite
    ↓
Push to Git
    ↓
Mark complete: UPDATE outbox SET status='completed'
```

**Guarantees**:
- ✅ **ACID**: All-or-nothing per event
- ✅ **Idempotent**: Same `external_message_id` = same row (upsert via `ON CONFLICT`)
- ✅ **Durable**: Items stay in `pending` if GitHub unreachable
- ✅ **Observable**: Query `SELECT * FROM outbox WHERE status = 'failed'` to see stuck items

---

### Claude Notes Vault: Direct File Write Pattern

**Storage Layers**:

**Layer 1: Local Markdown Files** (in-process)
```markdown
---
thread_name: "..."
user: "..."
created: "..."
updated: "..."
---

# Content
```

**Layer 2: Remote Git (GitHub)**
```
raw/claude-chat-queries/<user>_<date>_<thread>.md
wiki/analyses/<date> <title>.md
```

**Write Path**:

**Path A: Auto-Save Middleware (backup)**
```
Outgoing MCP response
    ↓
_auto_save_turn() scans for text content
    ↓
Append timestamped block to <user>_<date>_<session>.md
    ↓
Acquire per-file lock: _get_file_lock(path)
    ↓
Write + commit + push
```

**Path B: Explicit save_chat_transcript() (authoritative)**
```
LLM calls save_chat_transcript(thread_name, content)
    ↓
Acquire per-file lock
    ↓
Validate content (not empty)
    ↓
Read existing file (if any) to extract created_at
    ↓
Check for continuation from older files (date boundary handling)
    ↓
Write frontmatter + content
    ↓
Git commit + push (with fallback recovery)
```

**Guarantees**:
- ✅ **Dual save paths**: Middleware backup + explicit transcript
- ✅ **Thread-safe**: Per-file mutexes serialize concurrent writes
- ✅ **Session-agnostic**: Auto-save continues same file across reconnects
- ⚠️ **Not transactional**: If process crashes during write, Markdown may be partial
- ⚠️ **Not idempotent**: Duplicate middleware calls = duplicate blocks appended

---

## 3. Reliability & Failure Modes

### Chat-Save: Outbox-Based Recovery

**Failure: GitHub Unreachable**

1. Worker claims batch of `pending` items atomically
2. GitHub API call fails → exception caught
3. Update outbox: `status='failed', next_attempt_at = now + backoff(attempts)`
4. Worker returns, logs error
5. **Next cycle** (configurable interval): Worker retries
6. **Backoff**: Exponential (e.g., 2^attempts * jitter)

**Failure: Process Crashes**

1. Any items in `processing` state are incomplete
2. **On startup**, `recover()` runs: `UPDATE outbox SET status='pending' WHERE status='processing'`
3. Next worker tick retries them
4. **Result**: Zero data loss; eventual delivery guaranteed

**Failure: Duplicate Message Sent**

1. Same `external_message_id` received twice
2. First: `INSERT INTO messages ... → outbox (pending)`
3. Second: `INSERT ... ON CONFLICT(conversation_id, external_message_id) DO UPDATE ...`
4. `content_hash` updated if content changed
5. `content_hash` unchanged = same message = outbox NOT re-enqueued
6. **Result**: Idempotent; no duplicate GitHub commits

**Advantages**:
- ✅ Observable queue state: `SELECT * FROM outbox WHERE status IN ('pending', 'failed')`
- ✅ Predictable retry behavior: exponential backoff with tunable parameters
- ✅ Deterministic recovery: stuck items auto-reset on startup
- ✅ Deduplication: content hash prevents accidental re-saves

**Disadvantages**:
- ⚠️ Queue bloat if backoff parameters are too aggressive
- ⚠️ SQLite contention under high load (single writer)

---

### Claude Notes Vault: Middleware Redundancy + Git Recovery

**Failure: GitHub Unreachable (during save_chat_transcript)**

1. `_git_commit_and_push()` called
2. `git fetch origin/<branch>` fails → exception caught
3. Return error to caller: "fetch failed: {stderr}"
4. **No retry logic**: Caller (LLM) must decide to retry or give up
5. **BUT**: Markdown file was already written locally
6. **Eventual recovery**: Next save attempt will retry; if it succeeds, the file is pushed

**Failure: Git Push Conflicts (non-fast-forward)**

1. Another process pushed to same branch since last fetch
2. `git push` fails with "non-fast-forward" error
3. **Recovery sequence**:
   ```
   git fetch origin/<branch>
   git rebase origin/<branch>  (reapply our commits on top)
   ```
4. If rebase fails (conflicting changes):
   ```
   git rebase --abort
   git diff origin/<branch> HEAD  (capture what we committed locally but didn't push)
   git reset --hard origin/<branch>  (discard our commits)
   git apply --3way <diff>  (replay our diff on top)
   git add -A && git commit
   git push
   ```
5. **Result**: Sophisticated recovery; all locally-committed work preserved even if rebase fails

**Failure: Process Crashes Mid-Save**

1. Markdown file is being written
2. File may be partial/corrupted (no transaction boundary)
3. **Middleware auto-save** (backup): Earlier appended blocks remain intact
4. **Next LLM save**: Overwrites with fresh full transcript (corrupted partial is replaced)
5. **Result**: Lower risk due to dual paths, but single writes aren't atomic

**Failure: Duplicate MCP Calls**

1. Middleware auto-save called twice (unlikely, but possible during session reconnect)
2. First: Appends block to `<user>_<date>_<session>.md`
3. Second: Appends another block (duplicate content in file)
4. **save_chat_transcript()** later: Overwrites entire file with authoritative transcript
5. **Result**: Auto-save duplicates possible; overwritten on next explicit save

**Advantages**:
- ✅ Git recovery is sophisticated (rebase/reset/replay sequence handles drift)
- ✅ Dual paths (middleware + explicit) provide redundancy
- ✅ File locking prevents race conditions between concurrent MCP clients
- ✅ Markdown files are human-readable; Git history is the audit trail

**Disadvantages**:
- ⚠️ No transactional guarantee for single file writes
- ⚠️ No built-in deduplication for auto-save blocks
- ⚠️ Git recovery is complex; error messages may confuse users

---

## 4. Concurrency & Multi-User Support

### Chat-Save: SQLite Serialization + Atomic Claims

**Concurrency Model**:
```
Multiple capture agents (different users)
    ↓
All write to same remote MCP server
    ↓
Each MCP call includes CHATSAVE_USER header
    ↓
SQLite lock (single connection, serialized)
    ↓
Atomic claim: SELECT ... FOR UPDATE ... WHERE status='pending'
```

**Multi-User Handling**:
- User identity: `CHATSAVE_USER` environment variable (one per agent)
- Namespace: `raw_queries/<user>/claude/...` (directory per user)
- SQLite: Global shared database; no per-user isolation at DB level
- MCP server: Token-protected; `CHATSAVE_USER` tells server which user this is

**Race Conditions**:
- ✅ **Protected**: Outbox atomic claim prevents duplicate work
- ✅ **Protected**: SQLite serialization prevents concurrent writes to same conversation
- ⚠️ **Not protected**: Two users' captures of the same conversation ID (unlikely in practice)

---

### Claude Notes Vault: Per-File Mutexes + Context Variables

**Concurrency Model**:
```
Multiple MCP clients (different Claude sessions, different users)
    ↓
_IdentityMiddleware: Extract user from URL secret
    ↓
Store user in context var: _current_user (contextvars)
    ↓
Each tool call runs with that context
    ↓
When writing file: Acquire per-file lock
    ↓
Lock is shared by all threads accessing that file
    ↓
Write + commit + push
```

**Multi-User Handling**:
- User identity: Extracted from URL path secret during SSE handshake (leg 1)
- Context var: `_current_user` set for duration of tool call
- Session tracking: `_session_users` dict maps session_id → username (for leg 2 of SSE)
- Namespace: Frontmatter includes `user` field; filename prefix includes `<user>_`
- File naming: `<user>_<date>_<thread>.md` (thread name can differ between users)

**Race Conditions**:
- ✅ **Protected**: Per-file mutex serializes writes to same file
- ✅ **Protected**: Context var prevents cross-user contamination
- ✅ **Protected**: SSE session tracking ensures identity is known on tool calls
- ⚠️ **Not protected**: Two users writing different files simultaneously (allowed; no global lock)

---

## 5. Deduplication & Idempotency

### Chat-Save: Content-Hash Deduplication

**Mechanism**:
```python
content_hash = hashlib.sha256(text.encode()).hexdigest()
INSERT INTO messages (conversation_id, external_message_id, content, content_hash, ...)
  ON CONFLICT(conversation_id, external_message_id) 
  DO UPDATE SET content_hash = excluded.content_hash
```

**Deduplication Semantics**:
- Same `external_message_id` + same content = **No outbox entry enqueued**
- Same `external_message_id` + different content = **Content mutation detected; outbox entry enqueued**
- Different `external_message_id` = **New message; outbox entry enqueued**

**Query to Check**:
```sql
SELECT * FROM messages WHERE conversation_id = '...' AND content_hash = '...' AND role = 'assistant';
```

**Advantages**:
- ✅ Automatic deduplication; caller doesn't need to track anything
- ✅ Mutation tracking: content_hash change is detectable
- ✅ Silent: Duplicate sends are not errors; they're idempotent

---

### Claude Notes Vault: Session + Middleware Deduplication

**Mechanism**:
```
Auto-save middleware:
  _auto_save_turn(user, session_id, raw_body)
  ↓
  Extract text blocks from MCP response
  ↓
  Find most recent file for user+date (session-agnostic)
  ↓
  Append timestamped block
  
Explicit save_chat_transcript():
  _chat_transcript_path(thread_name)
  ↓
  Reuse file if updated today
  ↓
  OVERWRITE with full transcript
```

**Deduplication Semantics**:
- Auto-save: **Appends** blocks; duplicates = duplicate blocks in file
- Explicit save: **Overwrites** file; duplicates = ignored (earlier content replaced)
- Result: **Two-phase dedup** (auto-save not idempotent; explicit save overwrites)

**Query to Check**:
```bash
# List all saved transcripts for a user
ls raw/claude-chat-queries/<user>_*.md
# Check for duplicates within a file
grep -n "^###" <file>.md | tail -5  # see recent blocks
```

**Advantages**:
- ✅ Auto-save is automatic (no setup needed)
- ✅ Explicit save is authoritative (overwrites, so duplicates don't matter)

**Disadvantages**:
- ⚠️ Auto-save appends are not idempotent; duplicate middleware calls = duplicate blocks
- ⚠️ No content hashing; mutation detection is manual (read the Markdown)

---

## 6. Operational Characteristics

### Chat-Save: Observable Queue

**Monitoring**:
```bash
# Pending work
curl http://localhost:8000/status?key=<token>
# Output: {pending: 5, processing: 0, completed: 123, failed: 2}

# Stuck items
SELECT * FROM capture.db
  WHERE status = 'failed' 
  ORDER BY next_attempt_at DESC;

# Upcoming retries
SELECT id, conversation_id, next_attempt_at, last_error 
  FROM outbox 
  WHERE status IN ('failed', 'pending') 
  ORDER BY next_attempt_at;
```

**Debugging**:
- ✅ Query SQLite to see exact state
- ✅ Logs show backoff timing and error details
- ✅ Manual `/reconcile` endpoint to force re-scan

**Deployment**:
- Capture agent: Your PC (Python + SQLite)
- MCP server: Remote (Render or self-hosted)
- Config: `.env` with `CHATSAVE_MCP_URL`, `CHATSAVE_USER`, `MCP_AUTH_TOKEN`

---

### Claude Notes Vault: Git History as Audit Trail

**Monitoring**:
```bash
# Recent saves
git log --oneline raw/claude-chat-queries/ | head -20

# Failed pushes (from Render logs)
# grep "git commit succeeded locally but push failed"

# Check if save happened
ls -lt raw/claude-chat-queries/<user>_*.md | head -5
```

**Debugging**:
- ✅ Read Markdown files directly (human-readable)
- ✅ Git history shows exact content of each save
- ⚠️ No queue state to inspect (no "pending" concept)
- ⚠️ Hard to debug if save was skipped (no log trail unless MCP calls are logged)

**Deployment**:
- Single MCP server: Remote (Render)
- No separate capture agent
- Config: `.env` with `GITHUB_TOKEN`, `OV2_GITHUB_TOKEN`, `CLAUDE_OV_USERS` (JSON)

---

## 7. Capture Scope & Integration

### Chat-Save: What Can Be Captured?

| Source | Can Capture? | How |
|--------|---|---|
| Claude Code `.claude/projects` | ✅ Yes | File polling + stop hook |
| Claude Desktop chat tab | ❌ No | Server-side; not readable locally |
| claude.ai web | ❌ No | Server-side; not readable locally |
| Slack Claude Tag | ❌ No | Would need separate Slack API integration |
| Anthropic API direct calls | ❌ No | No local source |

**Key Limitation**: Only Claude Code's local project files are accessible for polling.

---

### Claude Notes Vault: What Can Be Captured?

| Source | Can Capture? | How |
|--------|---|---|
| Claude Code MCP tool calls | ✅ Yes | MCP server; middleware auto-save |
| Claude Desktop MCP tool calls | ✅ Yes | MCP server; same middleware |
| claude.ai web MCP tool calls | ✅ Yes | MCP server; same middleware |
| Direct `save_chat_transcript()` call | ✅ Yes | Explicit MCP call |
| Slack Claude Tag | ✅ Yes | If Claude Tag is connected to this MCP |
| Anthropic API direct calls | ⚠️ Partial | If API client calls MCP (out of band) |

**Key Advantage**: Works for all Claude interfaces; just needs MCP integration.

---

## 8. Decision Framework

### Use Chat-Save If:

- ✅ You primarily use **Claude Code** (local sessions)
- ✅ You want **guaranteed zero data loss** (durable queue)
- ✅ You need **automatic capture** without LLM involvement
- ✅ You want **observable queue state** and backoff diagnostics
- ✅ You're comfortable running **local capture agent** on your PC
- ✅ You need **deduplication** and **mutation tracking**

**Trade-off**: Higher complexity (SQLite + worker); single capture source (Claude Code only)

---

### Use Claude Notes Vault If:

- ✅ You use **multiple Claude interfaces** (Desktop, Code, Web)
- ✅ You want **single server deployment** (no client-side agent)
- ✅ You prefer **mandatory reminder system** (prevents accidental misses)
- ✅ You want **human-readable Markdown** in Git (easy to inspect)
- ✅ You need **sophisticated Git recovery** (rebase/reset/replay)
- ✅ You have **multi-user multi-session** scenarios

**Trade-off**: Lower durability (no persistent queue); depends on LLM calling save tool

---

### Hybrid Approach:

- Use **Chat-Save for Claude Code** (local polling + durable queue)
- Use **Claude Notes Vault for Claude Desktop/Web** (MCP middleware + dual-save)
- Both push to same GitHub repo; metadata (user, date, thread) keeps them separate

---

## 9. Comparative Examples

### Example 1: GitHub Becomes Unavailable (1 hour)

**Chat-Save**:
1. Worker tries to push; GitHub API returns 503
2. Exception caught; outbox item marked `failed` with `next_attempt_at = now + 5s` (first backoff)
3. Capture agent continues capturing; queue grows (`pending` + `failed` items accumulate)
4. **After 1 hour**: GitHub recovers
5. **Next worker tick**: Retries all `failed` items (exponential backoff now at 32s+ interval)
6. Items pushed successfully; queue drained
7. **Result**: ✅ Zero data loss; items recovered and pushed; backlog visible in `/status`

**Claude Notes Vault**:
1. `save_chat_transcript()` called during outage
2. `_git_commit_and_push()` fails at `git fetch` step
3. Return error to LLM: "fetch failed: Network unreachable"
4. LLM receives error; may ask user to retry or give up
5. File is already written locally (backup exists)
6. **After 1 hour**: GitHub recovers
7. **Next save**: LLM is prompted to retry by reminder; next save succeeds
8. **Result**: ⚠️ May lose the failed save if LLM gives up; recovery depends on LLM retrying

---

### Example 2: LLM Forgets to Call save_chat_transcript()

**Chat-Save**:
1. Capture agent polls Claude Code files every ~10s
2. Detects new messages via file signature (mtime:size)
3. Parses conversation; enqueues to SQLite automatically
4. Worker background thread pushes to GitHub
5. **Result**: ✅ Conversation saved automatically; LLM involvement not required

**Claude Notes Vault**:
1. LLM doesn't call `save_chat_transcript()`
2. Middleware auto-save still captures tool responses (backup)
3. BUT: Backup is incomplete (only LLM responses, not full transcript)
4. LLM reminder is injected into every tool response: "MUST call save_chat_transcript"
5. **If LLM still forgets**: Backup exists but incomplete
6. **Result**: ⚠️ Partial capture via auto-save; full capture depends on LLM remembering

---

### Example 3: Process Crashes

**Chat-Save**:
1. Agent crashes while processing outbox item (in `processing` state)
2. SQLite transaction not committed
3. **On restart**: `recover()` runs; `UPDATE outbox SET status='pending' WHERE status='processing'`
4. Item is retried on next cycle
5. **Result**: ✅ Crash-safe; zero data loss

**Claude Notes Vault**:
1. MCP server crashes during `_git_commit_and_push()`
2. Markdown file may be partially written (no transaction boundary)
3. **On restart**: MCP server restarts; new MCP clients reconnect
4. **Next save**: LLM calls `save_chat_transcript()` with fresh content
5. Overwrite replaces any corrupted partial file
6. **Result**: ⚠️ Single writes not crash-safe; overwrite on next save fixes it

---

## 10. Summary Table

| Criterion | Chat-Save | Claude Notes Vault |
|-----------|-----------|-------------------|
| **Data source** | Local file polling | Remote MCP server |
| **Capture scope** | Claude Code only | All Claude interfaces |
| **Capture trigger** | Automatic (no LLM needed) | Explicit + middleware auto-save |
| **Durability** | ACID queue + backoff | Middleware redundancy + Git recovery |
| **Idempotency** | Automatic via content hash | Manual; explicit save overwrites |
| **Crash safety** | Transactional; automatic recovery | Non-transactional; overwrite on retry |
| **Observable state** | Queue status queryable | Git history only |
| **Multi-user support** | Via env var per agent | Via URL secrets + context vars |
| **Operational complexity** | Medium (SQLite + worker) | Low (single MCP server) |
| **Git push reliability** | Simple (no conflict recovery) | Sophisticated (rebase/reset/replay) |
| **Deployment footprint** | Local agent + remote server | Single remote server |

---

## Conclusion

**Chat-Save** is optimized for **reliability and automation**: it never loses data (durable queue) and never forgets to save (automatic polling). Cost: operational complexity and limited to Claude Code.

**Claude Notes Vault** is optimized for **simplicity and scope**: single server, all Claude interfaces, sophisticated Git recovery. Cost: depends on LLM following explicit save instructions (mitigated by mandatory reminder system).

Neither is strictly "better"—choose based on your constraints:
- **Constraint: "No data loss"** → Chat-Save (durable queue)
- **Constraint: "All Claude interfaces"** → Claude Notes Vault (MCP middleware)
- **Constraint: "Minimal deployment"** → Claude Notes Vault (single server)
- **Constraint: "Automatic, no LLM involvement"** → Chat-Save (polling)

