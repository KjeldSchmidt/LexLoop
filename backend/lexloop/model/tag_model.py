from __future__ import annotations
from pydantic import BaseModel, UUID4


class TagOut(BaseModel):  # type: ignore
    uuid: UUID4
    title: str
    description: str
    course_uuid: UUID4

    @classmethod
    def from_internal_model(cls, internal_model: Tag) -> TagOut:
        return cls(
            uuid=internal_model.uuid,
            title=internal_model.title,
            description=internal_model.description,
            course_uuid=internal_model.course_uuid,
        )


class TagIn(BaseModel):  # type: ignore
    title: str
    description: str
    course_uuid: UUID4


class Tag(BaseModel):  # type: ignore
    uuid: UUID4
    title: str
    description: str
    course_uuid: UUID4

    # hash function so that tags can be stored in set
    def __hash__(self) -> int:
        return hash(self.uuid)
