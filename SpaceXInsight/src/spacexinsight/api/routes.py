from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from spacexinsight.clients.api_client import ApiClient, get_client
from spacexinsight.models.schemas import LaunchReliability, UpcomingLaunch
from spacexinsight.services.service import compute_reliability, list_upcoming

router = APIRouter(tags=["SpaceXInsight"])


def get_api_client():
    client = get_client()
    try:
        yield client
    finally:
        client.close()


@router.get("/launches/reliability", response_model=LaunchReliability)
def launch_reliability(
    sample: int = Query(100, ge=1, le=100, description="How many recent launches to score"),
    client: ApiClient = Depends(get_api_client),
) -> LaunchReliability:
    """SpaceX launch success rate over the most recent completed launches."""
    return compute_reliability(client, sample=sample)


@router.get("/launches/upcoming", response_model=list[UpcomingLaunch])
def upcoming_launches(
    limit: int = Query(5, ge=1, le=20, description="Number of upcoming launches to return"),
    client: ApiClient = Depends(get_api_client),
) -> list[UpcomingLaunch]:
    """Next scheduled SpaceX launches, for logistics and supply-chain planning."""
    return list_upcoming(client, limit=limit)
