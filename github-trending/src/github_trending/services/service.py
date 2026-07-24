from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from github_trending.config import get_settings
from github_trending.clients.api_client import ApiClient, get_client
from github_trending.models.schemas import Repository
from github_trending.core.exceptions import UpstreamError, NotFoundError


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
def fetch_trending_repositories(language: str) -> list[Repository]:
    client = get_client()
    try:
        items = client.get_trending_repositories(language)
        return [
            Repository(
                id=item.get("id", 0),
                name=item.get("name", ""),
                owner=item.get("owner", {}).get("login", ""),
                url=item.get("html_url"),
                description=item.get("description"),
                stars=item.get("stargazers_count", 0)
            )
            for item in items
        ]
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise NotFoundError(f"No trending repositories found for language: {language}")
        else:
            raise UpstreamError from e


def get_trending_repositories_for_language(language: str) -> list[Repository]:
    try:
        return fetch_trending_repositories(language)
    except (UpstreamError, NotFoundError) as e:
        raise e