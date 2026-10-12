"""S3 / Object Storage client for Chat-Save attachments.
Supports AWS S3, Cloudflare R2, MinIO, and S3-compatible object storage.
"""
import base64
import logging
import mimetypes
import re
import time
from typing import Optional

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

    if not content_type:
        guessed, _ = mimetypes.guess_type(filename)
        content_type = guessed or "application/octet-stream"

    s3_key = build_s3_key(filename, conversation_id, user_id)

    upload_url = client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": s3_key,
            "ContentType": content_type,
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
            "Content-Type": content_type,
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
    Returns the permanent public URL on success, or None on failure.
    """
    client = get_s3_client()
    if not client or not S3_BUCKET_NAME:
        return None

    s3_key = build_s3_key(filename, conversation_id, user_id)
    raw_bytes: bytes

    if isinstance(content_data, bytes):
        raw_bytes = content_data
    elif isinstance(content_data, str) and content_data.startswith("data:") and ";base64," in content_data:
        try:
            header, b64_str = content_data.split(";base64,", 1)
            if not content_type:
                content_type = header.replace("data:", "").strip()
            raw_bytes = base64.b64decode(b64_str)
        except Exception as e:
            logger.error("Failed to decode base64 for %s: %s", filename, e)
            return None
    else:
        raw_bytes = str(content_data).encode("utf-8")

    if not content_type:
        guessed, _ = mimetypes.guess_type(filename)
        content_type = guessed or "application/octet-stream"

    try:
        client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=raw_bytes,
            ContentType=content_type,
        )
        return build_public_file_url(s3_key)
    except Exception as e:
        logger.error("S3 put_object failed for key %s: %s", s3_key, e)
        return None
