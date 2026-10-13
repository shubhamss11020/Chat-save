"""MCP server: save-only. The capture agent calls this automatically; Claude never has to."""
import asyncio

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from . import gitstore
from .auth import current_user
from .config import ADMIN_USERS
from .models import Conversation, Message

mcp = FastMCP(
    "chat-save",
    instructions=(
        "MANDATORY TRANSCRIPT & ARTIFACT ARCHIVAL INSTRUCTIONS:\n"
        "1. UNIVERSAL AUTO-SAVE: You MUST call `save_chat_transcript` at the end of EVERY SINGLE RESPONSE.\n"
        "   - This applies to direct memory answers, simple explanations, follow-up questions, brainstorming, and code generation—NOT just web searches or tool-heavy turns.\n"
        "   - Never finish a response without invoking `save_chat_transcript`.\n"
        "2. THREAD CONTINUITY (CRITICAL): When continuing an ongoing conversation thread (even after hours or days), you MUST:\n"
        "   - Retain the EXACT SAME `id` and `title` established on the first turn.\n"
        "   - NEVER create a new conversation ID or new title for follow-up questions within the same chat.\n"
        "3. FULL CONVERSATION HISTORY: When calling `save_chat_transcript`, always include ALL prior turns (all user prompts and assistant replies in chronological order) in the `messages` array.\n"
        "4. EMBED FULL FILE & ARTIFACT CONTENTS: If you create, reference, or summarize markdown documents (e.g. `/home/claude/*.md`), comparison sheets, or code files, you MUST include the COMPLETE verbatim text of those files either inside the assistant message content or in the `files` argument ([{'name': '...', 'content': '...'}]). Never save only a file path without the file's body.\n"
        "5. You can also use search_chat_transcripts to find past conversations."
    ),
    stateless_http=True,
    json_response=True,
    max_request_body_size=64 * 1024 * 1024,
    # Host-header protection is for localhost servers; we sit behind a token instead.
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


# PREVIOUS MCP TOOL IMPLEMENTATION (COMMENTED OUT AS REQUESTED)
# The system now directly ingests via the REST API and commits to GitHub without LLM tool invocation:
#
# @mcp.tool()
# async def save_chat_transcript(
#     conversations: list[Conversation] | None = None,
#     thread_name: str | None = None,
#     content: str | None = None,
#     title: str | None = None,
#     messages: list[Message] | None = None,
#     files: list[dict] | None = None,
#     id: str | None = None,
# ) -> dict:
#     """Save or update full conversation transcripts and generated documents into the Git archive."""
#     user = current_user.get()
#     conv_list: list[Conversation] = []
#
#     if conversations:
#         conv_list = conversations
#     elif content or messages or thread_name or title or files:
#         t_name = title or thread_name or "conversation"
#         c_id = id or gitstore._slug(t_name)
#         msg_list: list[Message] = []
#         if messages:
#             msg_list = messages
#         elif content:
#             msg_list = gitstore._parse_existing_messages(content)
#             if not msg_list:
#                 msg_list = [Message(id="msg-1", role="user", content=content.strip())]
#         conv_list = [
#             Conversation(
#                 id=c_id,
#                 title=t_name,
#                 username=user or "shubham",
#                 platform="claude",
#                 messages=msg_list,
#                 files=files or [],
#             )
#         ]
#
#     for c in conv_list:
#         if user:
#             c.username = user
#         c.username = gitstore._normalize_username(c.username)
#
#     if not conv_list:
#         return {"saved": [], "failed": {"error": "No conversation content provided."}}
#
#     return await asyncio.to_thread(gitstore.save_batch, conv_list)


@mcp.tool()
async def checkpoint(thread_name: str = "conversation") -> str:
    """Lightweight turn checkpoint confirming the conversation thread."""
    return f"Checkpoint noted for thread '{thread_name}'."


DENIED = "Not allowed: you can only access your own transcripts."


def _scope(requested: str) -> tuple[bool, str]:
    """Decide which user's archive a read may touch. Returns (allowed, user_filter).

    - Open server (no auth configured) or an admin: any user, "" means everyone.
    - Anyone else: only their own archive, whatever `requested` says.
    """
    caller = gitstore._user_folder(current_user.get())
    requested = gitstore._user_folder(requested)
    if not caller or caller in ADMIN_USERS:
        return True, requested
    if requested and requested != caller:
        return False, caller
    return True, caller


@mcp.tool()
async def search_chat_transcripts(query: str, user: str = "") -> str:
    """Search saved Claude chat transcripts by topic, keyword, or content."""
    allowed, scope = _scope(user)
    if not allowed:
        return DENIED
    return await asyncio.to_thread(gitstore.search_transcripts, query, scope)


@mcp.tool()
async def list_chat_transcripts(user: str = "") -> str:
    """List all saved chat transcripts, newest first."""
    allowed, scope = _scope(user)
    if not allowed:
        return DENIED
    return await asyncio.to_thread(gitstore.list_transcripts, scope)


@mcp.tool()
async def get_chat_transcript(file_path: str) -> str:
    """Read the full content of a saved chat transcript."""
    allowed, scope = _scope("")
    if not allowed:
        return DENIED
    owner = scope or None  # None = admin/open server: any folder
    return await asyncio.to_thread(gitstore.get_transcript, file_path, owner)



