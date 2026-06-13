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

    app_name: str = "hn-pulse-api"
    environment: str = "development"
    log_level: str = "INFO"
    request_timeout: float = 10.0
    api_base_url: str = "https://hn.algolia.com/api/v1"

    # Upstream credentials (read from environment variables)
    # (no external credentials required)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
