"""Git writer: snapshot -> markdown file -> commit (-> push). Knows nothing about capture."""
import re
import shutil
import subprocess

from .config import GIT_BRANCH, GIT_DIR, GIT_EMAIL, GIT_NAME, GIT_REMOTE_URL, REPO_DIR
from .models import Conversation


class GitError(RuntimeError):
    pass


def _slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")[:80] or "unknown"


def _git(*args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    ident = (["-c", f"user.name={GIT_NAME}", "-c", f"user.email={GIT_EMAIL}"]
             if GIT_NAME and GIT_EMAIL else [])
    return subprocess.run(["git", "-C", str(REPO_DIR), *ident, *args],
                          capture_output=True, text=True, timeout=timeout)


def _check(r: subprocess.CompletedProcess, what: str) -> subprocess.CompletedProcess:
    if r.returncode:
        raise GitError(f"{what}: {(r.stderr or r.stdout).strip()}")
    return r


def _q(v: str) -> str:
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def render(conv: Conversation) -> str:
    out = ["---",
           f"conversation_id: {conv.id}",
           f"platform: {conv.platform}",
           f"username: {_q(conv.username)}",
           f"title: {_q(conv.title)}",
           f"created_at: {conv.created_at}",
           f"updated_at: {conv.updated_at}",
           "---", "", f"# {conv.title}", ""]
    for m in conv.messages:
        who = {"user": "User", "assistant": "Claude"}.get(m.role, m.role.title())
        out += [f"## {who}" + (f" ({m.timestamp})" if m.timestamp else ""), "", m.content, ""]
    return "\n".join(out)


def rel_path(conv: Conversation) -> str:
    # id, not title, is the identity: titles change and collide
    return f"{_slug(conv.username)}/{conv.platform}/{_slug(conv.id)}.md"


def commit_snapshot(conv: Conversation) -> None:
    """Write + commit one transcript. No-op if the file is unchanged."""
    rel = rel_path(conv)
    path = GIT_DIR / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(conv), encoding="utf-8", newline="\n")
    full = f"raw_queries/{rel}"
    _check(_git("add", "--", full), "git add")
    if _git("diff", "--cached", "--quiet", "--", full).returncode == 0:
        return  # identical to what is already committed
    _check(_git("commit", "-m", f"{conv.platform}: {conv.title} ({conv.id[:8]})", "--", full),
           "git commit")


def prepare() -> None:
    if not shutil.which("git"):
        raise GitError("git is not installed")
    if not (REPO_DIR / ".git").exists():
        _check(_git("init", "-b", GIT_BRANCH), "git init")
    if GIT_REMOTE_URL:
        cur = _git("remote", "get-url", "origin")
        if cur.returncode:
            _check(_git("remote", "add", "origin", GIT_REMOTE_URL), "git remote add")
        elif cur.stdout.strip() != GIT_REMOTE_URL:
            _check(_git("remote", "set-url", "origin", GIT_REMOTE_URL), "git remote set-url")


def push() -> None:
    """Push all local commits. Raises on failure so the batch is retried later."""
    if not GIT_REMOTE_URL:
        return
    _git("pull", "--rebase", "--autostash", "origin", GIT_BRANCH)  # best effort (new repo: no-op)
    _check(_git("push", "-u", "origin", f"HEAD:{GIT_BRANCH}"), "git push")
