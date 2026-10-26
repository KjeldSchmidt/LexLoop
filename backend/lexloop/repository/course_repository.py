"""Persistence for courses and student enrollments."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, Text, func, select
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, Session, mapped_column

from lexloop.model.course_model import Course, CourseIn
from lexloop.model.student_model import Student
from lexloop.repository.base import Base
from lexloop.repository.student_repository import StudentRepo


class CourseRepo(Base):
    __tablename__ = "lexloop_courses"

    uuid: Mapped[UUID4] = mapped_column(
        "uuid",
        POSTGRES_UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    description: Mapped[str] = mapped_column(
        "description", Text, nullable=False, default=""
    )
    owner_teacher_id: Mapped[UUID4 | None] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("user.id", name="course_owner_teacher_fk"),
        nullable=True,
    )
    signup_code: Mapped[str] = mapped_column(
        String(4), unique=True, nullable=False
    )

    def to_internal_model(self) -> Course:
        return Course(
            uuid=self.uuid,
            name=str(self.name),
            description=str(self.description or ""),
            owner_teacher_id=self.owner_teacher_id,
            signup_code=str(self.signup_code),
        )


class CourseEnrollmentRepo(Base):
    __tablename__ = "lexloop_course_enrollments"

    course_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey(
            "lexloop_courses.uuid",
            name="enrollment_course_fk",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    student_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey(
            "lexloop_students.uuid",
            name="enrollment_student_fk",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )


class CourseEnrollmentRequestRepo(Base):
    __tablename__ = "lexloop_course_enrollment_requests"

    course_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey(
            "lexloop_courses.uuid",
            name="join_request_course_fk",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    student_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey(
            "lexloop_students.uuid",
            name="join_request_student_fk",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )


def get_by_uuid(course_uuid: UUID4, session: Session) -> CourseRepo | None:
    return session.get(CourseRepo, course_uuid)


def get_by_signup_code(code: str, session: Session) -> CourseRepo | None:
    return session.scalar(
        select(CourseRepo).where(CourseRepo.signup_code == code)
    )


def list_for_teacher(
    teacher_id: UUID4, session: Session, *, offset: int, limit: int
) -> tuple[list[Course], int]:
    query = session.query(CourseRepo).where(
        CourseRepo.owner_teacher_id == teacher_id
    )
    total = query.count()
    rows = query.offset(offset).limit(limit).all()
    return [row.to_internal_model() for row in rows], total


def list_for_student(
    student_id: UUID4, session: Session, *, offset: int, limit: int
) -> tuple[list[Course], int]:
    query = (
        session.query(CourseRepo)
        .join(
            CourseEnrollmentRepo,
            CourseEnrollmentRepo.course_uuid == CourseRepo.uuid,
        )
        .where(CourseEnrollmentRepo.student_uuid == student_id)
    )
    total = query.count()
    rows = query.offset(offset).limit(limit).all()
    return [row.to_internal_model() for row in rows], total


def add(
    payload: CourseIn,
    owner_teacher_id: UUID4,
    signup_code: str,
    session: Session,
) -> Course:
    row = CourseRepo(
        uuid=uuid4(),
        name=payload.name,
        description=payload.description,
        owner_teacher_id=owner_teacher_id,
        signup_code=signup_code,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row.to_internal_model()


def update(
    course_uuid: UUID4,
    *,
    name: str | None,
    description: str | None,
    session: Session,
) -> Course:
    row = session.get(CourseRepo, course_uuid)
    if row is None:
        raise KeyError
    if name is not None:
        row.name = name
    if description is not None:
        row.description = description
    session.commit()
    session.refresh(row)
    return row.to_internal_model()


def set_signup_code(
    course_uuid: UUID4, signup_code: str, session: Session
) -> Course:
    row = session.get(CourseRepo, course_uuid)
    if row is None:
        raise KeyError
    row.signup_code = signup_code
    session.commit()
    session.refresh(row)
    return row.to_internal_model()


def delete_course(course_uuid: UUID4, session: Session) -> None:
    """Delete the course row (caller must remove content first)."""
    row = session.get(CourseRepo, course_uuid)
    if row is None:
        raise KeyError
    session.delete(row)
    session.commit()


def is_student_enrolled(
    course_uuid: UUID4, student_uuid: UUID4, session: Session
) -> bool:
    row = session.get(CourseEnrollmentRepo, (course_uuid, student_uuid))
    return row is not None


def list_enrolled_students(
    course_uuid: UUID4, session: Session
) -> list[Student]:
    rows = session.scalars(
        select(StudentRepo)
        .join(
            CourseEnrollmentRepo,
            CourseEnrollmentRepo.student_uuid == StudentRepo.uuid,
        )
        .where(CourseEnrollmentRepo.course_uuid == course_uuid)
    ).all()
    return [row.to_internal_model() for row in rows]


def add_enrollments(
    course_uuid: UUID4, student_uuids: list[UUID4], session: Session
) -> int:
    added = 0
    for student_uuid in student_uuids:
        existing = session.get(
            CourseEnrollmentRepo, (course_uuid, student_uuid)
        )
        if existing is not None:
            continue
        session.add(
            CourseEnrollmentRepo(
                course_uuid=course_uuid, student_uuid=student_uuid
            )
        )
        added += 1
    session.commit()
    return added


def remove_enrollments(
    course_uuid: UUID4, student_uuids: list[UUID4], session: Session
) -> int:
    if not student_uuids:
        return 0
    existing = session.scalars(
        select(CourseEnrollmentRepo).where(
            CourseEnrollmentRepo.course_uuid == course_uuid,
            CourseEnrollmentRepo.student_uuid.in_(student_uuids),
        )
    ).all()
    removed = len(existing)
    for row in existing:
        session.delete(row)
    session.commit()
    return removed


def has_join_request(
    course_uuid: UUID4, student_uuid: UUID4, session: Session
) -> bool:
    return (
        session.get(CourseEnrollmentRequestRepo, (course_uuid, student_uuid))
        is not None
    )


def add_join_request(
    course_uuid: UUID4, student_uuid: UUID4, session: Session
) -> None:
    if has_join_request(course_uuid, student_uuid, session):
        return
    session.add(
        CourseEnrollmentRequestRepo(
            course_uuid=course_uuid,
            student_uuid=student_uuid,
            requested_at=datetime.now(timezone.utc),
        )
    )
    session.commit()


def list_join_requests(
    course_uuid: UUID4, session: Session
) -> list[tuple[Student, datetime]]:
    rows = session.execute(
        select(StudentRepo, CourseEnrollmentRequestRepo.requested_at)
        .join(
            CourseEnrollmentRequestRepo,
            CourseEnrollmentRequestRepo.student_uuid == StudentRepo.uuid,
        )
        .where(CourseEnrollmentRequestRepo.course_uuid == course_uuid)
        .order_by(CourseEnrollmentRequestRepo.requested_at.asc())
    ).all()
    return [
        (student.to_internal_model(), requested_at)
        for student, requested_at in rows
    ]


def approve_join_requests(
    course_uuid: UUID4, student_uuids: list[UUID4], session: Session
) -> int:
    """Enroll pending students and remove their requests. Returns enrolled count."""
    if not student_uuids:
        return 0
    pending = session.scalars(
        select(CourseEnrollmentRequestRepo).where(
            CourseEnrollmentRequestRepo.course_uuid == course_uuid,
            CourseEnrollmentRequestRepo.student_uuid.in_(student_uuids),
        )
    ).all()
    enrolled = 0
    for request in pending:
        existing = session.get(
            CourseEnrollmentRepo,
            (course_uuid, request.student_uuid),
        )
        if existing is None:
            session.add(
                CourseEnrollmentRepo(
                    course_uuid=course_uuid,
                    student_uuid=request.student_uuid,
                )
            )
            enrolled += 1
        session.delete(request)
    session.commit()
    return enrolled


def approve_all_join_requests(course_uuid: UUID4, session: Session) -> int:
    pending_ids = list(
        session.scalars(
            select(CourseEnrollmentRequestRepo.student_uuid).where(
                CourseEnrollmentRequestRepo.course_uuid == course_uuid
            )
        ).all()
    )
    return approve_join_requests(course_uuid, pending_ids, session)
