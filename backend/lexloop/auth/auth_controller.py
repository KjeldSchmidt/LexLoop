import os
import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from lexloop.auth.user_manager import get_user_manager
from lexloop.auth.user_model import User, UserCreate, UserRead

JWT_SIGNING_SECRET = os.getenv("JWT_SIGNING_SECRET", "")

# Todo: Evaluate if systems are silly and we need to make the school secure with shorter timeouts
cookie_transport = CookieTransport(
    cookie_name="lexloop-userauth",
    cookie_max_age=60 * 60 * 12,
)


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    return JWTStrategy(secret=JWT_SIGNING_SECRET, lifetime_seconds=60 * 60 * 12)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(prefix="/auth")

router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(
        user_schema=UserRead, user_create_schema=UserCreate
    ),
    tags=["auth"],
)
