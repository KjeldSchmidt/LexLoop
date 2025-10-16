from lexloop.model.word_model import WordIn, Word
from lexloop.repository import word_repository

from pydantic import UUID4


def add(word: WordIn) -> Word:
    return word_repository.add(word)


def get_all() -> list[Word]:
    return word_repository.get_all()


def get_by_uuid(uuid: UUID4) -> Word:
    return word_repository.get_by_uuid(uuid)
