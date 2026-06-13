from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from hn_pulse_api.config import get_settings
from hn_pulse_api.clients.api_client import ApiClient, get_client
from hn_pulse_api.models.schemas import Item, ItemList
from hn_pulse_api.core.exceptions import AppError, UpstreamError, NotFoundError


def fetch_trending_stories(client: ApiClient) -> ItemList:
    try:
        raw_data = client.fetch_trending_stories()
        items = [Item(id=str(item.get("objectID") or item.get("id", "")), title=item.get("title") or "", url=item.get("url"), points=item.get("points", 0), author=item.get("author") or "") for item in raw_data["hits"]]
        return ItemList(items=items)
    except httpx.HTTPStatusError as e:
        raise UpstreamError from e


def search_stories(client: ApiClient, query: str) -> ItemList:
    try:
        raw_data = client.search_stories(query)
        items = [Item(id=str(item.get("objectID") or item.get("id", "")), title=item.get("title") or "", url=item.get("url"), points=item.get("points", 0), author=item.get("author") or "") for item in raw_data["hits"]]
        return ItemList(items=items)
    except httpx.HTTPStatusError as e:
        raise UpstreamError from e