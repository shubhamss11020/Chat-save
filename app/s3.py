"""S3 / Object Storage client for Chat-Save attachments.
Supports AWS S3, Cloudflare R2, MinIO, and S3-compatible object storage.
"""
import base64
import ipaddress
import logging
import mimetypes
import re
import socket
import time
import urllib.request
from typing import Optional
from urllib.parse import urlsplit

from .config import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET_NAME,
    S3_ENABLED,
    S3_ENDPOINT_URL,
    S3_PRESIGN_EXPIRATION_SECONDS,
    S3_PUBLIC_URL_PREFIX,
    S3_REGION,
    S3_SECRET_ACCESS_KEY,
)

logger = logging.getLogger(__name__)

_s3_client = None

MAX_REMOTE_ATTACHMENT_BYTES = 25 * 1024 * 1024


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse redirects: a public URL must not bounce the server to an internal address."""

    def redirect_request(self, *args, **kwargs):
        return None


_NO_REDIRECT_OPENER = urllib.request.build_opener(_NoRedirect)


def is_safe_remote_url(url: str) -> bool:
    """Only https URLs whose host resolves exclusively to public addresses.

    Stops the server from being used to probe internal networks (SSRF) when an
    attachment URL in a captured payload points at localhost, a LAN address or a
    cloud metadata endpoint.
    """
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname:
        return False
    try:
        infos = socket.getaddrinfo(parts.hostname, parts.port or 443, proto=socket.IPPROTO_TCP)
    except OSError:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            return False
    return True


def is_s3_configured() -> bool:
    """Check if S3 bucket and credentials are configured."""
    return bool(S3_BUCKET_NAME and (S3_ACCESS_KEY_ID or S3_ENDPOINT_URL))


def get_s3_client():
    """Get or create boto3 S3 client with configured endpoint and credentials."""
    global _s3_client
    if _s3_client is not None:
        return _s3_client

    try:
        import boto3
        from botocore.config import Config

        client_kwargs = {
            "service_name": "s3",
            "region_name": S3_REGION or "us-east-1",
            "config": Config(signature_version="s3v4"),
        }
        if S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY:
            client_kwargs["aws_access_key_id"] = S3_ACCESS_KEY_ID
            client_kwargs["aws_secret_access_key"] = S3_SECRET_ACCESS_KEY
        if S3_ENDPOINT_URL:
            client_kwargs["endpoint_url"] = S3_ENDPOINT_URL

        _s3_client = boto3.client(**client_kwargs)
        return _s3_client
    except Exception as e:
        logger.error("Failed to initialize S3 client: %s", e)
        return None


def resolve_mime_type(
    filename: str = "",
    content_type: Optional[str] = None,
    raw_bytes: bytes = b"",
) -> str:
    """Resolve a valid, canonical MIME type (never generic 'image', 'file', or extension-less).
    Ensures browsers can render images/documents directly instead of displaying a black screen.
    """
    # 1. Binary magic byte inspection is highest fidelity (immune to bad extension / headers)
    if raw_bytes:
        if raw_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if raw_bytes.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if raw_bytes.startswith(b"GIF87a") or raw_bytes.startswith(b"GIF89a"):
            return "image/gif"
        if raw_bytes.startswith(b"RIFF") and len(raw_bytes) >= 12 and raw_bytes[8:12] == b"WEBP":
            return "image/webp"
        if raw_bytes.startswith(b"%PDF-"):
            return "application/pdf"
        if raw_bytes.startswith(b"PK\x03\x04"):
            if filename.lower().endswith(".docx"):
                return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if filename.lower().endswith(".xlsx"):
                return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return "application/zip"
        # SVG detection
        sample = raw_bytes[:1024].lower()
        if b"<svg" in sample or (b"<?xml" in sample and b"<svg" in raw_bytes[:2048].lower()):
            return "image/svg+xml"

    # 2. Check provided content_type
    if content_type:
        ct = content_type.strip().lower()
        if ct == "svg":
            return "image/svg+xml"
        elif ct in ("jpg", "jpeg"):
            return "image/jpeg"
        elif ct == "png":
            return "image/png"
        elif ct == "gif":
            return "image/gif"
        elif ct == "webp":
            return "image/webp"
        elif ct == "pdf":
            return "application/pdf"
        elif "/" in ct and ct not in ("application/octet-stream", "binary/octet-stream", "image/*"):
            return ct

    # 3. Guess from filename
    if filename:
        ext_clean = filename.lower().strip()
        guessed, _ = mimetypes.guess_type(ext_clean)
        if guessed:
            return guessed
        ext = ext_clean.split(".")[-1] if "." in ext_clean else ""
        ext_map = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "webp": "image/webp",
            "svg": "image/svg+xml",
            "pdf": "application/pdf",
            "txt": "text/plain",
            "md": "text/markdown",
            "markdown": "text/markdown",
            "json": "application/json",
            "csv": "text/csv",
            "html": "text/html",
        }
        if ext in ext_map:
            return ext_map[ext]

    # 4. Fallback if content_type was generic 'image' or 'img'
    if content_type and content_type.strip().lower() in ("image", "img"):
        return "image/png"

    return "application/octet-stream"


def _clean_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal and bad S3 key characters."""
    clean = re.sub(r"[^a-zA-Z0-9._-]+", "_", filename).strip("_")
    return clean or f"attachment_{int(time.time())}"


def build_s3_key(filename: str, conversation_id: str, user_id: str = "user") -> str:
    """Construct deterministic yet unique S3 object key."""
    clean_name = _clean_filename(filename)
    clean_user = re.sub(r"[^a-zA-Z0-9_-]+", "-", user_id).strip("-") or "user"
    clean_conv = re.sub(r"[^a-zA-Z0-9_-]+", "-", conversation_id).strip("-") or "conv"
    timestamp = int(time.time())
    return f"attachments/{clean_user}/{clean_conv}/{timestamp}_{clean_name}"


def build_public_file_url(s3_key: str) -> str:
    """Generate the public or CDN URL for the uploaded S3 object."""
    if S3_PUBLIC_URL_PREFIX:
        return f"{S3_PUBLIC_URL_PREFIX}/{s3_key}"
    if S3_ENDPOINT_URL:
        # e.g., Cloudflare R2 or MinIO
        endpoint = S3_ENDPOINT_URL.rstrip("/")
        return f"{endpoint}/{S3_BUCKET_NAME}/{s3_key}"
    # Standard AWS S3 URL
    return f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{s3_key}"


def generate_presigned_download_url(
    s3_key: str,
    expiration: int = 86400,
) -> Optional[str]:
    """Generate a presigned GET URL for viewing an S3 object inline (valid for 24h).
    Enables viewing attachments even if the S3 bucket has Block Public Access enabled.
    """
    client = get_s3_client()
    if not client or not S3_BUCKET_NAME:
        return None
    try:
        guessed_type = resolve_mime_type(filename=s3_key)
        clean_basename = s3_key.split("/")[-1]
        params = {
            "Bucket": S3_BUCKET_NAME,
            "Key": s3_key,
            "ResponseContentDisposition": f'inline; filename="{clean_basename}"',
        }
        if guessed_type and guessed_type != "application/octet-stream":
            params["ResponseContentType"] = guessed_type

        return client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=expiration,
        )
    except Exception as e:
        logger.error("Failed to generate presigned download URL for %s: %s", s3_key, e)
        return None


def generate_presigned_upload_url(
    filename: str,
    content_type: Optional[str] = None,
    conversation_id: str = "default",
    user_id: str = "user",
    expiration: int = S3_PRESIGN_EXPIRATION_SECONDS,
) -> dict:
    """Generate presigned PUT URL for direct browser-to-S3 upload."""
    client = get_s3_client()
    if not client or not S3_BUCKET_NAME:
        raise RuntimeError("S3 is not configured. Set S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY.")

    canonical_mime = resolve_mime_type(filename=filename, content_type=content_type)

    clean_fname = filename
    if "." not in clean_fname:
        ext_map = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/svg+xml": ".svg",
            "application/pdf": ".pdf",
        }
        if canonical_mime in ext_map:
            clean_fname += ext_map[canonical_mime]

    s3_key = build_s3_key(clean_fname, conversation_id, user_id)
    content_disp = f'inline; filename="{clean_fname}"'

    upload_url = client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": s3_key,
            "ContentType": canonical_mime,
            "ContentDisposition": content_disp,
        },
        ExpiresIn=expiration,
    )

    file_url = build_public_file_url(s3_key)

    return {
        "upload_url": upload_url,
        "file_url": file_url,
        "s3_key": s3_key,
        "method": "PUT",
        "headers": {
            "Content-Type": canonical_mime,
            "Content-Disposition": content_disp,
        },
    }


def upload_attachment_data(
    filename: str,
    content_data: str | bytes,
    content_type: Optional[str] = None,
    conversation_id: str = "default",
    user_id: str = "user",
) -> Optional[str]:
    """Upload binary or base64 attachment directly to S3 from server.
    Ensures canonical MIME types and Content-Disposition: inline are applied
    so browsers render the file directly when clicked instead of a black screen.
    Returns the permanent public URL on success, or None on failure.
    """
    client = get_s3_client()
    if not client or not S3_BUCKET_NAME:
        return None

    raw_bytes: bytes = b""
    detected_mime: Optional[str] = None

    if isinstance(content_data, bytes):
        raw_bytes = content_data
    elif isinstance(content_data, str):
        content_str = content_data.strip()

        # Case A: Data URI e.g. "data:image/png;base64,iVBORw0KGgo..."
        if content_str.startswith("data:") and ";base64," in content_str:
            try:
                header, b64_str = content_str.split(";base64,", 1)
                mime_part = header.replace("data:", "").strip()
                if mime_part and "/" in mime_part:
                    detected_mime = mime_part
                raw_bytes = base64.b64decode(b64_str)
            except Exception as e:
                logger.error("Failed to decode data URI base64 for %s: %s", filename, e)
                return None

        # Case B: SVG XML text
        elif "<svg" in content_str.lower():
            raw_bytes = content_str.encode("utf-8")
            detected_mime = "image/svg+xml"

        # Case C: Remote HTTP URL - fetch actual bytes instead of saving URL string
        elif content_str.startswith("http://") or content_str.startswith("https://"):
            if not is_safe_remote_url(content_str):
                logger.warning("Refusing to fetch attachment URL %s (not https or not a public host)", content_str)
                return None
            try:
                req = urllib.request.Request(content_str, headers={"User-Agent": "Mozilla/5.0"})
                with _NO_REDIRECT_OPENER.open(req, timeout=10) as resp:
                    raw_bytes = resp.read(MAX_REMOTE_ATTACHMENT_BYTES + 1)
                    remote_ct = resp.headers.get_content_type()
                    if remote_ct and "/" in remote_ct:
                        detected_mime = remote_ct
                if len(raw_bytes) > MAX_REMOTE_ATTACHMENT_BYTES:
                    logger.warning("Attachment %s exceeds %d bytes, skipping", content_str, MAX_REMOTE_ATTACHMENT_BYTES)
                    return None
            except Exception as e:
                logger.warning("Could not fetch remote attachment URL %s: %s", content_str, e)
                return None

        # Case D: Browser blob URL cannot be fetched by server - avoid saving corrupt text
        elif content_str.startswith("blob:"):
            logger.warning("Cannot upload browser blob URL from server: %s", content_str)
            return None

        # Case E: Pure base64 string without data: prefix
        elif any(filename.lower().endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf")):
            try:
                clean_b64 = re.sub(r"\s+", "", content_str)
                raw_bytes = base64.b64decode(clean_b64, validate=True)
            except Exception:
                raw_bytes = content_str.encode("utf-8")
        else:
            raw_bytes = content_str.encode("utf-8")
    else:
        raw_bytes = str(content_data).encode("utf-8")

    if not raw_bytes:
        logger.warning("Empty attachment data for %s, skipping S3 upload", filename)
        return None

    # Guard: Never upload fake filename strings or invalid text placeholders as binary files
    if any(filename.lower().endswith(ext) for ext in (".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".docx", ".xlsx")):
        if isinstance(content_data, str) and content_data.strip() == filename.strip():
            logger.warning("Attachment %s content is merely its filename, skipping S3 upload", filename)
            return None
        if filename.lower().endswith(".pdf") and not raw_bytes.startswith(b"%PDF-"):
            logger.warning("Attachment %s lacks valid PDF header (%%PDF-), skipping S3 upload", filename)
            return None
        if filename.lower().endswith(".png") and not raw_bytes.startswith(b"\x89PNG"):
            logger.warning("Attachment %s lacks valid PNG header, skipping S3 upload", filename)
            return None
        if any(filename.lower().endswith(ext) for ext in (".jpg", ".jpeg")) and not raw_bytes.startswith(b"\xff\xd8"):
            logger.warning("Attachment %s lacks valid JPEG header, skipping S3 upload", filename)
            return None
        if len(raw_bytes) < 32:
            logger.warning("Attachment %s payload too small (%d bytes) for binary file, skipping S3 upload", filename, len(raw_bytes))
            return None

    # Resolve canonical MIME type (e.g. application/pdf, image/png, image/jpeg)
    canonical_mime = resolve_mime_type(
        filename=filename,
        content_type=detected_mime or content_type,
        raw_bytes=raw_bytes,
    )

    # Ensure filename has extension matching MIME if missing
    clean_fname = filename
    if "." not in clean_fname:
        ext_map = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/svg+xml": ".svg",
            "application/pdf": ".pdf",
        }
        if canonical_mime in ext_map:
            clean_fname += ext_map[canonical_mime]

    s3_key = build_s3_key(clean_fname, conversation_id, user_id)
    content_disp = f'inline; filename="{clean_fname}"'

    try:
        client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=raw_bytes,
            ContentType=canonical_mime,
            ContentDisposition=content_disp,
        )
        return build_public_file_url(s3_key)
    except Exception as e:
        logger.error("S3 put_object failed for key %s: %s", s3_key, e)
        return None

