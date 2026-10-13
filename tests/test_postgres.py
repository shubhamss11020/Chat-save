"""PostgreSQL backend tests. Skipped unless a test database URL is given:

    set CHATSAVE_TEST_DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
    pytest tests/test_postgres.py

The tests only touch rows whose ids start with "pgtest-" and remove them afterwards.
"""
import os

import pytest

from app import state
from app.models import Conversation, Message

URL = os.getenv("CHATSAVE_TEST_DATABASE_URL", "")
pytestmark = pytest.mark.skipif(not URL, reason="set CHATSAVE_TEST_DATABASE_URL to run PostgreSQL tests")


@pytest.fixture
def pg(monkeypatch):
    monkeypatch.setattr(state, "DATABASE_URL", URL)
    monkeypatch.setattr(state, "_db_initialized", False)
    monkeypatch.setattr(state, "_pg_pool", None)
    state._init_db()
    yield
    with state.conn() as c:
        c.execute("DELETE FROM outbox WHERE conversation_id LIKE 'pgtest-%'")
        c.execute("DELETE FROM messages WHERE conversation_id LIKE 'pgtest-%'")
        c.execute("DELETE FROM conversations WHERE id LIKE 'pgtest-%'")
        c.execute("DELETE FROM source_state WHERE source = 'pgtest'")
    if state._pg_pool is not None:
        state._pg_pool.close()


def _conv(name):
    return Conversation(
        id=f"pgtest-{name}", title=f"PG {name}", platform="claude", username="alex",
        created_at="2026-10-13T10:00:00Z", updated_at="2026-10-13T10:05:00Z",
        messages=[Message(id=f"pgtest-{name}_m1", role="user", content="hello",
                          timestamp="2026-10-13T10:00:00Z")],
    )


def test_save_claim_complete_roundtrip(pg):
    c = _conv("roundtrip")
    assert state.save_conversation_atomic(c) is True
    claimed = [item for item in state.claim(50) if item[1].id == c.id]
    assert len(claimed) == 1
    state.complete([claimed[0][0]])
    back = state.get_canonical_conversation(c.id)
    assert back.messages[0].content == "hello"


def test_identical_resave_is_not_duplicated(pg):
    c = _conv("dedupe")
    assert state.save_conversation_atomic(c) is True
    assert state.save_conversation_atomic(c) is False


def test_source_state_upsert(pg):
    state.set_sig("pgtest", "k1", "one")
    state.set_sig("pgtest", "k1", "two")
    assert state.get_sig("pgtest", "k1") == "two"


def test_archive_path_roundtrip(pg):
    c = _conv("path")
    state.save_conversation_atomic(c)
    state.set_archive_path(c.id, "alex/claude/x.md")
    assert state.get_archive_path(c.id) == "alex/claude/x.md"
