"""P0 regression tests: transcript path containment and token-bound identity."""
import asyncio

import pytest

from app import auth, gitstore


@pytest.fixture
def archive(tmp_path, monkeypatch):
    """A throwaway repo layout: tmp/raw_queries holds transcripts, tmp/secret.txt is outside it."""
    repo = tmp_path / "repo"
    git_dir = repo / "raw_queries"
    (git_dir / "alex" / "claude").mkdir(parents=True)
    (git_dir / "alex" / "claude" / "chat.md").write_text("hello transcript", encoding="utf-8")
    (repo / "secret.txt").write_text("SERVER SECRET", encoding="utf-8")
    monkeypatch.setattr(gitstore, "REPO_DIR", repo)
    monkeypatch.setattr(gitstore, "GIT_DIR", git_dir)
    monkeypatch.setattr(gitstore, "prepare", lambda: None)  # no git operations in tests
    return repo


# --- transcript path containment -------------------------------------------------

@pytest.mark.parametrize("path", [
    "alex/claude/chat.md",
    "raw_queries/alex/claude/chat.md",
])
def test_reads_transcripts_inside_archive(archive, path):
    assert gitstore.get_transcript(path) == "hello transcript"


@pytest.mark.parametrize("path", [
    "../secret.txt",
    "../../secret.txt",
    "alex/../../secret.txt",
    "raw_queries/../secret.txt",
    "/etc/passwd",
])
def test_refuses_paths_outside_archive(archive, path):
    result = gitstore.get_transcript(path)
    assert "SERVER SECRET" not in result
    assert result.startswith("File not found")


def test_absolute_path_to_secret_is_refused(archive):
    secret = archive / "secret.txt"
    result = gitstore.get_transcript(str(secret))
    assert "SERVER SECRET" not in result


# --- identity: token-bound users cannot be overridden by ?user= -------------------

async def _run_auth(headers_extra=None, query=b""):
    seen = {}

    async def inner(scope, receive, send):
        seen["user"] = auth.current_user.get()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    sent = []

    async def send(msg):
        sent.append(msg)

    async def receive():
        return {"type": "http.request"}

    headers = [(b"authorization", v) for v in (headers_extra or [])]
    scope = {"type": "http", "path": "/mcp", "method": "POST", "headers": headers,
             "query_string": query}
    await auth.TokenAuth(inner)(scope, receive, send)
    status = next((m["status"] for m in sent if m["type"] == "http.response.start"), None)
    return status, seen.get("user")


@pytest.fixture
def auth_config(monkeypatch):
    monkeypatch.setattr(auth, "USER_TOKENS_MAP", {"tok-rajat": "rajat"})
    monkeypatch.setattr(auth, "AUTH_TOKEN", "shared-secret")
    monkeypatch.setattr(auth, "USERNAME", "server-default")


def test_per_user_token_ignores_user_query_param(auth_config):
    status, user = asyncio.run(_run_auth([b"Bearer tok-rajat"], query=b"user=shubham"))
    assert status == 200
    assert user == "rajat"  # identity comes from the token, not the query string


def test_shared_token_cannot_name_another_user(auth_config):
    # The shared owner token must not let its holder act as someone else.
    status, user = asyncio.run(_run_auth([b"Bearer shared-secret"], query=b"user=alex"))
    assert status == 200
    assert user == "server-default"


def test_shared_token_without_user_falls_back_to_server_default(auth_config):
    status, user = asyncio.run(_run_auth([b"Bearer shared-secret"]))
    assert status == 200
    assert user == "server-default"


def test_unknown_token_is_rejected(auth_config):
    status, _ = asyncio.run(_run_auth([b"Bearer wrong"]))
    assert status == 401
