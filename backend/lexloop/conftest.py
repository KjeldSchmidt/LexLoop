from typing import Generator

from fastapi.testclient import TestClient
from supabase import Client, create_client, ClientOptions

from .main import app
from .auth.dependencies import get_supabase_admin, get_supabase_client
from .config import environment

import pytest


@pytest.fixture(scope="session")
def supabase_admin() -> Client:
    """Admin client that bypasses RLS for tests."""
    return get_supabase_admin()


@pytest.fixture(scope="session")
def test_user(supabase_admin: Client) -> dict[str, str]:
    """Create a test user and return credentials + JWT."""
    email = "test@example.com"
    password = "test-password-123"

    # Clean up user if exists (admin can do this)
    try:
        supabase_admin.auth.admin.delete_user(email)
    except Exception:
        pass

    # Sign up test user
    auth_response = supabase_admin.auth.sign_up(
        {"email": email, "password": password}
    )

    return {
        "email": email,
        "password": password,
        "user_id": auth_response.user.id,  # type: ignore[union-attr]
        "jwt": auth_response.session.access_token,  # type: ignore[union-attr]
    }


@pytest.fixture(scope="session")
def test_user2(supabase_admin: Client) -> dict[str, str]:
    """Second test user for testing RLS isolation."""
    email = "test2@example.com"
    password = "test-password-456"

    try:
        supabase_admin.auth.admin.delete_user(email)
    except Exception:
        pass

    auth_response = supabase_admin.auth.sign_up(
        {"email": email, "password": password}
    )

    return {
        "email": email,
        "password": password,
        "user_id": auth_response.user.id,  # type: ignore[union-attr]
        "jwt": auth_response.session.access_token,  # type: ignore[union-attr]
    }


@pytest.fixture
def user_client(test_user: dict[str, str]) -> Client:
    """Get a user-scoped Supabase client (RLS enabled)."""
    return create_client(
        environment.SUPABASE_URL,
        environment.SUPABASE_ANON_KEY,
        options=ClientOptions(
            headers={"Authorization": f"Bearer {test_user['jwt']}"}
        ),
    )


@pytest.fixture
def user2_client(test_user2: dict[str, str]) -> Client:
    """Get a second user-scoped Supabase client (for testing isolation)."""
    return create_client(
        environment.SUPABASE_URL,
        environment.SUPABASE_ANON_KEY,
        options=ClientOptions(
            headers={"Authorization": f"Bearer {test_user2['jwt']}"}
        ),
    )


@pytest.fixture(scope="session")
def client(supabase_admin: Client) -> TestClient:
    """Test client with auth dependency overridden to use admin client (default)."""
    # Override the auth dependency to use admin client in tests
    app.dependency_overrides[get_supabase_client] = lambda: supabase_admin
    return TestClient(app)


@pytest.fixture
def client_as_user1(
    test_user: dict[str, str], user_client: Client
) -> Generator[TestClient, None, None]:
    """Test client that acts as test_user (RLS enabled)."""
    app.dependency_overrides[get_supabase_client] = lambda: user_client
    test_client = TestClient(app)
    yield test_client
    # Reset to admin after test
    app.dependency_overrides[get_supabase_client] = lambda: get_supabase_admin()


@pytest.fixture
def client_as_user2(
    test_user2: dict[str, str], user2_client: Client
) -> Generator[TestClient, None, None]:
    """Test client that acts as test_user2 (for testing RLS isolation)."""
    app.dependency_overrides[get_supabase_client] = lambda: user2_client
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides[get_supabase_client] = lambda: get_supabase_admin()


@pytest.fixture(autouse=True)
def reset_database(supabase_admin: Client) -> Generator[None, None, None]:
    # Clear all data before each test (using admin client)
    supabase_admin.table("links").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
    supabase_admin.table("nodes").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
    yield
    # Clear all data after each test
    supabase_admin.table("links").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
    supabase_admin.table("nodes").delete().neq(
        "uuid", "00000000-0000-0000-0000-000000000000"
    ).execute()
