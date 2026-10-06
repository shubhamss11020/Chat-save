"""Capture controller: hook events + periodic/startup reconciliation -> hash -> outbox."""
import hashlib
import logging

from . import state
from .models import Conversation
from .sources.base import ConversationSource

log = logging.getLogger("chatsave")


def content_hash(conv: Conversation) -> str:
    """SHA-256 of the complete normalized snapshot (identity + title + every message)."""
    h = hashlib.sha256(f"{conv.platform}\0{conv.id}\0{conv.title}".encode())
    for m in conv.messages:
        h.update(f"\0{m.id}\0{m.role}\0{m.content}".encode())
    return h.hexdigest()


def enqueue_snapshot(conv: Conversation) -> bool:
    return state.enqueue(conv, content_hash(conv))


class CaptureController:
    def __init__(self, sources: dict[str, ConversationSource]):
        self.sources = sources

    def capture(self, platform: str, thread_id: str, sig: str | None = None) -> bool:
        """Read one full transcript and queue it if it changed. Safe to call repeatedly."""
        src = self.sources.get(platform)
        conv = src.get_conversation(thread_id) if src else None
        if not conv:
            return False
        queued = enqueue_snapshot(conv)
        if sig is not None:
            state.set_sig(platform, thread_id, sig)
        return queued

    def reconcile(self) -> int:
        """Find threads changed since the last scan (incl. while the agent was down)."""
        n = 0
        for name, src in self.sources.items():
            for thread_id, sig in src.scan().items():
                if state.get_sig(name, thread_id) == sig:
                    continue
                try:
                    n += self.capture(name, thread_id, sig)
                except Exception:
                    log.exception("capture failed for %s/%s", name, thread_id)
        return n
