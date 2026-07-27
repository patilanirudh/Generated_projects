"""Typed application settings loaded from the environment / .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All runtime configuration, validated at startup."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SpaceXInsight"
    environment: str = "development"
    log_level: str = "INFO"
    request_timeout: float = 10.0
    # Launch Library 2 (thespacedevs.com) — public, read-only, no auth required.
    api_base_url: str = "https://ll.thespacedevs.com/2.2.0/"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
