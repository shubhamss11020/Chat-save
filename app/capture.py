"""Capture controller: scans sources, hashes, and performs atomic transactional persistence into SQLite."""
import logging
from typing import Optional

from . import state
from .models import Conversation
from .sources.base import ConversationSource

log = logging.getLogger("chatsave")


def enqueue_snapshot(conv: Conversation) -> bool:
    """Atomic transactional persistence of conversation + messages + outbox."""
    return state.save_conversation_atomic(conv)


class CaptureController:
    def __init__(self, sources: dict[str, ConversationSource]):
        self.sources = sources

    def capture(self, source_name: str, thread_id: str, sig: Optional[str] = None) -> bool:
        """Fetch full conversation from source and save transactionally into SQLite."""
        src = self.sources.get(source_name)
        if not src:
            return False
        conv = src.get_conversation(thread_id)
        if not conv:
            return False
        
        saved = enqueue_snapshot(conv)
        if sig is not None:
            state.set_sig(source_name, thread_id, sig)
        return saved

    def reconcile(self) -> int:
        """Scan all configured sources for updated threads and save any changes transactionally."""
        n = 0
        for source_name, src in self.sources.items():
            try:
                scanned_map = src.scan()
            except Exception:
                log.exception("Scan failed for source %s", source_name)
                continue

            for thread_id, sig in scanned_map.items():
                if state.get_sig(source_name, thread_id) == sig:
                    continue
                try:
                    if self.capture(source_name, thread_id, sig):
                        n += 1
                except Exception:
                    log.exception("Capture failed for %s/%s", source_name, thread_id)
        return n
