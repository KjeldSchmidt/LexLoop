from uuid import uuid4

from lexloop.model.tag_model import TagIn, Tag

from pynamodb.attributes import UnicodeAttribute
from lexloop.repository import MetaBase, ModelBase

from pydantic import UUID4


class TagRepo(ModelBase):
    class Meta(MetaBase):
        table_name = "lexloop-tag"

    uuid = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute()
    description = UnicodeAttribute()

    def to_internal_model(self) -> Tag:
        return Tag(
            uuid=self.uuid,
            title=self.title,
            description=self.description,
        )


def add(tag: TagIn) -> Tag:
    tag_repo = TagRepo(
        uuid=str(uuid4()),
        title=tag.title,
        description=tag.description,
    )
    tag_repo.save()
    return tag_repo.to_internal_model()


def get_all() -> list[Tag]:
    # Todo: paginate
    return [tag.to_internal_model() for tag in TagRepo.scan()]


def get_by_uuid(uuid: UUID4) -> Tag:
    return TagRepo.get(str(uuid)).to_internal_model()
