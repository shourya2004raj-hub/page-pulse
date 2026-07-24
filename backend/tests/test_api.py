"""API-contract tests for success and important failure responses."""

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.api.audit import audit_service
from app.core.exceptions import AuditError
from app.main import app
from app.models.audit import AuditReport


def test_audit_endpoint_returns_report(monkeypatch) -> None:
    report = AuditReport(
        url="https://example.com",
        final_url="https://example.com/",
        http_status=200,
        response_time_ms=120,
        is_https=True,
        title="Example Domain",
        meta_description=None,
        h1_count=1,
        images_missing_alt=0,
        approximate_word_count=10,
        canonical_url=None,
        favicon_url="https://example.com/favicon.ico",
        open_graph_title=None,
    )
    monkeypatch.setattr(audit_service, "audit", AsyncMock(return_value=report))

    response = TestClient(app).post("/api/audit", json={"url": "https://example.com"})

    assert response.status_code == 200
    assert response.json()["title"] == "Example Domain"
    assert response.json()["response_time_ms"] == 120


def test_audit_endpoint_rejects_invalid_url() -> None:
    response = TestClient(app).post("/api/audit", json={"url": "ftp://example.com"})

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "invalid_url",
            "message": "Only HTTP and HTTPS URLs are supported.",
        }
    }


def test_audit_endpoint_returns_timeout_error(monkeypatch) -> None:
    async def raise_timeout(_: str) -> None:
        raise AuditError("timeout", "The website took too long to respond.", 504)

    monkeypatch.setattr(audit_service, "audit", raise_timeout)

    response = TestClient(app).post("/api/audit", json={"url": "https://slow.example"})

    assert response.status_code == 504
    assert response.json()["error"]["code"] == "timeout"


def test_audit_endpoint_returns_non_html_error(monkeypatch) -> None:
    async def raise_non_html(_: str) -> None:
        raise AuditError("non_html_content", "The URL did not return an HTML webpage.", 422)

    monkeypatch.setattr(audit_service, "audit", raise_non_html)

    response = TestClient(app).post("/api/audit", json={"url": "https://example.com/report.pdf"})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "non_html_content"

