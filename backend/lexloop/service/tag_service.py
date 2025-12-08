from sqlalchemy.orm import Session

from lexloop.model.tag_model import TagIn, Tag
from lexloop.repository import tag_repository

from pydantic import UUID4


def add(tag: TagIn, session: Session) -> Tag:
    return tag_repository.add(tag, session)


def get_all(session: Session) -> list[Tag]:
    return tag_repository.get_all(session)


def get_by_uuid(uuid: UUID4, session: Session) -> Tag:
    return tag_repository.get_by_uuid(uuid, session)


def get_all_for_node_uuid(node_uuid: UUID4, session: Session) -> list[Tag]:
    return tag_repository.get_all_for_node_uuid(node_uuid, session)
