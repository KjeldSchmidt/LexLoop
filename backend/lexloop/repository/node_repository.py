from uuid import uuid4

from lexloop.model.node_model import NodeIn, Node

from pynamodb.attributes import UnicodeAttribute
from lexloop.repository import MetaBase, ModelBase

from pydantic import UUID4


class NodeRepo(ModelBase):
    class Meta(MetaBase):
        table_name = "lexloop-words"

    uuid = UnicodeAttribute(hash_key=True)
    term = UnicodeAttribute()
    definition = UnicodeAttribute()

    def to_internal_model(self) -> Node:
        return Node(
            uuid=self.uuid,
            term=self.term,
            definition=self.definition,
        )


def add(node: NodeIn) -> Node:
    node_repo = NodeRepo(
        uuid=str(uuid4()),
        term=node.term,
        definition=node.definition,
    )
    node_repo.save()
    return node_repo.to_internal_model()


def get_all() -> list[Node]:
    # Todo: paginate
    return [word.to_internal_model() for word in NodeRepo.scan()]


def get_by_uuid(uuid: UUID4) -> Node:
    return NodeRepo.get(str(uuid)).to_internal_model()
