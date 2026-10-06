from typing import Literal

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from . import db

# Host-header protection is for localhost servers; we sit behind Render + a token.
mcp = FastMCP(
    "chat-memory",
    instructions="Search and read the user's saved ChatGPT/Claude conversations.",
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)
Platform = Literal["chatgpt", "claude", "all"]


@mcp.tool()
def search_conversations(query: str, platform: Platform = "all",
                         username: str | None = None, limit: int = 10) -> list[dict]:
    """Full-text search over saved conversations. Returns threads with a snippet."""
    return db.search_threads(query, platform, username, limit)


@mcp.tool()
def list_conversations(platform: Platform = "all", username: str | None = None,
                       limit: int = 20) -> list[dict]:
    """List the most recently updated conversations."""
    return db.list_threads(platform, username, limit)


@mcp.tool()
def get_conversation(thread_id: str, platform: Platform = "all") -> dict:
    """Get the full transcript of a conversation by thread_id."""
    for p in ("claude", "chatgpt") if platform == "all" else (platform,):
        t = db.get_thread(p, thread_id)
        if t:
            return t
    return {"error": f"thread {thread_id} not found"}
