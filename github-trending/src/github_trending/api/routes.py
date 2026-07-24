from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from github_trending.clients.api_client import ApiClient, get_client
from github_trending.models.schemas import Repository
from github_trending.services.service import fetch_trending_repositories, get_trending_repositories_for_language
from github_trending.core.exceptions import UpstreamError, NotFoundError

router = APIRouter(tags=["github-trending"])


def get_api_client():
    client = get_client()
    try:
        yield client
    finally:
        client.close()


@router.get("/trending/{language}", response_model=list[Repository])
def get_trending_repositories(language: str = Path(...), client: ApiClient = Depends(get_api_client)) -> list[Repository]:
    try:
        return get_trending_repositories_for_language(language)
    except (UpstreamError, NotFoundError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))