from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, UUID4


class CourseOut(BaseModel):  # type: ignore[explicit-any]
    uuid: UUID4
    name: str
    description: str
    owner_teacher_id: UUID4 | None = None
    signup_code: str | None = None

    @classmethod
    def from_internal_model(
        cls, internal_model: Course, *, include_signup_code: bool = False
    ) -> CourseOut:
        return cls(
            uuid=internal_model.uuid,
            name=internal_model.name,
            description=internal_model.description,
            owner_teacher_id=internal_model.owner_teacher_id,
            signup_code=(
                internal_model.signup_code if include_signup_code else None
            ),
        )


class CourseIn(BaseModel):  # type: ignore[explicit-any]
    name: str = Field(min_length=1, max_length=100)
    description: str = ""


class CourseUpdate(BaseModel):  # type: ignore[explicit-any]
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class CourseEnrollmentIn(BaseModel):  # type: ignore[explicit-any]
    student_uuids: list[UUID4]


class CourseJoinRequestIn(BaseModel):  # type: ignore[explicit-any]
    code: str = Field(min_length=4, max_length=4, pattern=r"(?i)^[A-Z]{4}$")


class CourseJoinRequestOut(BaseModel):  # type: ignore[explicit-any]
    course_uuid: UUID4
    course_name: str
    status: str  # pending | already_enrolled | already_pending


class CourseByCodeOut(BaseModel):  # type: ignore[explicit-any]
    course_uuid: UUID4
    course_name: str
    code: str


class CourseJoinRequestItemOut(BaseModel):  # type: ignore[explicit-any]
    uuid: UUID4
    username: str
    is_active: bool
    requested_at: datetime


class StudentPendingJoinOut(BaseModel):  # type: ignore[explicit-any]
    """A course the student has requested to join (not yet approved)."""

    course_uuid: UUID4
    course_name: str
    requested_at: datetime


class Course(BaseModel):  # type: ignore[explicit-any]
    uuid: UUID4
    name: str
    description: str = ""
    owner_teacher_id: UUID4 | None = None
    signup_code: str = ""

    def __hash__(self) -> int:
        return hash(self.uuid)
