"""Authorize course visibility for teachers (owner) and students (enrolled)."""

from __future__ import annotations

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.principal import Principal, PrincipalKind
from lexloop.repository import course_repository


def can_view_course(
    principal: Principal, course_uuid: UUID4, session: Session
) -> bool:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None:
        return False
    if principal.kind == PrincipalKind.TEACHER:
        return row.owner_teacher_id == principal.id
    return course_repository.is_student_enrolled(
        course_uuid, principal.id, session
    )


def ensure_can_view_course(
    principal: Principal, course_uuid: UUID4, session: Session
) -> None:
    """Raise 404 when the principal may not access the course."""
    if not can_view_course(principal, course_uuid, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )


def ensure_teacher_owns_course(
    teacher_id: UUID4, course_uuid: UUID4, session: Session
) -> None:
    """Raise 404 when the teacher does not own the course."""
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )
