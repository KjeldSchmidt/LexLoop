"""Application service for tags."""

from sqlalchemy.orm import Session

from lexloop.model.tag_model import TagIn, Tag
from lexloop.repository import tag_repository

from pydantic import UUID4


def add(tag: TagIn, session: Session) -> Tag:
    """Persist a new tag."""
    return tag_repository.add(tag, session)


def get_all(
    session: Session, *, offset: int, limit: int
) -> tuple[list[Tag], int]:
    """Return a page of every tag (prefer course-scoped queries)."""
    return tag_repository.get_all(session, offset=offset, limit=limit)


def get_by_course_uuid(
    session: Session, course_uuid: UUID4, *, offset: int, limit: int
) -> tuple[list[Tag], int]:
    """Return a page of tags for a course."""
    return tag_repository.get_by_course_uuid(
        session, course_uuid, offset=offset, limit=limit
    )


def get_by_uuid(uuid: UUID4, session: Session) -> Tag:
    """Return a tag by UUID."""
    return tag_repository.get_by_uuid(uuid, session)


def get_all_for_node_uuid(node_uuid: UUID4, session: Session) -> list[Tag]:
    """Return all tags attached to a node (small, unpaginated)."""
    return tag_repository.get_all_for_node_uuid(node_uuid, session)
