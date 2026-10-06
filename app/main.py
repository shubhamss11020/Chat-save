import logging
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException

from . import db, ingest
from .models import Conversation, ConversationEvent
from .sources.claude_code import ClaudeSource
from .worker import Pipeline

logging.basicConfig(level=logging.INFO)
pipeline = Pipeline({"claude": ClaudeSource()})


@asynccontextmanager
async def lifespan(_: FastAPI):
    pipeline.start()
    yield
    pipeline.stop()


app = FastAPI(title="Chat-Save", lifespan=lifespan)
Platform = Literal["chatgpt", "claude", "all"]


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
