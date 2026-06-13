from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from hn_pulse_api.config import get_settings
from hn_pulse_api.core.exceptions import UpstreamError


class ApiClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = httpx.Client(base_url=settings.api_base_url, timeout=settings.request_timeout)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
    def fetch_trending_stories(self) -> dict:
        response = self.client.get("/search_by_date?tags=story")
        response.raise_for_status()
        return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
    def search_stories(self, query: str) -> dict:
        response = self.client.get(f"/search?query={query}&tags=story")
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        self.client.close()


def get_client() -> ApiClient:
    return ApiClient()