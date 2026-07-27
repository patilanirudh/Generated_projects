from __future__ import annotations

from spacexinsight.clients.api_client import ApiClient
from spacexinsight.models.schemas import LaunchReliability, UpcomingLaunch


def _status_abbrev(item: dict) -> str:
    status = item.get("status") or {}
    return str(status.get("abbrev", ""))


def compute_reliability(client: ApiClient, sample: int = 100) -> LaunchReliability:
    """
    Compute SpaceX launch reliability from the most recent completed launches.
    A real, defensible signal (not a fabricated 'recommendation'): the share of
    launches that reached a Success status.
    """
    data = client.get_launches(upcoming=False, limit=sample)
    results = data.get("results", [])

    successful = sum(1 for r in results if _status_abbrev(r) == "Success")
    failed = sum(1 for r in results if _status_abbrev(r) == "Failure")
    counted = successful + failed
    rate = round(successful / counted * 100, 1) if counted else 0.0

    return LaunchReliability(
        provider="SpaceX",
        sample_size=len(results),
        successful=successful,
        failed=failed,
        success_rate_pct=rate,
    )


def list_upcoming(client: ApiClient, limit: int = 5) -> list[UpcomingLaunch]:
    """Return the next scheduled SpaceX launches for logistics/planning."""
    data = client.get_launches(upcoming=True, limit=limit)
    return [
        UpcomingLaunch(
            id=str(r.get("id", "")),
            name=str(r.get("name", "")),
            status=str((r.get("status") or {}).get("name", "")),
            net=r.get("net"),
            provider=str(r.get("lsp_name", "")),
        )
        for r in data.get("results", [])
    ]
