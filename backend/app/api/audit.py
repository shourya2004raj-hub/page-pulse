"""The Page Pulse audit endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from app.models.audit import AuditReport, AuditRequest
from app.services.audit_service import AuditService


router = APIRouter(prefix="/api", tags=["audit"])
audit_service = AuditService()


@router.post("/audit", response_model=AuditReport, summary="Audit a public webpage")
async def audit_page(payload: AuditRequest) -> AuditReport:
    """Fetch one public HTML page and return its audit metrics."""
    return await audit_service.audit(payload.url)

