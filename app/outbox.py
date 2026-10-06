"""Background outbox worker: pending snapshots -> git commits -> one push per batch."""
import logging

from . import gitstore, state
from .config import BATCH_SIZE

log = logging.getLogger("chatsave")


def drain() -> int:
    """Process due items. Returns number completed. Failures stay queued with backoff."""
    done = 0
    while True:
        batch = state.claim(BATCH_SIZE)
        if not batch:
            return done
        ok: list[int] = []
        try:
            gitstore.prepare()
            for item_id, conv in batch:
                try:
                    gitstore.commit_snapshot(conv)
                    ok.append(item_id)
                except Exception as e:
                    log.exception("commit failed for %s", conv.id)
                    state.fail([item_id], str(e))
            if ok:
                gitstore.push()  # commits already exist locally; a failed push retries safely
                state.complete(ok)
                done += len(ok)
                log.info("saved %d conversation(s)", len(ok))
        except Exception as e:
            log.warning("batch failed, will retry: %s", e)
            state.fail(ok or [i for i, _ in batch], str(e))
            return done
