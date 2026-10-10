"""SQLite canonical state & transactional outbox.

Tables:
1. conversations: metadata, titles, sequences, timestamps
2. messages: immutable individual turns, deduplicated by (platform, conversation_id, message_id) + content_hash
3. outbox: atomic event queue for GitHub materialization (pending -> processing -> completed)
4. source_state: scanner signatures for change detection
"""
import hashlib
import json
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Optional

from .config import STATE_DB, STORAGE, USERNAME
from .models import Conversation, ExtensionIngestPayload, Message

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY,
  platform TEXT NOT NULL DEFAULT 'claude',
  external_conversation_id TEXT,
  user_id TEXT NOT NULL DEFAULT 'shubham',
  title TEXT NOT NULL DEFAULT 'Untitled conversation',
  created_at TEXT,
  updated_at TEXT,
  last_message_sequence INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active',
  files TEXT DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  external_message_id TEXT NOT NULL,
  sequence INTEGER NOT NULL DEFAULT 0,
  role TEXT NOT NULL DEFAULT 'user',
  content TEXT NOT NULL,
  created_at TEXT,
  content_hash TEXT NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_messages_unique 
  ON messages(conversation_id, external_message_id);

CREATE TABLE IF NOT EXISTS outbox (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_type TEXT NOT NULL DEFAULT 'conversation.updated',
  conversation_id TEXT NOT NULL,
  message_id TEXT,
  content_hash TEXT,
  payload TEXT,
  status TEXT NOT NULL DEFAULT 'pending',
  attempts INTEGER NOT NULL DEFAULT 0,
  last_error TEXT,
  next_attempt_at REAL NOT NULL DEFAULT 0,
  created_at REAL NOT NULL,
  completed_at REAL
);

CREATE INDEX IF NOT EXISTS idx_outbox_status_due ON outbox(status, next_attempt_at);
CREATE INDEX IF NOT EXISTS idx_outbox_conv ON outbox(conversation_id, status);

CREATE TABLE IF NOT EXISTS source_state (
  source TEXT NOT NULL,
  key TEXT NOT NULL,
  sig TEXT NOT NULL,
  PRIMARY KEY (source, key)
);

CREATE TABLE IF NOT EXISTS client_heartbeats (
  client_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  extension_version TEXT,
  browser TEXT,
  pending_queue_count INTEGER DEFAULT 0,
  last_successful_sync TEXT,
  last_error TEXT,
  last_seen REAL NOT NULL
);
"""


@contextmanager
def conn():
    STORAGE.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(STATE_DB, timeout=30)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    try:
        c.execute("ALTER TABLE conversations ADD COLUMN files TEXT DEFAULT '[]'")
        c.commit()
    except Exception:
        pass
    try:
        yield c
        c.commit()
    finally:
        c.close()


def recover() -> None:
    """Startup recovery: items stuck in 'processing' are reset to 'pending'."""
    with conn() as c:
        c.execute("UPDATE outbox SET status='pending' WHERE status='processing'")


def compute_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_conversation_hash(conv: Conversation) -> str:
    h = hashlib.sha256(f"{conv.platform}\0{conv.id}\0{conv.title}".encode())
    for m in conv.messages:
        h.update(f"\0{m.id}\0{m.role}\0{m.content}".encode())
    for f in conv.files or []:
        fname = f.get("name") or f.get("path") or ""
        fcontent = str(f.get("content") or "")[:200]
        h.update(f"\0{fname}\0{fcontent}".encode())
    return h.hexdigest()


def save_conversation_atomic(conv: Conversation) -> bool:
    """Atomic transactional write:
    BEGIN
      INSERT/UPDATE conversation
      INSERT messages (deduplicated by external_message_id and content_hash)
      INSERT outbox event if conversation has changes
    COMMIT
    """
    conv_hash = compute_conversation_hash(conv)
    uname = conv.user_id or conv.username or USERNAME or "shubham"

    with conn() as c:
        # Check if identical snapshot was already queued/completed
        last_outbox = c.execute(
            "SELECT content_hash FROM outbox WHERE conversation_id=? ORDER BY id DESC LIMIT 1",
            (conv.id,)
        ).fetchone()
        if last_outbox and last_outbox["content_hash"] == conv_hash:
            return False

        files_json = json.dumps(conv.files or [])
        # 1. Upsert conversation
        c.execute(
            """
            INSERT INTO conversations (id, platform, external_conversation_id, user_id, title, created_at, updated_at, last_message_sequence, status, files)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                updated_at = excluded.updated_at,
                last_message_sequence = excluded.last_message_sequence,
                user_id = excluded.user_id,
                files = excluded.files
            """,
            (
                conv.id,
                conv.platform,
                conv.external_conversation_id or conv.id,
                uname,
                conv.title,
                conv.created_at,
                conv.updated_at,
                len(conv.messages),
                conv.status or "active",
                files_json
            )
        )

        # 2. Insert messages with deterministic sequence numbers
        for idx, m in enumerate(conv.messages, start=1):
            m_hash = m.content_hash or compute_content_hash(m.content)
            c.execute(
                """
                INSERT INTO messages (id, conversation_id, external_message_id, sequence, role, content, created_at, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(conversation_id, external_message_id) DO UPDATE SET
                    content = CASE 
                        WHEN length(excluded.content) >= length(messages.content) THEN excluded.content
                        ELSE messages.content
                    END,
                    content_hash = CASE 
                        WHEN length(excluded.content) >= length(messages.content) THEN excluded.content_hash
                        ELSE messages.content_hash
                    END,
                    sequence = excluded.sequence
                """,
                (
                    f"{conv.id}_{m.id}",
                    conv.id,
                    m.id,
                    idx,
                    m.role,
                    m.content,
                    m.timestamp,
                    m_hash
                )
            )

        # 3. Supercede any pending outbox records for this conversation with the newest state
        c.execute("DELETE FROM outbox WHERE conversation_id=? AND status='pending'", (conv.id,))
        
        # 4. Insert atomic outbox record
        c.execute(
            """
            INSERT INTO outbox (event_type, conversation_id, content_hash, payload, status, created_at)
            VALUES (?, ?, ?, ?, 'pending', ?)
            """,
            (
                "conversation.updated",
                conv.id,
                conv_hash,
                conv.model_dump_json(),
                time.time()
            )
        )
        return True


def get_canonical_conversation(conversation_id: str) -> Optional[Conversation]:
    """Reconstruct complete deterministic conversation state from SQLite."""
    with conn() as c:
        row = c.execute("SELECT * FROM conversations WHERE id=?", (conversation_id,)).fetchone()
        if not row:
            return None
        
        msg_rows = c.execute(
            "SELECT * FROM messages WHERE conversation_id=? ORDER BY sequence ASC",
            (conversation_id,)
        ).fetchall()
        
        msgs = [
            Message(
                id=r["external_message_id"],
                conversation_id=r["conversation_id"],
                sequence=r["sequence"],
                role=r["role"],
                content=r["content"],
                timestamp=r["created_at"],
                content_hash=r["content_hash"]
            )
            for r in msg_rows
        ]

        raw_files = row["files"] if "files" in row.keys() else "[]"
        try:
            conv_files = json.loads(raw_files or "[]")
        except Exception:
            conv_files = []

        return Conversation(
            id=row["id"],
            platform=row["platform"],
            external_conversation_id=row["external_conversation_id"],
            user_id=row["user_id"],
            username=row["user_id"],
            title=row["title"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            last_message_sequence=row["last_message_sequence"],
            status=row["status"],
            messages=msgs,
            files=conv_files
        )


def claim(limit: int) -> list[tuple[int, Conversation]]:
    """Claim pending outbox batches for the worker."""
    with conn() as c:
        rows = c.execute(
            "SELECT id, payload, conversation_id FROM outbox WHERE status='pending' "
            "AND next_attempt_at<=? ORDER BY id LIMIT ?",
            (time.time(), limit)
        ).fetchall()
        if not rows:
            return []
        
        ids = [r["id"] for r in rows]
        c.execute(f"UPDATE outbox SET status='processing' WHERE id IN ({','.join('?' * len(ids))})", ids)
        
        result = []
        for r in rows:
            # Prefer reconstructing canonical state directly from SQLite
            canonical = get_canonical_conversation(r["conversation_id"])
            if canonical:
                result.append((r["id"], canonical))
            elif r["payload"]:
                result.append((r["id"], Conversation.model_validate(json.loads(r["payload"]))))
        return result


def complete(ids: list[int]) -> None:
    with conn() as c:
        c.executemany(
            "UPDATE outbox SET status='completed', payload=NULL, last_error=NULL, completed_at=? WHERE id=?",
            [(time.time(), i) for i in ids]
        )


def fail(ids: list[int], error: str) -> None:
    MAX_ATTEMPTS = 10
    with conn() as c:
        for i in ids:
            row = c.execute("SELECT attempts FROM outbox WHERE id=?", (i,)).fetchone()
            attempts = (row["attempts"] if row else 0) + 1
            if attempts >= MAX_ATTEMPTS:
                # Dead Letter Queue: exceeded max retry attempts
                c.execute(
                    "UPDATE outbox SET status='dead_letter', attempts=?, last_error=?, completed_at=? WHERE id=?",
                    (attempts, f"DLQ: {error[:400]}", time.time(), i)
                )
            else:
                backoff = min(600, 5 * (2 ** attempts))
                c.execute(
                    "UPDATE outbox SET status='pending', attempts=?, last_error=?, next_attempt_at=? WHERE id=?",
                    (attempts, error[:500], time.time() + backoff, i)
                )


def retry_dead_letter() -> int:
    """Reset all dead_letter outbox items back to pending for retry."""
    with conn() as c:
        cur = c.cursor()
        cur.execute(
            "UPDATE outbox SET status='pending', attempts=0, next_attempt_at=0 WHERE status='dead_letter'"
        )
        return cur.rowcount


def stats() -> dict:
    with conn() as c:
        counts = {r["status"]: r["n"] for r in c.execute("SELECT status, COUNT(*) n FROM outbox GROUP BY status")}
        total_convs = c.execute("SELECT COUNT(*) n FROM conversations").fetchone()["n"]
        total_msgs = c.execute("SELECT COUNT(*) n FROM messages").fetchone()["n"]
        errs = [
            dict(r) for r in c.execute(
                "SELECT conversation_id, attempts, last_error FROM outbox "
                "WHERE last_error IS NOT NULL AND status!='completed' LIMIT 10"
            )
        ]
        clients = [
            dict(r) for r in c.execute(
                "SELECT client_id, user_id, extension_version, browser, pending_queue_count, last_successful_sync, last_error, last_seen "
                "FROM client_heartbeats ORDER BY last_seen DESC LIMIT 25"
            )
        ]
    return {
        "outbox": counts,
        "conversations": total_convs,
        "messages": total_msgs,
        "errors": errs,
        "extension_clients": clients
    }


def record_heartbeat(
    client_id: str,
    user_id: str,
    extension_version: str = "1.0.0",
    browser: str = "Chrome",
    pending_queue_count: int = 0,
    last_successful_sync: Optional[str] = None,
    last_error: Optional[str] = None,
) -> None:
    """Record health and connection status from a managed browser extension."""
    with conn() as c:
        c.execute(
            """
            INSERT INTO client_heartbeats (
                client_id, user_id, extension_version, browser, pending_queue_count,
                last_successful_sync, last_error, last_seen
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(client_id) DO UPDATE SET
                user_id = excluded.user_id,
                extension_version = excluded.extension_version,
                browser = excluded.browser,
                pending_queue_count = excluded.pending_queue_count,
                last_successful_sync = COALESCE(excluded.last_successful_sync, client_heartbeats.last_successful_sync),
                last_error = excluded.last_error,
                last_seen = excluded.last_seen
            """,
            (
                client_id,
                user_id,
                extension_version,
                browser,
                pending_queue_count,
                last_successful_sync,
                last_error,
                time.time()
            )
        )


def get_heartbeats() -> list[dict]:
    """Retrieve all reporting extension clients."""
    with conn() as c:
        rows = c.execute(
            "SELECT * FROM client_heartbeats ORDER BY last_seen DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def ingest_extension(payload: ExtensionIngestPayload, effective_user: str) -> dict:
    """Ingest a conversation turn or snapshot captured by the browser extension.
    
    Guarantees:
    - Atomically updates conversations and messages tables.
    - Prevents duplicates via content hash and message identity checks.
    - Queues an outbox event for Git archival only if content actually changed.
    - Updates client heartbeat metrics with last sync receipt.
    """
    user = payload.user_id or effective_user or USERNAME or "shubham"
    now_str = datetime.now().isoformat()
    
    # 1. Sanitize incoming messages: strictly filter out empty messages
    valid_incoming = [m for m in (payload.messages or []) if m.content and m.content.strip()]
    existing = get_canonical_conversation(payload.conversation_id)

    if not valid_incoming and not existing:
        return {
            "receipt_id": "rcpt_empty",
            "conversation_id": payload.conversation_id,
            "saved_messages": 0,
            "status": "ignored_empty",
            "deduplicated": True,
            "timestamp": now_str
        }

    messages_to_save: list[Message] = []
    if existing and valid_incoming:
        # Merge existing conversation history with incoming turns to guarantee ZERO data loss
        existing_by_id = {m.id: m for m in existing.messages if m.content and m.content.strip()}
        existing_by_seq = {m.sequence: m for m in existing.messages if m.content and m.content.strip()}

        # Protect against message trimming: if an earlier version of a turn has longer text, preserve it!
        for inc_idx, inc_m in enumerate(valid_incoming, start=1):
            prior_m = existing_by_id.get(inc_m.id) or existing_by_seq.get(inc_idx)
            if prior_m and prior_m.role == inc_m.role:
                if len(prior_m.content.strip()) > len(inc_m.content.strip()):
                    inc_m.content = prior_m.content
                if prior_m.timestamp and not inc_m.timestamp:
                    inc_m.timestamp = prior_m.timestamp

        if len(valid_incoming) >= len(existing.messages):
            # Incoming has full turn set: use incoming with preserved complete contents
            messages_to_save = valid_incoming
        else:
            # Incoming only has partial turns (older turns were scrolled/virtualized):
            # Merge onto existing messages so older turns are never dropped
            merged = {m.id: m for m in existing.messages if m.content and m.content.strip()}
            for inc_m in valid_incoming:
                merged[inc_m.id] = inc_m
            messages_to_save = list(merged.values())
    elif valid_incoming:
        # Full snapshot
        messages_to_save = valid_incoming
    elif existing:
        messages_to_save = [m for m in existing.messages if m.content and m.content.strip()]

    # Ensure sequential turn ordering and compute clean hashes
    for idx, m in enumerate(messages_to_save, start=1):
        m.content = m.content.strip()
        m.conversation_id = payload.conversation_id
        m.sequence = idx
        m.content_hash = compute_content_hash(m.content)

    # Merge existing files/attachments with incoming files
    existing_files = existing.files if existing else []
    incoming_files = payload.files or []
    files_map = {f.get("name") or f.get("path"): f for f in existing_files if (f.get("name") or f.get("path"))}
    for inc_f in incoming_files:
        k = inc_f.get("name") or inc_f.get("path")
        if k:
            if k in files_map and len(str(files_map[k].get("content", ""))) > len(str(inc_f.get("content", ""))):
                continue
            files_map[k] = inc_f
    merged_files = list(files_map.values())

    conv = Conversation(
        id=payload.conversation_id,
        platform=payload.platform,
        external_conversation_id=payload.conversation_id,
        user_id=user,
        username=user,
        title=payload.title or (existing.title if existing else "Untitled conversation"),
        created_at=existing.created_at if existing and existing.created_at else (payload.captured_at or now_str),
        updated_at=now_str,
        status="active",
        messages=messages_to_save,
        files=merged_files
    )

    persisted = save_conversation_atomic(conv)

    # 2. Record heartbeat/receipt for this client
    if payload.client_id:
        record_heartbeat(
            client_id=payload.client_id,
            user_id=user,
            last_successful_sync=now_str,
            last_error=None,
            pending_queue_count=0
        )

    receipt_hash = hashlib.sha256(f"{conv.id}:{time.time()}:{len(conv.messages)}".encode()).hexdigest()[:16]
    return {
        "receipt_id": f"rcpt_{receipt_hash}",
        "conversation_id": conv.id,
        "saved_messages": len(conv.messages),
        "status": "persisted" if persisted else "unchanged",
        "deduplicated": not persisted,
        "timestamp": now_str
    }


def get_sig(source: str, key: str) -> str | None:
    with conn() as c:
        r = c.execute("SELECT sig FROM source_state WHERE source=? AND key=?", (source, key)).fetchone()
        return r["sig"] if r else None


def set_sig(source: str, key: str, sig: str) -> None:
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO source_state VALUES (?,?,?)", (source, key, sig))
