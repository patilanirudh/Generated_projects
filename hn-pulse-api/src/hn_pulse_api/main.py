"""Application entry point: builds the FastAPI app and runs it under uvicorn."""

from fastapi import FastAPI

from hn_pulse_api.api.health import router as health_router
from hn_pulse_api.api.routes import router as api_router
from hn_pulse_api.config import get_settings
from hn_pulse_api.core.exceptions import register_exception_handlers
from hn_pulse_api.logging_config import configure_logging


def create_app() -> FastAPI:
    """Application factory — wires routers, logging, and error handlers."""
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="A microservice providing trending and searched Hacker News stories via the public HN Algolia API.",
    )

    app.include_router(health_router)
    app.include_router(api_router, prefix="/api/v1")
    register_exception_handlers(app)
    return app


app = create_app()


def main() -> None:
    """Run the service with uvicorn (used by `python -m hn_pulse_api.main`)."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "hn_pulse_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )


if __name__ == "__main__":
    main()
