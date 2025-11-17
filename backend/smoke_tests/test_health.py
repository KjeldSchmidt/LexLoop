import os

import httpx


def test_health_endpoint() -> None:
    """Test that the API health endpoint is accessible."""
    api_base_url = os.environ["API_BASE_URL"]

    response = httpx.get(f"{api_base_url}/health", timeout=10.0)

    assert response.status_code == 204


def test_health_endpoint() -> None:
    """Test that the API health endpoint is accessible."""
    api_base_url = os.environ["API_BASE_URL"]

    response = httpx.get(f"{api_base_url}/health/database", timeout=10.0)

    assert response.status_code == 204
