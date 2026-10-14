from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID

from lexloop.model.course_model import Course
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

    def to_internal_model(self) -> Course:
        return Course(
            uuid=self.uuid,
            name=str(self.name),
        )


def get_all(
    session: Session, *, offset: int, limit: int
) -> tuple[list[Course], int]:
    """Return a page of courses and the total count."""
    total = session.query(CourseRepo).count()
    rows: list[CourseRepo] = (
        session.query(CourseRepo).offset(offset).limit(limit).all()
    )
    return [course.to_internal_model() for course in rows], total
