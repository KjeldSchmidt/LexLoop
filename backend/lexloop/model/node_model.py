from __future__ import annotations

from pydantic import BaseModel, UUID4

from lexloop.model.tag_model import Tag


class NodeOut(BaseModel):  # type: ignore
    uuid: UUID4
    term: str
    definition: str
    tags: set[UUID4]

    @classmethod
    def from_internal_model(cls, internal_model: Node) -> NodeOut:
        return cls(
            uuid=internal_model.uuid,
            term=internal_model.term,
            definition=internal_model.definition,
            tags={tag.uuid for tag in internal_model.tags},
        )


class NodeIn(BaseModel):  # type: ignore
    term: str
    definition: str
    tags: list[str]
    course_uuid: UUID4


class Node(BaseModel):  # type: ignore
    uuid: UUID4
    term: str
    definition: str
    tags: set[Tag]
