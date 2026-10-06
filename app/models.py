from typing import Literal, Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: str
    role: Literal["user", "assistant", "tool"]
    content: str
    timestamp: Optional[str] = None


class Conversation(BaseModel):
    id: str
    title: str = "Untitled conversation"
    username: Optional[str] = ""
    platform: Literal["chatgpt", "claude"] = "claude"
    created_at: Optional[str] = ""
    updated_at: Optional[str] = ""
    messages: list[Message]



class ConversationEvent(BaseModel):
    event: str = "conversation.updated"
    platform: Literal["chatgpt", "claude"]
    thread_id: str
