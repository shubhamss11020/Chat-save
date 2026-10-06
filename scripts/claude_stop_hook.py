"""Claude Code Stop hook: tell the capture agent a conversation just changed.

Fails open: never blocks or errors Claude, even if the agent is down (the agent's
periodic reconciliation will still pick the conversation up).
"""
import json
import os
import sys
import urllib.request
from pathlib import Path


def _token() -> str:
    if os.getenv("MCP_AUTH_TOKEN"):
        return os.environ["MCP_AUTH_TOKEN"]
    env = Path(__file__).resolve().parent.parent / ".env"
    for line in env.read_text(encoding="utf-8").splitlines():
        if line.startswith("MCP_AUTH_TOKEN="):
            return line.split("=", 1)[1].strip()
    return ""


try:
    payload = json.load(sys.stdin)
    body = json.dumps({"platform": "claude", "thread_id": payload["session_id"]}).encode()
    headers = {"Content-Type": "application/json"}
    try:
        if t := _token():
            headers["Authorization"] = f"Bearer {t}"
    except OSError:
        pass
    url = os.getenv("CHATSAVE_URL", "http://127.0.0.1:8000") + "/events"
    urllib.request.urlopen(urllib.request.Request(url, body, headers), timeout=2).read()
except Exception:
    pass
sys.exit(0)
