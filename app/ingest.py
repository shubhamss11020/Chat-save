import hashlib

from . import db, gitstore
from .models import Conversation


def content_hash(conv: Conversation) -> str:
    h = hashlib.sha256(conv.id.encode())
    for m in conv.messages:
        h.update(f"\0{m.role}\0{m.content}".encode())
    return h.hexdigest()


def save(conv: Conversation) -> str:
    """Idempotent: returns 'unchanged' or 'saved'."""
    h = content_hash(conv)
    if db.get_hash(conv.platform, conv.id) == h:
        return "unchanged"
    rel = gitstore.write(conv)
    db.upsert(conv, h, rel)
    return "saved"


def index_only(conv: Conversation, git_path: str) -> str:
    """Index a transcript that already lives in git (no write/commit)."""
    h = content_hash(conv)
    if db.get_hash(conv.platform, conv.id) == h:
        return "unchanged"
    db.upsert(conv, h, git_path)
    return "indexed"
