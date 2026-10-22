from __future__ import annotations

from pydantic import BaseModel, UUID4, Field


class CourseOut(BaseModel):  # type: ignore[explicit-any]
    uuid: UUID4
    name: str
    description: str
    owner_teacher_id: UUID4 | None = None

    @classmethod
    def from_internal_model(cls, internal_model: Course) -> CourseOut:
        return cls(
            uuid=internal_model.uuid,
            name=internal_model.name,
            description=internal_model.description,
            owner_teacher_id=internal_model.owner_teacher_id,
        )


class CourseIn(BaseModel):  # type: ignore[explicit-any]
    name: str = Field(min_length=1, max_length=100)
    description: str = ""


class CourseUpdate(BaseModel):  # type: ignore[explicit-any]
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class CourseEnrollmentIn(BaseModel):  # type: ignore[explicit-any]
    student_uuids: list[UUID4]


class Course(BaseModel):  # type: ignore[explicit-any]
    uuid: UUID4
    name: str
    description: str = ""
    owner_teacher_id: UUID4 | None = None

    def __hash__(self) -> int:
        return hash(self.uuid)
