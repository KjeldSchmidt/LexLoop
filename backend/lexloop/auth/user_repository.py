from uuid import uuid4

from pydantic import UUID4, EmailStr
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
from pynamodb.models import Model

from lexloop.auth.user_model import (
    UserUpdate,
    User,
    UserCreateIn,
)
from lexloop.repository import MetaBase


class UserRepo(Model):
    class Meta(MetaBase):
        table_name = "lexloop-users"

    uuid = UnicodeAttribute(hash_key=True, default_for_new=lambda: str(uuid4()))
    email = UnicodeAttribute()
    hashed_password = UnicodeAttribute()
    is_active = BooleanAttribute(default=True)
    is_superuser = BooleanAttribute(default=False)
    is_verified = BooleanAttribute(default=False)

    def to_internal_model(self) -> User:
        return User(
            id=self.uuid,
            email=self.email,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
        )


def get(uuid: UUID4) -> User | None:
    try:
        return UserRepo.get(str(uuid)).to_internal_model()
    except UserRepo.DoesNotExist:
        return None


def get_by_email(email: EmailStr) -> User | None:
    for user in UserRepo.scan(UserRepo.email == email):
        return user.to_internal_model()
    return None


def add(user: UserCreateIn) -> User:
    user_repo = UserRepo(
        uuid=str(uuid4()),
        email=user.email,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified,
    )
    user_repo.save()
    return user_repo.to_internal_model()


def update(user: User, user_update: UserUpdate) -> User:
    user_repo = UserRepo.get(user.id)

    updated_email = user_update.email or user_repo.email
    updated_password = user_update.password or user_repo.hashed_password
    updated_is_active = user_update.is_active or user_repo.is_active
    updated_is_superuser = user_update.is_superuser or user_repo.is_superuser
    updated_is_verified = user_update.is_verified or user_repo.is_verified

    user_repo.update(
        actions=[
            UserRepo.email.set(updated_email),
            UserRepo.hashed_password.set(updated_password),
            UserRepo.is_active.set(updated_is_active),
            UserRepo.is_superuser.set(updated_is_superuser),
            UserRepo.is_verified.set(updated_is_verified),
        ]
    )
    return user_repo.to_internal_model()


def delete(user: User) -> None:
    UserRepo.get(user.id).delete()
