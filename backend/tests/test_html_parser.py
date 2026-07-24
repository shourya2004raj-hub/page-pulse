"""Unit tests for deterministic HTML metric extraction."""

from pathlib import Path

from app.parsers.html_parser import parse_html_metrics


def test_parse_html_metrics_extracts_required_and_optional_fields() -> None:
    html = (Path(__file__).parent / "fixtures" / "sample_page.html").read_text(encoding="utf-8")

    metrics = parse_html_metrics(html, "https://example.com/audit/result")

    assert metrics["title"] == "Page Pulse Example"
    assert metrics["meta_description"] == "A concise example page for parser tests."
    assert metrics["h1_count"] == 2
    assert metrics["images_missing_alt"] == 1
    assert metrics["approximate_word_count"] == 10
    assert metrics["canonical_url"] == "https://example.com/canonical-page"
    assert metrics["favicon_url"] == "https://example.com/assets/favicon.png"
    assert metrics["open_graph_title"] == "Open Graph Example"


def test_parse_html_metrics_uses_favicon_fallback_and_allows_absent_metadata() -> None:
    metrics = parse_html_metrics("<html><body><p>Hello world.</p></body></html>", "https://example.com/path")

    assert metrics["title"] is None
    assert metrics["meta_description"] is None
    assert metrics["canonical_url"] is None
    assert metrics["favicon_url"] == "https://example.com/favicon.ico"
    assert metrics["approximate_word_count"] == 2
