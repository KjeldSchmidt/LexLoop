"""Authenticated principal: teacher (fastapi-users) or student (custom JWT)."""

from __future__ import annotations

from enum import Enum

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, UUID4

from lexloop.auth.auth_controller import fastapi_users
from lexloop.auth.student_auth import get_optional_student
from lexloop.auth.user_model import User
from lexloop.model.student_model import Student

optional_active_teacher = fastapi_users.current_user(
    active=True, verified=True, optional=True
)


class PrincipalKind(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"


class Principal(BaseModel):  # type: ignore[explicit-any]
    kind: PrincipalKind
    id: UUID4


async def require_principal(
    teacher: User | None = Depends(optional_active_teacher),
    student: Student | None = Depends(get_optional_student),
) -> Principal:
    """Require a logged-in teacher or student."""
    if teacher is not None:
        return Principal(kind=PrincipalKind.TEACHER, id=teacher.id)
    if student is not None:
        return Principal(kind=PrincipalKind.STUDENT, id=student.uuid)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


async def require_teacher(
    teacher: User | None = Depends(optional_active_teacher),
) -> User:
    """Require a verified teacher session."""
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Teacher authentication required",
        )
    if getattr(teacher, "role", "teacher") != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher role required",
        )
    return teacher
