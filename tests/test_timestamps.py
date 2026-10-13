"""Timestamps: the archive shows when things were said (Claude's times), not when they were saved."""
from app import gitstore, state
from app.models import ExtensionIngestPayload, Message, Conversation


def _conv(**kw):
    return Conversation(
        id="c1",
        title="Hello",
        platform="claude",
        created_at="2026-10-12T13:00:00Z",
        updated_at="2026-10-12T15:00:00Z",
        messages=[
            Message(id="c1_msg_1_user", role="user", content="hi from phone",
                    timestamp="2026-10-12T14:05:00Z"),
            Message(id="c1_msg_2_assistant", role="assistant", content="hello",
                    timestamp="2026-10-12T14:06:00Z"),
        ],
        **kw,
    )


def test_each_turn_shows_its_own_claude_time(monkeypatch):
    monkeypatch.setattr(gitstore, "USERNAME", "alex")
    text = gitstore.render(_conv())
    # 14:05 UTC is 10:05 EDT in October.
    assert "## User (2026-10-12 10:05:00 EDT)" in text
    assert "## Claude (2026-10-12 10:06:00 EDT)" in text


def test_header_shows_claude_last_activity_not_save_time(monkeypatch):
    monkeypatch.setattr(gitstore, "USERNAME", "alex")
    text = gitstore.render(_conv())
    assert 'updated_at: "2026-10-12 11:00:00 EDT"' in text  # 15:00 UTC
    assert 'created_at: "2026-10-12 09:00:00 EDT"' in text  # 13:00 UTC


def test_turn_without_time_falls_back_to_conversation_time_not_now(monkeypatch):
    monkeypatch.setattr(gitstore, "USERNAME", "alex")
    conv = _conv()
    conv.messages[0].timestamp = None
    text = gitstore.render(conv)
    assert "## User (2026-10-12 11:00:00 EDT)" in text


def test_ingest_keeps_claude_created_and_updated_times(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "STATE_DB", tmp_path / "capture.db")
    monkeypatch.setattr(state, "STORAGE", tmp_path)
    monkeypatch.setattr(state, "_db_initialized", False)
    payload = ExtensionIngestPayload(
        conversation_id="c9",
        title="T",
        messages=[Message(id="c9_msg_1_user", role="user", content="x",
                          timestamp="2026-10-12T14:05:00Z")],
        captured_at="2026-10-12T15:00:00Z",   # Claude's updated time from cloud sync
        created_at="2026-10-12T13:00:00Z",    # Claude's created time
        source="reconcile",
    )
    state.ingest_extension(payload, effective_user="alex")
    conv = state.get_canonical_conversation("c9")
    assert conv.updated_at == "2026-10-12T15:00:00Z"
    assert conv.created_at == "2026-10-12T13:00:00Z"
    assert conv.messages[0].timestamp == "2026-10-12T14:05:00Z"


def test_corrected_time_on_existing_turn_is_saved(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "STATE_DB", tmp_path / "capture.db")
    monkeypatch.setattr(state, "STORAGE", tmp_path)
    monkeypatch.setattr(state, "_db_initialized", False)

    def send(ts):
        return ExtensionIngestPayload(
            conversation_id="c7", title="T",
            messages=[Message(id="c7_msg_1_user", role="user", content="same text", timestamp=ts)],
            captured_at="2026-10-12T15:00:00Z", source="reconcile",
        )

    state.ingest_extension(send(None), effective_user="alex")       # first save: no time
    receipt = state.ingest_extension(send("2026-10-12T14:05:00Z"), effective_user="alex")  # same text, now with time
    conv = state.get_canonical_conversation("c7")
    assert conv.messages[0].timestamp == "2026-10-12T14:05:00Z"
    assert receipt["status"] == "persisted", "a corrected time must count as a change"
