"""Application service for students."""

from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.memorable_ids import generate_password, generate_username
from lexloop.auth.student_auth import hash_password, verify_password
from lexloop.model.student_model import (
    Student,
    StudentCreate,
    StudentCreatedCreds,
)
from lexloop.repository import student_repository

_MAX_USERNAME_ATTEMPTS = 32


def create_for_teacher(
    payload: StudentCreate, teacher_id: UUID4, session: Session
) -> Student:
    existing = student_repository.get_by_username(payload.username, session)
    if existing is not None:
        raise ValueError("USERNAME_TAKEN")
    return student_repository.add(
        payload, hash_password(payload.password), teacher_id, session
    )


def bulk_create_for_teacher(
    count: int, teacher_id: UUID4, session: Session
) -> list[StudentCreatedCreds]:
    """Create ``count`` students with memorable usernames and phrase passwords."""
    created: list[StudentCreatedCreds] = []
    for _ in range(count):
        username = _unused_username(session)
        password = generate_password()
        student = student_repository.add(
            StudentCreate(username=username, password=password),
            hash_password(password),
            teacher_id,
            session,
        )
        created.append(
            StudentCreatedCreds(
                uuid=student.uuid,
                username=student.username,
                password=password,
                is_active=student.is_active,
            )
        )
    return created


def _unused_username(session: Session) -> str:
    for _ in range(_MAX_USERNAME_ATTEMPTS):
        candidate = generate_username()
        if student_repository.get_by_username(candidate, session) is None:
            return candidate
    raise RuntimeError("USERNAME_GENERATION_FAILED")


def list_for_teacher(teacher_id: UUID4, session: Session) -> list[Student]:
    return student_repository.list_for_teacher(teacher_id, session)


def authenticate(
    username: str, password: str, session: Session
) -> Student | None:
    row = student_repository.get_by_username(username, session)
    if row is None or not row.is_active:
        return None
    if not verify_password(password, row.hashed_password):
        return None
    return row.to_internal_model()


def reset_password(
    student_uuid: UUID4,
    teacher_id: UUID4,
    new_password: str,
    session: Session,
) -> Student:
    row = student_repository.get_by_uuid(student_uuid, session)
    if row is None or row.created_by_teacher_id != teacher_id:
        raise KeyError
    return student_repository.set_password(
        student_uuid, hash_password(new_password), session
    )


def set_active(
    student_uuid: UUID4,
    teacher_id: UUID4,
    is_active: bool,
    session: Session,
) -> Student:
    row = student_repository.get_by_uuid(student_uuid, session)
    if row is None or row.created_by_teacher_id != teacher_id:
        raise KeyError
    return student_repository.set_active(student_uuid, is_active, session)
