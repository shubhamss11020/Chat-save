import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

STORAGE = Path(os.getenv("CHATSAVE_STORAGE", ROOT / "storage"))
STATE_DB = STORAGE / "capture.db"  # operational state: outbox + scan state

# Archive: markdown transcripts committed to git under raw_queries/
REPO_DIR = Path(os.getenv("CHATSAVE_REPO_DIR", str(ROOT)))
GIT_DIR = REPO_DIR / "raw_queries"
GIT_REMOTE_URL = "".join(os.getenv("CHATSAVE_GIT_URL", "").split()).rstrip("/")  # empty = commit locally, no push
GIT_BRANCH = os.getenv("CHATSAVE_GIT_BRANCH", "main").strip()
GIT_NAME = os.getenv("CHATSAVE_GIT_NAME", "").strip()
GIT_EMAIL = os.getenv("CHATSAVE_GIT_EMAIL", "").strip()

USERNAME = os.getenv("CHATSAVE_USER", os.getenv("USERNAME", "user")).strip()
CLAUDE_PROJECTS = Path(os.getenv("CLAUDE_PROJECTS", str(Path.home() / ".claude" / "projects")))

RECONCILE_SECONDS = float(os.getenv("CHATSAVE_RECONCILE_SECONDS", "10"))
BATCH_SIZE = int(os.getenv("CHATSAVE_BATCH", "25"))

# --- roles -------------------------------------------------------------------
# Capture agent (runs on your PC): watches Claude's files, delivers via the outbox.
CAPTURE = os.getenv("CHATSAVE_CAPTURE", "1") == "1"
# If set, the agent delivers each transcript to this MCP server (save_chat_transcript)
# instead of writing Git itself. Example: https://chat-save.onrender.com/mcp
MCP_URL = "".join(os.getenv("CHATSAVE_MCP_URL", "").split()).rstrip("/")
# MCP server (e.g. on Render): requires this token (Bearer header or ?key=). The agent
# sends the same value. Empty = no auth.
AUTH_TOKEN = "".join(os.getenv("MCP_AUTH_TOKEN", "").split())

