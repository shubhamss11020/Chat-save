from typing import Protocol

from ..models import Conversation


class ConversationSource(Protocol):
    name: str

    def scan(self) -> dict[str, str]:
        """thread_id -> change signature, cheap (no transcript parsing). Read-only."""

    def get_conversation(self, thread_id: str) -> Conversation | None:
        """Full current transcript of one thread. Read-only."""
