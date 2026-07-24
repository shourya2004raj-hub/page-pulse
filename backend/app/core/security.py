"""URL validation and protections against requests to internal networks."""

from __future__ import annotations

import asyncio
import ipaddress
import socket
from urllib.parse import urlsplit

from app.core.exceptions import AuditError


def validate_url_format(raw_url: str) -> str:
    """Validate the URL shape before any DNS lookup or HTTP request."""
    url = raw_url.strip()
    if not url:
        raise AuditError("invalid_url", "Please provide a URL.", 400)

    try:
        parsed = urlsplit(url)
        _ = parsed.port  # Accessing this raises ValueError for invalid ports.
    except ValueError as exc:
        raise AuditError("invalid_url", "The URL is malformed.", 400) from exc

    if parsed.scheme not in {"http", "https"}:
        raise AuditError("invalid_url", "Only HTTP and HTTPS URLs are supported.", 400)
    if not parsed.hostname:
        raise AuditError("invalid_url", "The URL must include a hostname.", 400)
    if parsed.username or parsed.password:
        raise AuditError("invalid_url", "URLs with embedded credentials are not supported.", 400)

    return url


async def ensure_safe_destination(url: str) -> None:
    """Reject loopback, private, and otherwise non-public destinations.

    Resolving before each request also protects redirect hops. A production
    crawler may need a richer allow-list policy; this conservative baseline is
    appropriate for a public single-page audit tool.
    """
    safe_url = validate_url_format(url)
    hostname = urlsplit(safe_url).hostname
    assert hostname is not None  # Guaranteed by validate_url_format.

    normalized_host = hostname.rstrip(".").lower()
    if normalized_host == "localhost" or normalized_host.endswith(".localhost"):
        raise AuditError("unsafe_url", "Local and private network URLs are not allowed.", 400)

    try:
        addresses = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: socket.getaddrinfo(normalized_host, None, type=socket.SOCK_STREAM),
        )
    except socket.gaierror as exc:
        raise AuditError("dns_failure", "The domain could not be resolved.", 502) from exc

    resolved_ips = {record[4][0] for record in addresses}
    if not resolved_ips:
        raise AuditError("dns_failure", "The domain could not be resolved.", 502)

    try:
        if any(not ipaddress.ip_address(address).is_global for address in resolved_ips):
            raise AuditError("unsafe_url", "Local and private network URLs are not allowed.", 400)
    except ValueError as exc:
        raise AuditError("dns_failure", "The domain could not be resolved.", 502) from exc

