"""capture.db: 'what still needs to be saved?' (git holds 'what was saved').

outbox        one row per captured snapshot: pending -> processing -> completed
source_state  last scanned signature per source thread, so scans only read changes
"""
import json
import sqlite3
import time
from contextlib import contextmanager

from .config import STATE_DB, STORAGE
from .models import Conversation

SCHEMA = """
CREATE TABLE IF NOT EXISTS outbox (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  platform TEXT NOT NULL, thread_id TEXT NOT NULL, content_hash TEXT NOT NULL,
  payload TEXT,                       -- full snapshot; cleared once completed
  status TEXT NOT NULL DEFAULT 'pending',
  attempts INTEGER NOT NULL DEFAULT 0, last_error TEXT,
  next_attempt_at REAL NOT NULL DEFAULT 0, created_at REAL NOT NULL, completed_at REAL
);
CREATE INDEX IF NOT EXISTS outbox_thread ON outbox(platform, thread_id, id);
CREATE INDEX IF NOT EXISTS outbox_due ON outbox(status, next_attempt_at);
CREATE TABLE IF NOT EXISTS source_state (
  source TEXT NOT NULL, key TEXT NOT NULL, sig TEXT NOT NULL,
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
    """After a crash, items stuck in 'processing' go back to pending."""
    with conn() as c:
        c.execute("UPDATE outbox SET status='pending' WHERE status='processing'")


def enqueue(conv: Conversation, content_hash: str) -> bool:
    """Queue a snapshot unless it matches the newest one already queued/saved."""
    with conn() as c:
        last = c.execute("SELECT content_hash FROM outbox WHERE platform=? AND thread_id=? "
                         "ORDER BY id DESC LIMIT 1", (conv.platform, conv.id)).fetchone()
        if last and last["content_hash"] == content_hash:
            return False
        # a newer snapshot supersedes any older one still waiting
        c.execute("DELETE FROM outbox WHERE platform=? AND thread_id=? AND status='pending'",
                  (conv.platform, conv.id))
        c.execute("INSERT INTO outbox(platform,thread_id,content_hash,payload,created_at) "
                  "VALUES (?,?,?,?,?)",
                  (conv.platform, conv.id, content_hash, conv.model_dump_json(), time.time()))
        return True


def claim(limit: int) -> list[tuple[int, Conversation]]:
    with conn() as c:
        rows = c.execute("SELECT id,payload FROM outbox WHERE status='pending' "
                         "AND next_attempt_at<=? ORDER BY id LIMIT ?", (time.time(), limit)).fetchall()
        if rows:
            c.execute(f"UPDATE outbox SET status='processing' WHERE id IN "
                      f"({','.join('?' * len(rows))})", [r["id"] for r in rows])
        return [(r["id"], Conversation.model_validate(json.loads(r["payload"]))) for r in rows]


def complete(ids: list[int]) -> None:
    with conn() as c:
        c.executemany("UPDATE outbox SET status='completed', payload=NULL, last_error=NULL, "
                      "completed_at=? WHERE id=?", [(time.time(), i) for i in ids])


def fail(ids: list[int], error: str) -> None:
    with conn() as c:
        for i in ids:
            n = c.execute("SELECT attempts FROM outbox WHERE id=?", (i,)).fetchone()["attempts"] + 1
            c.execute("UPDATE outbox SET status='pending', attempts=?, last_error=?, "
                      "next_attempt_at=? WHERE id=?",
                      (n, error[:500], time.time() + min(600, 5 * 2 ** n), i))


def stats() -> dict:
    with conn() as c:
        counts = {r["status"]: r["n"] for r in
                  c.execute("SELECT status, COUNT(*) n FROM outbox GROUP BY status")}
        errs = [dict(r) for r in c.execute(
            "SELECT platform,thread_id,attempts,last_error FROM outbox "
            "WHERE last_error IS NOT NULL AND status!='completed' LIMIT 10")]
    return {"outbox": counts, "errors": errs}


def get_sig(source: str, key: str) -> str | None:
    with conn() as c:
        r = c.execute("SELECT sig FROM source_state WHERE source=? AND key=?",
                      (source, key)).fetchone()
        return r["sig"] if r else None


def set_sig(source: str, key: str, sig: str) -> None:
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO source_state VALUES (?,?,?)", (source, key, sig))
