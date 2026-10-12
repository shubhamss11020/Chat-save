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

    # 9. Test Attachments (image, pdf) & Generated README.md files
    file_conv_id = f"test-files-{int(time.time())}"
    # 1x1 transparent png data url
    sample_png = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    readme_content = "# Project Documentation\n\nThis is a complete README generated by Claude.\n\n## Features\n- Fast\n- Reliable"
    
    files_payload = {
        "client_id": "test-ext-001",
        "user_id": "shubham",
        "conversation_id": file_conv_id,
        "title": "Project Setup with Readme",
        "platform": "claude",
        "messages": [
            {
                "id": "msg-file-1",
                "role": "user",
                "content": "Here is the spec diagram and pdf, please generate a README.md",
                "sequence": 1
            },
            {
                "id": "msg-file-2",
                "role": "assistant",
                "content": "I have created the README.md file for you based on the attached files.",
                "sequence": 2
            }
        ],
        "files": [
            {
                "name": "spec_diagram.png",
                "path": "attachments/spec_diagram.png",
                "type": "image",
                "content": sample_png,
                "role": "user",
                "turn_sequence": 1,
                "is_attachment": True
            },
            {
                "name": "spec_sheet.pdf",
                "path": "attachments/spec_sheet.pdf",
                "type": "pdf",
                "content": "Specification PDF Document Content",
                "role": "user",
                "turn_sequence": 1,
                "is_attachment": True
            },
            {
                "name": "README.md",
                "path": "README.md",
                "type": "md",
                "content": readme_content,
                "role": "assistant",
                "is_artifact": True
            }
        ]
    }
    r_files = client.post("/api/extension/ingest", json=files_payload, headers=headers)
    assert r_files.status_code == 200

    # Verify canonical conversation in database retained files
    c_files = state.get_canonical_conversation(file_conv_id)
    assert len(c_files.files) == 3
    readme_item = next((f for f in c_files.files if f["name"] == "README.md"), None)
    assert readme_item is not None
    assert readme_item["content"] == readme_content

    # Verify files were committed directly to disk in structured folder
    from app.config import GIT_DIR
    companion_dir = GIT_DIR / "shubham" / "claude" / "project-setup-with-readme_files"
    if not companion_dir.exists():
        companion_dir = GIT_DIR / "shubham" / "claude" / "Project-Setup-with-Readme_files"
    assert companion_dir.exists(), f"Companion folder was not created!"
    
    saved_readme = companion_dir / "README.md"
    assert saved_readme.exists(), "README.md was not saved on disk!"
    assert "This is a complete README generated by Claude" in saved_readme.read_text(encoding="utf-8")

    from app import s3
    if not s3.is_s3_configured():
        saved_img = companion_dir / "attachments" / "spec_diagram.png"
        assert saved_img.exists(), "Image attachment was not saved on disk!"
        assert saved_img.stat().st_size > 0

    # Verify main transcript links
    transcript_md = GIT_DIR / "shubham" / "claude" / "project-setup-with-readme.md"
    if not transcript_md.exists():
        transcript_md = GIT_DIR / "shubham" / "claude" / "Project-Setup-with-Readme.md"
    assert transcript_md.exists()
    t_text = transcript_md.read_text(encoding="utf-8")
    assert "spec_diagram.png" in t_text
    assert "README.md" in t_text
    assert "## Generated Documents & Files" in t_text

    print("ALL EXTENSION & RETRY/DLQ & MULTI-TURN & ATTACHMENT/README TESTS PASSED SUCCESSFULLY!")


def test_s3_flow():
    import time
    from unittest.mock import MagicMock, patch
    from app import s3
    from app.config import AUTH_TOKEN, GIT_DIR

    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}

    # 1. Test /api/attachments/status
    r_status = client.get("/api/attachments/status", headers=headers)
    assert r_status.status_code == 200
    status_data = r_status.json()
    assert "s3_configured" in status_data
    assert "bucket" in status_data

    # 2. Test S3 Presign generation
    with patch("app.s3.S3_BUCKET_NAME", "my-test-bucket"), \
         patch("app.s3.S3_ACCESS_KEY_ID", "test-key"), \
         patch("app.s3.S3_SECRET_ACCESS_KEY", "test-secret"), \
         patch("app.s3.S3_REGION", "us-east-1"):
        
        mock_client = MagicMock()
        mock_client.generate_presigned_url.return_value = "https://my-test-bucket.s3.amazonaws.com/attachments/test/presigned-put-url"
        
        with patch("app.s3.get_s3_client", return_value=mock_client):
            presign_payload = {
                "filename": "screenshot.png",
                "content_type": "image/png",
                "conversation_id": "test-conv-s3",
                "size_bytes": 10240
            }
            r_presign = client.post("/api/attachments/presign", json=presign_payload, headers=headers)
            assert r_presign.status_code == 200
            data = r_presign.json()
            assert data["upload_url"].startswith("https://")
            assert "screenshot" in data["file_url"]
            assert data["method"] == "PUT"
            assert data["headers"]["Content-Type"] == "image/png"

    # 3. Test Ingestion with S3 upload integration
    with patch("app.s3.is_s3_configured", return_value=True), \
         patch("app.s3.upload_attachment_data", return_value="https://my-test-bucket.s3.amazonaws.com/attachments/user/cloud_diagram.png"):
        
        s3_conv_id = f"test-conv-s3-ingest-{int(time.time())}"
        s3_payload = {
            "client_id": "test-ext-001",
            "user_id": "shubham",
            "conversation_id": s3_conv_id,
            "title": "S3 Attachment Test",
            "platform": "claude",
            "messages": [
                {
                    "id": "s3-msg-1",
                    "role": "user",
                    "content": "Check this cloud architecture diagram",
                    "sequence": 1
                }
            ],
            "files": [
                {
                    "name": "cloud_diagram.png",
                    "type": "image",
                    "content": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                    "role": "user",
                    "turn_sequence": 1,
                    "is_attachment": True
                }
            ]
        }
        r_ingest = client.post("/api/extension/ingest", json=s3_payload, headers=headers)
        assert r_ingest.status_code == 200

        # Verify markdown transcript has S3 link directly
        t_path = GIT_DIR / "shubham" / "claude" / "s3-attachment-test.md"
        assert t_path.exists()
        t_text = t_path.read_text(encoding="utf-8")
        assert "https://my-test-bucket.s3.amazonaws.com/attachments/user/cloud_diagram.png" in t_text
        print("ALL S3 & PRESIGNED URL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_extension_flow()
    test_s3_flow()

