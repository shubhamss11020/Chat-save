from typing import Literal, Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: str
    role: Literal["user", "assistant", "tool"]
    content: str
    timestamp: Optional[str] = None


class Conversation(BaseModel):
    id: str
    title: str
    username: str
    platform: Literal["chatgpt", "claude"]
    created_at: str
    updated_at: str
    messages: list[Message]


class ConversationEvent(BaseModel):
    event: str = "conversation.updated"
    platform: Literal["chatgpt", "claude"]
    thread_id: str
