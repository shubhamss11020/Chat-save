"""Claude Code Stop hook: tell the capture agent a conversation just changed.

Fails open: never blocks or errors Claude, even if the agent is down (the agent's
periodic reconciliation will still pick the conversation up).
"""
import json
import os
import sys
import urllib.request

try:
    payload = json.load(sys.stdin)
    body = json.dumps({"platform": "claude", "thread_id": payload["session_id"]}).encode()
    url = os.getenv("CHATSAVE_URL", "http://127.0.0.1:8000") + "/events"
    req = urllib.request.Request(url, body, {"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=2).read()
except Exception:
    pass
sys.exit(0)
