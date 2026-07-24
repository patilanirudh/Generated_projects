from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Repository(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int = 0
    name: str = ""
    owner: str = ""
    url: str | None = None
    description: str | None = None
    stars: int = 0