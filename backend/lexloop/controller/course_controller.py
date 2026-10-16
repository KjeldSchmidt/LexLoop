"""HTTP endpoints for courses."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lexloop.auth.principal import require_principal
from lexloop.controller import get_db
from lexloop.model.course_model import CourseOut
from lexloop.model.pagination import Page, PaginationParams, pagination_params

from lexloop.service import course_service

router = APIRouter(dependencies=[Depends(require_principal)])


@router.get("/courses")
async def get_courses(
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[CourseOut]:
    """List courses (paginated)."""
    courses, total = course_service.get_all(
        session, offset=pagination.offset, limit=pagination.limit
    )
    return Page(
        items=[CourseOut.from_internal_model(course) for course in courses],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )
