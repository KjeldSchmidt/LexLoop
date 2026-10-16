"""Student DTOs — username only, no email or name."""

from __future__ import annotations

from pydantic import BaseModel, UUID4, Field


class Student(BaseModel):  # type: ignore[explicit-any]
    uuid: UUID4
    username: str
    is_active: bool
    created_by_teacher_id: UUID4


class StudentOut(BaseModel):  # type: ignore[explicit-any]
    uuid: UUID4
    username: str
    is_active: bool

    @classmethod
    def from_internal_model(cls, student: Student) -> StudentOut:
        return cls(
            uuid=student.uuid,
            username=student.username,
            is_active=student.is_active,
        )


class StudentCreate(BaseModel):  # type: ignore[explicit-any]
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class StudentLogin(BaseModel):  # type: ignore[explicit-any]
    username: str
    password: str


class StudentPasswordReset(BaseModel):  # type: ignore[explicit-any]
    password: str = Field(min_length=8, max_length=128)
