"""Pure HTML-to-metrics parsing for Page Pulse."""

from __future__ import annotations

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


WORD_PATTERN = re.compile(r"\b[\w'-]+\b", re.UNICODE)


def _normalise_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalised = " ".join(value.split())
    return normalised or None


def _find_meta_content(soup: BeautifulSoup, attribute: str, value: str) -> str | None:
    tag = soup.find(
        "meta",
        attrs={attribute: lambda current: isinstance(current, str) and current.lower() == value},
    )
    return _normalise_text(tag.get("content")) if tag else None


def _find_canonical_url(soup: BeautifulSoup, base_url: str) -> str | None:
    for link in soup.find_all("link", href=True):
        rel = {item.lower() for item in link.get("rel", [])}
        if "canonical" in rel:
            return urljoin(base_url, link["href"])
    return None


def _find_favicon_url(soup: BeautifulSoup, base_url: str) -> str | None:
    for link in soup.find_all("link", href=True):
        rel = {item.lower() for item in link.get("rel", [])}
        if any("icon" in item for item in rel):
            return urljoin(base_url, link["href"])
    return urljoin(base_url, "/favicon.ico")


def parse_html_metrics(html: str, base_url: str) -> dict[str, str | int | None]:
    """Extract Page Pulse metrics without any network access."""
    soup = BeautifulSoup(html, "lxml")
    title_tag = soup.find("title")
    title = _normalise_text(title_tag.get_text()) if title_tag else None
    meta_description = _find_meta_content(soup, "name", "description")
    canonical_url = _find_canonical_url(soup, base_url)
    favicon_url = _find_favicon_url(soup, base_url)
    open_graph_title = _find_meta_content(soup, "property", "og:title")

    for ignored in soup(["head", "script", "style", "noscript", "template"]):
        ignored.decompose()

    visible_text = soup.get_text(" ", strip=True)

    return {
        "title": title,
        "meta_description": meta_description,
        "h1_count": len(soup.find_all("h1")),
        "images_missing_alt": sum(1 for image in soup.find_all("img") if not image.has_attr("alt")),
        "approximate_word_count": len(WORD_PATTERN.findall(visible_text)),
        "canonical_url": canonical_url,
        "favicon_url": favicon_url,
        "open_graph_title": open_graph_title,
    }
