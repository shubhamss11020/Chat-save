"""Archive batching and the conversation-to-file index, against a real temporary git repo."""
import subprocess

import pytest

from app import gitstore, state
from app.models import Conversation, Message


@pytest.fixture
def repo(tmp_path, monkeypatch):
    repo_dir = tmp_path / "repo"
    monkeypatch.setattr(gitstore, "REPO_DIR", repo_dir)
    monkeypatch.setattr(gitstore, "GIT_DIR", repo_dir / "raw_queries")
    monkeypatch.setattr(gitstore, "GIT_REMOTE_URL", "")  # never push from tests
    monkeypatch.setattr(gitstore, "GIT_NAME", "test")
    monkeypatch.setattr(gitstore, "GIT_EMAIL", "test@example.com")
    monkeypatch.setattr(gitstore, "USERNAME", "alex")
    monkeypatch.setattr(state, "STATE_DB", tmp_path / "capture.db")
    monkeypatch.setattr(state, "STORAGE", tmp_path)
    monkeypatch.setattr(state, "_db_initialized", False)
    return repo_dir


def _conv(i, title=None):
    return Conversation(
        id=f"conv-{i}", title=title or f"Chat {i}", platform="claude", username="alex",
        created_at="2026-10-12T13:00:00Z", updated_at="2026-10-12T15:00:00Z",
        messages=[Message(id=f"conv-{i}_msg_1_user", role="user", content=f"hello {i}",
                          timestamp="2026-10-12T14:05:00Z")],
    )


def _commit_count(repo_dir):
    out = subprocess.run(["git", "-C", str(repo_dir), "rev-list", "--count", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return int(out or 0)


def test_batch_of_five_becomes_one_commit(repo):
    gitstore.prepare()
    convs = [_conv(i) for i in range(5)]
    for c in convs:
        state.save_conversation_atomic(c)
    result = gitstore.save_batch(convs)
    assert sorted(result["saved"]) == sorted(c.id for c in convs), result["failed"]
    assert _commit_count(repo) == 1
    assert len(list((repo / "raw_queries" / "alex" / "claude").glob("*.md"))) == 5


def test_renamed_conversation_keeps_its_file_through_the_index(repo):
    gitstore.prepare()
    first = _conv(1)
    state.save_conversation_atomic(first)
    gitstore.save_batch([first])
    indexed = state.get_archive_path("conv-1")
    assert indexed, "the archive path should be recorded after a save"

    renamed = _conv(1, title="A completely new title")
    state.save_conversation_atomic(renamed)
    result = gitstore.save_batch([renamed])
    assert result["saved"] == ["conv-1"], result["failed"]

    files = list((repo / "raw_queries" / "alex" / "claude").glob("*.md"))
    assert len(files) == 1, [f.name for f in files]
    assert state.get_archive_path("conv-1") == indexed


def test_identical_resave_makes_no_new_commit(repo):
    gitstore.prepare()
    c = _conv(7)
    state.save_conversation_atomic(c)
    gitstore.save_batch([c])
    before = _commit_count(repo)
    gitstore.save_batch([c])  # same content again
    assert _commit_count(repo) == before


def test_uploaded_attachment_does_not_break_the_batch_commit(repo):
    """An attachment already in S3 leaves an empty folder locally; the commit must still work."""
    gitstore.prepare()
    c = _conv(3)
    c.files = [{"name": "big.pdf", "path": "attachments/big.pdf", "type": "application/pdf",
                "url": "https://cdn.example/big.pdf", "uploaded_to_s3": True,
                "role": "user", "turn_sequence": 1, "is_attachment": True}]
    state.save_conversation_atomic(c)
    result = gitstore.save_batch([c])
    assert result["saved"] == ["conv-3"], result["failed"]
    assert _commit_count(repo) == 1


def test_one_failing_conversation_does_not_block_the_batch(repo, monkeypatch):
    """If the batch commit fails, each conversation is committed on its own."""
    gitstore.prepare()
    convs = [_conv(i) for i in range(3)]
    for c in convs:
        state.save_conversation_atomic(c)

    real_commit = gitstore._commit_paths
    def flaky(paths, labels, when):
        if len(labels) > 1:
            raise RuntimeError("simulated batch failure")
        return real_commit(paths, labels, when)
    monkeypatch.setattr(gitstore, "_commit_paths", flaky)

    result = gitstore.save_batch(convs)
    assert sorted(result["saved"]) == sorted(c.id for c in convs), result["failed"]
    assert _commit_count(repo) == 3  # one commit per conversation after the fallback
