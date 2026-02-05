from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID

from lexloop.repository.base import Base


class CourseRepo(Base):
    __tablename__ = "lexloop_courses"

    uuid: Mapped[UUID4] = mapped_column(
        "uuid",
        POSTGRES_UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column("name", String(100))
