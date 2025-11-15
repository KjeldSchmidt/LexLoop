from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from pydantic import UUID4
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from lexloop.repository.base import Base


class UserRepo(SQLAlchemyBaseUserTableUUID, Base):
    pass


# Create async engine and sessionmaker for auth only
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5435/lexloopdb"

# Lazy initialization to avoid event loop issues in tests
_async_engine = None
_async_sessionmaker = None


def get_engine() -> AsyncEngine:
    global _async_engine
    if _async_engine is None:
        _async_engine = create_async_engine(
            DATABASE_URL, echo=False, poolclass=NullPool
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
