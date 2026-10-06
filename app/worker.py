"""Event queue + background worker + polling watcher."""
import asyncio
import logging

from . import ingest
from .config import POLL_SECONDS
from .models import ConversationEvent
from .sources.base import ConversationSource

log = logging.getLogger("chatsave")


class Pipeline:
    def __init__(self, sources: dict[str, ConversationSource]):
        self.sources = sources
        self.queue: asyncio.Queue[ConversationEvent] = asyncio.Queue()
        self._tasks: list[asyncio.Task] = []

    def submit(self, ev: ConversationEvent) -> None:
        self.queue.put_nowait(ev)  # returns immediately

    async def _worker(self):
        while True:
            ev = await self.queue.get()
            try:
                src = self.sources.get(ev.platform)
                conv = await asyncio.to_thread(src.get_conversation, ev.thread_id) if src else None
                if conv:
                    r = await asyncio.to_thread(ingest.save, conv)
                    log.info("%s %s -> %s", ev.platform, ev.thread_id[:8], r)
            except Exception:
                log.exception("failed to process %s", ev)
            finally:
                self.queue.task_done()

    async def _watch(self):
        while True:
            for src in self.sources.values():
                try:
                    for ev in await asyncio.to_thread(src.detect_changes):
                        self.submit(ev)
                except Exception:
                    log.exception("watcher failed")
            await asyncio.sleep(POLL_SECONDS)

    def start(self):
        self._tasks = [asyncio.create_task(self._worker()), asyncio.create_task(self._watch())]

    def stop(self):
        for t in self._tasks:
            t.cancel()
