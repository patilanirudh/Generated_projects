# GitHub Trending Service

## Overview
The GitHub Trending Service is a microservice designed to provide access to trending repositories on GitHub via clean JSON endpoints. It wraps the GitHub REST API, allowing users to fetch trending repositories for specific programming languages.

## Architecture
The service follows a layered architecture:
- **API Layer**: Handles HTTP requests and responses.
- **Services Layer**: Contains business logic and interacts with the clients layer.
- **Clients Layer**: Communicates with the upstream GitHub API.
- **Models Layer**: Defines data models for repository information.

## Project Structure
```
github_trending/
├── api/
│   ├── __init__.py
│   └── routes.py
├── core/
│   ├── __init__.py
│   ├── exceptions.py
│   └── services.py
├── clients/
│   ├── __init__.py
│   └── github_client.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── models/
│   ├── __init__.py
│   └── repository.py
├── main.py
├── requirements.txt
└── README.md
```

## Prerequisites
- Python 3.10+
- Docker (optional)
- GitHub API credentials

## Configuration
The following environment variables are required:
- `API_BASE_URL`: Base URL of the GitHub API.
- `REQUEST_TIMEOUT`: Timeout for requests to the GitHub API.
- `GITHUB_CLIENT_ID`: Client ID for authenticating with the GitHub API.
- `GITHUB_CLIENT_SECRET`: Client secret for authenticating with the GitHub API.

Example values:
```
API_BASE_URL=https://api.github.com
REQUEST_TIMEOUT=10
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
```

## Running Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run the service: `PYTHONPATH=src uvicorn github_trending.main:app --reload`
3. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

## Running with Docker
1. Build and run the container: `docker compose up --build`

## API
### GET /api/v1/trending/{language}
- **Method**: GET
- **Path**: `/api/v1/trending/{language}`
- **Sample Request**:
  ```sh
  curl -X GET "http://localhost:8000/api/v1/trending/python" -H "accept: application/json"
  ```
- **Sample Response**:
  ```json
  [
    {
      "id": 12345,
      "name": "example-repo",
      "owner": "user",
      "url": "https://github.com/user/example-repo",
      "description": "An example repository.",
      "stars": 100
    }
  ]
  ```

## Testing
Run tests using pytest: `PYTHONPATH=src pytest`

## License
MIT