"""MCP server: save-only. The capture agent calls this automatically; Claude never has to."""
import asyncio

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from . import gitstore
from .auth import current_user
from .models import Conversation

mcp = FastMCP(
    "chat-save",
    instructions="Saves conversation transcripts to Git. Normally called by the capture "
                 "agent, not by the model.",
    stateless_http=True,
    json_response=True,
    max_request_body_size=64 * 1024 * 1024,
    # Host-header protection is for localhost servers; we sit behind a token instead.
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


@mcp.tool()
async def save_chat_transcript(conversations: list[Conversation]) -> dict:
    """Save or update full conversation transcripts as markdown in the Git archive.

    Idempotent: re-sending an unchanged conversation creates no new commit.
    Returns {"saved": [ids], "failed": {id: error}}.
    """
    user = current_user.get()
    if user:
        for c in conversations:
            if not c.username or c.username in ("user", "unknown", "rajat"):
                c.username = user
    return await asyncio.to_thread(gitstore.save_batch, conversations)

