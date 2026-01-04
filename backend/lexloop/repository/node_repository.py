from __future__ import annotations

from uuid import uuid4

from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship

from lexloop.model.node_model import NodeIn, Node

from lexloop.repository.base import Base
from lexloop.repository.tag_repository import TagRepo
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID

from pydantic import UUID4


class NodeToTagsRepo(Base):
    __tablename__ = "lexloop_node_to_tags"
    node_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("lexloop_nodes.uuid"),
        primary_key=True,
    )
    tag_uuid: Mapped[UUID4] = mapped_column(
        POSTGRES_UUID(as_uuid=True),
        ForeignKey("lexloop_tags.uuid"),
        primary_key=True,
    )


class NodeRepo(Base):
    __tablename__ = "lexloop_nodes"

    uuid: Mapped[UUID4] = mapped_column(
        "uuid",
        POSTGRES_UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        primary_key=True,
    )
    term: Mapped[str] = mapped_column("title", String(100))
    definition: Mapped[str] = mapped_column("description", String(300))
    tags: Mapped[list[TagRepo]] = relationship(
        "TagRepo",
        secondary="lexloop_node_to_tags",
    )

    def to_internal_model(self) -> Node:
        return Node(
            uuid=self.uuid,
            term=str(self.term),
            definition=str(self.definition),
            tags={tag.to_internal_model() for tag in self.tags},
        )


def add(node: NodeIn, session: Session) -> Node:
    # Fetch actual TagRepo objects from UUIDs
    tag_repos = [session.get(TagRepo, tag_uuid) for tag_uuid in node.tags]
    tag_repos = [tag for tag in tag_repos if tag is not None]

    node_repo = NodeRepo(
        uuid=str(uuid4()),
        term=node.term,
        definition=node.definition,
        tags=tag_repos,
    )
    session.add(node_repo)
    session.commit()
    session.refresh(node_repo)
    return node_repo.to_internal_model()


def get_all(session: Session) -> list[Node]:
    all_nodes: list[NodeRepo] = session.query(NodeRepo).all()
    return [node.to_internal_model() for node in all_nodes]


def get_by_uuid(uuid: UUID4, session: Session) -> Node:
    node: NodeRepo | None = session.get(NodeRepo, uuid)
    if node is None:
        raise KeyError
    return node.to_internal_model()


def get_all_for_tag_uuid(tag_uuid: UUID4, session: Session) -> list[Node]:
    statement = (
        select(NodeRepo)
        .join(NodeToTagsRepo)
        .where(NodeToTagsRepo.tag_uuid == tag_uuid)
    )
    nodes = session.scalars(statement).all()
    return [node.to_internal_model() for node in nodes]
    # Todo: paginate


def add_tag_to_node(
    node_uuid: UUID4, tag_uuid: UUID4, session: Session
) -> Node:
    node: NodeRepo | None = session.get(NodeRepo, node_uuid)
    tag: TagRepo | None = session.get(TagRepo, tag_uuid)
    if node is None or tag is None:
        raise KeyError
    if tag not in node.tags:
        node.tags.append(tag)
        session.commit()
        session.refresh(node)
    return node.to_internal_model()


def update_tags(
    node_uuid: UUID4, tags_uuids: list[UUID4], session: Session
) -> Node:
    node: NodeRepo | None = session.get(NodeRepo, node_uuid)
    if node is None:
        raise KeyError

    stmt = select(TagRepo).where(TagRepo.uuid.in_(tags_uuids))
    new_tags: list[TagRepo] = list(session.scalars(stmt))

    if len(tags_uuids) != len(new_tags):
        raise KeyError

    node.tags.clear()
    for tag in new_tags:
        node.tags.append(tag)

    session.commit()
    session.refresh(node)
    return node.to_internal_model()
