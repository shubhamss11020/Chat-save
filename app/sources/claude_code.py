"""Claude Code session transcripts (~/.claude/projects/*/<session>.jsonl). Read-only."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from ..config import CLAUDE_PROJECTS, USERNAME
from ..models import Conversation, Message

# IDE/harness context blocks injected into user turns, not written by the user
_INJECTED = re.compile(r"<(ide_[a-z_]+|system-reminder|pasted_content)\b[^>]*>.*?</\1[^>]*>", re.S)


def _text(content) -> str:
    if isinstance(content, str):
        raw = content
    else:
        raw = "\n".join(b.get("text", "") for b in content or []
                        if isinstance(b, dict) and b.get("type") == "text")
    return _INJECTED.sub("", raw)


class ClaudeSource:
    name = "claude"

    def __init__(self, root: Path = CLAUDE_PROJECTS):
        self.root = root

    def _path(self, thread_id: str) -> Path | None:
        return next(self.root.glob(f"*/{thread_id}.jsonl"), None)

    def scan(self) -> dict[str, str]:
        out = {}
        for f in self.root.glob("*/*.jsonl"):
            try:
                st = f.stat()
            except OSError:
                continue
            out[f.stem] = f"{st.st_mtime_ns}:{st.st_size}"
        return out

    def get_conversation(self, thread_id: str) -> Conversation | None:
        f = self._path(thread_id)
        if not f:
            return None
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            mtime = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc).isoformat()
        except OSError:
            return None  # locked/being rotated: stays pending for the next scan
        msgs: list[Message] = []
        for line in lines:
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue  # last line may be mid-write
            if o.get("type") not in ("user", "assistant") or o.get("isMeta"):
                continue
            text = _text(o.get("message", {}).get("content")).strip()
            if text:
                msgs.append(Message(id=o.get("uuid", str(len(msgs))), role=o["type"],
                                    content=text, timestamp=o.get("timestamp")))
        if not msgs:
            return None
        first_user = next((m.content for m in msgs if m.role == "user"), "untitled")
        return Conversation(id=thread_id, title=first_user.splitlines()[0][:80],
                            username=USERNAME, platform="claude",
                            created_at=msgs[0].timestamp or mtime, updated_at=mtime,
                            messages=msgs)
