import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

STORAGE = Path(os.getenv("CHATSAVE_STORAGE", ROOT / "storage"))
STATE_DB = STORAGE / "capture.db"  # operational state: outbox + scan state

# Archive: markdown transcripts committed to git under raw_queries/
REPO_DIR = Path(os.getenv("CHATSAVE_REPO_DIR", ROOT))
GIT_DIR = REPO_DIR / "raw_queries"
GIT_REMOTE_URL = os.getenv("CHATSAVE_GIT_URL", "")  # empty = commit locally, no push
GIT_BRANCH = os.getenv("CHATSAVE_GIT_BRANCH", "main")
GIT_NAME = os.getenv("CHATSAVE_GIT_NAME", "")
GIT_EMAIL = os.getenv("CHATSAVE_GIT_EMAIL", "")

USERNAME = os.getenv("CHATSAVE_USER", os.getenv("USERNAME", "user"))
CLAUDE_PROJECTS = Path(os.getenv("CLAUDE_PROJECTS", Path.home() / ".claude" / "projects"))

RECONCILE_SECONDS = float(os.getenv("CHATSAVE_RECONCILE_SECONDS", "10"))
BATCH_SIZE = int(os.getenv("CHATSAVE_BATCH", "25"))
