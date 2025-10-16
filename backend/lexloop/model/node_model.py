from __future__ import annotations
from pydantic import BaseModel, UUID4


class NodeOut(BaseModel):  # type: ignore
    uuid: UUID4
    term: str
    definition: str


class NodeIn(BaseModel):  # type: ignore
    term: str
    definition: str


class Node(BaseModel):  # type: ignore
    uuid: UUID4
    term: str
    definition: str
