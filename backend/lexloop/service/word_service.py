from lexloop.model import Word
from lexloop.repositories import word_repository
from lexloop.repositories.word_repository import WordModel


def add(word: Word) -> None:
    word_repository.add(word)


def get_all() -> list[WordModel]:
    return word_repository.get_all()
