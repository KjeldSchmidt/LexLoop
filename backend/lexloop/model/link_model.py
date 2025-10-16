from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, UUID4

from lexloop.model.node_model import Node


class LinkType(Enum):
    SYNONYM = "SYNONYM"


class LinkIn(BaseModel):  # type: ignore
    node1: str
    node2: str
    type: str
    annotation: str


class Link(BaseModel):  # type: ignore
    uuid: UUID4
    node1: Node
    node2: Node
    type: LinkType
    annotation: str


class LinkOut(BaseModel):  # type: ignore
    uuid: UUID4
    type: LinkType
    node1: UUID4
    node2: UUID4
    annotation: str

    @classmethod
    def from_internal_model(cls, internal_model: Link) -> LinkOut:
        return cls(
            uuid=internal_model.uuid,
            type=internal_model.type,
            node1=internal_model.node1.uuid,
            node2=internal_model.node2.uuid,
            annotation=internal_model.annotation,
        )
