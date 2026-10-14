"""Application service for links between nodes."""

from sqlalchemy.orm import Session

from lexloop.model.link_model import LinkIn
from lexloop.repository import link_repository
from lexloop.repository.link_repository import Link

from pydantic import UUID4


def add(link: LinkIn, session: Session) -> Link:
    """Persist a new link."""
    return link_repository.add(link, session)


def get_all(session: Session) -> list[Link]:
    """Return every link (unscoped; prefer course-scoped queries)."""
    return link_repository.get_all(session)


def get_by_course_uuid(session: Session, course_uuid: UUID4) -> list[Link]:
    """Return links for a course."""
    return link_repository.get_by_course_uuid(session, course_uuid)


def get_by_uuid(uuid: UUID4, session: Session) -> Link:
    """Return a link by UUID."""
    return link_repository.get_by_uuid(uuid, session)


def get_all_for_node_uuid(node_uuid: UUID4, session: Session) -> list[Link]:
    """Return links that involve the given node."""
    return link_repository.get_all_for_node_uuid(node_uuid, session)
