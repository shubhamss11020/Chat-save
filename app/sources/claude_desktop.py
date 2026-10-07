"""Claude Desktop & Local Client transcript capture source."""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from ..config import CLAUDE_PROJECTS, USERNAME
from ..models import Conversation, Message

_INJECTED = re.compile(r"<(ide_[a-z_]+|system-reminder|pasted_content)\b[^>]*>.*?</\1[^>]*>", re.S)


def _get_desktop_paths() -> list[Path]:
    """Find potential Claude Desktop data directories across platforms."""
    paths = []
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")
        if appdata:
            paths.append(Path(appdata) / "Claude")
            paths.append(Path(appdata) / "Claude" / "local-storage")
        localappdata = os.getenv("LOCALAPPDATA")
        if localappdata:
            paths.append(Path(localappdata) / "Claude")
    elif sys.platform == "darwin":
        paths.append(Path.home() / "Library" / "Application Support" / "Claude")
    else:
        paths.append(Path.home() / ".config" / "Claude")
    
    # Also include standard ~/.claude roots
    paths.append(Path.home() / ".claude")
    paths.append(CLAUDE_PROJECTS)
    return [p for p in paths if p.exists()]


def _extract_text(content) -> str:
    if isinstance(content, str):
        raw = content
    elif isinstance(content, list):
        raw = "\n".join(
            b.get("text", "") for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    elif isinstance(content, dict):
        raw = content.get("text", "")
    else:
        raw = str(content or "")
    return _INJECTED.sub("", raw).strip()


class ClaudeDesktopSource:
    name = "claude_desktop"

    def __init__(self, roots: list[Path] | None = None):
        self.roots = roots or _get_desktop_paths()

    def scan(self) -> dict[str, str]:
        """Scan candidate files and return {thread_id: signature} without heavy parsing."""
        out = {}
        for root in self.roots:
            if not root.exists():
                continue
            # Look for jsonl transcripts and session exports
            for pattern in ("*/*.jsonl", "*.jsonl", "projects/*/*.jsonl", "threads/*.json"):
                for f in root.glob(pattern):
                    try:
                        st = f.stat()
                        # signature = mtime_ns:size
                        out[f"{root.name}_{f.stem}"] = f"{st.st_mtime_ns}:{st.st_size}"
                    except OSError:
                        continue
        return out

    def get_conversation(self, thread_key: str) -> Conversation | None:
        """Parse full conversation from discovered file."""
        target_file: Path | None = None
        for root in self.roots:
            for pattern in ("*/*.jsonl", "*.jsonl", "projects/*/*.jsonl", "threads/*.json"):
                for f in root.glob(pattern):
                    if f"{root.name}_{f.stem}" == thread_key:
                        target_file = f
                        break
                if target_file:
                    break

        if not target_file or not target_file.exists():
            return None

        try:
            mtime = datetime.fromtimestamp(target_file.stat().st_mtime, timezone.utc).isoformat()
            if target_file.suffix == ".jsonl":
                lines = target_file.read_text(encoding="utf-8", errors="replace").splitlines()
                msgs: list[Message] = []
                for idx, line in enumerate(lines, start=1):
                    try:
                        o = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    msg_type = o.get("type")
                    if msg_type not in ("user", "assistant") or o.get("isMeta"):
                        continue
                    text = _extract_text(o.get("message", {}).get("content"))
                    if text:
                        msgs.append(
                            Message(
                                id=o.get("uuid", f"msg_{idx}"),
                                sequence=idx,
                                role=msg_type,
                                content=text,
                                timestamp=o.get("timestamp") or mtime
                            )
                        )
                if not msgs:
                    return None
                
                first_user = next((m.content for m in msgs if m.role == "user"), "Untitled Conversation")
                title = first_user.splitlines()[0][:80].strip()
                thread_id = target_file.stem

                return Conversation(
                    id=thread_id,
                    external_conversation_id=thread_id,
                    platform="claude",
                    user_id=USERNAME or "shubham",
                    username=USERNAME or "shubham",
                    title=title,
                    created_at=msgs[0].timestamp or mtime,
                    updated_at=mtime,
                    messages=msgs
                )

        except Exception:
            return None
        return None
