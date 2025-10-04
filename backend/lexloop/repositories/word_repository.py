from uuid import uuid4

from lexloop.model import WordIn

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from lexloop.repositories import MetaBase


class WordRepo(Model):
    class Meta(MetaBase):
        table_name = "lexloop-words"

    uuid = UnicodeAttribute(hash_key=True)
    word = UnicodeAttribute()
    definition = UnicodeAttribute()


def add(word: WordIn) -> WordRepo:
    word_repo = WordRepo(
        uuid=str(uuid4()), word=word.word, definition=word.definition
    )
    word_repo.save()
    return word_repo


def get_all() -> list[WordRepo]:
    # Todo: paginate
    return list(WordRepo.scan())
