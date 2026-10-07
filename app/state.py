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
from typing import Optional

from .config import STATE_DB, STORAGE, USERNAME
from .models import Conversation, Message

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
  status TEXT DEFAULT 'active'
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
"""


@contextmanager
def conn():
    STORAGE.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(STATE_DB, timeout=30)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
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

        # 1. Upsert conversation
        c.execute(
            """
            INSERT INTO conversations (id, platform, external_conversation_id, user_id, title, created_at, updated_at, last_message_sequence, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                updated_at = excluded.updated_at,
                last_message_sequence = excluded.last_message_sequence,
                user_id = excluded.user_id
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
                conv.status or "active"
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
                    content = excluded.content,
                    content_hash = excluded.content_hash,
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
            messages=msgs
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
    with conn() as c:
        for i in ids:
            row = c.execute("SELECT attempts FROM outbox WHERE id=?", (i,)).fetchone()
            attempts = (row["attempts"] if row else 0) + 1
            backoff = min(600, 5 * (2 ** attempts))
            c.execute(
                "UPDATE outbox SET status='pending', attempts=?, last_error=?, next_attempt_at=? WHERE id=?",
                (attempts, error[:500], time.time() + backoff, i)
            )


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
    return {
        "outbox": counts,
        "conversations": total_convs,
        "messages": total_msgs,
        "errors": errs
    }


def get_sig(source: str, key: str) -> str | None:
    with conn() as c:
        r = c.execute("SELECT sig FROM source_state WHERE source=? AND key=?", (source, key)).fetchone()
        return r["sig"] if r else None


def set_sig(source: str, key: str, sig: str) -> None:
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO source_state VALUES (?,?,?)", (source, key, sig))
