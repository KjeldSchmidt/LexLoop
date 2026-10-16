"""Teacher auth: cookie JWT + Google OAuth. Public password register is disabled."""

import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from httpx_oauth.clients.google import GoogleOAuth2

from lexloop.auth.user_manager import get_user_manager
from lexloop.auth.user_model import User, UserRead, UserUpdate
from lexloop.config import env_settings

cookie_transport = CookieTransport(
    cookie_name="lexloop-userauth",
    cookie_max_age=60 * 60 * 12,
)


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    return JWTStrategy(
        secret=env_settings.JWT_SIGNING_SECRET,
        lifetime_seconds=60 * 60 * 12,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_teacher = fastapi_users.current_user(active=True, verified=True)

router = APIRouter(prefix="/auth")

router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["auth"],
)

google_oauth_client = GoogleOAuth2(
    env_settings.GOOGLE_OAUTH_CLIENT_ID,
    env_settings.GOOGLE_OAUTH_CLIENT_SECRET,
)

router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        state_secret=env_settings.JWT_SIGNING_SECRET,
        redirect_url=env_settings.GOOGLE_OAUTH_REDIRECT_URL,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix="/google",
    tags=["auth"],
)
