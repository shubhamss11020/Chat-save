import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.config import AUTH_TOKEN
from app.main import app
from app import state

client = TestClient(app)

def test_extension_flow():
    # 0. Unauthorized test
    r_unauth = client.post("/api/extension/heartbeat", json={"client_id": "test"})
    assert r_unauth.status_code == 401

    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}

    # 1. Test heartbeat
    hb_data = {
        "client_id": "test-ext-001",
        "user_id": "alex",
        "extension_version": "1.0.0",
        "browser": "Chrome 130",
        "pending_queue_count": 0,
        "last_successful_sync": None,
        "last_error": None
    }
    r = client.post("/api/extension/heartbeat", json=hb_data, headers=headers)
    assert r.status_code == 200, r.text
    assert r.json()["ok"] is True

    # 2. Test clients listing
    r = client.get("/api/extension/clients", headers=headers)
    assert r.status_code == 200
    clients = r.json()["clients"]
    assert any(c["client_id"] == "test-ext-001" for c in clients)

    # 3. Test conversation turn ingestion
    import time
    conv_id = f"test-conv-ext-{int(time.time())}"
    payload = {
        "client_id": "test-ext-001",
        "user_id": "alex",
        "conversation_id": conv_id,
        "title": "Debugging Kubernetes Networking",
        "platform": "claude",
        "url": f"https://claude.ai/chat/{conv_id}",
        "messages": [
            {
                "id": "turn-1-user",
                "role": "user",
                "content": "Why is my service returning 503?",
                "sequence": 1
            },
            {
                "id": "turn-1-assistant",
                "role": "assistant",
                "content": "A 503 Service Unavailable typically indicates no healthy endpoints.",
                "sequence": 2
            }
        ]
    }
    r = client.post("/api/extension/ingest", json=payload, headers=headers)
    assert r.status_code == 200, r.text
    res = r.json()
    assert res["conversation_id"] == conv_id
    assert res["saved_messages"] == 2
    assert res["status"] == "persisted"
    assert res["deduplicated"] is False
    assert res["receipt_id"].startswith("rcpt_")

    # 4. Test deduplication when sending identical conversation
    r2 = client.post("/api/extension/ingest", json=payload, headers=headers)
    assert r2.status_code == 200
    res2 = r2.json()
    assert res2["status"] == "unchanged"
    assert res2["deduplicated"] is True

    # 5. Check stats endpoint includes extension_clients
    r_stats = client.get("/status", headers=headers)
    assert r_stats.status_code == 200
    stats_data = r_stats.json()
    assert "extension_clients" in stats_data
    assert any(c["client_id"] == "test-ext-001" for c in stats_data["extension_clients"])

    print("ALL EXTENSION API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_extension_flow()
