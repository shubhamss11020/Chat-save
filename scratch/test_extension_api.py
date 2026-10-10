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

    # 6. Test empty message filtering: sending empty messages should be safely ignored
    empty_payload = {
        "client_id": "test-ext-001",
        "user_id": "alex",
        "conversation_id": f"test-empty-{int(time.time())}",
        "title": "Empty Thread Test",
        "platform": "claude",
        "messages": [
            {"id": "msg-empty-1", "role": "user", "content": "   ", "sequence": 1},
            {"id": "msg-empty-2", "role": "assistant", "content": "", "sequence": 2}
        ]
    }
    r_empty = client.post("/api/extension/ingest", json=empty_payload, headers=headers)
    assert r_empty.status_code == 200
    assert r_empty.json()["saved_messages"] == 0

    # 7. Test DLQ retry endpoint
    r_dlq = client.post("/api/outbox/retry-dlq", headers=headers)
    assert r_dlq.status_code == 200
    assert "requeued" in r_dlq.json()

    # 8. Test Multi-Turn Non-Trimming Guarantee:
    # First turn has full long response (e.g. 1000 chars)
    # Second turn arrives where turn 1 is shortened/trimmed in payload:
    # Verify canonical conversation retains full 1000 chars of turn 1!
    long_response_1 = "AskCruz is an AI product connecting company data... " + ("X" * 1000)
    mt_conv_id = f"test-multiturn-{int(time.time())}"
    turn1_payload = {
        "client_id": "test-ext-001",
        "user_id": "shubham",
        "conversation_id": mt_conv_id,
        "title": "Askcruz multi-turn test",
        "platform": "claude",
        "messages": [
            {"id": "msg-1-user", "role": "user", "content": "can u give me details about askcruz", "sequence": 1},
            {"id": "msg-2-assistant", "role": "assistant", "content": long_response_1, "sequence": 2}
        ]
    }
    r_turn1 = client.post("/api/extension/ingest", json=turn1_payload, headers=headers)
    assert r_turn1.status_code == 200

    # Verify Turn 1 in state
    c1 = state.get_canonical_conversation(mt_conv_id)
    assert len(c1.messages) == 2
    assert len(c1.messages[1].content) >= 1000

    # Now turn 2 arrives, but msg-2 is trimmed down to 50 chars in incoming payload!
    turn2_payload = {
        "client_id": "test-ext-001",
        "user_id": "shubham",
        "conversation_id": mt_conv_id,
        "title": "Askcruz multi-turn test",
        "platform": "claude",
        "messages": [
            {"id": "msg-1-user", "role": "user", "content": "can u give me details about askcruz", "sequence": 1},
            {"id": "msg-2-assistant", "role": "assistant", "content": "AskCruz is an AI product...", "sequence": 2},
            {"id": "msg-3-user", "role": "user", "content": "what about sabre alloys", "sequence": 3},
            {"id": "msg-4-assistant", "role": "assistant", "content": "Sabre Alloys is a customer...", "sequence": 4}
        ]
    }
    r_turn2 = client.post("/api/extension/ingest", json=turn2_payload, headers=headers)
    assert r_turn2.status_code == 200

    # Verify that msg-2 in canonical conversation was NOT trimmed!
    c2 = state.get_canonical_conversation(mt_conv_id)
    assert len(c2.messages) == 4
    assert len(c2.messages[1].content) >= 1000, "Turn 1 response was incorrectly trimmed!"
    assert c2.messages[3].content == "Sabre Alloys is a customer..."

    print("ALL EXTENSION & RETRY/DLQ & MULTI-TURN PRESERVATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_extension_flow()
