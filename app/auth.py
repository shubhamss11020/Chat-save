import contextvars
import hmac
import json
import os
from urllib.parse import parse_qs

from .config import ALLOW_OPEN, AUTH_TOKEN, UNKNOWN_USER, USERNAME

current_user: contextvars.ContextVar[str] = contextvars.ContextVar("current_user", default="")
# True when the request authenticated with a per-person token (identity cannot be overridden).
token_bound_var: contextvars.ContextVar[bool] = contextvars.ContextVar("token_bound", default=False)


async def _reject(send) -> None:
    body = b'{"detail":"unauthorized"}'
    await send({
        "type": "http.response.start", "status": 401,
        "headers": [(b"content-type", b"application/json"),
                    (b"content-length", str(len(body)).encode())]
    })
    await send({"type": "http.response.body", "body": body})


def _load_user_tokens() -> dict[str, str]:
    """Parse USER_TOKENS env var if provided.
    Supports either JSON: '{"token1": "rajat", "token2": "shubham"}'
    or comma-separated: 'rajat:token1,shubham:token2'
    """
    raw = os.getenv("USER_TOKENS", "").strip()
    if not raw:
        return {}
    if raw.startswith("{"):
        try:
            return json.loads(raw)
        except Exception:
            pass
    mapping = {}
    for part in raw.split(","):
        if ":" in part:
            user, tok = part.strip().split(":", 1)
            mapping[tok.strip()] = user.strip()
    return mapping


USER_TOKENS_MAP = _load_user_tokens()


class TokenAuth:
    """ASGI middleware: require MCP_AUTH_TOKEN / user tokens and bind user identity."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # /.well-known stays open (it 404s) so clients don't mistake our 401 for an OAuth server
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope["path"]
        if path == "/health" or path.startswith("/.well-known/") or scope.get("method") == "OPTIONS":
            return await self.app(scope, receive, send)

        # Fail closed: a server with no tokens configured accepts nobody (unless opted in).
        if not AUTH_TOKEN and not USER_TOKENS_MAP and not ALLOW_OPEN:
            return await _reject(send)

        headers = dict(scope.get("headers", []))
        got = headers.get(b"authorization", b"").decode().removeprefix("Bearer ").strip()
        qs = parse_qs(scope.get("query_string", b"").decode())
        if not got:
            got = qs.get("key", [""])[0].strip()

        explicit_user = qs.get("user", [""])[0].strip()

        if got and got in USER_TOKENS_MAP:
            # Per-person token: the token alone decides who this is. ?user= is ignored.
            matched_user = USER_TOKENS_MAP[got]
            token_bound = True
        elif AUTH_TOKEN and got and hmac.compare_digest(got.encode(), AUTH_TOKEN.encode()):
            # Shared owner token: identity is the server owner. ?user= is NOT honoured,
            # otherwise anyone holding the shared token could act as any person.
            matched_user = USERNAME or UNKNOWN_USER
            token_bound = False
        elif ALLOW_OPEN and not AUTH_TOKEN and not USER_TOKENS_MAP:
            # Explicit local-development mode only.
            matched_user = explicit_user or USERNAME or UNKNOWN_USER
            token_bound = False
        else:
            return await _reject(send)

        user_reset = current_user.set(matched_user)
        bound_reset = token_bound_var.set(token_bound)
        try:
            return await self.app(scope, receive, send)
        finally:
            token_bound_var.reset(bound_reset)
            current_user.reset(user_reset)

