import re
import shutil
import subprocess

from .config import GIT_DIR
from .models import Conversation


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "untitled"


def _git(*args: str) -> None:
    subprocess.run(["git", "-C", str(GIT_DIR), *args], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render(conv: Conversation) -> str:
    out = [f"# {conv.title}", "",
           f"- platform: {conv.platform}", f"- thread_id: {conv.id}",
           f"- updated_at: {conv.updated_at}", ""]
    for m in conv.messages:
        out += [f"## {m.role}" + (f" ({m.timestamp})" if m.timestamp else ""), "", m.content, ""]
    return "\n".join(out)


def write(conv: Conversation) -> str:
    """Write the transcript markdown and commit it. Returns path relative to GIT_DIR."""
    rel = f"{_slug(conv.username)}/{conv.platform}/{_slug(conv.title)}-{conv.id[:8]}.md"
    path = GIT_DIR / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(conv), encoding="utf-8")
    if shutil.which("git"):
        if not (GIT_DIR / ".git").exists():
            _git("init")
        _git("add", rel)
        _git("-c", "user.name=chat-save", "-c", "user.email=chat-save@local",
             "commit", "-m", f"{conv.platform}: {conv.title} ({conv.id[:8]})")
    return rel
