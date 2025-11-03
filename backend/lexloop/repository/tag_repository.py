from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from lexloop.model.tag_model import TagIn, Tag

from lexloop.repository import Base

from pydantic import UUID4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID

if TYPE_CHECKING:
    from lexloop.repository import NodeRepo


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
    lexloop_nodes: Mapped[list[NodeRepo]] = relationship(
        "NodeRepo",
        secondary="lexloop_node_to_tags",
        back_populates="tags",
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
    )
    session.add(tag_repo)
    session.commit()
    session.refresh(tag_repo)
    return tag_repo.to_internal_model()


def get_all(session: Session) -> list[Tag]:
    # Todo: paginate
    all_tags: list[TagRepo] = session.query(TagRepo).all()
    return [tag.to_internal_model() for tag in all_tags]


def get_by_uuid(uuid: UUID4, session: Session) -> Tag:
    tag: TagRepo | None = session.get(TagRepo, uuid)
    if tag is None:
        raise KeyError
    return tag.to_internal_model()
