"""P1 regression tests: no guessed identities, scoped MCP reads, fail-closed auth, SSRF guard."""
import asyncio

import pytest

from app import auth, gitstore, mcp_server, s3
from app.config import UNKNOWN_USER


# --- identity: unidentified transcripts go to "unknown", never to a guessed person ----

def test_missing_identity_is_recorded_as_unknown(monkeypatch):
    monkeypatch.setattr(gitstore, "USERNAME", "")
    assert gitstore._normalize_username("") == UNKNOWN_USER
    assert gitstore._normalize_username("user") == UNKNOWN_USER


def test_configured_owner_is_used_for_unidentified_transcripts(monkeypatch):
    monkeypatch.setattr(gitstore, "USERNAME", "alex")
    assert gitstore._normalize_username("") == "alex"


def test_email_identity_is_reduced_to_username(monkeypatch):
    monkeypatch.setattr(gitstore, "USERNAME", "")
    # Existing folder naming: domain dropped, dots become dashes.
    assert gitstore._normalize_username("Rajat.Jain@Company.com") == "rajat-jain"


# --- MCP read scoping ---------------------------------------------------------------

@pytest.fixture
def set_caller(monkeypatch):
    def _set(name, admins=frozenset()):
        token = auth.current_user.set(name)
        monkeypatch.setattr(mcp_server, "ADMIN_USERS", set(admins))
        return token
    yield _set


def test_regular_user_is_scoped_to_own_archive(set_caller):
    tok = set_caller("rajat")
    try:
        assert mcp_server._scope("") == (True, "rajat")
        assert mcp_server._scope("rajat") == (True, "rajat")
        assert mcp_server._scope("shubham") == (False, "rajat")
    finally:
        auth.current_user.reset(tok)


def test_admin_can_read_any_archive(set_caller):
    tok = set_caller("travis", admins={"travis"})
    try:
        assert mcp_server._scope("") == (True, "")
        assert mcp_server._scope("shubham") == (True, "shubham")
    finally:
        auth.current_user.reset(tok)


def test_open_server_does_not_restrict(monkeypatch):
    monkeypatch.setattr(mcp_server, "ADMIN_USERS", set())
    assert mcp_server._scope("anyone") == (True, "anyone")


def test_get_transcript_respects_owner(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    git_dir = repo / "raw_queries"
    (git_dir / "alex" / "claude").mkdir(parents=True)
    (git_dir / "bob" / "claude").mkdir(parents=True)
    (git_dir / "alex" / "claude" / "a.md").write_text("alex notes", encoding="utf-8")
    (git_dir / "bob" / "claude" / "b.md").write_text("bob notes", encoding="utf-8")
    monkeypatch.setattr(gitstore, "REPO_DIR", repo)
    monkeypatch.setattr(gitstore, "GIT_DIR", git_dir)
    monkeypatch.setattr(gitstore, "prepare", lambda: None)

    assert gitstore.get_transcript("alex/claude/a.md", owner="alex") == "alex notes"
    assert "bob notes" not in gitstore.get_transcript("bob/claude/b.md", owner="alex")
    assert gitstore.get_transcript("bob/claude/b.md", owner=None) == "bob notes"


# --- fail-closed auth -----------------------------------------------------------------

async def _call(path="/mcp", headers=None):
    sent = []

    async def inner(scope, receive, send):
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    async def send(msg):
        sent.append(msg)

    async def receive():
        return {"type": "http.request"}

    scope = {"type": "http", "path": path, "method": "POST",
             "headers": [(b"authorization", v) for v in (headers or [])], "query_string": b""}
    await auth.TokenAuth(inner)(scope, receive, send)
    return next(m["status"] for m in sent if m["type"] == "http.response.start")


def test_no_tokens_configured_rejects_everyone(monkeypatch):
    monkeypatch.setattr(auth, "AUTH_TOKEN", "")
    monkeypatch.setattr(auth, "USER_TOKENS_MAP", {})
    monkeypatch.setattr(auth, "ALLOW_OPEN", False)
    assert asyncio.run(_call()) == 401


def test_explicit_open_mode_allows_requests(monkeypatch):
    monkeypatch.setattr(auth, "AUTH_TOKEN", "")
    monkeypatch.setattr(auth, "USER_TOKENS_MAP", {})
    monkeypatch.setattr(auth, "ALLOW_OPEN", True)
    assert asyncio.run(_call()) == 200


def test_health_stays_open_without_tokens(monkeypatch):
    monkeypatch.setattr(auth, "AUTH_TOKEN", "")
    monkeypatch.setattr(auth, "USER_TOKENS_MAP", {})
    monkeypatch.setattr(auth, "ALLOW_OPEN", False)
    assert asyncio.run(_call(path="/health")) == 200


# --- SSRF guard for attachment fetches -------------------------------------------------

@pytest.mark.parametrize("url", [
    "http://example.com/file.pdf",          # not https
    "https://127.0.0.1/file.pdf",           # loopback
    "https://localhost/file.pdf",           # loopback by name
    "https://169.254.169.254/latest/meta",  # cloud metadata endpoint
    "https://10.0.0.5/internal.pdf",        # private LAN
    "https:///no-host",
])
def test_unsafe_attachment_urls_are_refused(url):
    assert s3.is_safe_remote_url(url) is False


# --- review follow-ups ------------------------------------------------------------------

def test_unknown_token_is_rejected_when_only_user_tokens_are_configured(monkeypatch):
    # Regression: this used to fall through to the open branch and be let in as anonymous.
    monkeypatch.setattr(auth, "AUTH_TOKEN", "")
    monkeypatch.setattr(auth, "USER_TOKENS_MAP", {"tok-alex": "alex"})
    monkeypatch.setattr(auth, "ALLOW_OPEN", False)
    assert asyncio.run(_call(headers=[b"Bearer not-a-token"])) == 401


def test_known_person_token_is_accepted_and_bound(monkeypatch):
    monkeypatch.setattr(auth, "AUTH_TOKEN", "")
    monkeypatch.setattr(auth, "USER_TOKENS_MAP", {"tok-alex": "alex"})
    monkeypatch.setattr(auth, "ALLOW_OPEN", False)
    assert asyncio.run(_call(headers=[b"Bearer tok-alex"])) == 200


def test_caller_named_unknown_is_scoped_to_its_own_folder(set_caller, monkeypatch):
    # Regression: "unknown" used to be remapped to the server owner, so this caller could
    # neither read its own folder nor was kept out of the owner's.
    monkeypatch.setattr(gitstore, "USERNAME", "owner")
    tok = set_caller("unknown")
    try:
        assert mcp_server._scope("") == (True, "unknown")
        assert mcp_server._scope("owner") == (False, "unknown")
    finally:
        auth.current_user.reset(tok)
