from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lexloop.controller import get_db
from lexloop.model.course_model import CourseOut

from lexloop.service import course_service

router = APIRouter()


@router.get("/courses")
async def get_courses(session: Session = Depends(get_db)) -> list[CourseOut]:
    course_list = course_service.get_all(session)
    return [CourseOut.from_internal_model(course) for course in course_list]
