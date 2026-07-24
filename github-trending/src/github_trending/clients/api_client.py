from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from github_trending.config import get_settings
from github_trending.core.exceptions import UpstreamError


class ApiClient:
    def __init__(self):
        settings = get_settings()
        self.client = httpx.Client(
            base_url=settings.api_base_url,
            timeout=httpx.Timeout(settings.request_timeout),
            headers={"Authorization": f"token {settings.github_api_key}"}
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
    def get_trending_repositories(self, language: str) -> list:
        response = self.client.get(f"/search/repositories?q=language:{language}&sort=stars&order=desc")
        response.raise_for_status()
        return response.json()["items"]

    def close(self) -> None:
        self.client.close()


def get_client() -> ApiClient:
    return ApiClient()