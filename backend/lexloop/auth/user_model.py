import uuid
from pydantic import BaseModel, UUID4

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):  # type: ignore
    pass


class UserCreate(schemas.BaseUserCreate):  # type: ignore
    pass


class UserUpdate(schemas.BaseUserUpdate):  # type: ignore
    pass


class User(BaseModel):  # type: ignore
    id: UUID4
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreateIn(BaseModel):  # type: ignore
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
