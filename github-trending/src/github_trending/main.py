"""Application entry point: builds the FastAPI app and runs it under uvicorn."""

from fastapi import FastAPI

from github_trending.api.health import router as health_router
from github_trending.api.routes import router as api_router
from github_trending.config import get_settings
from github_trending.core.exceptions import register_exception_handlers
from github_trending.logging_config import configure_logging


def create_app() -> FastAPI:
    """Application factory — wires routers, logging, and error handlers."""
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Provides access to the trending GitHub repositories.",
    )

    app.include_router(health_router)
    app.include_router(api_router, prefix="/api/v1")
    register_exception_handlers(app)
    return app


app = create_app()


def main() -> None:
    """Run the service with uvicorn (used by `python -m github_trending.main`)."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "github_trending.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )


if __name__ == "__main__":
    main()
