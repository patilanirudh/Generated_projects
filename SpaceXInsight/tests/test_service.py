"""Domain-logic tests for the service layer, using mocked Launch Library responses.

These verify the reliability math and the upcoming-launch mapping WITHOUT hitting
the live API, so they are deterministic and offline-safe.
"""

from __future__ import annotations

import httpx
import respx

from spacexinsight.clients.api_client import get_client
from spacexinsight.services.service import compute_reliability, list_upcoming

BASE = "https://ll.thespacedevs.com/2.2.0/"


@respx.mock
def test_compute_reliability_counts_success_and_failure() -> None:
    respx.get(f"{BASE}launch/previous/").mock(
        return_value=httpx.Response(
            200,
            json={
                "results": [
                    {"status": {"abbrev": "Success"}},
                    {"status": {"abbrev": "Success"}},
                    {"status": {"abbrev": "Failure"}},
                ]
            },
        )
    )
    client = get_client()
    try:
        result = compute_reliability(client, sample=3)
    finally:
        client.close()

    assert result.sample_size == 3
    assert result.successful == 2
    assert result.failed == 1
    assert result.success_rate_pct == 66.7


@respx.mock
def test_list_upcoming_maps_fields() -> None:
    respx.get(f"{BASE}launch/upcoming/").mock(
        return_value=httpx.Response(
            200,
            json={
                "results": [
                    {
                        "id": "abc-123",
                        "name": "Falcon 9 | Starlink",
                        "status": {"name": "Go for Launch"},
                        "net": "2026-08-01T12:00:00Z",
                        "lsp_name": "SpaceX",
                    }
                ]
            },
        )
    )
    client = get_client()
    try:
        launches = list_upcoming(client, limit=1)
    finally:
        client.close()

    assert len(launches) == 1
    launch = launches[0]
    assert launch.id == "abc-123"
    assert launch.name == "Falcon 9 | Starlink"
    assert launch.status == "Go for Launch"
    assert launch.provider == "SpaceX"
