"""Application service for courses."""

from sqlalchemy.orm import Session

from lexloop.model.course_model import Course
from lexloop.repository import course_repository


def get_all(
    session: Session, *, offset: int, limit: int
) -> tuple[list[Course], int]:
    """Return a page of courses."""
    return course_repository.get_all(session, offset=offset, limit=limit)
