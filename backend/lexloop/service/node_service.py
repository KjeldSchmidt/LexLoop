"""Application service for vocabulary nodes."""

from sqlalchemy.orm import Session

from lexloop.model.node_model import NodeIn, Node
from lexloop.repository import node_repository

from pydantic import UUID4


def add(node: NodeIn, session: Session) -> Node:
    """Persist a new node."""
    return node_repository.add(node, session)


def update_tags(
    node_uuid: UUID4, tags_uuids: list[UUID4], session: Session
) -> Node:
    """Replace tags on an existing node."""
    return node_repository.update_tags(node_uuid, tags_uuids, session)


def add_tag_to_node(
    node_uuid: UUID4, tag_uuid: UUID4, session: Session
) -> Node:
    """Attach one tag to a node."""
    return node_repository.add_tag_to_node(node_uuid, tag_uuid, session)


def get_all(session: Session) -> list[Node]:
    """Return every node (unscoped; prefer course-scoped queries)."""
    return node_repository.get_all(session)


def get_by_course_uuid(session: Session, course_uuid: UUID4) -> list[Node]:
    """Return nodes for a course."""
    return node_repository.get_by_course_uuid(session, course_uuid)


def get_by_uuid(uuid: UUID4, session: Session) -> Node:
    """Return a node by UUID."""
    return node_repository.get_by_uuid(uuid, session)


def get_all_for_tag_uuid(tag_uuid: UUID4, session: Session) -> list[Node]:
    """Return nodes that have the given tag."""
    return node_repository.get_all_for_tag_uuid(tag_uuid, session)
