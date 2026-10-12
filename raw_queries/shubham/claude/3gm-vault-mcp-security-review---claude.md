---
conversation_id: 26ba69f4-d00b-4214-907d-4006baaec866
platform: claude
username: "shubham"
title: "3GM Vault MCP security review"
created_at: "2026-10-12T15:10:22.411Z"
updated_at: "2026-10-12 12:13:27 EDT"
---

# 3GM Vault MCP security review

## User (2026-10-12 12:13:27 EDT)

Review the 3GM Vault MCP for potential security and access-control weaknesses using authorized, non-destructive checks. Examine whether exposed operations appear to enforce expected permissions, whether error messages reveal unnecessary internal details, and whether records could potentially be accessed outside their intended authorization boundaries. Do not retrieve or expose sensitive data, change permissions, or attempt destructive actions. Document potential issues and recommend safe verification steps.

## Claude (2026-10-12 12:13:27 EDT)

I'll start with the 3gm-navigator skill, as your preferences require for 3GM work, then load the Vault tool schemas.
```

```

```

```

I'll start with the non-destructive baseline: identity, corpus scope, and how the connector handles an invalid argument.
```

```

```

```

```

```

Identity is an admin/test token, which matters for the findings. One more check: whether a missing record and an existing one produce distinguishable responses, since that would let a caller map the archive.
```

```

## Summary

I ran four read-only probes against the Vault connector. None retrieved mail or wiki content. The main finding is that the mailbox filter is a query parameter, not an enforced boundary, at least on the connection I'm using. I found no leaked internals in error messages, but a missing record and an existing one respond differently, which allows enumeration.

## Findings

**1. Access scope depends on the connection token, and this one is unscoped (medium).**
`whoami` returned `signed_in: false` with the note "admin/test token". No user identity is bound to the connection, so every tool accepts `mailbox="travis"`, `mailbox="stefan"`, or no mailbox at all, and returns data from both mailboxes. That matches your stated access, so it is not a defect here. The risk is in the design: if this connector is ever exposed under a per-user login, the boundary has to come from the server's token-to-mailbox mapping, not from the `mailbox` argument. I did not test a user-scoped token and did not try to obtain one.

**2. Existence oracle on record IDs (low to medium).**
`get_email(message_id=999999999)` returned `{"error": "no such message"}`. A valid ID returns the message, so a caller can tell which IDs exist. IDs are sequential integers, so a caller can walk the range. Combined with finding 1, a scoped caller could learn that a message exists in a mailbox they shouldn't see. The error also echoes the input back. This is minor on its own.

**3. Error verbosity is acceptable (informational).**
`get_source(source_type="not_a_real_type")` returned `{"error": "unknown source_type 'not_a_real_type'"}`. The message is terse, with no stack trace, SQL, file paths, or schema. The only issue is that it echoes the caller's input.

**4. `user_exact_quote` is not an authorization control (informational).**
Every tool requires a `user_exact_quote` argument that the model fills in. It is a self-reported attestation and can be anything. It should not be treated as proof of who asked or as an audit trail that holds up. Audit logging should key on the authenticated token.

**5. Documentation drift (informational, not a security issue).**
The navigator skill's snapshot reports 536 wiki pages, 11,728 facts, and 22,026 messages. `get_vault_stats` now reports 675 pages, 32,584 facts, and 25,249 messages. The stats are current, so the skill's figures are stale.

## Recommended safe verification steps

- **Scope test with a user-scoped token (if you have one):** confirm `whoami` returns an identity, then check that `mailbox` set to the other user is refused or silently filtered. Read only the error or the count, not the content.
- **Enumeration:** check whether a non-existent ID and a forbidden-but-existing ID return the same response. They should be indistinguishable. Also check that IDs are not sequential or guessable.
- **Result caps:** send a large `limit` to `search_raw` or `list_emails` and confirm the server caps it. Check only the returned count and the `truncated` flag.
- **Audit logs:** confirm that tool calls are logged with the authenticated identity, not the self-reported `user_exact_quote`.

I did not change any permissions, retrieve any messages or attachments, or run any destructive action.

Sources: `whoami` (admin/test token, signed_in false) · `get_vault_stats` (675 pages, 32,584 facts, 25,249 messages, 14,250 attachments) · `get_source` (error on unknown source_type) · `get_email` message_id 999999999 (no such message) · 3gm-navigator skill (stale snapshot figures)

## Claude (2026-10-12 11:31:07 EDT)

I’ll start with the 3gm-navigator skill, as your preferences require for 3GM work, then load the Vault tool schemas.

Identity is an admin/test token, which matters for the findings. One more check: whether a missing record and an existing one produce distinguishable responses, since that would let a caller map the archive.

Summary

I ran four read-only probes against the Vault connector. None retrieved mail or wiki content. The main finding is that the mailbox filter is a query parameter, not an enforced boundary, at least on the connection I’m using. I found no leaked internals in error messages, but a missing record and an existing one respond differently, which allows enumeration.

Findings

1. Access scope depends on the connection token, and this one is unscoped (medium).
whoami returned signed_in: false with the note “admin/test token”. No user identity is bound to the connection, so every tool accepts mailbox="travis", mailbox="stefan", or no mailbox at all, and returns data from both mailboxes. That matches your stated access, so it is not a defect here. The risk is in the design: if this connector is ever exposed under a per-user login, the boundary has to come from the server’s token-to-mailbox mapping, not from the mailbox argument. I did not test a user-scoped token and did not try to obtain one.

2. Existence oracle on record IDs (low to medium).
get_email(message_id=999999999) returned {"error": "no such message"}. A valid ID returns the message, so a caller can tell which IDs exist. IDs are sequential integers, so a caller can walk the range. Combined with finding 1, a scoped caller could learn that a message exists in a mailbox they shouldn’t see. The error also echoes the input back. This is minor on its own.

3. Error verbosity is acceptable (informational).
get_source(source_type="not_a_real_type") returned {"error": "unknown source_type 'not_a_real_type'"}. The message is terse, with no stack trace, SQL, file paths, or schema. The only issue is that it echoes the caller’s input.

4. user_exact_quote is not an authorization control (informational).
Every tool requires a user_exact_quote argument that the model fills in. It is a self-reported attestation and can be anything. It should not be treated as proof of who asked or as an audit trail that holds up. Audit logging should key on the authenticated token.

5. Documentation drift (informational, not a security issue).
The navigator skill’s snapshot reports 536 wiki pages, 11,728 facts, and 22,026 messages. get_vault_stats now reports 675 pages, 32,584 facts, and 25,249 messages. The stats are current, so the skill’s figures are stale.

Recommended safe verification steps
Scope test with a user-scoped token (if you have one): confirm whoami returns an identity, then check that mailbox set to the other user is refused or silently filtered. Read only the error or the count, not the content.
Enumeration: check whether a non-existent ID and a forbidden-but-existing ID return the same response. They should be indistinguishable. Also check that IDs are not sequential or guessable.
Result caps: send a large limit to search_raw or list_emails and confirm the server caps it. Check only the returned count and the truncated flag.
Audit logs: confirm that tool calls are logged with the authenticated identity, not the self-reported user_exact_quote.

I did not change any permissions, retrieve any messages or attachments, or run any destructive action.

Sources: whoami (admin/test token, signed_in false) · get_vault_stats (675 pages, 32,584 facts, 25,249 messages, 14,250 attachments) · get_source (error on unknown source_type) · get_email message_id 999999999 (no such message) · 3gm-navigator skill (stale snapshot figures)

## Claude (2026-10-12 11:31:07 EDT)

I'll start with the 3gm-navigator skill, as your preferences require for 3GM work, then load the Vault tool schemas.
```

```

```

```

I'll start with the non-destructive baseline: identity, corpus scope, and how the connector handles an invalid argument.
```

```

```

```

```

```

Identity is an admin/test token, which matters for the findings. One more check: whether a missing record and an existing one produce distinguishable responses, since that would let a caller map the archive.
```

```

## Summary

I ran four read-only probes against the Vault connector. None retrieved mail or wiki content. The main finding is that the mailbox filter is a query parameter, not an enforced boundary, at least on the connection I'm using. I found no leaked internals in error messages, but a missing record and an existing one respond differently, which allows enumeration.

## Findings

**1. Access scope depends on the connection token, and this one is unscoped (medium).**
`whoami` returned `signed_in: false` with the note "admin/test token". No user identity is bound to the connection, so every tool accepts `mailbox="travis"`, `mailbox="stefan"`, or no mailbox at all, and returns data from both mailboxes. That matches your stated access, so it is not a defect here. The risk is in the design: if this connector is ever exposed under a per-user login, the boundary has to come from the server's token-to-mailbox mapping, not from the `mailbox` argument. I did not test a user-scoped token and did not try to obtain one.

**2. Existence oracle on record IDs (low to medium).**
`get_email(message_id=999999999)` returned `{"error": "no such message"}`. A valid ID returns the message, so a caller can tell which IDs exist. IDs are sequential integers, so a caller can walk the range. Combined with finding 1, a scoped caller could learn that a message exists in a mailbox they shouldn't see. The error also echoes the input back. This is minor on its own.

**3. Error verbosity is acceptable (informational).**
`get_source(source_type="not_a_real_type")` returned `{"error": "unknown source_type 'not_a_real_type'"}`. The message is terse, with no stack trace, SQL, file paths, or schema. The only issue is that it echoes the caller's input.

**4. `user_exact_quote` is not an authorization control (informational).**
Every tool requires a `user_exact_quote` argument that the model fills in. It is a self-reported attestation and can be anything. It should not be treated as proof of who asked or as an audit trail that holds up. Audit logging should key on the authenticated token.

**5. Documentation drift (informational, not a security issue).**
The navigator skill's snapshot reports 536 wiki pages, 11,728 facts, and 22,026 messages. `get_vault_stats` now reports 675 pages, 32,584 facts, and 25,249 messages. The stats are current, so the skill's figures are stale.

## Recommended safe verification steps

- **Scope test with a user-scoped token (if you have one):** confirm `whoami` returns an identity, then check that `mailbox` set to the other user is refused or silently filtered. Read only the error or the count, not the content.
- **Enumeration:** check whether a non-existent ID and a forbidden-but-existing ID return the same response. They should be indistinguishable. Also check that IDs are not sequential or guessable.
- **Result caps:** send a large `limit` to `search_raw` or `list_emails` and confirm the server caps it. Check only the returned count and the `truncated` flag.
- **Audit logs:** confirm that tool calls are logged with the authenticated identity, not the self-reported `user_exact_quote`.

I did not change any permissions, retrieve any messages or attachments, or run any destructive action.

Sources: `whoami` (admin/test token, signed_in false) · `get_vault_stats` (675 pages, 32,584 facts, 25,249 messages, 14,250 attachments) · `get_source` (error on unknown source_type) · `get_email` message_id 999999999 (no such message) · 3gm-navigator skill (stale snapshot figures)
