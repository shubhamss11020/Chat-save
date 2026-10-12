import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException

from . import capture, outbox, s3, state
from .auth import TokenAuth, current_user
from .config import CAPTURE, RECONCILE_SECONDS
from .mcp_server import mcp
from .models import (
    Conversation,
    ConversationEvent,
    ExtensionHeartbeat,
    ExtensionIngestPayload,
    ExtensionIngestResponse,
    PresignUploadRequest,
    PresignUploadResponse,
)
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


@app.post("/api/extension/ingest", response_model=ExtensionIngestResponse)
def extension_ingest(payload: ExtensionIngestPayload, bg: BackgroundTasks):
    """Ingest endpoint for managed browser extension.
    
    Accepts full or incremental conversation turns captured from Claude Team web UI.
    Deduplicates and persists atomically, triggers async outbox drain to Git,
    and returns a save receipt with deduplication status.
    """
    effective_user = current_user.get() or payload.user_id or ""
    receipt = state.ingest_extension(payload, effective_user=effective_user)
    bg.add_task(outbox.drain)
    return receipt


@app.post("/api/extension/heartbeat")
def extension_heartbeat(hb: ExtensionHeartbeat):
    """Health & connection heartbeat reported by browser extensions."""
    effective_user = current_user.get() or hb.user_id or "user"
    state.record_heartbeat(
        client_id=hb.client_id,
        user_id=effective_user,
        extension_version=hb.extension_version or "1.0.0",
        browser=hb.browser or "Chrome",
        pending_queue_count=hb.pending_queue_count,
        last_successful_sync=hb.last_successful_sync,
        last_error=hb.last_error,
    )
    return {"ok": True, "client_id": hb.client_id}


@app.get("/api/extension/clients")
def list_extension_clients():
    """List all reporting browser extensions and their telemetry for monitoring."""
    return {"clients": state.get_heartbeats()}


@app.post("/api/outbox/retry-dlq")
def retry_dead_letter_queue(bg: BackgroundTasks):
    """Re-queue all dead_letter outbox items back to pending and drain."""
    requeued = state.retry_dead_letter()
    if requeued > 0:
        bg.add_task(outbox.drain)
    return {"requeued": requeued}


@app.post("/reconcile")
def reconcile_now(bg: BackgroundTasks):
    bg.add_task(_tick)
    return {"started": True}


@app.get("/api/attachments/status")
def attachment_storage_status():
    """Check if S3 attachment storage is configured and active."""
    return {
        "s3_configured": s3.is_s3_configured(),
        "bucket": s3.S3_BUCKET_NAME,
        "region": s3.S3_REGION,
        "endpoint": s3.S3_ENDPOINT_URL,
    }


@app.post("/api/attachments/presign", response_model=PresignUploadResponse)
def presign_attachment_upload(req: PresignUploadRequest):
    """Generate a presigned PUT URL for direct browser-to-S3 upload."""
    if not s3.is_s3_configured():
        raise HTTPException(
            status_code=503,
            detail="S3 storage is not configured on the server. Set S3_BUCKET_NAME in environment."
        )
    effective_user = current_user.get() or "user"
    try:
        data = s3.generate_presigned_upload_url(
            filename=req.filename,
            content_type=req.content_type,
            conversation_id=req.conversation_id or "default",
            user_id=effective_user,
        )
        return data
    except Exception as e:
        log.exception("Failed to generate presigned upload URL")
        raise HTTPException(status_code=500, detail=str(e))


app.mount("/", mcp_app)  # serves /mcp; keep last so API routes win
