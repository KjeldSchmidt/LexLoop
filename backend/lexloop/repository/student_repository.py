"""Persistence for student accounts."""

from __future__ import annotations

from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import Boolean, ForeignKey, String, select
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, Session, mapped_column

from lexloop.model.student_model import Student, StudentCreate
from lexloop.repository.base import Base


class StudentRepo(Base):
    __tablename__ = "lexloop_students"

    uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_by_teacher_id: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("user.id", name="student_teacher_fk"),
        nullable=False,
    )

    def to_internal_model(self) -> Student:
        return Student(
            uuid=self.uuid,
            username=self.username,
            is_active=self.is_active,
            created_by_teacher_id=self.created_by_teacher_id,
        )


def add(
    payload: StudentCreate,
    hashed_password: str,
    teacher_id: UUID4,
    session: Session,
) -> Student:
    row = StudentRepo(
        uuid=uuid4(),
        username=payload.username,
        hashed_password=hashed_password,
        is_active=True,
        created_by_teacher_id=teacher_id,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row.to_internal_model()


def get_by_username(username: str, session: Session) -> StudentRepo | None:
    return session.scalar(
        select(StudentRepo).where(StudentRepo.username == username)
    )


def get_by_uuid(student_uuid: UUID4, session: Session) -> StudentRepo | None:
    return session.get(StudentRepo, student_uuid)


def list_for_teacher(teacher_id: UUID4, session: Session) -> list[Student]:
    rows = session.scalars(
        select(StudentRepo).where(
            StudentRepo.created_by_teacher_id == teacher_id
        )
    ).all()
    return [row.to_internal_model() for row in rows]


def set_password(
    student_uuid: UUID4, hashed_password: str, session: Session
) -> Student:
    row = session.get(StudentRepo, student_uuid)
    if row is None:
        raise KeyError
    row.hashed_password = hashed_password
    session.commit()
    session.refresh(row)
    return row.to_internal_model()


def set_active(
    student_uuid: UUID4, is_active: bool, session: Session
) -> Student:
    row = session.get(StudentRepo, student_uuid)
    if row is None:
        raise KeyError
    row.is_active = is_active
    session.commit()
    session.refresh(row)
    return row.to_internal_model()
