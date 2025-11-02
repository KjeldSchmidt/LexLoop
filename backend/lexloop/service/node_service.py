from lexloop.model.node_model import NodeIn, Node
from lexloop.repository import node_repository

from pydantic import UUID4


def add(node: NodeIn) -> Node:
    return node_repository.add(node)


def get_all() -> list[Node]:
    return node_repository.get_all()


def get_by_uuid(uuid: UUID4) -> Node:
    return node_repository.get_by_uuid(uuid)


def get_all_for_tag_uuid(tag_uuid: UUID4) -> list[Node]:
    return node_repository.get_all_for_tag_uuid(tag_uuid)
