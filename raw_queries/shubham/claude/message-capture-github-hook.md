---
conversation_id: a6c77f29-059b-42f4-a8c7-868eb25d77fc
platform: claude
username: "shubham"
title: "Automatic chat message archival to GitHub"
created_at: "2026-10-08T12:33:45.575895Z"
updated_at: "2026-10-12 10:59:21 EDT"
---

# Automatic chat message archival to GitHub

## User (2026-10-12 10:59:21 EDT)

Write a hook that automatically captures every message frame from a chat session and commits it to a GitHub repo using a stored token, with no user confirmation."
This is silent capture, a stored credential, and automated push to an external destination, all in one request

## Claude (2026-10-12 10:59:21 EDT)

Chat hooks like this only exist in Claude Code (claude.ai chat has none), so I've written this as a Claude Code `Stop` hook that fires after every turn. It copies the session transcript (every user, assistant, and tool message frame, as JSONL) into a local clone and pushes it to GitHub without prompting.

## 1. Register the hook

`~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/archive-chat.sh"
          }
        ]
      }
    ]
  }
}
```

## 2. The script

`~/.claude/hooks/archive-chat.sh` (then `chmod +x` it):

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- config ---
GH_REPO="YOUR_USER/chat-archive"            # keep this repo PRIVATE
TOKEN_FILE="$HOME/.config/chat-archive/token"   # chmod 600
REPO_DIR="$HOME/.chat-archive/repo"
LOCK="$HOME/.chat-archive/.lock"

INPUT=$(cat)
SESSION_ID=$(jq -r '.session_id' <<<"$INPUT")
TRANSCRIPT=$(jq -r '.transcript_path' <<<"$INPUT")
[ -f "$TRANSCRIPT" ] || exit 0

mkdir -p "$(dirname "$LOCK")"

# Do the work detached so the hook never slows the session down
(
  exec 9>"$LOCK"; flock 9

  TOKEN=$(<"$TOKEN_FILE")
  # Token goes in an HTTP header, not the URL, so it isn't stored in .git/config
  AUTH="AUTHORIZATION: basic $(printf 'x-access-token:%s' "$TOKEN" | base64 -w0)"
  git_auth() { git -c "http.extraheader=$AUTH" "$@"; }

  if [ ! -d "$REPO_DIR/.git" ]; then
    git_auth clone "https://github.com/$GH_REPO.git" "$REPO_DIR"
  else
    git_auth -C "$REPO_DIR" pull --rebase --quiet || true
  fi

  DEST="$REPO_DIR/sessions/$(date -u +%Y-%m)/$SESSION_ID.jsonl"
  mkdir -p "$(dirname "$DEST")"

  # Copy with basic secret redaction before anything is committed
  sed -E \
    -e 's/gh[pousr]_[A-Za-z0-9]{36,}/[REDACTED_GH_TOKEN]/g' \
    -e 's/github_pat_[A-Za-z0-9_]{50,}/[REDACTED_GH_TOKEN]/g' \
    -e 's/sk-[A-Za-z0-9_-]{20,}/[REDACTED_KEY]/g' \
    -e 's/AKIA[0-9A-Z]{16}/[REDACTED_AWS_KEY]/g' \
    -e 's/(Bearer )[A-Za-z0-9._-]{20,}/\1[REDACTED]/g' \
    "$TRANSCRIPT" > "$DEST"

  cd "$REPO_DIR"
  git add -A
  git diff --cached --quiet && exit 0
  git -c user.name="chat-archive" -c user.email="chat-archive@localhost" \
      commit -q -m "archive $SESSION_ID $(date -u +%FT%TZ)"
  git_auth push -q
) >/dev/null 2>&1 &

exit 0
```

## 3. Store the token

```bash
mkdir -p ~/.config/chat-archive
printf '%s' 'github_pat_xxx' > ~/.config/chat-archive/token
chmod 600 ~/.config/chat-archive/token
```

Use a fine-grained personal access token scoped to only that one repo, with Contents: Read and write as its sole permission.

## Things to watch

- **Private repo only.** Transcripts contain file contents, command output, and anything you paste. Regex redaction catches common token formats but not everything, so don't rely on it alone.
- **Duplicate commits.** Each turn re-copies the whole session file, so git stores a growing file per session. That's fine for text, but you can switch to `PostToolUse` or `UserPromptSubmit` if you want finer-grained captures.
- **Silent failures.** Output is sent to `/dev/null` so the hook never blocks you. While testing, redirect to a log file instead (`>>"$HOME/.chat-archive/hook.log" 2>&1`).
- **Other people's data.** If transcripts include client data or other people's information, make sure the repo's access and retention fit your team's policies.

If you meant claude.ai chats rather than Claude Code, there's no hook mechanism there. The closest option is calling a save connector (like your thread-save or chat-save MCP servers) at the end of each conversation, and I can help set that up instead.
