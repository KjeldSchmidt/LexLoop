from lexloop.model.link_model import LinkIn
from lexloop.repository import link_repository
from lexloop.repository.link_repository import Link

from pydantic import UUID4


def add(link: LinkIn) -> Link:
    return link_repository.add(link)


def get_all() -> list[Link]:
    return link_repository.get_all()


def get_by_uuid(uuid: UUID4) -> Link:
    return link_repository.get_by_uuid(uuid)


def get_all_for_node_uuid(node_uuid: UUID4) -> list[Link]:
    return link_repository.get_all_for_node_uuid(node_uuid)
