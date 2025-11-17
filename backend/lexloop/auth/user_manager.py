import os
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

from lexloop.repository import UserRepo
from .user_model import User
from ..config import env_settings
from sqlalchemy.pool import NullPool

# Create async engine and sessionmaker for auth only

# Lazy initialization to avoid event loop issues in tests
_async_engine = None
_async_sessionmaker = None


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


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[UserRepo, UUID4], None]:
    yield SQLAlchemyUserDatabase(session, UserRepo)


RESET_PASSWORD_TOKEN_SECRET = os.getenv("RESET_PASSWORD_TOKEN_SECRET", "")
VERIFICATION_TOKEN_SECRET = os.getenv("VERIFICATION_TOKEN_SECRET", "")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = VERIFICATION_TOKEN_SECRET


async def get_user_manager(
    user_db: BaseUserDatabase[User, uuid.UUID] = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
