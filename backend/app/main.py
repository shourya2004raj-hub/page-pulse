"""FastAPI application entry point for Page Pulse."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.audit import router as audit_router
from app.core.config import settings
from app.core.exceptions import AuditError
from app.models.audit import ErrorDetail, ErrorResponse


app = FastAPI(
    title="Page Pulse API",
    version="1.0.0",
    description="Audits public HTML webpages and returns useful metadata.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


def error_payload(code: str, message: str) -> dict[str, object]:
    return ErrorResponse(error=ErrorDetail(code=code, message=message)).model_dump()


@app.exception_handler(AuditError)
async def handle_audit_error(_: Request, error: AuditError) -> JSONResponse:
    return JSONResponse(
        status_code=error.status_code,
        content=error_payload(error.code, error.message),
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, __: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=error_payload("invalid_request", "Send JSON with a non-empty 'url' field."),
    )


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(audit_router)

