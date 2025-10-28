"""Auth dependencies for FastAPI routes."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client, create_client, ClientOptions
from lexloop.config import environment

security = HTTPBearer()


def get_supabase_client(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Client:
    """
    Create a user-scoped Supabase client using the JWT from the request.

    RLS policies will automatically filter data based on the authenticated user.
    """
    token = credentials.credentials

    try:
        # Create client with user's JWT - RLS will be enforced
        client = create_client(
            environment.SUPABASE_URL,
            environment.SUPABASE_ANON_KEY,  # Use anon key for RLS
            options=ClientOptions(headers={"Authorization": f"Bearer {token}"}),
        )
        return client
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


def get_supabase_admin() -> Client:
    """
    Get admin Supabase client (bypasses RLS).
    Use only for tests or admin operations.
    """
    return create_client(
        environment.SUPABASE_URL, environment.SUPABASE_SERVICE_ROLE_KEY
    )
