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


class ExtensionIngestPayload(BaseModel):
    client_id: Optional[str] = "unknown"
    user_id: Optional[str] = None
    conversation_id: str
    title: Optional[str] = "Untitled conversation"
    platform: Literal["chatgpt", "claude"] = "claude"
    url: Optional[str] = None
    messages: list[Message] = Field(default_factory=list)
    files: list[dict] = Field(default_factory=list)
    is_final: bool = True
    captured_at: Optional[str] = None


class ExtensionHeartbeat(BaseModel):
    client_id: str
    user_id: Optional[str] = None
    extension_version: Optional[str] = "1.0.0"
    browser: Optional[str] = "Chrome"
    pending_queue_count: int = 0
    last_successful_sync: Optional[str] = None
    last_error: Optional[str] = None
    active_tab_url: Optional[str] = None


class ExtensionIngestResponse(BaseModel):
    receipt_id: str
    conversation_id: str
    saved_messages: int
    status: str
    timestamp: str
    deduplicated: bool = False
