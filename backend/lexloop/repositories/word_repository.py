from uuid import uuid4

from lexloop.model import Word

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from lexloop.repositories import MetaBase


class WordModel(Model):
    class Meta(MetaBase):
        table_name = "lexloop-words"

    id = UnicodeAttribute(hash_key=True)
    word = UnicodeAttribute()
    definition = UnicodeAttribute()


def add(word: Word) -> None:
    WordModel(id=str(uuid4()), word=word.word, definition=word.definition).save()


def get_all() -> list[WordModel]:
    # Todo: paginate
    return list(WordModel.scan())
