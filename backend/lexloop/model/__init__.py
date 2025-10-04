from __future__ import annotations
from pydantic import BaseModel


class Word(BaseModel):  # type: ignore #Todo: figure this out
    word: str
    definition: str
