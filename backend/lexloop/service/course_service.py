"""Application service for courses and enrollments."""

from datetime import datetime

from pydantic import UUID4
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from lexloop.auth.principal import Principal, PrincipalKind
from lexloop.auth.signup_codes import (
    generate_signup_code,
    normalize_signup_code,
)
from lexloop.model.course_model import Course, CourseIn, CourseUpdate
from lexloop.model.student_model import Student
from lexloop.repository import course_repository, student_repository
from lexloop.repository.link_repository import LinkRepo
from lexloop.repository.node_repository import NodeRepo, NodeToTagsRepo
from lexloop.repository.tag_repository import TagRepo


def list_for_principal(
    principal: Principal, session: Session, *, offset: int, limit: int
) -> tuple[list[Course], int]:
    """Return courses the principal may see."""
    if principal.kind == PrincipalKind.TEACHER:
        return course_repository.list_for_teacher(
            principal.id, session, offset=offset, limit=limit
        )
    return course_repository.list_for_student(
        principal.id, session, offset=offset, limit=limit
    )


def get_by_uuid(course_uuid: UUID4, session: Session) -> Course:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None:
        raise KeyError
    return row.to_internal_model()


def get_by_signup_code(code: str, session: Session) -> Course:
    normalized = normalize_signup_code(code)
    row = course_repository.get_by_signup_code(normalized, session)
    if row is None:
        raise KeyError
    return row.to_internal_model()


def create_for_teacher(
    payload: CourseIn, teacher_id: UUID4, session: Session
) -> Course:
    code = generate_signup_code(session)
    return course_repository.add(payload, teacher_id, code, session)


def update_for_teacher(
    course_uuid: UUID4,
    payload: CourseUpdate,
    teacher_id: UUID4,
    session: Session,
) -> Course:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    return course_repository.update(
        course_uuid,
        name=payload.name,
        description=payload.description,
        session=session,
    )


def regenerate_signup_code(
    course_uuid: UUID4, teacher_id: UUID4, session: Session
) -> Course:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    code = generate_signup_code(session)
    return course_repository.set_signup_code(course_uuid, code, session)


def delete_for_teacher(
    course_uuid: UUID4, teacher_id: UUID4, session: Session
) -> None:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    _delete_course_content(course_uuid, session)
    course_repository.delete_course(course_uuid, session)


def _delete_course_content(course_uuid: UUID4, session: Session) -> None:
    node_uuids = list(
        session.scalars(
            select(NodeRepo.uuid).where(NodeRepo.course_uuid == course_uuid)
        ).all()
    )
    if node_uuids:
        session.execute(
            delete(NodeToTagsRepo).where(
                NodeToTagsRepo.node_uuid.in_(node_uuids)
            )
        )
    session.execute(delete(LinkRepo).where(LinkRepo.course_uuid == course_uuid))
    session.execute(delete(NodeRepo).where(NodeRepo.course_uuid == course_uuid))
    session.execute(delete(TagRepo).where(TagRepo.course_uuid == course_uuid))
    session.flush()


def list_enrolled_students(
    course_uuid: UUID4, teacher_id: UUID4, session: Session
) -> list[Student]:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    return course_repository.list_enrolled_students(course_uuid, session)


def enroll_students(
    course_uuid: UUID4,
    student_uuids: list[UUID4],
    teacher_id: UUID4,
    session: Session,
) -> int:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    for student_uuid in student_uuids:
        student = student_repository.get_by_uuid(student_uuid, session)
        if student is None or student.created_by_teacher_id != teacher_id:
            raise ValueError("STUDENT_NOT_OWNED")
    return course_repository.add_enrollments(
        course_uuid, student_uuids, session
    )


def unenroll_students(
    course_uuid: UUID4,
    student_uuids: list[UUID4],
    teacher_id: UUID4,
    session: Session,
) -> int:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    return course_repository.remove_enrollments(
        course_uuid, student_uuids, session
    )


def request_join_by_code(
    code: str, student_uuid: UUID4, session: Session
) -> tuple[Course, str]:
    """Create a pending join request. Returns (course, status)."""
    course = get_by_signup_code(code, session)
    if course_repository.is_student_enrolled(
        course.uuid, student_uuid, session
    ):
        return course, "already_enrolled"
    if course_repository.has_join_request(course.uuid, student_uuid, session):
        return course, "already_pending"
    course_repository.add_join_request(course.uuid, student_uuid, session)
    return course, "pending"


def list_join_requests(
    course_uuid: UUID4, teacher_id: UUID4, session: Session
) -> list[tuple[Student, datetime]]:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    return course_repository.list_join_requests(course_uuid, session)


def list_pending_joins_for_student(
    student_uuid: UUID4, session: Session
) -> list[tuple[Course, datetime]]:
    return course_repository.list_join_requests_for_student(
        student_uuid, session
    )


def approve_join_requests(
    course_uuid: UUID4,
    student_uuids: list[UUID4],
    teacher_id: UUID4,
    session: Session,
) -> int:
    """Approve pending requests (any student) — enrolls without ownership check."""
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    return course_repository.approve_join_requests(
        course_uuid, student_uuids, session
    )


def approve_all_join_requests(
    course_uuid: UUID4, teacher_id: UUID4, session: Session
) -> int:
    row = course_repository.get_by_uuid(course_uuid, session)
    if row is None or row.owner_teacher_id != teacher_id:
        raise KeyError
    return course_repository.approve_all_join_requests(course_uuid, session)
