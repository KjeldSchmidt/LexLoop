from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lexloop.repository.base import Base


class OAuthAccountRepo(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class UserRepo(SQLAlchemyBaseUserTableUUID, Base):
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default="teacher"
    )
    oauth_accounts: Mapped[list[OAuthAccountRepo]] = relationship(
        "OAuthAccountRepo", lazy="joined"
    )
