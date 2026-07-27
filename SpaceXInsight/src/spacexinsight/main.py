"""Application entry point: builds the FastAPI app and runs it under uvicorn."""

from fastapi import FastAPI

from spacexinsight.api.health import router as health_router
from spacexinsight.api.routes import router as api_router
from spacexinsight.config import get_settings
from spacexinsight.core.exceptions import register_exception_handlers
from spacexinsight.logging_config import configure_logging


def create_app() -> FastAPI:
    """Application factory — wires routers, logging, and error handlers."""
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Analyzes SpaceX launch data to provide insights into potential operational efficiencies and cost reductions.",  # noqa: E501 - description may exceed line length
    )

    app.include_router(health_router)
    app.include_router(api_router, prefix="/api/v1")
    register_exception_handlers(app)
    return app


app = create_app()


def main() -> None:
    """Run the service with uvicorn (used by `python -m spacexinsight.main`)."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "spacexinsight.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )


if __name__ == "__main__":
    main()
