import sqlite3
from contextlib import contextmanager

from .config import DB_PATH, STORAGE
from .models import Conversation

SCHEMA = """
CREATE TABLE IF NOT EXISTS threads (
  platform TEXT NOT NULL, thread_id TEXT NOT NULL, username TEXT, title TEXT,
  created_at TEXT, updated_at TEXT, git_path TEXT, content_hash TEXT,
  PRIMARY KEY (platform, thread_id)
);
CREATE TABLE IF NOT EXISTS messages (
  platform TEXT NOT NULL, thread_id TEXT NOT NULL, message_id TEXT NOT NULL,
  position INTEGER, role TEXT, content TEXT, timestamp TEXT,
  PRIMARY KEY (platform, thread_id, message_id)
);
CREATE VIRTUAL TABLE IF NOT EXISTS search USING fts5(
  platform UNINDEXED, thread_id UNINDEXED, title, body
);
"""


@contextmanager
def conn():
    STORAGE.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    try:
        yield c
        c.commit()
    finally:
        c.close()


def get_hash(platform: str, thread_id: str) -> str | None:
    with conn() as c:
        r = c.execute("SELECT content_hash FROM threads WHERE platform=? AND thread_id=?",
                      (platform, thread_id)).fetchone()
        return r["content_hash"] if r else None


def upsert(conv: Conversation, content_hash: str, git_path: str) -> None:
    p, t = conv.platform, conv.id
    with conn() as c:
        c.execute("INSERT OR REPLACE INTO threads VALUES (?,?,?,?,?,?,?,?)",
                  (p, t, conv.username, conv.title, conv.created_at, conv.updated_at,
                   git_path, content_hash))
        c.execute("DELETE FROM messages WHERE platform=? AND thread_id=?", (p, t))
        c.executemany("INSERT OR REPLACE INTO messages VALUES (?,?,?,?,?,?,?)",
                      [(p, t, m.id, i, m.role, m.content, m.timestamp)
                       for i, m in enumerate(conv.messages)])
        c.execute("DELETE FROM search WHERE platform=? AND thread_id=?", (p, t))
        c.execute("INSERT INTO search VALUES (?,?,?,?)",
                  (p, t, conv.title, "\n".join(m.content for m in conv.messages)))


def list_threads(platform: str | None, username: str | None, limit: int) -> list[dict]:
    q, a = "SELECT platform,thread_id,title,username,updated_at FROM threads WHERE 1=1", []
    if platform and platform != "all":
        q += " AND platform=?"
        a.append(platform)
    if username:
        q += " AND username=?"
        a.append(username)
    q += " ORDER BY updated_at DESC LIMIT ?"
    a.append(limit)
    with conn() as c:
        return [dict(r) for r in c.execute(q, a)]


def search_threads(query: str, platform: str | None, username: str | None, limit: int) -> list[dict]:
    # quote each term so user input can't break FTS syntax
    fts = " ".join('"%s"' % w.replace('"', "") for w in query.split())
    if not fts:
        return []
    q = ("SELECT t.platform,t.thread_id,t.title,t.username,t.updated_at,"
         " snippet(search,3,'[',']','...',12) AS snippet"
         " FROM search JOIN threads t ON t.platform=search.platform AND t.thread_id=search.thread_id"
         " WHERE search MATCH ?")
    a: list = [fts]
    if platform and platform != "all":
        q += " AND t.platform=?"
        a.append(platform)
    if username:
        q += " AND t.username=?"
        a.append(username)
    q += " ORDER BY rank LIMIT ?"
    a.append(limit)
    with conn() as c:
        return [dict(r) for r in c.execute(q, a)]


def get_thread(platform: str, thread_id: str) -> dict | None:
    with conn() as c:
        t = c.execute("SELECT * FROM threads WHERE platform=? AND thread_id=?",
                      (platform, thread_id)).fetchone()
        if not t:
            return None
        msgs = c.execute("SELECT message_id AS id,role,content,timestamp FROM messages "
                         "WHERE platform=? AND thread_id=? ORDER BY position",
                         (platform, thread_id)).fetchall()
        return {**dict(t), "messages": [dict(m) for m in msgs]}
