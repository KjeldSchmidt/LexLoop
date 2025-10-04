from __future__ import annotations
from pydantic import BaseModel, UUID4


class WordOut(BaseModel):  # type: ignore
    uuid: UUID4
    word: str
    definition: str


class WordIn(BaseModel):  # type: ignore
    word: str
    definition: str
