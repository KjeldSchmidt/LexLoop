from typing import Generator

from fastapi.testclient import TestClient

from .main import app
from .repository import supabase

import pytest


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    # Clear all data before each test
    supabase.table("links").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
    supabase.table("nodes").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
    yield
    # Clear all data after each test
    supabase.table("links").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
    supabase.table("nodes").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
