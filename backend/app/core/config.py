"""Environment-backed configuration with safe development defaults."""

from __future__ import annotations

from dataclasses import dataclass
import os


def _positive_int(name: str, default: int) -> int:
    value = os.getenv(name, str(default))
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer.") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return parsed


def _positive_float(name: str, default: float) -> float:
    value = os.getenv(name, str(default))
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number.") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return parsed


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded once when the application starts."""

    app_env: str
    cors_origins: tuple[str, ...]
    request_timeout_seconds: float
    max_response_bytes: int
    max_redirects: int
    user_agent: str


def get_settings() -> Settings:
    raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    origins = tuple(origin.strip() for origin in raw_origins.split(",") if origin.strip())

    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        cors_origins=origins,
        request_timeout_seconds=_positive_float("REQUEST_TIMEOUT_SECONDS", 10),
        max_response_bytes=_positive_int("MAX_RESPONSE_BYTES", 2_000_000),
        max_redirects=_positive_int("MAX_REDIRECTS", 5),
        user_agent=os.getenv("USER_AGENT", "PagePulse/1.0"),
    )


settings = get_settings()

