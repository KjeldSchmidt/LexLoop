from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from lexloop.repository import Base


class UserRepo(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:  # type: ignore
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[UserRepo, UUID4], None]:
    yield SQLAlchemyUserDatabase(session, UserRepo)
