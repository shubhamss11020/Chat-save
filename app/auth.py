import contextvars
import hmac
import json
import os
from urllib.parse import parse_qs

from .config import AUTH_TOKEN, USERNAME

current_user: contextvars.ContextVar[str] = contextvars.ContextVar("current_user", default="")


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
        if path == "/health" or path.startswith("/.well-known/"):
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))
        got = headers.get(b"authorization", b"").decode().removeprefix("Bearer ").strip()
        qs = parse_qs(scope.get("query_string", b"").decode())
        if not got:
            got = qs.get("key", [""])[0].strip()

        explicit_user = qs.get("user", [""])[0].strip()
        matched_user = ""

        if got and got in USER_TOKENS_MAP:
            matched_user = USER_TOKENS_MAP[got]
        elif AUTH_TOKEN:
            if got and hmac.compare_digest(got.encode(), AUTH_TOKEN.encode()):
                matched_user = explicit_user or USERNAME or "user"
            else:
                body = b'{"detail":"unauthorized"}'
                await send({
                    "type": "http.response.start", "status": 401,
                    "headers": [(b"content-type", b"application/json"),
                                (b"content-length", str(len(body)).encode())]
                })
                await send({"type": "http.response.body", "body": body})
                return
        else:
            matched_user = explicit_user or USERNAME or "user"

        if explicit_user:
            matched_user = explicit_user

        token = current_user.set(matched_user)
        try:
            return await self.app(scope, receive, send)
        finally:
            current_user.reset(token)

