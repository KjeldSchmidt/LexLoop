import uuid
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db.base import BaseUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import UUID4
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from lexloop.auth.user_repository import OAuthAccountRepo, UserRepo
from lexloop.auth.user_model import User
from lexloop.config import env_settings

_async_engine: AsyncEngine | None = None
_async_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _async_engine
    if _async_engine is None:
        _async_engine = create_async_engine(
            env_settings.DB_URL, echo=False, poolclass=NullPool
        )
    return _async_engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    global _async_sessionmaker
    if _async_sessionmaker is None:
        _async_sessionmaker = async_sessionmaker(
            get_engine(), expire_on_commit=False
        )
    return _async_sessionmaker


async def dispose_async_engine() -> None:
    """Dispose the lazy auth engine if tests or shutdown created one."""
    global _async_engine, _async_sessionmaker
    if _async_engine is not None:
        await _async_engine.dispose()
        _async_engine = None
        _async_sessionmaker = None


def reset_async_engine_for_tests() -> None:
    """Drop cached auth engine handles without disposing (test setup)."""
    global _async_engine, _async_sessionmaker
    _async_engine = None
    _async_sessionmaker = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[UserRepo, UUID4], None]:
    yield SQLAlchemyUserDatabase(session, UserRepo, OAuthAccountRepo)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = env_settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = env_settings.VERIFICATION_TOKEN_SECRET

    async def on_after_register(
        self, user: User, request: object | None = None
    ) -> None:
        """Google (and any) signups are teachers."""
        _ = request
        if getattr(user, "role", None) != "teacher":
            await self.user_db.update(user, {"role": "teacher"})


async def get_user_manager(
    user_db: BaseUserDatabase[User, uuid.UUID] = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
