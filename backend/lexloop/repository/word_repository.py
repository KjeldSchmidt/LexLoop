from uuid import uuid4

from lexloop.model.word_model import WordIn, Word

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from lexloop.repository import MetaBase

from pydantic import UUID4


class WordRepo(Model):
    class Meta(MetaBase):
        table_name = "lexloop-words"

    uuid = UnicodeAttribute(hash_key=True)
    word = UnicodeAttribute()
    definition = UnicodeAttribute()

    def to_internal_model(self) -> Word:
        return Word(
            uuid=self.uuid,
            word=self.word,
            definition=self.definition,
        )


def add(word: WordIn) -> Word:
    word_repo = WordRepo(
        uuid=str(uuid4()),
        word=word.word,
        definition=word.definition,
    )
    word_repo.save()
    return word_repo.to_internal_model()


def get_all() -> list[Word]:
    # Todo: paginate
    return [word.to_internal_model() for word in WordRepo.scan()]


def get_by_uuid(uuid: UUID4) -> Word:
    return WordRepo.get(str(uuid)).to_internal_model()
