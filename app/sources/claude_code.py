"""Reads Claude Code session transcripts (~/.claude/projects/*/<session>.jsonl)."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from ..config import CLAUDE_PROJECTS, USERNAME
from ..models import Conversation, ConversationEvent, Message


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
    def __init__(self, root: Path = CLAUDE_PROJECTS):
        self.root = root
        self._seen: dict[str, tuple[float, int]] = {}

    def detect_changes(self) -> list[ConversationEvent]:
        events = []
        for f in self.root.glob("*/*.jsonl"):
            st = f.stat()
            sig = (st.st_mtime, st.st_size)
            if self._seen.get(f.stem) != sig:
                self._seen[f.stem] = sig
                events.append(ConversationEvent(platform="claude", thread_id=f.stem))
        return events

    def get_conversation(self, thread_id: str) -> Conversation | None:
        f = next(self.root.glob(f"*/{thread_id}.jsonl"), None)
        if not f:
            return None
        msgs: list[Message] = []
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue  # file may be mid-write
            if o.get("type") not in ("user", "assistant") or o.get("isMeta"):
                continue
            text = _text(o.get("message", {}).get("content")).strip()
            if text:
                msgs.append(Message(id=o.get("uuid", str(len(msgs))), role=o["type"],
                                    content=text, timestamp=o.get("timestamp")))
        if not msgs:
            return None
        mtime = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc).isoformat()
        first_user = next((m.content for m in msgs if m.role == "user"), "untitled")
        return Conversation(id=thread_id, title=first_user.splitlines()[0][:80],
                            username=USERNAME, platform="claude",
                            created_at=msgs[0].timestamp or mtime, updated_at=mtime,
                            messages=msgs)
