"""HTTP endpoints for courses and enrollments."""

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.principal import (
    Principal,
    PrincipalKind,
    require_principal,
    require_teacher,
)
from lexloop.auth.student_auth import require_student
from lexloop.auth.user_model import User
from lexloop.controller import get_db
from lexloop.model.course_model import (
    Course,
    CourseByCodeOut,
    CourseEnrollmentIn,
    CourseIn,
    CourseJoinRequestIn,
    CourseJoinRequestItemOut,
    CourseJoinRequestOut,
    CourseOut,
    CourseUpdate,
    StudentPendingJoinOut,
)
from lexloop.model.pagination import Page, PaginationParams, pagination_params
from lexloop.model.student_model import Student, StudentOut
from lexloop.service import course_access, course_service

router = APIRouter()


def _course_out(course: Course, principal: Principal) -> CourseOut:
    include = principal.kind == PrincipalKind.TEACHER
    return CourseOut.from_internal_model(course, include_signup_code=include)


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
        items=[_course_out(course, principal) for course in courses],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/courses/by-code/{code}")
async def get_course_by_code(
    code: str,
    _student: Student = Depends(require_student),
    session: Session = Depends(get_db),
) -> CourseByCodeOut:
    """Resolve a signup code to a course name (for join preview)."""
    try:
        course = course_service.get_by_signup_code(code, session)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return CourseByCodeOut(
        course_uuid=course.uuid,
        course_name=course.name,
        code=course.signup_code,
    )


@router.get("/courses/join-requests")
async def list_my_join_requests(
    student: Student = Depends(require_student),
    session: Session = Depends(get_db),
) -> list[StudentPendingJoinOut]:
    """List courses the student has requested to join (pending approval)."""
    items = course_service.list_pending_joins_for_student(student.uuid, session)
    return [
        StudentPendingJoinOut(
            course_uuid=course.uuid,
            course_name=course.name,
            requested_at=requested_at,
        )
        for course, requested_at in items
    ]


@router.post("/courses/join-requests", status_code=status.HTTP_200_OK)
async def request_course_join(
    join_request: CourseJoinRequestIn = Body(embed=True),
    student: Student = Depends(require_student),
    session: Session = Depends(get_db),
) -> CourseJoinRequestOut:
    """Student requests enrollment using a course signup code."""
    try:
        course, status_value = course_service.request_join_by_code(
            join_request.code, student.uuid, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="INVALID_CODE"
        ) from exc
    return CourseJoinRequestOut(
        course_uuid=course.uuid,
        course_name=course.name,
        status=status_value,
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
    return _course_out(row, principal)


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseIn = Body(embed=True),
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> CourseOut:
    """Teacher creates a course they own."""
    created = course_service.create_for_teacher(course, teacher.id, session)
    return CourseOut.from_internal_model(created, include_signup_code=True)


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
    return CourseOut.from_internal_model(updated, include_signup_code=True)


@router.post("/course/{course_uuid}/signup-code/regenerate")
async def regenerate_signup_code(
    course_uuid: UUID4,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> CourseOut:
    """Generate a new signup code for an owned course."""
    try:
        updated = course_service.regenerate_signup_code(
            course_uuid, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    except RuntimeError as exc:
        if str(exc) == "SIGNUP_CODE_GENERATION_FAILED":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="SIGNUP_CODE_GENERATION_FAILED",
            ) from exc
        raise
    return CourseOut.from_internal_model(updated, include_signup_code=True)


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


@router.get("/course/{course_uuid}/join-requests")
async def list_join_requests(
    course_uuid: UUID4,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> list[CourseJoinRequestItemOut]:
    """List pending enrollment requests for an owned course."""
    try:
        items = course_service.list_join_requests(
            course_uuid, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return [
        CourseJoinRequestItemOut(
            uuid=student.uuid,
            username=student.username,
            is_active=student.is_active,
            requested_at=requested_at,
        )
        for student, requested_at in items
    ]


@router.post(
    "/course/{course_uuid}/join-requests/approve",
    status_code=status.HTTP_200_OK,
)
async def approve_join_requests(
    course_uuid: UUID4,
    enrollment: CourseEnrollmentIn = Body(embed=True),
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> dict[str, int]:
    """Approve pending requests (enrolls students, clears requests)."""
    try:
        enrolled = course_service.approve_join_requests(
            course_uuid, enrollment.student_uuids, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return {"enrolled": enrolled}


@router.post(
    "/course/{course_uuid}/join-requests/approve-all",
    status_code=status.HTTP_200_OK,
)
async def approve_all_join_requests(
    course_uuid: UUID4,
    teacher: User = Depends(require_teacher),
    session: Session = Depends(get_db),
) -> dict[str, int]:
    """Approve every pending enrollment request for the course."""
    try:
        enrolled = course_service.approve_all_join_requests(
            course_uuid, teacher.id, session
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from exc
    return {"enrolled": enrolled}


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
