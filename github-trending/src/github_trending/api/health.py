"""Liveness and readiness probes."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Liveness probe")
def health() -> dict:
    """Return 200 if the process is alive."""
    return {"status": "ok"}


@router.get("/ready", summary="Readiness probe")
def ready() -> dict:
    """Return 200 if the service is ready to accept traffic."""
    return {"status": "ready"}
