"""Git writer: snapshot -> markdown file -> commit (-> push). Knows nothing about capture."""
import re
import shutil
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .config import GIT_BRANCH, GIT_DIR, GIT_EMAIL, GIT_NAME, GIT_REMOTE_URL, REPO_DIR, ROOT, USERNAME
from .models import Conversation, Message

EASTERN = ZoneInfo("America/New_York")
_lock = threading.Lock()  # one git operation at a time (agent worker + MCP requests)


class GitError(RuntimeError):
    pass


def _slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")[:80] or "unknown"


def _normalize_username(uname: str) -> str:
    """Normalize username into canonical lowercase folder name. Defaults to 'shubham'."""
    if not uname:
        return "shubham"
    u = uname.strip().lower()
    u = re.sub(r"[^a-z0-9]+", "-", u).strip("-")
    if u in ("user", "unknown", "rajat", "rajat-jain") or u.startswith("shubham"):
        return "shubham"
    return u or "shubham"


def _git(*args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    ident = (["-c", f"user.name={GIT_NAME}", "-c", f"user.email={GIT_EMAIL}"]
             if GIT_NAME and GIT_EMAIL else [])
    return subprocess.run(["git", "-C", str(REPO_DIR), *ident, *args],
                          capture_output=True, text=True, timeout=timeout)


def _check(r: subprocess.CompletedProcess, what: str) -> subprocess.CompletedProcess:
    if r.returncode:
        raise GitError(f"{what}: {(r.stderr or r.stdout).strip()}")
    return r


def _q(v: str) -> str:
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def render(conv: Conversation, created_at: str = "", updated_at: str = "") -> str:
    uname = _normalize_username(conv.username or USERNAME)
    c_at = created_at or conv.created_at or ""
    u_at = updated_at or conv.updated_at or ""
    out = ["---",
           f"conversation_id: {conv.id}",
           f"platform: {conv.platform}",
           f"username: {_q(uname)}",
           f"title: {_q(conv.title)}",
           f"created_at: {_q(c_at)}",
           f"updated_at: {_q(u_at)}",
           "---", "", f"# {conv.title}", ""]
    for m in conv.messages:
        who = {"user": "User", "assistant": "Claude"}.get(m.role, m.role.title())
        t = m.timestamp
        if not t or "00:00:00" in t:
            t = u_at
        out += [f"## {who}" + (f" ({t})" if t else ""), "", m.content, ""]
    return "\n".join(out)


def rel_path(conv: Conversation) -> str:
    # Use title for filename so it's human-readable on GitHub
    uname = _normalize_username(conv.username or USERNAME)
    name_slug = _slug(conv.title) if conv.title and conv.title.lower() != "untitled conversation" else _slug(conv.id)
    return f"{uname}/{conv.platform}/{name_slug}.md"


def _parse_existing_messages(text: str) -> list[Message]:
    """Parse existing markdown messages into a list of Message objects."""
    messages = []
    sections = re.split(r'(?m)^## (User|Claude|Assistant)(?: \((.*?)\))?\s*$', text)
    if len(sections) < 3:
        return []
    idx = 1
    msg_num = 1
    while idx < len(sections) - 2:
        raw_role = sections[idx].lower()
        role = "user" if raw_role == "user" else "assistant"
        ts = sections[idx + 1] or None
        body = sections[idx + 2].strip()
        if body:
            messages.append(Message(id=f"msg-prev-{msg_num}", role=role, content=body, timestamp=ts))
            msg_num += 1
        idx += 3
    return messages


def _merge_messages(existing: list[Message], incoming: list[Message]) -> list[Message]:
    """Merge existing transcript messages with incoming messages, preserving full history."""
    if not existing:
        return incoming
    if not incoming:
        return existing
    merged = list(existing)
    existing_contents = [m.content.strip() for m in existing]
    for inc in incoming:
        if inc.content.strip() in existing_contents:
            continue
        merged.append(inc)
        existing_contents.append(inc.content.strip())
    return merged


def _find_existing_thread_file(conv: Conversation) -> Path | None:
    """Find if a file already exists for this thread by matching id, title, or message content."""
    uname = _normalize_username(conv.username or USERNAME)
    search_dirs = [GIT_DIR / uname / conv.platform]
    legacy_user_dir = GIT_DIR / "user" / conv.platform
    if legacy_user_dir.exists() and legacy_user_dir not in search_dirs:
        search_dirs.append(legacy_user_dir)

    all_files: list[Path] = []
    for d in search_dirs:
        if d.exists():
            all_files.extend(sorted(d.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True))

    if not all_files:
        return None

    # 1. Direct slug / filename match
    target_slug = _slug(conv.title) if conv.title and conv.title.lower() != "untitled conversation" else _slug(conv.id)
    for f in all_files:
        if f.stem == target_slug or f.stem == _slug(conv.id):
            return f

    # 2. Match conversation_id in YAML frontmatter
    if conv.id:
        for f in all_files:
            try:
                txt = f.read_text(encoding="utf-8")
                if f'conversation_id: "{conv.id}"' in txt or f'conversation_id: {conv.id}' in txt:
                    return f
            except Exception:
                continue

    # 3. Match message content: check if ANY incoming message snippet is already in the existing file
    snippets: list[str] = []
    for m in conv.messages:
        content_clean = m.content.strip()
        if len(content_clean) >= 20:
            snippets.append(content_clean[:80])

    if snippets:
        for f in all_files:
            try:
                txt = f.read_text(encoding="utf-8")
                for snip in snippets:
                    if snip in txt:
                        return f
            except Exception:
                continue

    return None


def commit_snapshot(conv: Conversation) -> None:
    """Write + commit one transcript. Merges new turns into existing file if present."""
    uname = _normalize_username(conv.username or USERNAME)
    existing_file = _find_existing_thread_file(conv)

    if existing_file:
        rel = f"{uname}/{conv.platform}/{existing_file.name}"
        path = GIT_DIR / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if existing_file.resolve() != path.resolve() and existing_file.exists():
            try:
                old_rel = existing_file.relative_to(GIT_DIR)
                existing_file.unlink()
                _git("rm", "-f", "--", f"raw_queries/{old_rel}")
            except Exception:
                pass
    else:
        rel = rel_path(conv)
        path = GIT_DIR / rel
        path.parent.mkdir(parents=True, exist_ok=True)

    now_est = datetime.now(EASTERN).strftime("%Y-%m-%d %H:%M:%S %Z")
    created_at = None
    existing_messages: list[Message] = []

    if path.exists():
        try:
            old_text = path.read_text(encoding="utf-8")
            m = re.search(r'^created_at:\s*(.+)$', old_text, re.MULTILINE)
            if m:
                created_at = m.group(1).strip().strip('"\'')
            existing_messages = _parse_existing_messages(old_text)
        except Exception:
            pass

    if not created_at or "00:00:00" in created_at:
        if conv.created_at and "00:00:00" not in conv.created_at:
            created_at = conv.created_at
        else:
            created_at = now_est

    updated_at = now_est

    # Merge incoming messages with any existing messages in the thread
    merged_messages = _merge_messages(existing_messages, conv.messages)
    conv.messages = merged_messages

    rendered_text = render(conv, created_at=created_at, updated_at=updated_at)
    path.write_text(rendered_text, encoding="utf-8", newline="\n")

    full = f"raw_queries/{rel}"
    _check(_git("add", "--", full), "git add")
    if _git("diff", "--cached", "--quiet", "--", full).returncode == 0:
        return  # identical to what is already committed
    _check(_git("commit", "-m", f"{conv.platform}: {conv.title} ({conv.id[:8]})", "--", full),
           "git commit")


def prepare() -> None:
    if not shutil.which("git"):
        raise GitError("git is not installed")
    if not (REPO_DIR / ".git").exists():
        if GIT_REMOTE_URL and REPO_DIR.resolve() != ROOT.resolve():
            # hosted server: its working copy is a clone of the archive repo
            REPO_DIR.parent.mkdir(parents=True, exist_ok=True)
            _check(subprocess.run(["git", "clone", GIT_REMOTE_URL, str(REPO_DIR)],
                                  capture_output=True, text=True, timeout=300), "git clone")
        else:
            REPO_DIR.mkdir(parents=True, exist_ok=True)
            _check(_git("init", "-b", GIT_BRANCH), "git init")
    if GIT_REMOTE_URL:
        cur = _git("remote", "get-url", "origin")
        if cur.returncode:
            _check(_git("remote", "add", "origin", GIT_REMOTE_URL), "git remote add")
        elif cur.stdout.strip() != GIT_REMOTE_URL:
            _check(_git("remote", "set-url", "origin", GIT_REMOTE_URL), "git remote set-url")


def push() -> None:
    """Push all local commits. Raises on failure so the batch is retried later."""
    if not GIT_REMOTE_URL:
        return
    _git("pull", "--rebase", "--autostash", "origin", GIT_BRANCH)  # best effort (new repo: no-op)
    _check(_git("push", "-u", "origin", f"HEAD:{GIT_BRANCH}"), "git push")


def save_batch(convs: list[Conversation]) -> dict:
    """Commit every snapshot, then push once. Per-conversation commit errors are reported
    in 'failed'; a push failure raises so the whole batch is retried (commits are idempotent).
    """
    with _lock:
        prepare()
        saved, failed = [], {}
        for c in convs:
            try:
                commit_snapshot(c)
                saved.append(c.id)
            except Exception as e:
                failed[c.id] = str(e)
        if saved:
            push()
        return {"saved": saved, "failed": failed}


def search_transcripts(query: str, user: str = "") -> str:
    """Search saved markdown transcripts by keyword, title, or content."""
    with _lock:
        prepare()
        if not GIT_DIR.exists():
            return "No transcripts saved yet."
        u = _normalize_username(user) if user else ""
        target_dir = GIT_DIR / u if u and u != "user" else GIT_DIR
        if not target_dir.exists():
            return f"No transcripts found for user '{user}'."
        files = sorted(target_dir.rglob("*.md"), reverse=True)
        if not files:
            return "No transcripts found."
        q = query.lower()
        results = []
        for path in files:
            try:
                content = path.read_text(encoding="utf-8")
                lines = content.splitlines()
                matches = []
                for i, line in enumerate(lines):
                    if q in line.lower():
                        start = max(0, i - 1)
                        end = min(len(lines), i + 3)
                        matches.append("\n".join(lines[start:end]))
                if matches:
                    rel = path.relative_to(REPO_DIR)
                    results.append(f"### {rel}\n" + "\n---\n".join(matches[:3]))
            except Exception:
                continue
        if not results:
            return f"No results for '{query}'."
        return f"Total results for '{query}': {len(results)}\n\n" + "\n\n".join(results[:10])


def list_transcripts(user: str = "") -> str:
    """List all saved markdown transcripts, newest first."""
    with _lock:
        prepare()
        if not GIT_DIR.exists():
            return "No transcripts saved yet."
        u = _normalize_username(user) if user else ""
        target_dir = GIT_DIR / u if u and u != "user" else GIT_DIR
        if not target_dir.exists():
            return f"No transcripts found for user '{user}'."
        files = sorted(target_dir.rglob("*.md"), reverse=True)
        if not files:
            return "No transcripts saved yet."
        lines = []
        for f in files[:100]:
            rel = str(f.relative_to(REPO_DIR))
            lines.append(f"- [{f.stem}]({rel})")
        return f"Total saved transcripts: {len(files)}\n\n" + "\n".join(lines)


def get_transcript(file_path: str) -> str:
    """Read a transcript by relative path."""
    with _lock:
        prepare()
        p = REPO_DIR / file_path if not file_path.startswith(str(REPO_DIR)) else Path(file_path)
        if not p.exists():
            p = GIT_DIR / file_path
        if not p.exists():
            return f"File not found: {file_path}"
        return p.read_text(encoding="utf-8")
