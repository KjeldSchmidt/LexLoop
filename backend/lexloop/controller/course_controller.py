"""HTTP endpoints for courses and enrollments."""

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.principal import Principal, require_principal, require_teacher
from lexloop.auth.user_model import User
from lexloop.controller import get_db
from lexloop.model.course_model import (
    CourseEnrollmentIn,
    CourseIn,
    CourseOut,
    CourseUpdate,
)
from lexloop.model.pagination import Page, PaginationParams, pagination_params
from lexloop.model.student_model import StudentOut
from lexloop.service import course_access, course_service

router = APIRouter()


@router.get("/courses")
async def get_courses(
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[CourseOut]:
    """List courses visible to the current principal (paginated)."""
    courses, total = course_service.list_for_principal(
        principal, session, offset=pagination.offset, limit=pagination.limit
    )
    return Page(
        items=[CourseOut.from_internal_model(course) for course in courses],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/courses/{course_uuid}")
async def get_course(
    course_uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> CourseOut:
    """Fetch a single course the principal may view."""
    course_access.ensure_can_view_course(principal, course_uuid, session)
    row = course_service.get_by_uuid(course_uuid, session)
    return CourseOut.from_internal_model(row)


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseIn = Body(embed=True),
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> CourseOut:
    """Teacher creates a course they own."""
    created = course_service.create_for_teacher(course, teacher.id, session)
    return CourseOut.from_internal_model(created)


@router.patch("/courses/{course_uuid}")
async def update_course(
    course_uuid: UUID4,
    course: CourseUpdate = Body(embed=True),
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> CourseOut:
    """Teacher updates name/description of an owned course."""
    try:
        updated = course_service.update_for_teacher(
            course_uuid, course, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return CourseOut.from_internal_model(updated)


@router.delete("/courses/{course_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_uuid: UUID4,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> Response:
    """Teacher deletes an owned course and its content."""
    try:
        course_service.delete_for_teacher(course_uuid, teacher.id, session)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/course/{course_uuid}/students")
async def list_course_students(
    course_uuid: UUID4,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> list[StudentOut]:
    """List students enrolled in a course owned by the teacher."""
    try:
        students = course_service.list_enrolled_students(
            course_uuid, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return [StudentOut.from_internal_model(s) for s in students]


@router.post(
    "/course/{course_uuid}/enrollments", status_code=status.HTTP_200_OK
)
async def enroll_students(
    course_uuid: UUID4,
    enrollment: CourseEnrollmentIn = Body(embed=True),
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> dict[str, int]:
    """Enroll teacher-owned students into a course (idempotent)."""
    try:
        added = course_service.enroll_students(
            course_uuid, enrollment.student_uuids, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    except ValueError as exc:
        if str(exc) == "STUDENT_NOT_OWNED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="STUDENT_NOT_OWNED",
            ) from exc
        raise
    return {"added": added}


@router.post(
    "/course/{course_uuid}/enrollments/remove", status_code=status.HTTP_200_OK
)
async def unenroll_students(
    course_uuid: UUID4,
    enrollment: CourseEnrollmentIn = Body(embed=True),
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> dict[str, int]:
    """Remove students from a course enrollment list."""
    try:
        removed = course_service.unenroll_students(
            course_uuid, enrollment.student_uuids, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return {"removed": removed}
