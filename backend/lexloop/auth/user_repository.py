from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from pydantic import UUID4
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from lexloop.repository import Base


class UserRepo(SQLAlchemyBaseUserTableUUID, Base):
    pass


# Create async engine and sessionmaker for auth only
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5435/lexloopdb"
async_engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[UserRepo, UUID4], None]:
    yield SQLAlchemyUserDatabase(session, UserRepo)
