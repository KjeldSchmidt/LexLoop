from lexloop.model import WordIn
from lexloop.repositories import word_repository
from lexloop.repositories.word_repository import WordRepo

from pydantic import UUID4


def add(word: WordIn) -> WordRepo:
    return word_repository.add(word)


def get_all() -> list[WordRepo]:
    return word_repository.get_all()


def get_by_uuid(uuid: UUID4) -> WordRepo:
    return word_repository.get_by_uuid(uuid)
