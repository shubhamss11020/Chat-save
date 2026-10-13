"""Background outbox worker: pending conversations -> local Git archive -> completed."""
import logging
import threading
import time

from . import gitstore, state
from .config import BATCH_SIZE

log = logging.getLogger("chatsave")
_drain_lock = threading.Lock()  # hook events and the periodic tick must not claim twice


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
            result = gitstore.save_batch([c for _, c in batch])
        except Exception as e:  # Git unreachable: nothing is lost, retry later
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
        if ok:
            state.set_sig("archive", "last_commit", str(time.time()))  # for /status monitoring
        done += len(ok)
        log.info("saved %d conversation(s) to the archive", len(ok))
