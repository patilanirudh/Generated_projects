"""Typed application errors and FastAPI exception handlers."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

log = logging.getLogger(__name__)


class AppError(Exception):
    """Base class for expected, client-facing errors."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class UpstreamError(AppError):
    """Raised when the upstream API fails or returns an unexpected response."""

    def __init__(self, message: str = "upstream service error") -> None:
        super().__init__(message, status_code=502)


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "not found") -> None:
        super().__init__(message, status_code=404)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach JSON error handlers so the service never leaks stack traces."""

    @app.exception_handler(AppError)
    async def _handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"error": exc.message})

    @app.exception_handler(Exception)
    async def _handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        log.exception("unhandled error: %s", exc)
        return JSONResponse(status_code=500, content={"error": "internal server error"})
