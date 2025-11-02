from typing import Any
from uuid import UUID

from fastapi_users.db.base import BaseUserDatabase
from pydantic import UUID4, EmailStr

from . import user_repository
from .user_model import (
    UserUpdate,
    User,
    UserCreateIn,
)


class PynamoDBUserDatabase(BaseUserDatabase[User, UUID]):
    async def get(self, uuid: UUID4) -> User | None:
        return user_repository.get(uuid)

    async def get_by_email(self, email: EmailStr) -> User | None:
        return user_repository.get_by_email(email)

    async def create(self, create_dict: dict[str, Any]) -> User:  # type: ignore[explicit-any]
        user_create = UserCreateIn(**create_dict)
        return user_repository.add(user_create)

    async def update(self, user: User, update_dict: dict[str, Any]) -> User:  # type: ignore[explicit-any]
        user_update = UserUpdate(**update_dict)
        return user_repository.update(user, user_update)

    async def delete(self, user: User) -> None:
        return user_repository.delete(user)


def get_user_db() -> BaseUserDatabase[User, UUID]:
    return PynamoDBUserDatabase()
