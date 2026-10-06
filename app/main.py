import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI

from . import capture, outbox, state
from .config import GIT_DIR, RECONCILE_SECONDS
from .models import Conversation
from .models import ConversationEvent
from .sources.claude_code import ClaudeSource

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("chatsave")
controller = capture.CaptureController({"claude": ClaudeSource()})


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
    GIT_DIR.mkdir(parents=True, exist_ok=True)
    state.recover()
    task = asyncio.create_task(_loop(_tick, RECONCILE_SECONDS))
    yield
    task.cancel()


app = FastAPI(title="Chat-Save (capture only)", lifespan=lifespan)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/status")
def status():
    """Outbox counts and the latest errors (what is still waiting to be saved)."""
    return state.stats()


def _handle_event(ev: ConversationEvent):
    controller.capture(ev.platform, ev.thread_id)
    outbox.drain()


@app.post("/events", status_code=202)
def post_event(ev: ConversationEvent, bg: BackgroundTasks):
    """Lifecycle hook endpoint (e.g. Claude Code Stop hook). Returns immediately."""
    bg.add_task(_handle_event, ev)
    return {"queued": True}


@app.post("/conversations")
def save_conversation(conv: Conversation, bg: BackgroundTasks):
    """Manual fallback: push a full normalized transcript. Idempotent."""
    queued = capture.enqueue_snapshot(conv)
    bg.add_task(outbox.drain)
    return {"queued": queued}


@app.post("/reconcile")
def reconcile_now(bg: BackgroundTasks):
    bg.add_task(_tick)
    return {"started": True}
