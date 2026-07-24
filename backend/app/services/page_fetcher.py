"""Bounded, redirect-aware HTTP retrieval for webpage audits."""

from __future__ import annotations

from dataclasses import dataclass
import ssl
import time
from urllib.parse import urljoin

import httpx

from app.core.config import settings
from app.core.exceptions import AuditError
from app.core.security import ensure_safe_destination


REDIRECT_STATUS_CODES = {301, 302, 303, 307, 308}
HTML_CONTENT_TYPES = {"text/html", "application/xhtml+xml"}


@dataclass(frozen=True)
class FetchedPage:
    final_url: str
    status_code: int
    html: str
    response_time_ms: int


def _is_html_response(content_type: str | None) -> bool:
    if not content_type:
        return False
    media_type = content_type.split(";", 1)[0].strip().lower()
    return media_type in HTML_CONTENT_TYPES


def _map_httpx_error(error: httpx.HTTPError) -> AuditError:
    if isinstance(error, httpx.TimeoutException):
        return AuditError("timeout", "The website took too long to respond.", 504)

    error_text = str(error).lower()
    cause = error.__cause__
    if isinstance(cause, ssl.SSLError) or "ssl" in error_text or "certificate" in error_text:
        return AuditError("ssl_failure", "A secure connection to this website could not be established.", 502)
    return AuditError("network_failure", "The website could not be reached.", 502)


async def fetch_page(url: str) -> FetchedPage:
    """Fetch a public HTML page, validating every redirect destination."""
    started_at = time.perf_counter()
    current_url = url
    timeout = httpx.Timeout(settings.request_timeout_seconds)
    headers = {"User-Agent": settings.user_agent, "Accept": "text/html,application/xhtml+xml"}

    try:
        async with httpx.AsyncClient(timeout=timeout, headers=headers, follow_redirects=False) as client:
            for redirect_count in range(settings.max_redirects + 1):
                await ensure_safe_destination(current_url)

                async with client.stream("GET", current_url) as response:
                    if response.status_code in REDIRECT_STATUS_CODES:
                        location = response.headers.get("location")
                        if not location:
                            raise AuditError("network_failure", "The website returned an invalid redirect.", 502)
                        if redirect_count == settings.max_redirects:
                            raise AuditError("too_many_redirects", "The website redirected too many times.", 502)
                        current_url = urljoin(str(response.url), location)
                        continue

                    if not _is_html_response(response.headers.get("content-type")):
                        raise AuditError("non_html_content", "The URL did not return an HTML webpage.", 422)

                    declared_size = response.headers.get("content-length")
                    if declared_size and int(declared_size) > settings.max_response_bytes:
                        raise AuditError("content_too_large", "The webpage is too large to audit safely.", 422)

                    content = bytearray()
                    async for chunk in response.aiter_bytes():
                        content.extend(chunk)
                        if len(content) > settings.max_response_bytes:
                            raise AuditError("content_too_large", "The webpage is too large to audit safely.", 422)

                    encoding = response.encoding or "utf-8"
                    elapsed_ms = round((time.perf_counter() - started_at) * 1_000)
                    return FetchedPage(
                        final_url=str(response.url),
                        status_code=response.status_code,
                        html=content.decode(encoding, errors="replace"),
                        response_time_ms=elapsed_ms,
                    )
    except AuditError:
        raise
    except httpx.HTTPError as exc:
        raise _map_httpx_error(exc) from exc
    except ValueError as exc:
        raise AuditError("network_failure", "The website returned an invalid response.", 502) from exc

    raise AuditError("network_failure", "The website could not be reached.", 502)

