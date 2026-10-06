import hmac
from urllib.parse import parse_qs

from .config import AUTH_TOKEN


class TokenAuth:
    """ASGI middleware: require MCP_AUTH_TOKEN (Bearer header or ?key=) on all but /health."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not AUTH_TOKEN or scope["path"] == "/health":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])
        got = headers.get(b"authorization", b"").decode().removeprefix("Bearer ").strip()
        if not got:
            got = parse_qs(scope["query_string"].decode()).get("key", [""])[0]
        if hmac.compare_digest(got.encode(), AUTH_TOKEN.encode()):
            return await self.app(scope, receive, send)
        body = b'{"detail":"unauthorized"}'
        await send({"type": "http.response.start", "status": 401,
                    "headers": [(b"content-type", b"application/json"),
                                (b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})
