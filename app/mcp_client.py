"""Capture agent -> MCP server delivery (automatic; no LLM involved)."""
import asyncio
import json
from datetime import timedelta

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from .config import AUTH_TOKEN, MCP_URL
from .models import Conversation


async def _save(convs: list[Conversation]) -> dict:
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else None
    async with streamablehttp_client(MCP_URL, headers=headers, timeout=60) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool(
                "save_chat_transcript",
                {"conversations": [json.loads(c.model_dump_json()) for c in convs]},
                read_timeout_seconds=timedelta(minutes=5))
            text = "".join(getattr(b, "text", "") for b in res.content)
            if res.isError:
                raise RuntimeError(f"MCP save failed: {text[:300]}")
            return res.structuredContent or json.loads(text)


def save_batch(convs: list[Conversation]) -> dict:
    try:
        return asyncio.run(_save(convs))
    except BaseExceptionGroup as eg:  # surface the real cause (e.g. connection refused)
        leaf = eg
        while isinstance(leaf, BaseExceptionGroup):
            leaf = leaf.exceptions[0]
        raise RuntimeError(f"MCP server unreachable: {leaf!r}") from None
