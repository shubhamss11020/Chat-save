import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException

from . import db, gitsync, ingest
from .auth import TokenAuth
from .config import PULL_SECONDS, WATCH
from .mcp_server import mcp
from .models import Conversation, ConversationEvent
from .sources.claude_code import ClaudeSource
from .worker import Pipeline

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("chatsave")
pipeline = Pipeline({"claude": ClaudeSource()} if WATCH else {})
mcp_app = mcp.streamable_http_app()  # also creates mcp.session_manager


async def _pull_loop():
    while True:
        await asyncio.sleep(PULL_SECONDS)
        try:
            await asyncio.to_thread(gitsync.sync)
        except Exception:
            log.exception("periodic sync failed")


@asynccontextmanager
async def lifespan(_: FastAPI):
    log.info("startup sync: %d threads indexed", await asyncio.to_thread(gitsync.sync))
    pipeline.start()
    puller = asyncio.create_task(_pull_loop()) if PULL_SECONDS else None
    async with mcp.session_manager.run():
        yield
    if puller:
        puller.cancel()
    pipeline.stop()


app = FastAPI(title="Chat-Save", lifespan=lifespan)
app.add_middleware(TokenAuth)
Platform = Literal["chatgpt", "claude", "all"]


@app.get("/health")
def health():
    return {"ok": True}


# --- capture side -----------------------------------------------------------
@app.post("/events", status_code=202)
def post_event(ev: ConversationEvent):
    """Hook endpoint: queue a 'conversation changed' event and return immediately."""
    pipeline.submit(ev)
    return {"queued": True}


@app.post("/conversations")
def save_conversation(conv: Conversation):
    """Push a full normalized transcript (manual / fallback path). Idempotent."""
    return {"status": ingest.save(conv)}


@app.post("/sync")
async def sync_now():
    """Pull the transcript repo and reindex."""
    return {"indexed": await asyncio.to_thread(gitsync.sync)}


# --- retrieval side (mirrors the MCP tools) ---------------------------------
@app.get("/conversations")
def list_conversations(platform: Platform = "all", username: str | None = None, limit: int = 20):
    return db.list_threads(platform, username, limit)


@app.get("/search")
def search_conversations(query: str, platform: Platform = "all",
                         username: str | None = None, limit: int = 10):
    return db.search_threads(query, platform, username, limit)


@app.get("/conversations/{platform}/{thread_id}")
def get_conversation(platform: Literal["chatgpt", "claude"], thread_id: str):
    t = db.get_thread(platform, thread_id)
    if not t:
        raise HTTPException(404, "not found")
    return t


app.mount("/", mcp_app)  # serves /mcp; keep last so API routes win
