import logging
import re
import shutil
import subprocess
import threading

from .config import GIT_BRANCH, GIT_DIR, GIT_EMAIL, GIT_NAME, GIT_REMOTE_URL, REPO_DIR
from .models import Conversation

log = logging.getLogger("chatsave")
_push_lock = threading.Lock()


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "untitled"


def _git(*args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    ident = (["-c", f"user.name={GIT_NAME}", "-c", f"user.email={GIT_EMAIL}"]
             if GIT_NAME and GIT_EMAIL else [])
    return subprocess.run(["git", "-C", str(REPO_DIR), *ident, *args], capture_output=True,
                          text=True, timeout=timeout)


def render(conv: Conversation) -> str:
    out = [f"# {conv.title}", "",
           f"- platform: {conv.platform}", f"- thread_id: {conv.id}",
           f"- updated_at: {conv.updated_at}", ""]
    for m in conv.messages:
        out += [f"## {m.role}" + (f" ({m.timestamp})" if m.timestamp else ""), "", m.content, ""]
    return "\n".join(out)


def _ensure_remote() -> None:
    if not GIT_REMOTE_URL:
        return
    cur = _git("remote", "get-url", "origin")
    if cur.returncode != 0:
        _git("remote", "add", "origin", GIT_REMOTE_URL)
    elif cur.stdout.strip() != GIT_REMOTE_URL:
        _git("remote", "set-url", "origin", GIT_REMOTE_URL)


def _push() -> None:
    with _push_lock:
        try:
            _git("pull", "--rebase", "--autostash", "origin", GIT_BRANCH, timeout=120)
            r = _git("push", "-u", "origin", f"HEAD:{GIT_BRANCH}", timeout=120)
            if r.returncode != 0:
                log.warning("git push failed: %s", r.stderr.strip())
        except Exception:
            log.exception("git push crashed")


def write(conv: Conversation) -> str:
    """Write transcript markdown to raw_queries/, commit it, push in background.

    Returns path relative to raw_queries/.
    """
    rel = f"{_slug(conv.username)}/{conv.platform}/{_slug(conv.title)}-{conv.id[:8]}.md"
    path = GIT_DIR / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(conv), encoding="utf-8")
    if not shutil.which("git"):
        return rel
    if not (REPO_DIR / ".git").exists():
        _git("init", "-b", GIT_BRANCH)
    _ensure_remote()
    full = f"raw_queries/{rel}"
    _git("add", full)
    c = _git("commit", "-m", f"{conv.platform}: {conv.title} ({conv.id[:8]})", "--", full)
    if c.returncode != 0 and "nothing to commit" not in c.stdout:
        log.warning("git commit failed: %s", (c.stderr or c.stdout).strip())
    elif c.returncode == 0 and GIT_REMOTE_URL:
        threading.Thread(target=_push, daemon=True).start()
    return rel
