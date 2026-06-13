from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from hn_pulse_api.clients.api_client import ApiClient, get_client
from hn_pulse_api.models.schemas import ItemList, Item
from hn_pulse_api.services.service import fetch_trending_stories, search_stories


router = APIRouter(tags=["items"])


def get_api_client():
    client = get_client()
    try:
        yield client
    finally:
        client.close()


@router.get("/items/trending", response_model=ItemList)
def list_trending_items(client: ApiClient = Depends(get_api_client)) -> ItemList:
    return fetch_trending_stories(client)


@router.get("/items/search", response_model=ItemList)
def search_items(query: str = Query(...), client: ApiClient = Depends(get_api_client)) -> ItemList:
    return search_stories(client, query)