from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, UUID4


class LinkType(Enum):
    SYNONYM = "SYNONYM"


class LinkOut(BaseModel):  # type: ignore
    uuid: UUID4
    type: LinkType
    word1: str
    word2: str
    annotation: str


class LinkIn(BaseModel):  # type: ignore
    word1: str
    word2: str
    type: str
    annotation: str
