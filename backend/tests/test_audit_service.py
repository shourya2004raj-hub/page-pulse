"""Tests for service-level validation and parser-failure behavior."""

import asyncio
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import AuditError
from app.services.audit_service import AuditService
from app.services.page_fetcher import FetchedPage


def test_audit_service_rejects_unsupported_protocol_before_fetching() -> None:
    with pytest.raises(AuditError) as exc_info:
        asyncio.run(AuditService().audit("ftp://example.com"))

    assert exc_info.value.code == "invalid_url"
    assert exc_info.value.status_code == 400


def test_audit_service_returns_parser_failure_when_parser_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    fetched_page = FetchedPage(
        final_url="https://example.com/",
        status_code=200,
        html="<html></html>",
        response_time_ms=25,
    )
    monkeypatch.setattr("app.services.audit_service.fetch_page", AsyncMock(return_value=fetched_page))

    def raise_parser_error(_: str, __: str) -> dict[str, str]:
        raise ValueError("Malformed markup exposed a parser problem")

    monkeypatch.setattr("app.services.audit_service.parse_html_metrics", raise_parser_error)

    with pytest.raises(AuditError) as exc_info:
        asyncio.run(AuditService().audit("https://example.com"))

    assert exc_info.value.code == "parser_failure"
    assert exc_info.value.status_code == 500

