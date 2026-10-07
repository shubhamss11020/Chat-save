"""Canonical domain models for Chat-Save."""
from typing import Literal, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    id: str
    conversation_id: Optional[str] = ""
    sequence: Optional[int] = 0
    role: Literal["user", "assistant", "tool", "system"] = "user"
    content: str
    timestamp: Optional[str] = None
    content_hash: Optional[str] = None


class Conversation(BaseModel):
    id: str
    platform: Literal["chatgpt", "claude"] = "claude"
    external_conversation_id: Optional[str] = None
    user_id: Optional[str] = "shubham"
    username: Optional[str] = "shubham"
    title: str = "Untitled conversation"
    created_at: Optional[str] = ""
    updated_at: Optional[str] = ""
    last_message_sequence: Optional[int] = 0
    status: Optional[str] = "active"
    messages: list[Message] = Field(default_factory=list)
    files: list[dict] = Field(default_factory=list)


class ConversationEvent(BaseModel):
    event_type: str = "conversation.updated"
    platform: Literal["chatgpt", "claude"] = "claude"
    conversation_id: str
    message_id: Optional[str] = None
    turn_number: Optional[int] = None
    role: Literal["user", "assistant", "tool", "system"] = "user"
    content: str = ""
    created_at: Optional[str] = None
    thread_id: Optional[str] = None  # alias for backward compat
