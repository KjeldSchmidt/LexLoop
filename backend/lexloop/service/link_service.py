from lexloop.model.link_model import LinkIn
from lexloop.repositories import link_repository
from lexloop.repositories.link_repository import LinkRepo

from pydantic import UUID4


def add(link: LinkIn) -> LinkRepo:
    return link_repository.add(link)


def get_all() -> list[LinkRepo]:
    return link_repository.get_all()


def get_by_uuid(uuid: UUID4) -> LinkRepo:
    return link_repository.get_by_uuid(uuid)


def get_all_of_word_uuid(uuid: UUID4) -> list[LinkRepo]:
    return link_repository.get_all_of_word_uuid(uuid)
