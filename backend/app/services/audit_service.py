"""Orchestrates a fetch and a parsing pass into one audit report."""

from __future__ import annotations

from app.core.exceptions import AuditError
from app.core.security import validate_url_format
from app.models.audit import AuditReport
from app.parsers.html_parser import parse_html_metrics
from app.services.page_fetcher import fetch_page


class AuditService:
    """Application service for the URL-audit use case."""

    async def audit(self, raw_url: str) -> AuditReport:
        requested_url = validate_url_format(raw_url)
        page = await fetch_page(requested_url)

        try:
            metrics = parse_html_metrics(page.html, page.final_url)
        except Exception as exc:  # Parser libraries can fail on malformed input.
            raise AuditError("parser_failure", "The webpage could not be parsed safely.", 500) from exc

        return AuditReport(
            url=requested_url,
            final_url=page.final_url,
            http_status=page.status_code,
            response_time_ms=page.response_time_ms,
            is_https=page.final_url.startswith("https://"),
            **metrics,
        )

