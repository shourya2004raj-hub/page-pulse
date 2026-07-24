"""Application errors that can safely be exposed through the API."""

from __future__ import annotations


class AuditError(Exception):
    """Known audit failure with a stable API error code and HTTP status."""

    def __init__(self, code: str, message: str, status_code: int) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

