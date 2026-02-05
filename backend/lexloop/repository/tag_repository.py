from __future__ import annotations

from uuid import uuid4

from lexloop.model.tag_model import TagIn, Tag

from lexloop.repository.base import Base

from pydantic import UUID4

from sqlalchemy import String, select, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID

from lexloop.repository.course_repository import CourseRepo


class TagRepo(Base):
    __tablename__ = "lexloop_tags"

    uuid: Mapped[UUID4] = mapped_column(
        "uuid",
        POSTGRES_UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        primary_key=True,
    )
    title: Mapped[str] = mapped_column("title", String(100))
    description: Mapped[str] = mapped_column("description", String(300))

    course_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("lexloop_courses.uuid", name="tag_course_fk"),
    )
    course: Mapped[CourseRepo] = relationship(
        "CourseRepo", foreign_keys=[course_uuid], lazy="selectin"
    )

    # Todo: instrumented attribute?
    def to_internal_model(self) -> Tag:
        return Tag(
            uuid=self.uuid,
            title=str(self.title),
            description=str(self.description),
        )


def add(tag: TagIn, session: Session) -> Tag:
    tag_repo = TagRepo(
        uuid=str(uuid4()),
        title=tag.title,
        description=tag.description,
        course_uuid=tag.course_uuid,
    )
    session.add(tag_repo)
    session.commit()
    session.refresh(tag_repo)
    return tag_repo.to_internal_model()


def get_all(session: Session) -> list[Tag]:
    # Todo: paginate
    all_tags: list[TagRepo] = session.query(TagRepo).all()
    return [tag.to_internal_model() for tag in all_tags]


def get_by_course_uuid(session: Session, course_uuid: UUID4) -> list[Tag]:
    all_nodes: list[TagRepo] = (
        session.query(TagRepo).where(TagRepo.course_uuid == course_uuid).all()
    )
    return [node.to_internal_model() for node in all_nodes]


def get_by_uuid(uuid: UUID4, session: Session) -> Tag:
    tag: TagRepo | None = session.get(TagRepo, uuid)
    if tag is None:
        raise KeyError
    return tag.to_internal_model()


def get_all_for_node_uuid(node_uuid: UUID4, session: Session) -> list[Tag]:
    from lexloop.repository.node_repository import NodeToTagsRepo

    statement = (
        select(TagRepo)
        .join(NodeToTagsRepo)
        .where(NodeToTagsRepo.node_uuid == node_uuid)
    )
    tags = session.scalars(statement).all()
    return [tag.to_internal_model() for tag in tags]
