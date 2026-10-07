# Automatic Claude Desktop Thread Saving: Architecture & Implementation

A production-grade, zero-LLM-dependent transcript capture and git-archival system.

---

## 1. Core Principle: Removing the LLM from the Critical Path

The fundamental architectural principle of this system is:
```text
Conversation event occurred (Host/Local Data Layer)
        ↓
Automatically capture & persist transactionally (SQLite)
        ↓
Outbox Worker drains to GitHub
```
**NOT**:
```text
LLM decides whether to call a save tool (Probabilistic & Fragile)
```

---

## 2. Layered Architecture

```text
                         CLAUDE DESKTOP / CLIENT
                                    │
                                    │ Local data events / session logs
                                    ▼
                    ┌───────────────────────────────┐
                    │    Capture & Adapter Layer    │
                    │   (app/sources/ & capture.py) │
                    │   • Claude Desktop Watcher    │
                    │   • Claude Code CLI Watcher   │
                    │   • REST Lifecycle Hooks      │
                    └───────────────┬───────────────┘
                                    │ Canonical Event
                                    ▼
                    ┌───────────────────────────────┐
                    │   Transactional SQLite Store  │
                    │         (app/state.py)        │
                    │   • conversations             │
                    │   • messages (deduplicated)   │
                    │   • outbox (PENDING queue)    │
                    └───────────────┬───────────────┘
                                    │ Atomic Outbox Claim
                                    ▼
                    ┌───────────────────────────────┐
                    │  Background Outbox Worker     │
                    │        (app/outbox.py)        │
                    │   • Exponential Backoff       │
                    │   • Deterministic Markdown    │
                    │   • Serialized Git Sync       │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │          GitHub Repo          │
                    │ raw_queries/<user>/claude/    │
                    │        <title-slug>.md        │
                    └───────────────────────────────┘

                    ┌───────────────────────────────┐
                    │     MCP Integration Layer     │
                    │      (app/mcp_server.py)      │
                    │   • Status & Inspection       │
                    │   • Search / Read Transcripts │
                    │   • Manual Fallback           │
                    └───────────────────────────────┘
```

---

## 3. Canonical SQLite Data Model

### 1. `conversations` Table
Tracks high-level thread metadata, ownership, and current state.
* `id` (TEXT PRIMARY KEY)
* `platform` (TEXT)
* `external_conversation_id` (TEXT)
* `user_id` (TEXT)
* `title` (TEXT)
* `created_at` (TEXT)
* `updated_at` (TEXT)
* `last_message_sequence` (INTEGER)
* `status` (TEXT)

### 2. `messages` Table
Immutable message records with strict deduplication constraints.
* `id` (TEXT PRIMARY KEY)
* `conversation_id` (TEXT REFERENCES conversations)
* `external_message_id` (TEXT)
* `sequence` (INTEGER)
* `role` (TEXT)
* `content` (TEXT)
* `created_at` (TEXT)
* `content_hash` (TEXT)
* **Constraint**: `UNIQUE(conversation_id, external_message_id)`

### 3. `outbox` Table
Durable transactional queue ensuring zero data loss across restarts or GitHub downtime.
* `id` (INTEGER PRIMARY KEY)
* `event_type` (TEXT)
* `conversation_id` (TEXT)
* `content_hash` (TEXT)
* `payload` (TEXT)
* `status` (`pending`, `processing`, `completed`, `failed`)
* `attempts` (INTEGER)
* `last_error` (TEXT)
* `next_attempt_at` (REAL)
* `created_at` / `completed_at` (REAL)

---

## 4. Atomic Transactional Persistence

Every captured message is written within a single database transaction:
```sql
BEGIN TRANSACTION;
  INSERT/UPDATE conversations ...;
  INSERT INTO messages ... ON CONFLICT(conversation_id, external_message_id) DO UPDATE ...;
  INSERT INTO outbox (status = 'pending') ...;
COMMIT;
```
If a crash occurs before `COMMIT`, SQLite rolls back cleanly. No partially written records or orphaned outbox events can exist.

---

## 5. Startup Recovery & Background Reconciliation

1. **Crash Recovery (`state.recover()`)**:
   On process startup, any outbox events left in `processing` state from an abrupt shutdown are immediately reset to `pending`.
2. **Deterministic Periodic Reconciler**:
   Every `RECONCILE_SECONDS` (default: 10s), the background controller scans source storage directories, detects modified files via change signatures (`mtime:size`), parses new turns, and transactionally enqueues them into SQLite.
3. **Outbox Drain Loop**:
   The worker claims batches of `pending` items, reconstructs canonical conversations from SQLite, materializes Markdown, and pushes to Git. If GitHub is unreachable, records remain in the outbox with exponential backoff retry.
