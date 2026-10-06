"""Clone/pull the transcript repo and rebuild the SQLite index from raw_queries/."""
import logging
import re
import subprocess

from . import ingest
from .config import GIT_BRANCH, GIT_DIR, GIT_REMOTE_URL, REPO_DIR, ROOT
from .gitstore import _git
from .models import Conversation, Message

log = logging.getLogger("chatsave")
_HEAD = re.compile(r"^## (user|assistant|tool)(?: \((.*)\))?$", re.M)


def parse(text: str) -> Conversation | None:
    """Inverse of gitstore.render()."""
    title = re.search(r"^# (.*)$", text, re.M)
    meta = dict(re.findall(r"^- (platform|thread_id|updated_at): (.*)$", text, re.M))
    if not title or "thread_id" not in meta or meta.get("platform") not in ("chatgpt", "claude"):
        return None
    heads = list(_HEAD.finditer(text))
    msgs = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        msgs.append(Message(id=str(i), role=h.group(1), timestamp=h.group(2),
                            content=text[h.end():end].strip("\n")))
    ts = meta.get("updated_at", "")
    return Conversation(id=meta["thread_id"], title=title.group(1), platform=meta["platform"],
                        username="", created_at=ts, updated_at=ts, messages=msgs)


def reindex() -> int:
    n = 0
    for f in GIT_DIR.rglob("*.md"):
        rel = f.relative_to(GIT_DIR)
        conv = parse(f.read_text(encoding="utf-8"))
        if not conv:
            continue
        conv.username = rel.parts[0] if len(rel.parts) > 2 else ""
        if ingest.index_only(conv, rel.as_posix()) == "indexed":
            n += 1
    return n


def pull() -> None:
    if not GIT_REMOTE_URL:
        return
    if not (REPO_DIR / ".git").exists():
        if REPO_DIR == ROOT:
            return
        REPO_DIR.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "clone", GIT_REMOTE_URL, str(REPO_DIR)],
                           capture_output=True, text=True, timeout=300)
        if r.returncode:
            log.warning("git clone failed: %s", r.stderr.strip())
        return
    r = _git("pull", "--rebase", "--autostash", "origin", GIT_BRANCH, timeout=120)
    if r.returncode:
        log.warning("git pull failed: %s", r.stderr.strip())


def sync() -> int:
    pull()
    GIT_DIR.mkdir(parents=True, exist_ok=True)
    return reindex()
