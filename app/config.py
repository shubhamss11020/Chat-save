import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORAGE = Path(os.getenv("CHATSAVE_STORAGE", ROOT / "storage"))
DB_PATH = STORAGE / "conversations.db"
GIT_DIR = STORAGE / "conversations"
USERNAME = os.getenv("CHATSAVE_USER", os.getenv("USERNAME", "user"))
CLAUDE_PROJECTS = Path(os.getenv("CLAUDE_PROJECTS", Path.home() / ".claude" / "projects"))
POLL_SECONDS = float(os.getenv("CHATSAVE_POLL", "5"))
