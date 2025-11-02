from typing import Generator

from fastapi.testclient import TestClient

from .main import app

import pytest


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_dynamodb() -> Generator[None, None, None]:
    yield
