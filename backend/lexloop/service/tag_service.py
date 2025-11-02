from lexloop.model.tag_model import TagIn, Tag
from lexloop.repository import tag_repository

from pydantic import UUID4


def add(tag: TagIn) -> Tag:
    return tag_repository.add(tag)


def get_all() -> list[Tag]:
    return tag_repository.get_all()


def get_by_uuid(uuid: UUID4) -> Tag:
    return tag_repository.get_by_uuid(uuid)
