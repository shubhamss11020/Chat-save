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

# Owner of this capture agent. No OS-username fallback: an unset identity is recorded as
# UNKNOWN_USER so a transcript is never filed under a real person by accident.
USERNAME = os.getenv("CHATSAVE_USER", "").strip()
UNKNOWN_USER = "unknown"
# Users allowed to search/read every person's transcripts over MCP (comma-separated).
# Everyone else only sees their own archive.
ADMIN_USERS = {u.strip().lower() for u in os.getenv("CHATSAVE_ADMIN_USERS", "").split(",") if u.strip()}
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
# Without any token the server refuses every request, unless you explicitly opt in to an
# open server for local development (CHATSAVE_ALLOW_OPEN=1).
ALLOW_OPEN = os.getenv("CHATSAVE_ALLOW_OPEN", "0") == "1"
# Browser origins allowed to call the API directly (comma-separated). Empty = none.
CORS_ORIGINS = [o.strip().rstrip("/") for o in os.getenv("CHATSAVE_CORS_ORIGINS", "").split(",") if o.strip()]

# --- S3 / Object Storage for attachments (images, PDFs, media) ---
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", os.getenv("AWS_S3_BUCKET", "")).strip()
S3_REGION = os.getenv("S3_REGION", os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))).strip()
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID", os.getenv("AWS_ACCESS_KEY_ID", "")).strip()
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY", os.getenv("AWS_SECRET_ACCESS_KEY", "")).strip()
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "").strip() or None  # Set for R2 or custom endpoint
S3_PUBLIC_URL_PREFIX = os.getenv("S3_PUBLIC_URL_PREFIX", "").strip().rstrip("/")
S3_PRESIGN_EXPIRATION_SECONDS = int(os.getenv("S3_PRESIGN_EXPIRATION_SECONDS", "3600"))
S3_ENABLED = bool(S3_BUCKET_NAME)

