from typing import Protocol

from ..models import Conversation, ConversationEvent


class ConversationSource(Protocol):
    def detect_changes(self) -> list[ConversationEvent]: ...
    def get_conversation(self, thread_id: str) -> Conversation | None: ...
