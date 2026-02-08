from sqlalchemy.orm import Session

from lexloop.model.course_model import Course
from lexloop.repository import course_repository


def get_all(session: Session) -> list[Course]:
    return course_repository.get_all(session)
