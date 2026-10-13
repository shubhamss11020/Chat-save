"""Scale-prep tests: per-user ingest limit and archive-lag monitoring."""
from app import auth, main
from app.ratelimit import SlidingWindowLimiter


def test_limiter_allows_up_to_limit_then_reports_wait():
    lim = SlidingWindowLimiter(limit=3, window_seconds=60)
    assert [lim.check("alex") for _ in range(3)] == [0.0, 0.0, 0.0]
    wait = lim.check("alex")
    assert 0 < wait <= 60


def test_limiter_is_per_user():
    lim = SlidingWindowLimiter(limit=1, window_seconds=60)
    assert lim.check("alex") == 0.0
    assert lim.check("bob") == 0.0  # bob has his own budget
    assert lim.check("alex") > 0


def test_limiter_window_resets(monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr("app.ratelimit.time.monotonic", lambda: clock[0])
    lim = SlidingWindowLimiter(limit=1, window_seconds=60)
    assert lim.check("alex") == 0.0
    assert lim.check("alex") > 0
    clock[0] += 61
    assert lim.check("alex") == 0.0


def test_zero_limit_means_unlimited():
    lim = SlidingWindowLimiter(limit=0)
    assert all(lim.check("alex") == 0.0 for _ in range(1000))


def _open_auth(monkeypatch):
    monkeypatch.setattr(auth, "AUTH_TOKEN", "")
    monkeypatch.setattr(auth, "USER_TOKENS_MAP", {})
    monkeypatch.setattr(auth, "ALLOW_OPEN", True)


def test_ingest_route_returns_429_with_retry_after(monkeypatch):
    from fastapi.testclient import TestClient
    from app import state
    _open_auth(monkeypatch)
    monkeypatch.setattr(main, "ingest_limiter", SlidingWindowLimiter(limit=1, window_seconds=60))
    monkeypatch.setattr(state, "ingest_extension", lambda payload, effective_user: {
        "receipt_id": "r", "conversation_id": payload.conversation_id, "saved_messages": 0,
        "status": "persisted", "deduplicated": False, "timestamp": "t"})
    monkeypatch.setattr(main.outbox, "drain", lambda: 0)

    client = TestClient(main.app)
    body = {"conversation_id": "c1", "messages": []}
    first = client.post("/api/extension/ingest", json=body, headers={"X-Test": "1"})
    assert first.status_code == 200
    second = client.post("/api/extension/ingest", json=body)
    assert second.status_code == 429
    assert int(second.headers["Retry-After"]) >= 1


def test_status_reports_archive_lag(tmp_path, monkeypatch):
    from app import state
    monkeypatch.setattr(state, "STATE_DB", tmp_path / "capture.db")
    monkeypatch.setattr(state, "STORAGE", tmp_path)
    monkeypatch.setattr(state, "_db_initialized", False)
    status = state.stats()
    assert status["waiting_saves"] == 0
    assert status["oldest_waiting_seconds"] == 0
    assert status["last_archive_at"] is None  # nothing archived yet
    state.set_sig("archive", "last_commit", "1700000000")
    assert state.stats()["last_archive_at"] is not None


def test_batch_endpoint_returns_one_receipt_per_item(monkeypatch):
    from fastapi.testclient import TestClient
    from app import state
    _open_auth(monkeypatch)
    monkeypatch.setattr(main, "ingest_limiter", SlidingWindowLimiter(limit=100))
    monkeypatch.setattr(main.outbox, "drain", lambda: 0)

    def fake_ingest(payload, effective_user):
        if payload.conversation_id == "bad":
            raise RuntimeError("disk on fire")
        return {"receipt_id": "r", "conversation_id": payload.conversation_id, "saved_messages": 1,
                "status": "persisted", "deduplicated": False, "timestamp": "t"}

    monkeypatch.setattr(state, "ingest_extension", fake_ingest)
    client = TestClient(main.app)
    body = {"items": [{"conversation_id": "a"}, {"conversation_id": "bad"}, {"conversation_id": "c"}]}
    r = client.post("/api/extension/ingest-batch", json=body)
    assert r.status_code == 200
    results = r.json()["results"]
    assert [x["conversation_id"] for x in results] == ["a", "bad", "c"]
    assert results[0]["status"] == "persisted"
    assert results[1]["status"] == "error"          # one bad item does not fail the batch
    assert results[2]["status"] == "persisted"


def test_batch_over_25_items_is_rejected(monkeypatch):
    from fastapi.testclient import TestClient
    _open_auth(monkeypatch)
    client = TestClient(main.app)
    r = client.post("/api/extension/ingest-batch", json={"items": [{"conversation_id": str(i)} for i in range(26)]})
    assert r.status_code == 422


def test_upload_key_is_stable_for_the_same_bytes():
    from app import s3
    a = s3.build_s3_key("notes.txt", "conv-1", "alex", digest="ab" * 32)
    b = s3.build_s3_key("notes.txt", "conv-1", "alex", digest="ab" * 32)
    c = s3.build_s3_key("notes.txt", "conv-1", "alex", digest="cd" * 32)
    assert a == b, "retrying the same upload must overwrite, not duplicate"
    assert a != c
