import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

STORAGE = Path(os.getenv("CHATSAVE_STORAGE", ROOT / "storage"))
DB_PATH = STORAGE / "conversations.db"

# Transcripts are committed into a git repo under raw_queries/.
# Locally that is the project repo; on Render set CHATSAVE_REPO_DIR to a clone dir.
REPO_DIR = Path(os.getenv("CHATSAVE_REPO_DIR", ROOT))
GIT_DIR = REPO_DIR / "raw_queries"
# GitHub repo URL (with token for private repos on Render) to pull from / push to
GIT_REMOTE_URL = os.getenv("CHATSAVE_GIT_URL", "")
GIT_BRANCH = os.getenv("CHATSAVE_GIT_BRANCH", "main")
GIT_NAME = os.getenv("CHATSAVE_GIT_NAME", "")
GIT_EMAIL = os.getenv("CHATSAVE_GIT_EMAIL", "")

USERNAME = os.getenv("CHATSAVE_USER", os.getenv("USERNAME", "user"))
CLAUDE_PROJECTS = Path(os.getenv("CLAUDE_PROJECTS", Path.home() / ".claude" / "projects"))
POLL_SECONDS = float(os.getenv("CHATSAVE_POLL", "5"))

# Retrieval-only deployments (Render) have no local Claude files to watch
WATCH = os.getenv("CHATSAVE_WATCH", "1") == "1"
# Seconds between `git pull` + reindex; 0 disables
PULL_SECONDS = float(os.getenv("CHATSAVE_PULL_SECONDS", "0"))
# If set, everything except /health requires it (Authorization: Bearer or ?key=)
AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN", "")
