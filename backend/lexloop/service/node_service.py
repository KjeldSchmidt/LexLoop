from lexloop.model.node_model import NodeIn, Node
from lexloop.repository import node_repository

from pydantic import UUID4


def add(word: NodeIn) -> Node:
    return node_repository.add(word)


def get_all() -> list[Node]:
    return node_repository.get_all()


def get_by_uuid(uuid: UUID4) -> Node:
    return node_repository.get_by_uuid(uuid)
