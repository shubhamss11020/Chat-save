"""Per-user request limit for ingest, so one client cannot flood the archive.

Sliding window kept in memory. Good enough for one server instance; a multi-instance
deployment would move the counters to a shared store.
"""
import threading
import time
from collections import deque


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_seconds: float = 60.0):
        self.limit = limit
        self.window = window_seconds
        self._hits: dict[str, deque] = {}
        self._lock = threading.Lock()

    def check(self, key: str) -> float:
        """Record one request for `key`. Returns 0.0 if allowed, else seconds to wait."""
        if self.limit <= 0:
            return 0.0
        now = time.monotonic()
        with self._lock:
            hits = self._hits.setdefault(key, deque())
            while hits and now - hits[0] > self.window:
                hits.popleft()
            if len(hits) >= self.limit:
                return max(0.0, self.window - (now - hits[0]))
            hits.append(now)
            return 0.0
