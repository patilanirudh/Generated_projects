"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from github_trending.main import create_app


@pytest.fixture()
def client() -> TestClient:
    """A TestClient bound to a fresh app instance."""
    with TestClient(create_app()) as test_client:
        yield test_client
