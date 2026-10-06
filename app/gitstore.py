"""Git writer: snapshot -> markdown file -> commit (-> push). Knows nothing about capture."""
import re
import shutil
import subprocess
import threading

from datetime import datetime
from zoneinfo import ZoneInfo

from .config import GIT_BRANCH, GIT_DIR, GIT_EMAIL, GIT_NAME, GIT_REMOTE_URL, REPO_DIR, ROOT, USERNAME
from .models import Conversation

EASTERN = ZoneInfo("America/New_York")
_lock = threading.Lock()  # one git operation at a time (agent worker + MCP requests)


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


def render(conv: Conversation, created_at: str = "", updated_at: str = "") -> str:
    uname = conv.username or USERNAME or "user"
    c_at = created_at or conv.created_at or ""
    u_at = updated_at or conv.updated_at or ""
    out = ["---",
           f"conversation_id: {conv.id}",
           f"platform: {conv.platform}",
           f"username: {_q(uname)}",
           f"title: {_q(conv.title)}",
           f"created_at: {_q(c_at)}",
           f"updated_at: {_q(u_at)}",
           "---", "", f"# {conv.title}", ""]
    for m in conv.messages:
        who = {"user": "User", "assistant": "Claude"}.get(m.role, m.role.title())
        t = m.timestamp
        if not t or "00:00:00" in t:
            t = u_at
        out += [f"## {who}" + (f" ({t})" if t else ""), "", m.content, ""]
    return "\n".join(out)


def rel_path(conv: Conversation) -> str:
    # id, not title, is the identity: titles change and collide
    uname = conv.username or USERNAME or "user"
    return f"{_slug(uname)}/{conv.platform}/{_slug(conv.id)}.md"


def commit_snapshot(conv: Conversation) -> None:
    """Write + commit one transcript. No-op if the file is unchanged."""
    rel = rel_path(conv)
    path = GIT_DIR / rel
    path.parent.mkdir(parents=True, exist_ok=True)

    now_est = datetime.now(EASTERN).strftime("%Y-%m-%d %H:%M:%S %Z")
    created_at = None

    if path.exists():
        try:
            old_text = path.read_text(encoding="utf-8")
            m = re.search(r'^created_at:\s*(.+)$', old_text, re.MULTILINE)
            if m:
                created_at = m.group(1).strip().strip('"\'')
        except Exception:
            pass

    if not created_at or "00:00:00" in created_at:
        if conv.created_at and "00:00:00" not in conv.created_at:
            created_at = conv.created_at
        else:
            created_at = now_est

    updated_at = now_est
    rendered_text = render(conv, created_at=created_at, updated_at=updated_at)
    path.write_text(rendered_text, encoding="utf-8", newline="\n")

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
        if GIT_REMOTE_URL and REPO_DIR.resolve() != ROOT.resolve():
            # hosted server: its working copy is a clone of the archive repo
            REPO_DIR.parent.mkdir(parents=True, exist_ok=True)
            _check(subprocess.run(["git", "clone", GIT_REMOTE_URL, str(REPO_DIR)],
                                  capture_output=True, text=True, timeout=300), "git clone")
        else:
            REPO_DIR.mkdir(parents=True, exist_ok=True)
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


def save_batch(convs: list[Conversation]) -> dict:
    """Commit every snapshot, then push once. Per-conversation commit errors are reported
    in 'failed'; a push failure raises so the whole batch is retried (commits are idempotent).
    """
    with _lock:
        prepare()
        saved, failed = [], {}
        for c in convs:
            try:
                commit_snapshot(c)
                saved.append(c.id)
            except Exception as e:
                failed[c.id] = str(e)
        if saved:
            push()
        return {"saved": saved, "failed": failed}
