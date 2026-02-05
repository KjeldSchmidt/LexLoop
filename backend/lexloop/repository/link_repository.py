from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import mapped_column, Mapped, relationship, Session

from lexloop.model.link_model import LinkType, LinkIn, Link
from lexloop.repository.base import Base

if TYPE_CHECKING:
    from lexloop.repository import NodeRepo

from pydantic import UUID4
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID


class LinkRepo(Base):
    __tablename__ = "lexloop_links"

    uuid: Mapped[UUID4] = mapped_column(
        "uuid",
        POSTGRES_UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        primary_key=True,
    )
    type: Mapped[LinkType] = mapped_column("type", String(100))
    annotation: Mapped[str] = mapped_column("annotation", String(300))
    node1_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True), ForeignKey("lexloop_nodes.uuid")
    )
    node1: Mapped[NodeRepo] = relationship(
        "NodeRepo", foreign_keys=[node1_uuid], lazy="selectin"
    )
    node2_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True), ForeignKey("lexloop_nodes.uuid")
    )
    node2: Mapped[NodeRepo] = relationship(
        "NodeRepo", foreign_keys=[node2_uuid], lazy="selectin"
    )

    def to_internal_model(self) -> Link:
        """
        Convert a repo object to an internal Link representation.
        :return: Link object with data from LinkRepo
        """
        return Link(
            uuid=self.uuid,
            node1=self.node1.to_internal_model(),
            node2=self.node2.to_internal_model(),
            type=LinkType(self.type),
            annotation=str(self.annotation),
        )


def add(link: LinkIn, session: Session) -> Link:
    # Fetch actual NodeRepo objects from UUIDs
    from lexloop.repository.node_repository import NodeRepo

    node1_repo = session.get(NodeRepo, link.node1)
    node2_repo = session.get(NodeRepo, link.node2)

    if node1_repo is None or node2_repo is None:
        raise ValueError("Node not found")

    link_repo = LinkRepo(
        uuid=str(uuid4()),
        type=link.type,  # Store as string, not enum
        node1_uuid=link.node1,
        node2_uuid=link.node2,
        annotation=link.annotation,
    )
    session.add(link_repo)
    session.commit()
    session.refresh(link_repo)
    return link_repo.to_internal_model()


def get_all(session: Session) -> list[Link]:
    # Todo: paginate
    all_links: list[LinkRepo] = session.query(LinkRepo).all()
    return [node.to_internal_model() for node in all_links]


def get_all_for_node_uuid(node_uuid: UUID4, session: Session) -> list[Link]:
    # search in both columns
    statement = select(LinkRepo).where(
        (LinkRepo.node1_uuid == node_uuid) | (LinkRepo.node2_uuid == node_uuid)
    )
    links = session.scalars(statement).all()
    # Todo: paginate
    return [link.to_internal_model() for link in links]


def get_by_uuid(uuid: UUID4, session: Session) -> Link:
    link: LinkRepo | None = session.get(LinkRepo, uuid)
    if link is None:
        raise KeyError
    return link.to_internal_model()
