from uuid import uuid4, UUID

from lexloop.model.node_model import NodeIn, Node

from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute
from lexloop.repository import MetaBase, ModelBase, tag_repository

from pydantic import UUID4


class NodeRepo(ModelBase):
    class Meta(MetaBase):
        table_name = "lexloop-words"

    uuid = UnicodeAttribute(hash_key=True)
    term = UnicodeAttribute()
    definition = UnicodeAttribute()
    tags = UnicodeSetAttribute()

    def to_internal_model(self) -> Node:
        # if a UnicodeSetAttribute is empty, None is returned
        tags = set()
        if self.tags is not None:
            tags = self.tags
        return Node(
            uuid=self.uuid,
            term=self.term,
            definition=self.definition,
            tags={tag_repository.get_by_uuid(UUID(str(tag))) for tag in tags},
        )


def add(node: NodeIn) -> Node:
    node_repo = NodeRepo(
        uuid=str(uuid4()),
        term=node.term,
        definition=node.definition,
        tags=set(node.tags),
    )
    node_repo.save()
    return node_repo.to_internal_model()


def get_all() -> list[Node]:
    # Todo: paginate
    return [node.to_internal_model() for node in NodeRepo.scan()]


def get_by_uuid(uuid: UUID4) -> Node:
    return NodeRepo.get(str(uuid)).to_internal_model()


def get_all_for_tag_uuid(tag_uuid: UUID4) -> list[Node]:
    condition = None
    condition &= NodeRepo.tags.contains(str(tag_uuid))
    # Todo: paginate
    return [
        node.to_internal_model()
        for node in NodeRepo.scan(filter_condition=condition)
    ]
