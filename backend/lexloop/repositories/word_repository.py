from uuid import uuid4

from lexloop.model import WordIn

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute
from lexloop.repositories import MetaBase

from pydantic import UUID4


class WordRepo(Model):
    class Meta(MetaBase):
        table_name = "lexloop-words"

    uuid = UnicodeAttribute(hash_key=True)
    word = UnicodeAttribute()
    definition = UnicodeAttribute()
    synonyms = ListAttribute(of=UnicodeAttribute)


def add(word: WordIn) -> WordRepo:
    word_repo = WordRepo(
        uuid=str(uuid4()),
        word=word.word,
        definition=word.definition,
        synonyms=word.synonyms,
    )
    word_repo.save()
    return word_repo


def get_all() -> list[WordRepo]:
    # Todo: paginate
    return list(WordRepo.scan())


def get_by_uuid(uuid: UUID4) -> WordRepo:
    return WordRepo.get(str(uuid))
