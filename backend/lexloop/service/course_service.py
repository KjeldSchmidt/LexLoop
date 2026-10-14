"""Application service for courses."""

from sqlalchemy.orm import Session

from lexloop.model.course_model import Course
from lexloop.repository import course_repository


def get_all(session: Session) -> list[Course]:
    """Return all courses."""
    return course_repository.get_all(session)
