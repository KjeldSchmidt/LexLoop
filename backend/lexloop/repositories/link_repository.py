from uuid import uuid4

from lexloop.model.link_model import LinkType, LinkIn

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb_attributes import UnicodeEnumAttribute
from lexloop.repositories import MetaBase

from pydantic import UUID4


class LinkRepo(Model):
    class Meta(MetaBase):
        table_name = "lexloop-links"

    uuid = UnicodeAttribute(hash_key=True)
    word1 = UnicodeAttribute()
    word2 = UnicodeAttribute()
    type = UnicodeEnumAttribute(LinkType)
    annotation = UnicodeAttribute()


def add(link: LinkIn) -> LinkRepo:
    link_repo = LinkRepo(
        uuid=str(uuid4()),
        type=LinkType[link.type],
        word1=link.word1,
        word2=link.word2,
        annotation=link.annotation,
    )
    link_repo.save()
    return link_repo


def get_all() -> list[LinkRepo]:
    # Todo: paginate
    return list(LinkRepo.scan())


def get_all_of_word_uuid(word: UUID4) -> list[LinkRepo]:
    return list()


def get_by_uuid(uuid: UUID4) -> LinkRepo:
    return LinkRepo.get(str(uuid))
