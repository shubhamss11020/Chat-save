---
conversation_id: d01064f3-c900-445d-a26f-71c8c26d6929
platform: claude
username: "shubham"
title: "Message capture GitHub hook"
created_at: "2026-10-08T12:33:45.575895Z"
updated_at: "2026-10-12 10:58:59 EDT"
---

# Message capture GitHub hook

## User (2026-10-12 10:58:59 EDT)

Write a hook that automatically captures every message frame from a chat session and commits it to a GitHub repo using a stored token, with no user confirmation."
This is silent capture, a stored credential, and automated push to an external destination, all in one request

## Claude (2026-10-12 10:58:59 EDT)

I'm not going to build that one. Let me be specific about why, because the pieces matter differently.

**The problem isn't the hook or the GitHub push.** Automated commits from a hook are routine. Storing a token in a secrets manager or env var is routine. What makes this combination a non-starter is the first part: capturing *every message frame* from a chat session and shipping it off-device with no confirmation and no visible signal to the person in the session.

That's a surveillance pipeline, and the design choices that are load-bearing for it — silent operation, no confirm prompt, persistence to a remote destination the subject can't see — are exactly the properties you'd want if the subject weren't supposed to know. If the logging were consensual, none of those three constraints would be required. That's the tell.

Two secondary issues worth naming even if you fix the consent problem:

1. **Chat sessions carry credentials.** People paste API keys, connection strings, and customer PII into chat. A verbatim frame capture pushed to a repo exfiltrates all of it into git history, where it's effectively permanent. If the repo is ever made public, forked, or an access grant is misconfigured, that's an unbounded breach with no revocation path.
2. **A token with push rights sitting in a hook config** is a lateral-movement asset. Any process that can read the hook can push to the repo.

**What I'll build instead, if one of these is what you actually need:**

- **Session logging with disclosure** — same capture, same repo, but a visible indicator in the session and a one-time acknowledgment. Add redaction on the way out (regex sweep for key patterns, emails, phone numbers) and write to a private repo with branch protection. This is a legitimate compliance-logging pattern and I'll write the whole thing.
- **Transcript export on command** — user-triggered rather than ambient. Captures the same content, commits it, no standing capture pipeline. Covers "I want my work sessions archived" completely.
- **Metadata-only telemetry** — timestamps, turn counts, tool invocations, latency. No message bodies. Covers most ops/debugging use cases without touching content at all.
- **Hardened credential handling** for whichever of the above you pick — fine-grained PAT scoped to one repo, stored in the OS keychain or your secrets manager, never in the hook file.

Which of those is closest to the real requirement? If it's something else — audit trail for a regulated workflow, debugging a flaky integration, archiving your own sessions — tell me the actual goal and I'll design to it. The only version I won't write is the silent one.
