"""Persistence for student accounts."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import Boolean, ForeignKey, String, select
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, Session, mapped_column

from lexloop.model.student_model import Student, StudentCreate
from lexloop.repository.base import Base


@dataclass(frozen=True, slots=True)
class StudentInsert:
    username: str
    hashed_password: str


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


def add_many(
    inserts: list[StudentInsert],
    teacher_id: UUID4,
    session: Session,
) -> list[Student]:
    """Insert many students in a single transaction."""
    rows = [
        StudentRepo(
            uuid=uuid4(),
            username=item.username,
            hashed_password=item.hashed_password,
            is_active=True,
            created_by_teacher_id=teacher_id,
        )
        for item in inserts
    ]
    session.add_all(rows)
    session.commit()
    for row in rows:
        session.refresh(row)
    return [row.to_internal_model() for row in rows]


def get_by_username(username: str, session: Session) -> StudentRepo | None:
    return session.scalar(
        select(StudentRepo).where(StudentRepo.username == username)
    )


def usernames_in_use(usernames: set[str], session: Session) -> set[str]:
    if not usernames:
        return set()
    rows = session.scalars(
        select(StudentRepo.username).where(StudentRepo.username.in_(usernames))
    ).all()
    return set(rows)


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


def set_passwords(
    updates: list[tuple[UUID4, str]], session: Session
) -> list[Student]:
    """Update many passwords in a single transaction."""
    rows: list[StudentRepo] = []
    for student_uuid, hashed_password in updates:
        row = session.get(StudentRepo, student_uuid)
        if row is None:
            raise KeyError
        row.hashed_password = hashed_password
        rows.append(row)
    session.commit()
    for row in rows:
        session.refresh(row)
    return [row.to_internal_model() for row in rows]


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


def delete(student_uuid: UUID4, session: Session) -> None:
    row = session.get(StudentRepo, student_uuid)
    if row is None:
        raise KeyError
    session.delete(row)
    session.commit()


def delete_many(student_uuids: list[UUID4], session: Session) -> None:
    rows = [
        session.get(StudentRepo, student_uuid) for student_uuid in student_uuids
    ]
    if any(row is None for row in rows):
        raise KeyError
    for row in rows:
        assert row is not None
        session.delete(row)
    session.commit()
