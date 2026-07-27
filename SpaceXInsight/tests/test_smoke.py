"""Smoke tests: the app boots and exposes its API surface (no network calls)."""


def test_app_boots(client) -> None:
    assert client.get("/health").status_code == 200


def test_ready(client) -> None:
    assert client.get("/ready").status_code == 200


def test_api_routes_registered(client) -> None:
    # Read the OpenAPI schema rather than walking app.routes: newer FastAPI
    # represents included routers as mount objects with no flat `.path`, so
    # introspecting app.routes misses them even though the endpoints work.
    schema = client.get("/openapi.json").json()
    assert any(path.startswith("/api/v1") for path in schema.get("paths", {}))
