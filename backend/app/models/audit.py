"""Request and response schemas for the page-audit API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AuditRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2_048, examples=["https://example.com"])


class AuditReport(BaseModel):
    url: str
    final_url: str
    http_status: int
    response_time_ms: int
    is_https: bool
    title: str | None
    meta_description: str | None
    h1_count: int
    images_missing_alt: int
    approximate_word_count: int
    canonical_url: str | None
    favicon_url: str | None
    open_graph_title: str | None


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail

