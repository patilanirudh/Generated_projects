# SpaceXInsight

A small FastAPI microservice that turns raw SpaceX launch data into decision-ready
signals for teams whose work depends on the launch schedule — aerospace, logistics,
and supply-chain planning.

It reads from the **[Launch Library 2 API](https://ll.thespacedevs.com/)**
(thespacedevs.com) — a public, documented, no-auth space-launch data source — and
exposes two clean JSON endpoints:

- **Launch reliability** — the SpaceX success rate over the most recent completed
  launches (a real, defensible signal, not a guess).
- **Upcoming launches** — the next scheduled SpaceX launches with dates, for
  planning around the manifest.

## Architecture

A thin, layered service:

- **api/** — FastAPI routers (`routes.py`, `health.py`).
- **services/** — the business logic: reliability math and upcoming-launch mapping.
- **clients/** — `api_client.py`, the only code that talks to Launch Library 2.
- **models/** — pydantic response schemas.
- **core/** — typed errors + exception handlers.

## Configuration

No credentials required. Configuration is read from the environment / `.env`:

| Variable          | Description                              | Default                              |
|-------------------|------------------------------------------|--------------------------------------|
| `API_BASE_URL`    | Launch Library 2 base URL                | `https://ll.thespacedevs.com/2.2.0/` |
| `REQUEST_TIMEOUT` | Upstream HTTP timeout (seconds)          | `10`                                 |
| `LOG_LEVEL`       | Log level                                | `INFO`                               |

## Running locally

```sh
pip install -r requirements.txt
PYTHONPATH=src uvicorn spacexinsight.main:app --reload
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs).

## API

### GET /api/v1/launches/reliability

SpaceX success rate over the most recent completed launches.

```sh
curl "http://localhost:8000/api/v1/launches/reliability?sample=100"
```

```json
{
  "provider": "SpaceX",
  "sample_size": 100,
  "successful": 99,
  "failed": 1,
  "success_rate_pct": 99.0
}
```

### GET /api/v1/launches/upcoming

The next scheduled SpaceX launches.

```sh
curl "http://localhost:8000/api/v1/launches/upcoming?limit=3"
```

```json
[
  {
    "id": "…",
    "name": "Falcon 9 Block 5 | Starlink Group 17-52",
    "status": "Go for Launch",
    "net": "2026-07-30T02:00:00Z",
    "provider": "SpaceX"
  }
]
```

> Note: Launch Library 2 rate-limits anonymous requests. For heavy use, add an API
> key per their docs; the service degrades gracefully (HTTP 502) if the upstream is
> unavailable.

## Testing

```sh
PYTHONPATH=src pytest
```

The suite covers health/readiness, the app's API surface, and the domain logic
(reliability math + upcoming mapping) against mocked Launch Library responses, so
it runs offline and deterministically.

## License

MIT
