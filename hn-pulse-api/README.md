# README.md

## Overview
The `hn-pulse-api` microservice provides trending and searched Hacker News stories via the public HN Algolia API. It fetches data from the upstream API, processes it, and exposes clean JSON endpoints for retrieving trending and searched stories.

This service is designed for developers who need to integrate Hacker News data into their applications without having to manage the complexities of fetching and processing raw data from the upstream API.

## Architecture
The service follows a layered architecture:
- **API Layer**: Handles HTTP requests and responses.
- **Services Layer**: Contains business logic and interacts with the clients layer.
- **Clients Layer**: Communicates with the upstream Hacker News Algolia API.
- **Models Layer**: Defines data models for processing and exposing data.

## Project Structure
```
hn_pulse_api/
├── .env.example
├── config.py
├── core/
│   ├── __init__.py
│   ├── exceptions.py
│   └── utils.py
├── clients/
│   ├── __init__.py
│   └── algolia_client.py
├── models/
│   ├── __init__.py
│   └── item_model.py
├── services/
│   ├── __init__.py
│   ├── item_service.py
│   └── search_service.py
├── main.py
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_item_service.py
    └── test_search_service.py
```

## Prerequisites
- Python 3.10+
- Docker (optional)
- Hacker News Algolia API key

## Configuration
The following environment variables are required:
- `API_BASE_URL`: Base URL for the service.
- `REQUEST_TIMEOUT`: Timeout for HTTP requests to the upstream API.
- `ALGOLIA_APP_ID`: Hacker News Algolia App ID.
- `ALGOLIA_API_KEY`: Hacker News Algolia API Key.

Example values:
```env
API_BASE_URL=http://localhost:8000/api/v1
REQUEST_TIMEOUT=5
ALGOLIA_APP_ID=your_app_id
ALGOLIA_API_KEY=your_api_key
```

## Running Locally
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Set environment variables (from `.env.example`):
   ```sh
   export API_BASE_URL=http://localhost:8000/api/v1
   export REQUEST_TIMEOUT=5
   export ALGOLIA_APP_ID=your_app_id
   export ALGOLIA_API_KEY=your_api_key
   ```
3. Run the service:
   ```sh
   PYTHONPATH=src uvicorn hn_pulse_api.main:app --reload
   ```
4. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Running with Docker
1. Build and run the container:
   ```sh
   docker compose up --build
   ```

## API
### GET /items/trending
- **Method**: GET
- **Path**: `/api/v1/items/trending`
- **Sample cURL**:
  ```sh
  curl -X 'GET' \
    'http://localhost:8000/api/v1/items/trending' \
    -H 'accept: application/json'
  ```
- **JSON Response**:
  ```json
  [
    {
      "id": 12345,
      "title": "Example Story",
      "url": "https://example.com",
      "points": 100,
      "author": "user123",
      "created_at_i": 1672531200
    }
  ]
  ```

### GET /items/search?q={query}
- **Method**: GET
- **Path**: `/api/v1/items/search?q=example`
- **Sample cURL**:
  ```sh
  curl -X 'GET' \
    'http://localhost:8000/api/v1/items/search?q=example' \
    -H 'accept: application/json'
  ```
- **JSON Response**:
  ```json
  [
    {
      "id": 12345,
      "title": "Example Story",
      "url": "https://example.com",
      "points": 100,
      "author": "user123",
      "created_at_i": 1672531200
    }
  ]
  ```

## Testing
Run tests using:
```sh
PYTHONPATH=src pytest
```

## License
MIT