import uuid
from pydantic import BaseModel, UUID4

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):  # type: ignore[explicit-any]
    pass


class UserCreate(schemas.BaseUserCreate):  # type: ignore[explicit-any]
    pass


class UserUpdate(schemas.BaseUserUpdate):  # type: ignore[explicit-any]
    pass


class User(BaseModel):  # type: ignore[explicit-any]
    id: UUID4
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreateIn(BaseModel):  # type: ignore[explicit-any]
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
