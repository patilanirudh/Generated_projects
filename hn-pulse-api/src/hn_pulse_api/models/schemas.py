from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = ""
    title: str = ""
    url: str | None = None
    points: int = 0
    author: str = ""


class ItemList(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[Item] = []