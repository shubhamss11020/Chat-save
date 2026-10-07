import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI

from . import capture, outbox, state
from .auth import TokenAuth
from .config import CAPTURE, RECONCILE_SECONDS
from .mcp_server import mcp
from .models import Conversation, ConversationEvent
from .sources.claude_code import ClaudeSource
from .sources.claude_desktop import ClaudeDesktopSource

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("chatsave")

controller = capture.CaptureController({
    "claude": ClaudeSource(),
    "claude_desktop": ClaudeDesktopSource()
})
mcp_app = mcp.streamable_http_app()  # also creates mcp.session_manager


async def _loop(fn, seconds: float):
    while True:
        try:
            await asyncio.to_thread(fn)
        except Exception:
            log.exception("%s failed", getattr(fn, "__name__", fn))
        await asyncio.sleep(seconds)


def _tick():
    controller.reconcile()  # startup reconciliation = the first tick
    outbox.drain()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # 1. Startup Recovery: reset any processing records back to pending
    state.recover()
    # 2. Initial Reconcile & Outbox Drain
    if CAPTURE:
        try:
            await asyncio.to_thread(_tick)
        except Exception:
            log.exception("Startup reconciliation failed")
    # 3. Start periodic background capture & drain loop
    task = asyncio.create_task(_loop(_tick, RECONCILE_SECONDS)) if CAPTURE else None
    async with mcp.session_manager.run():
        yield
    if task:
        task.cancel()


app = FastAPI(title="Chat-Save", lifespan=lifespan)
app.add_middleware(TokenAuth)


@app.get("/health")
def health():
    return {"ok": True, "capture": CAPTURE}


@app.get("/status")
def status():
    """Canonical counts and outbox queue status."""
    return state.stats()


def _handle_event(ev: ConversationEvent):
    thread_id = ev.conversation_id or ev.thread_id or "unknown"
    controller.capture(ev.platform, thread_id)
    outbox.drain()


@app.post("/events", status_code=202)
def post_event(ev: ConversationEvent, bg: BackgroundTasks):
    """Lifecycle hook endpoint (e.g. Claude Code Stop hook). Returns immediately."""
    bg.add_task(_handle_event, ev)
    return {"queued": True}


@app.post("/conversations")
def save_conversation(conv: Conversation, bg: BackgroundTasks):
    """Save/update canonical conversation and drain outbox."""
    queued = capture.enqueue_snapshot(conv)
    bg.add_task(outbox.drain)
    return {"queued": queued}


@app.post("/reconcile")
def reconcile_now(bg: BackgroundTasks):
    bg.add_task(_tick)
    return {"started": True}


app.mount("/", mcp_app)  # serves /mcp; keep last so API routes win
