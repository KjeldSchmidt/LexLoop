from uuid import uuid4, UUID

from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from lexloop.model.link_model import LinkType, LinkIn, Link

from pynamodb.attributes import UnicodeAttribute
from pynamodb_attributes import UnicodeEnumAttribute
from lexloop.repository import MetaBase, node_repository, ModelBase

from pydantic import UUID4


class LinkGSI(GlobalSecondaryIndex):  # type: ignore
    """
    GSI class attached to a PynamoDB model.
    """

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        index_name = "link-gsi"  # Required: name of the GSI in DynamoDB
        projection = (
            AllProjection()
        )  # Required: what attributes the GSI includes

    node1 = UnicodeAttribute(hash_key=True)  # Required: hash key for the GSI
    node2 = UnicodeAttribute(range_key=True)  # Optional: sort key for the GSI


class LinkRepo(ModelBase):
    class Meta(MetaBase):
        table_name = "lexloop-links"

    uuid = UnicodeAttribute(hash_key=True)
    type = UnicodeEnumAttribute(LinkType)
    annotation = UnicodeAttribute()
    node1 = UnicodeAttribute()  # Required: hash key for the GSI
    node2 = UnicodeAttribute()  # Optional: sort key for the GSI

    link_gsi = LinkGSI()

    def to_internal_model(self) -> Link:
        return Link(
            uuid=self.uuid,
            node1=node_repository.get_by_uuid(UUID(self.node1)),
            node2=node_repository.get_by_uuid(UUID(self.node2)),
            type=self.type,
            annotation=self.annotation,
        )


def add(link: LinkIn) -> Link:
    link_repo = LinkRepo(
        uuid=str(uuid4()),
        type=LinkType[link.type],
        node1=link.node1,
        node2=link.node2,
        annotation=link.annotation,
    )
    link_repo.save()
    return link_repo.to_internal_model()


def get_all() -> list[Link]:
    # Todo: paginate
    return [link.to_internal_model() for link in LinkRepo.scan()]


def get_all_for_node_uuid(node_uuid: UUID4) -> list[Link]:
    LinkRepo.link_gsi.query(str(node_uuid))
    condition = None
    condition &= LinkRepo.node1 == str(node_uuid)
    condition |= LinkRepo.node2 == str(node_uuid)
    # Todo: paginate
    return [
        link.to_internal_model()
        for link in LinkRepo.link_gsi.scan(filter_condition=condition)
    ]


def get_by_uuid(uuid: UUID4) -> Link:
    return LinkRepo.get(str(uuid)).to_internal_model()
