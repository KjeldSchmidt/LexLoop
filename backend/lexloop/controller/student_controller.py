"""Student login and teacher-managed student CRUD."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.principal import require_teacher
from lexloop.auth.student_auth import (
    clear_student_cookie,
    create_student_token,
    require_student,
    set_student_cookie,
)
from lexloop.auth.user_model import User
from lexloop.controller import get_db
from lexloop.model.student_model import (
    Student,
    StudentBulkCreate,
    StudentBulkCreateOut,
    StudentBulkIds,
    StudentCreate,
    StudentLogin,
    StudentOut,
    StudentPasswordReset,
)
from lexloop.service import student_service

router = APIRouter(prefix="/students")


@router.post("/login")
async def student_login(
    payload: StudentLogin,
    response: Response,
    session: Session = Depends(get_db),
) -> StudentOut:
    """Log in a student with username and password."""
    student = student_service.authenticate(
        payload.username, payload.password, session
    )
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="LOGIN_BAD_CREDENTIALS",
        )
    set_student_cookie(response, create_student_token(student.uuid))
    return StudentOut.from_internal_model(student)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def student_logout(response: Response) -> None:
    """Clear the student session cookie."""
    clear_student_cookie(response)


@router.get("/me")
async def student_me(
    student: Annotated[Student, Depends(require_student)],
) -> StudentOut:
    """Return the current student principal."""
    return StudentOut.from_internal_model(student)


@router.get("")
async def list_students(
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> list[StudentOut]:
    """List students created by the current teacher."""
    students = student_service.list_for_teacher(teacher.id, session)
    return [StudentOut.from_internal_model(s) for s in students]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_student(
    payload: StudentCreate,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> StudentOut:
    """Teacher creates a student account."""
    try:
        student = student_service.create_for_teacher(
            payload, teacher.id, session
        )
    except ValueError as exc:
        if str(exc) == "USERNAME_TAKEN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="USERNAME_TAKEN",
            ) from exc
        raise
    return StudentOut.from_internal_model(student)


@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_create_students(
    payload: StudentBulkCreate,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> StudentBulkCreateOut:
    """Create many students with auto-generated memorable credentials.

    Plaintext passwords are returned once in the response for the teacher
    to download or distribute; they are stored hashed only.
    """
    try:
        accounts = student_service.bulk_create_for_teacher(
            payload.count, teacher.id, session
        )
    except RuntimeError as exc:
        if str(exc) == "USERNAME_GENERATION_FAILED":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="USERNAME_GENERATION_FAILED",
            ) from exc
        raise
    return StudentBulkCreateOut(accounts=accounts)


@router.post("/bulk-delete", status_code=status.HTTP_204_NO_CONTENT)
async def bulk_delete_students(
    payload: StudentBulkIds,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> None:
    """Permanently delete selected students owned by the current teacher."""
    try:
        student_service.bulk_delete_for_teacher(
            payload.student_uuids, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc


@router.post("/bulk-passwords", status_code=status.HTTP_200_OK)
async def bulk_reset_student_passwords(
    payload: StudentBulkIds,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> StudentBulkCreateOut:
    """Reset passwords for selected students; return one-time plaintext phrases."""
    try:
        accounts = student_service.bulk_reset_passwords_for_teacher(
            payload.student_uuids, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return StudentBulkCreateOut(accounts=accounts)


@router.post("/{student_uuid}/password")
async def reset_student_password(
    student_uuid: UUID4,
    payload: StudentPasswordReset,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> StudentOut:
    """Teacher resets a student's password."""
    try:
        student = student_service.reset_password(
            student_uuid, teacher.id, payload.password, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return StudentOut.from_internal_model(student)


@router.post("/{student_uuid}/deactivate")
async def deactivate_student(
    student_uuid: UUID4,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> StudentOut:
    """Teacher deactivates a student."""
    try:
        student = student_service.set_active(
            student_uuid, teacher.id, False, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return StudentOut.from_internal_model(student)
