from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from spacexinsight.config import get_settings
from spacexinsight.core.exceptions import UpstreamError


class ApiClient:
    """Thin client for the Launch Library 2 API (thespacedevs.com), read-only."""

    def __init__(self) -> None:
        settings = get_settings()
        self.client = httpx.Client(
            base_url=settings.api_base_url,
            timeout=httpx.Timeout(settings.request_timeout),
            headers={"User-Agent": "SpaceXInsight/0.1 (+https://github.com/patilanirudh)"},
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
    def get_launches(self, *, upcoming: bool, limit: int, search: str = "SpaceX") -> dict:
        """
        Fetch a page of SpaceX launches. `upcoming=True` returns scheduled launches,
        `upcoming=False` returns completed ones. Relative path (no leading slash) so
        the API version prefix in base_url is preserved.
        """
        path = "launch/upcoming/" if upcoming else "launch/previous/"
        try:
            response = self.client.get(
                path,
                params={"search": search, "limit": limit, "mode": "list"},
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise UpstreamError(f"Launch Library request failed: {exc}") from exc
        return response.json()

    def close(self) -> None:
        self.client.close()


def get_client() -> ApiClient:
    return ApiClient()
