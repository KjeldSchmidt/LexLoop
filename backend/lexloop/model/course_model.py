from __future__ import annotations
from pydantic import BaseModel, UUID4


class CourseOut(BaseModel):  # type: ignore
    uuid: UUID4
    name: str

    @classmethod
    def from_internal_model(cls, internal_model: Course) -> CourseOut:
        return cls(
            uuid=internal_model.uuid,
            name=internal_model.name,
        )


class CourseIn(BaseModel):  # type: ignore
    name: str


class Course(BaseModel):  # type: ignore
    uuid: UUID4
    name: str

    # hash function so that tags can be stored in set
    def __hash__(self) -> int:
        return hash(self.uuid)
