"""Smoke tests: the app boots and exposes its API surface (no network calls)."""


def test_app_boots(client) -> None:
    assert client.get("/health").status_code == 200


def test_ready(client) -> None:
    assert client.get("/ready").status_code == 200


def test_api_routes_registered(client) -> None:
    paths = [getattr(route, "path", "") for route in client.app.routes]
    assert any(p.startswith("/api/v1") for p in paths)
