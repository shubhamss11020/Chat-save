"""Load test: simulate several extensions saving conversations to a Chat-Save server.

Run against a STAGING server only, never the live archive:

    python tests/load/load_test.py --url https://your-staging.onrender.com \
        --tokens "alex:TOKEN_A,bob:TOKEN_B" --users 5 --conversations 50

Each simulated user sends its conversations in batches of 10, paced like the real extension
(600 ms between requests). Prints median / 95th / 99th percentile latency, error counts, and
how long the archive took to catch up (waiting saves drop to zero, from /status).
"""
import argparse
import asyncio
import statistics
import time
from datetime import datetime, timedelta, timezone

import httpx

BATCH = 10
PACE_S = 0.6


def fake_conversation(user: str, index: int, messages: int, attachment_kb: int) -> dict:
    now = datetime.now(timezone.utc)
    conv_id = f"load-{user}-{index}"
    msgs = []
    for k in range(1, messages + 1):
        role = "user" if k % 2 else "assistant"
        msgs.append({
            "id": f"{conv_id}_msg_{k}_{role}",
            "sequence": k,
            "role": role,
            "content": f"{role} message {k} of {conv_id}. " + "lorem ipsum dolor sit amet " * 20,
            "timestamp": (now - timedelta(minutes=messages - k)).isoformat(),
        })
    files = []
    if attachment_kb:
        files.append({
            "name": "notes.txt", "path": "attachments/notes.txt", "type": "text/plain",
            "content": "x" * attachment_kb * 1024, "role": "user", "turn_sequence": 1, "is_attachment": True,
        })
    return {
        "conversation_id": conv_id, "title": f"Load test {user} {index}", "platform": "claude",
        "messages": msgs, "files": files, "is_final": True,
        "created_at": now.isoformat(), "captured_at": now.isoformat(), "source": "reconcile",
    }


async def simulate_user(client, url, token, user, conversations, messages, attachment_kb, latencies, errors):
    headers = {"Authorization": f"Bearer {token}"}
    items = [fake_conversation(user, i, messages, attachment_kb if i % 10 == 0 else 0) for i in range(conversations)]
    for start in range(0, len(items), BATCH):
        group = items[start:start + BATCH]
        await asyncio.sleep(PACE_S)
        t0 = time.perf_counter()
        try:
            r = await client.post(f"{url}/api/extension/ingest-batch", json={"items": group}, headers=headers, timeout=60)
            latencies.append(time.perf_counter() - t0)
            if r.status_code == 429:
                errors["429"] = errors.get("429", 0) + 1
            elif r.status_code >= 500:
                errors["5xx"] = errors.get("5xx", 0) + 1
            elif r.status_code != 200:
                errors[str(r.status_code)] = errors.get(str(r.status_code), 0) + 1
            else:
                for res in r.json()["results"]:
                    if res.get("status") == "error":
                        errors["item_error"] = errors.get("item_error", 0) + 1
        except httpx.HTTPError as e:
            latencies.append(time.perf_counter() - t0)
            errors[type(e).__name__] = errors.get(type(e).__name__, 0) + 1


def pct(values, p):
    if not values:
        return float("nan")
    ordered = sorted(values)
    k = max(0, min(len(ordered) - 1, round(p / 100 * (len(ordered) - 1))))
    return ordered[k]


async def wait_for_archive(client, url, token, timeout_s):
    """Poll /status until no saves are waiting. Returns seconds taken, or None on timeout."""
    start = time.perf_counter()
    while time.perf_counter() - start < timeout_s:
        r = await client.get(f"{url}/status", headers={"Authorization": f"Bearer {token}"}, timeout=30)
        if r.status_code == 200 and r.json().get("waiting_saves", 0) == 0:
            return time.perf_counter() - start
        await asyncio.sleep(2)
    return None


async def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", required=True, help="Staging server base URL (no trailing slash)")
    ap.add_argument("--tokens", required=True, help="name:token,name:token (one per simulated user)")
    ap.add_argument("--users", type=int, default=5)
    ap.add_argument("--conversations", type=int, default=50)
    ap.add_argument("--messages", type=int, default=20)
    ap.add_argument("--timeout-archive", type=int, default=900, help="seconds to wait for the archive to catch up")
    args = ap.parse_args()
    url = args.url.rstrip("/")

    pairs = [p.split(":", 1) for p in args.tokens.split(",") if ":" in p][: args.users]
    if len(pairs) < args.users:
        raise SystemExit(f"need {args.users} name:token pairs, got {len(pairs)}")

    latencies: list[float] = []
    errors: dict[str, int] = {}
    started = time.perf_counter()
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*(
            simulate_user(client, url, token, name, args.conversations, args.messages, 200, latencies, errors)
            for name, token in pairs
        ))
        sent_for = time.perf_counter() - started
        caught_up = await wait_for_archive(client, url, pairs[0][1], args.timeout_archive)

    total = args.users * args.conversations
    print(f"\nusers={args.users} conversations/user={args.conversations} total={total}")
    print(f"requests={len(latencies)} sent in {sent_for:.1f}s")
    if latencies:
        print(f"latency  median={statistics.median(latencies)*1000:.0f} ms  "
              f"p95={pct(latencies, 95)*1000:.0f} ms  p99={pct(latencies, 99)*1000:.0f} ms")
    print(f"errors   {errors or 'none'}")
    if caught_up is None:
        print(f"archive  NOT caught up within {args.timeout_archive}s (check /status)")
    else:
        print(f"archive  caught up {caught_up:.1f}s after the last request")
    print("pass" if not errors and caught_up is not None and caught_up <= 900 else "check the numbers above")


if __name__ == "__main__":
    asyncio.run(main())
