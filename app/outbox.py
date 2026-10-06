"""Background outbox worker: pending snapshots -> MCP server (or local Git) -> completed."""
import logging
import threading

from . import gitstore, mcp_client, state
from .config import BATCH_SIZE, MCP_URL

log = logging.getLogger("chatsave")
_drain_lock = threading.Lock()  # hook events and the periodic tick must not claim twice


def _deliver(convs) -> dict:
    return mcp_client.save_batch(convs) if MCP_URL else gitstore.save_batch(convs)


def drain() -> int:
    """Deliver due items. Returns number completed. Failures stay queued with backoff."""
    with _drain_lock:
        return _drain()


def _drain() -> int:
    done = 0
    while True:
        batch = state.claim(BATCH_SIZE)
        if not batch:
            return done
        try:
            result = _deliver([c for _, c in batch])
        except Exception as e:  # server/Git unreachable: nothing is lost, retry later
            log.warning("delivery failed, will retry: %s", e)
            state.fail([i for i, _ in batch], str(e))
            return done
        saved = set(result.get("saved", []))
        failed = result.get("failed", {})
        ok = [i for i, c in batch if c.id in saved]
        for i, c in batch:
            if c.id not in saved:
                state.fail([i], failed.get(c.id, "not saved"))
        state.complete(ok)
        done += len(ok)
        log.info("saved %d conversation(s) via %s", len(ok), "MCP" if MCP_URL else "Git")
