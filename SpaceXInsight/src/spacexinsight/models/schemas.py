from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LaunchReliability(BaseModel):
    """Aggregated success/failure signal over recent SpaceX launches."""

    model_config = ConfigDict(extra="ignore")

    provider: str = "SpaceX"
    sample_size: int = 0
    successful: int = 0
    failed: int = 0
    success_rate_pct: float = 0.0


class UpcomingLaunch(BaseModel):
    """A single scheduled SpaceX launch, for logistics and planning."""

    model_config = ConfigDict(extra="ignore")

    id: str = ""
    name: str = ""
    status: str = ""
    net: str | None = None  # scheduled launch datetime, UTC (ISO 8601)
    provider: str = ""
