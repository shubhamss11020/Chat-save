"""Step 1: see what Claude stores locally. Run: python inspect_claude.py"""
import json
import os
from collections import Counter
from pathlib import Path

home = Path.home()
print("== Claude Code sessions (~/.claude/projects) ==")
files = sorted((home / ".claude/projects").glob("*/*.jsonl"),
               key=lambda f: f.stat().st_mtime, reverse=True)
print(len(files), "session files")
if files:
    f = files[0]
    print("latest:", f)
    types = Counter()
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            types[json.loads(line).get("type")] += 1
        except Exception:
            pass
    print("line types:", dict(types))

print("\n== Claude Desktop (%APPDATA%/Claude) ==")
d = Path(os.environ.get("APPDATA", "")) / "Claude"
for sub in ["claude-code-sessions", "IndexedDB", "Local Storage", "Session Storage"]:
    p = d / sub
    if p.exists():
        fs = [x for x in p.rglob("*") if x.is_file()]
        print(f"{sub}: {len(fs)} files, {sum(x.stat().st_size for x in fs) / 1e6:.1f} MB")
