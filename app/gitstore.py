import base64
import os
import re
import shutil
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from typing import Optional

from . import s3, state
from .config import GIT_BRANCH, GIT_DIR, GIT_EMAIL, GIT_NAME, GIT_REMOTE_URL, REPO_DIR, ROOT, UNKNOWN_USER, USERNAME
from .models import Conversation, Message

EASTERN = ZoneInfo("America/New_York")
_lock = threading.Lock()  # one git operation at a time (agent worker + MCP requests)


class GitError(RuntimeError):
    pass


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", s.lower()).strip("-")[:80] or "unknown"


def _format_to_edt(val: Optional[str]) -> str:
    """Convert any UTC/ISO timestamp or datetime string into clean Eastern Time (EDT/EST)."""
    if not val:
        return ""
    val_clean = str(val).strip().strip('"\'')
    if "EDT" in val_clean or "EST" in val_clean:
        return val_clean
    try:
        iso_str = val_clean.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        dt_edt = dt.astimezone(EASTERN)
        return dt_edt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return val_clean


def _user_folder(uname: Optional[str]) -> str:
    """Canonical folder name for a user, with no fallback: domain dropped, unsafe chars -> '-'.
    Use this to compare identities. Use _normalize_username to decide where to write."""
    u = (uname or "").strip().lower()
    if "@" in u:
        u = u.split("@")[0]
    return re.sub(r"[^a-z0-9_-]+", "-", u).strip("-")


def _normalize_username(uname: Optional[str]) -> str:
    """Folder to write to. Missing or placeholder identities go to the owner, or 'unknown'."""
    if not uname:
        return USERNAME or UNKNOWN_USER
    u = _user_folder(uname)
    if u in ("user", "unknown", "none", "null", ""):
        return USERNAME or UNKNOWN_USER
    return u


def _git(*args: str, timeout: int = 15) -> subprocess.CompletedProcess:
    ident = (["-c", f"user.name={GIT_NAME}", "-c", f"user.email={GIT_EMAIL}"]
             if GIT_NAME and GIT_EMAIL else [])
    env = {
        **os.environ,
        "GIT_TERMINAL_PROMPT": "0",
        "GCM_INTERACTIVE": "never",
        "GIT_ASKPASS": "echo",
    }
    return subprocess.run(["git", "-C", str(REPO_DIR), *ident, *args],
                          capture_output=True, text=True, timeout=timeout, env=env)


def _check(r: subprocess.CompletedProcess, what: str) -> subprocess.CompletedProcess:
    if r.returncode:
        raise GitError(f"{what}: {(r.stderr or r.stdout).strip()}")
    return r


def _q(v: str) -> str:
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def render(conv: Conversation, created_at: str = "", updated_at: str = "") -> str:
    uname = _normalize_username(conv.username or conv.user_id or USERNAME)
    raw_c_at = created_at or conv.created_at or ""
    raw_u_at = updated_at or conv.updated_at or ""
    c_at = _format_to_edt(raw_c_at) or raw_c_at
    u_at = _format_to_edt(raw_u_at) or raw_u_at
    out = ["---",
           f"conversation_id: {conv.id}",
           f"platform: {conv.platform}",
           f"username: {_q(uname)}",
           f"title: {_q(conv.title)}",
           f"created_at: {_q(c_at)}",
           f"updated_at: {_q(u_at)}",
           "---", "", f"# {conv.title}", ""]
    name_slug = _slug(conv.title) if conv.title and conv.title.lower() != "untitled conversation" else _slug(conv.id)
    files_folder = f"{name_slug}_files"

    for idx, m in enumerate(conv.messages, start=1):
        content = m.content.strip() if m.content else ""
        if not content:
            continue
        # Strip Anthropic unsupported tool widget placeholder banners and empty code blocks
        content = re.sub(r'(?ms)```[a-zA-Z0-9_-]*\s*This block is not supported on your current device yet\.?\s*```', '', content)
        content = re.sub(r'(?mi)^\s*This block is not supported on your current device yet\.?\s*$', '', content)
        while re.search(r'(?ms)```[a-zA-Z0-9_-]*\s*```', content):
            content = re.sub(r'(?ms)```[a-zA-Z0-9_-]*\s*```', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content).strip()
        if not content:
            continue
        who = {"user": "User", "assistant": "Claude"}.get(m.role, m.role.title())
        # Deduplicate consecutive identical messages
        if out and len(out) >= 4 and out[-2] == content and out[-4].startswith(f"## {who}"):
            continue
        t = _format_to_edt(m.timestamp) if m.timestamp else u_at
        if not t or "00:00:00" in t:
            t = u_at
        out += [f"## {who}" + (f" ({t})" if t else ""), "", content, ""]

        # Attachments belonging to this turn
        turn_attachments = [
            f for f in (conv.files or [])
            if f.get("is_attachment") and (
                f.get("turn_sequence") == m.sequence or 
                f.get("turn_sequence") == idx or 
                (f.get("role") == m.role and not f.get("turn_sequence"))
            )
        ]
        if turn_attachments:
            out += ["**Attachments:**"]
            for att in turn_attachments:
                att_name = att.get("name") or "attachment"
                rel_link = att.get("url")
                if not rel_link and (att.get("uploaded_to_s3") or att.get("has_file_on_disk")):
                    rel_link = f"{files_folder}/{(att.get('path') or f'attachments/{att_name}')}"
                elif not rel_link and att.get("extracted_txt_path"):
                    rel_link = f"{files_folder}/{att.get('extracted_txt_path')}"

                att_type = (att.get("type") or "").lower()
                is_img = (
                    att_type in ("image", "png", "jpg", "jpeg", "gif", "webp", "svg")
                    or att_type.startswith("image/")
                    or any(att_name.lower().endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"))
                )
                if is_img and rel_link:
                    out += [f"- ![{att_name}]({rel_link})"]
                elif rel_link:
                    out += [f"- 📎 [{att_name}]({rel_link})"]
                else:
                    out += [f"- 📎 **{att_name}** *(Attached in Claude conversation)*"]
            out += [""]

    # Generated files & artifacts (README.md, scripts, diagrams, etc.)
    generated_docs = [
        f for f in (conv.files or [])
        if f.get("is_artifact") or not f.get("is_attachment")
    ]
    if generated_docs:
        out += ["", "## Generated Documents & Files", ""]
        for f in generated_docs:
            fname = f.get("name") or f.get("path") or "document.md"
            fpath = f.get("path") or fname
            rel_link = f"{files_folder}/{fpath}"
            fcontent = (f.get("content") or f.get("body") or "").strip()
            ext = fname.split(".")[-1].lower() if "." in fname else ""
            lang = {"md": "markdown", "py": "python", "js": "javascript", "ts": "typescript", "sh": "bash", "html": "html", "css": "css", "json": "json"}.get(ext, ext)
            out += [f"### File: [`{fname}`]({rel_link})", "", f"```{lang}", fcontent, "```", ""]
    return "\n".join(out)


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
        # Clean out any trailing attachments or generated docs section markers
        body = re.sub(r'(?ms)\n\*\*Attachments:\*\*.*$', '', body).strip()
        body = re.sub(r'(?ms)\n## Generated Documents & Files.*$', '', body).strip()
        if body:
            messages.append(Message(id=f"msg-prev-{msg_num}", role=role, content=body, timestamp=ts))
            msg_num += 1
        idx += 3
    return messages


def _merge_messages(existing: list[Message], incoming: list[Message]) -> list[Message]:
    """Robustly merge existing transcript messages with incoming messages.
    Ensures that conversations with multiple prompts (e.g. 8+ prompts) retain
    every prompt and response in correct chronological sequence without dropping or swapping turns.
    """
    if not existing:
        return incoming
    if not incoming:
        return existing

    # Case 1: Incoming has at least as many messages as existing and covers from the start
    # (Typical of authoritative API fetch or full DOM capture)
    if len(incoming) >= len(existing):
        first_ex = existing[0].content.strip()
        first_inc = incoming[0].content.strip()
        # Check if they start with the same prompt (first 40 chars)
        if first_ex[:40] == first_inc[:40] or first_ex in first_inc or first_inc in first_ex:
            merged = list(incoming)
            for i in range(min(len(existing), len(incoming))):
                if existing[i].role == incoming[i].role:
                    # Keep longer/richer content if existing had more detail
                    if len(existing[i].content.strip()) > len(incoming[i].content.strip()):
                        merged[i].content = existing[i].content
            return merged

    # Case 2: Incoming is an extension or tail (e.g. user added prompts 7 and 8)
    # Find where incoming's first message matches an existing message
    first_inc_role = incoming[0].role
    first_inc_content = incoming[0].content.strip()
    match_idx = -1
    for idx, ex in enumerate(existing):
        if ex.role == first_inc_role:
            ex_c = ex.content.strip()
            if ex_c == first_inc_content or (len(first_inc_content) > 30 and (ex_c.startswith(first_inc_content[:40]) or first_inc_content.startswith(ex_c[:40]))):
                match_idx = idx
                break

    if match_idx != -1:
        # Incoming continues starting from match_idx:
        # Keep earlier existing turns [0:match_idx], and merge incoming from match_idx onwards
        merged = list(existing[:match_idx])
        for offset, inc_m in enumerate(incoming):
            curr_idx = match_idx + offset
            if curr_idx < len(existing) and existing[curr_idx].role == inc_m.role:
                if len(existing[curr_idx].content.strip()) > len(inc_m.content.strip()):
                    inc_m.content = existing[curr_idx].content
            merged.append(inc_m)
        return merged

    # Case 3: If no direct overlap at start, append any new incoming turns to existing
    existing_hashes = {f"{m.role}:{m.content.strip()[:60]}" for m in existing}
    merged = list(existing)
    for inc_m in incoming:
        h = f"{inc_m.role}:{inc_m.content.strip()[:60]}"
        if h not in existing_hashes:
            merged.append(inc_m)
            existing_hashes.add(h)
    return merged


def _find_existing_thread_file(conv: Conversation) -> Path | None:
    """Find if a file already exists for this thread deterministically by conversation_id or exact slug."""
    # Fast path: the database remembers where each conversation was written, so saves do not scan folders.
    indexed = state.get_archive_path(conv.id) if conv.id else None
    if indexed and (GIT_DIR / indexed).is_file():
        return GIT_DIR / indexed
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

    # 1. Match conversation_id in YAML frontmatter (highest precision, 100% deterministic)
    if conv.id:
        for f in all_files:
            try:
                txt = f.read_text(encoding="utf-8")
                if f'conversation_id: "{conv.id}"' in txt or f'conversation_id: {conv.id}' in txt:
                    return f
            except Exception:
                continue

    # 2. Match exact conv.id filename
    for f in all_files:
        if f.stem == _slug(conv.id):
            return f

    # 3. Direct slug / filename match (with or without date prefix)
    target_slug = _slug(conv.title) if conv.title and conv.title.lower() != "untitled conversation" else _slug(conv.id)
    for f in all_files:
        if f.stem == target_slug or f.stem.endswith(f"_{target_slug}"):
            try:
                txt = f.read_text(encoding="utf-8")
                m = re.search(r'^conversation_id:\s*["\']?([^"\'\s]+)', txt, re.MULTILINE)
                if not m or not m.group(1) or m.group(1) == conv.id:
                    return f
            except Exception:
                continue

    # Never match or hijack an unrelated conversation file!
    return None


def _paths_for(conv: Conversation) -> list[str]:
    """Paths of an already-written conversation, for committing on its own."""
    rel = state.get_archive_path(conv.id)
    if not rel:
        return []
    paths = [f"raw_queries/{rel}"]
    stem = Path(rel).stem
    files_dir = GIT_DIR / Path(rel).parent / f"{stem}_files"
    if files_dir.exists() and any(p.is_file() for p in files_dir.rglob("*")):
        paths.append(f"raw_queries/{Path(rel).parent.as_posix()}/{stem}_files")
    return paths


def write_snapshot(conv: Conversation) -> list[str]:
    """Write one transcript to disk. Merges new turns into the existing file if present.
    Returns the git-relative paths to commit (empty if nothing changed)."""
    uname = _normalize_username(conv.username or conv.user_id or USERNAME)
    existing_file = _find_existing_thread_file(conv)

    if existing_file:
        rel = existing_file.relative_to(GIT_DIR).as_posix()
        path = GIT_DIR / rel
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        # Determine query date prefix (YYYY-MM-DD) in EDT for chronological + alphabetical sorting
        raw_query_time = conv.created_at or conv.updated_at or ""
        edt_ts = _format_to_edt(raw_query_time)
        date_prefix = ""
        if edt_ts and len(edt_ts) >= 10:
            date_prefix = edt_ts[:10]  # "YYYY-MM-DD"
        elif raw_query_time and len(raw_query_time) >= 10:
            date_prefix = raw_query_time[:10]

        base_slug = _slug(conv.title) if conv.title and conv.title.lower() != "untitled conversation" else _slug(conv.id)
        if date_prefix and not base_slug.startswith(date_prefix):
            name_slug = f"{date_prefix}_{base_slug}"
        else:
            name_slug = base_slug

        candidate = GIT_DIR / uname / conv.platform / f"{name_slug}.md"
        # If candidate file exists and belongs to a different conversation_id, disambiguate with short id
        if candidate.exists():
            try:
                txt = candidate.read_text(encoding="utf-8")
                m = re.search(r'^conversation_id:\s*["\']?([^"\'\s]+)', txt, re.MULTILINE)
                if m and m.group(1) and m.group(1) != conv.id:
                    candidate = GIT_DIR / uname / conv.platform / f"{name_slug}-{conv.id[:8]}.md"
            except Exception:
                candidate = GIT_DIR / uname / conv.platform / f"{name_slug}-{conv.id[:8]}.md"
        path = candidate
        rel = f"{uname}/{conv.platform}/{path.name}"
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

    # Header time = Claude's last activity on the conversation, not the time it was saved here.
    updated_at = _format_to_edt(conv.updated_at) or now_est

    # Authoritative canonical message list: merge robustly to preserve all multi-prompt turns
    valid_incoming = [m for m in conv.messages if m.content and m.content.strip()]
    if valid_incoming and existing_messages:
        conv.messages = _merge_messages(existing_messages, valid_incoming)
    elif valid_incoming:
        conv.messages = valid_incoming
    elif existing_messages:
        conv.messages = existing_messages

    # S3 Direct Upload: If S3 is configured, upload inline attachment data directly to S3
    if s3.is_s3_configured() and conv.files:
        for f in conv.files:
            if f.get("is_attachment") or (isinstance(f.get("content"), str) and f.get("content", "").startswith("data:")):
                if f.get("url") and str(f.get("url")).startswith("http"):
                    continue
                fname = f.get("name") or f.get("path") or "attachment"
                fcontent = f.get("content") or f.get("body") or ""
                if fcontent:
                    try:
                        s3_url = s3.upload_attachment_data(
                            filename=fname,
                            content_data=fcontent,
                            content_type=f.get("type"),
                            conversation_id=conv.id,
                            user_id=uname,
                        )
                        if s3_url:
                            f["url"] = s3_url
                            f["uploaded_to_s3"] = True
                    except Exception:
                        pass

    rendered_text = render(conv, created_at=created_at, updated_at=updated_at)
    if path.exists():
        try:
            old_full = path.read_text(encoding="utf-8")
            old_body = re.sub(r'(?m)^updated_at:.*$', '', old_full).strip()
            new_body = re.sub(r'(?m)^updated_at:.*$', '', rendered_text).strip()
            if old_body == new_body and not conv.files:
                return []  # Identical snapshot already on disk, nothing to write or commit
        except Exception:
            pass
    path.write_text(rendered_text, encoding="utf-8", newline="\n")

    # Save structured standalone files (README.md, scripts, diagrams, etc.) into companion folder
    files_dir = path.parent / f"{path.stem}_files"
    if conv.files:
        files_dir.mkdir(parents=True, exist_ok=True)
        for f in conv.files:
            # If successfully uploaded to S3, skip storing heavy binary file in git repo
            if f.get("uploaded_to_s3") or (f.get("is_attachment") and f.get("url") and str(f.get("url")).startswith("http")):
                continue
            rel_f = f.get("path") or f.get("name") or "document.md"
            target_f = files_dir / rel_f
            target_f.parent.mkdir(parents=True, exist_ok=True)
            fcontent = f.get("content") or f.get("body") or ""
            fname = f.get("name") or rel_f

            # Handle base64 data URLs for binary image/attachment files (fallback when S3 disabled)
            if isinstance(fcontent, str) and fcontent.startswith("data:") and ";base64," in fcontent:
                try:
                    _, b64 = fcontent.split(";base64,", 1)
                    target_f.write_bytes(base64.b64decode(b64))
                    f["has_file_on_disk"] = True
                    continue
                except Exception:
                    pass
            elif isinstance(fcontent, bytes):
                target_f.write_bytes(fcontent)
                f["has_file_on_disk"] = True
                continue

            # Save Claude extracted document text if available
            extracted_txt = f.get("extracted_text") or ""
            if extracted_txt and extracted_txt != fname:
                txt_name = f"{Path(rel_f).stem}.extracted.txt"
                txt_target = files_dir / "attachments" / txt_name
                txt_target.parent.mkdir(parents=True, exist_ok=True)
                txt_target.write_text(extracted_txt, encoding="utf-8", errors="replace")
                f["extracted_txt_path"] = f"attachments/{txt_name}"
                continue

            # Never write placeholder filename strings as files
            if fcontent and str(fcontent).strip() != str(fname).strip():
                target_f.write_text(str(fcontent), encoding="utf-8", newline="\n")
                f["has_file_on_disk"] = True

    # Remember where this conversation lives, so the next save finds it without a folder scan.
    state.set_archive_path(conv.id, rel)
    paths = [f"raw_queries/{rel}"]
    if files_dir.exists() and any(p.is_file() for p in files_dir.rglob("*")):
        paths.append(f"raw_queries/{uname}/{conv.platform}/{path.stem}_files")
    return paths


def _commit_paths(paths: list[str], labels: list[str], when: str) -> None:
    """Stage the given paths and make ONE commit for all of them (skipped if nothing changed)."""
    unique = list(dict.fromkeys(paths))
    if not unique:
        return
    _check(_git("add", "--", *unique), "git add")
    if _git("diff", "--cached", "--quiet").returncode == 0:
        return  # identical to what is already committed
    if len(labels) == 1:
        commit_msg = f"claude: [{when}] {labels[0]}"
    else:
        commit_msg = f"claude: [{when}] archived {len(labels)} conversations"
    _check(_git("commit", "-m", commit_msg, "--", *unique), "git commit")


def commit_snapshot(conv: Conversation) -> None:
    """Write and commit one transcript."""
    paths = write_snapshot(conv)
    when = _format_to_edt(conv.updated_at or conv.created_at) or datetime.now(EASTERN).strftime("%Y-%m-%d %H:%M:%S %Z")
    _commit_paths(paths, [f"{conv.title} ({conv.id[:8]})"], when)


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
    """Push all local commits. Pulls with rebase to integrate concurrent remote commits,
    then pushes. If push fails temporarily, it retries and logs without crashing the user's turn.
    """
    if not GIT_REMOTE_URL:
        return
    try:
        # Step 1: Pull with rebase & autostash
        _git("pull", "--rebase", "--autostash", "origin", GIT_BRANCH)
        _check(_git("push", "-u", "origin", f"HEAD:{GIT_BRANCH}"), "git push")
    except Exception:
        try:
            # Step 2: Retry with explicit fetch + rebase
            _git("fetch", "origin", GIT_BRANCH)
            _git("rebase", f"origin/{GIT_BRANCH}")
            _check(_git("push", "-u", "origin", f"HEAD:{GIT_BRANCH}"), "git push retry")
        except Exception as retry_err:
            # Non-fatal: Local commit is safe on disk; push will sync on next batch
            print(f"[Warning] Git push deferred (will auto-sync on next turn): {retry_err}")


def save_batch(convs: list[Conversation]) -> dict:
    """Commit every snapshot locally, then push. Per-conversation commit errors are reported
    in 'failed'. Push issues are handled gracefully so local saves are never failed in the UI.
    """
    with _lock:
        prepare()
        saved, failed = [], {}
        written, paths = [], []
        for c in convs:
            try:
                paths.extend(write_snapshot(c))
                written.append(c)
            except Exception as e:
                failed[c.id] = str(e)
        if written:
            try:
                when = datetime.now(EASTERN).strftime("%Y-%m-%d %H:%M:%S %Z")
                labels = [f"{c.title} ({c.id[:8]})" for c in written]
                _commit_paths(paths, labels, when)
                saved = [c.id for c in written]
            except Exception:
                # Commit each conversation separately, so one bad item cannot hold up the rest.
                saved = []
                for c in written:
                    try:
                        _commit_paths(_paths_for(c), [f"{c.title} ({c.id[:8]})"], when)
                        saved.append(c.id)
                    except Exception as single_err:
                        failed[c.id] = str(single_err)
        if saved:
            try:
                push()
            except Exception as e:
                print(f"[Warning] Git push error in save_batch: {e}")
        return {"saved": saved, "failed": failed}


def search_transcripts(query: str, user: str = "") -> str:
    """Search saved markdown transcripts by keyword, title, or content."""
    # Reads take no lock: a save never makes a search or list wait.
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
    # Reads take no lock: a save never makes a search or list wait.
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


def _safe_transcript_path(file_path: str) -> Path | None:
    """Resolve a caller-supplied path, accepting only files inside GIT_DIR (no traversal)."""
    root = GIT_DIR.resolve()
    candidates = [REPO_DIR / file_path, GIT_DIR / file_path]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.is_relative_to(root) and resolved.is_file():
            return resolved
    return None


def get_transcript(file_path: str, owner: str | None = None) -> str:
    """Read a transcript by relative path. If `owner` is given, only that user's folder is readable."""
    # Reads take no lock: a save never makes a search or list wait.
    p = _safe_transcript_path(file_path)
    if p is None:
        return f"File not found: {file_path}"
    if owner is not None:
        first = p.relative_to(GIT_DIR.resolve()).parts[0]
        if first != _user_folder(owner):
            return f"File not found: {file_path}"
    return p.read_text(encoding="utf-8")
