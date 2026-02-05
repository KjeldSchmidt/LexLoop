from __future__ import annotations
from pydantic import BaseModel, UUID4


class TagOut(BaseModel):  # type: ignore
    uuid: UUID4
    title: str
    description: str

    @classmethod
    def from_internal_model(cls, internal_model: Tag) -> TagOut:
        return cls(
            uuid=internal_model.uuid,
            title=internal_model.title,
            description=internal_model.description,
        )


class TagIn(BaseModel):  # type: ignore
    title: str
    description: str
    course_uuid: UUID4


class Tag(BaseModel):  # type: ignore
    uuid: UUID4
    title: str
    description: str

    # hash function so that tags can be stored in set
    def __hash__(self) -> int:
        return hash(self.uuid)
