from uuid import uuid4, UUID

from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from lexloop.model.link_model import LinkType, LinkIn, Link

from pynamodb.attributes import UnicodeAttribute
from pynamodb_attributes import UnicodeEnumAttribute
from lexloop.repository import MetaBase, node_repository, ModelBase

from pydantic import UUID4


class Node1GSI(GlobalSecondaryIndex):  # type: ignore
    """
    GSI to filter for the first node
    """

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        index_name = "node1-gsi"  # Required: name of the GSI in DynamoDB
        projection = (
            AllProjection()
        )  # Required: what attributes the GSI includes

    node1 = UnicodeAttribute(hash_key=True)  # Required: hash key for the GSI
    node2 = UnicodeAttribute(range_key=True)  # Optional: sort key for the GSI


class Node2GSI(GlobalSecondaryIndex):  # type: ignore
    """
    GSI to filter for the second node
    """

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        index_name = "node2-gsi"  # Required: name of the GSI in DynamoDB
        projection = (
            AllProjection()
        )  # Required: what attributes the GSI includes

    node2 = UnicodeAttribute(hash_key=True)  # Required: hash key for the GSI
    node1 = UnicodeAttribute(range_key=True)  # Optional: sort key for the GSI


class LinkRepo(ModelBase):
    """
    Repository for storing links with two GSIs so search for both nodes of the link
    separately
    """

    class Meta(MetaBase):
        table_name = "lexloop-links"

    uuid = UnicodeAttribute(hash_key=True)
    type = UnicodeEnumAttribute(LinkType)
    annotation = UnicodeAttribute()
    node1 = UnicodeAttribute()  # Required: hash key for the GSI
    node2 = UnicodeAttribute()  # Optional: sort key for the GSI

    node1_gsi = Node1GSI()
    node2_gsi = Node2GSI()

    def to_internal_model(self) -> Link:
        """
        Convert a repo object to an internal Link representation.
        :return: Link object with data from LinkRepo
        """
        return Link(
            uuid=self.uuid,
            node1=node_repository.get_by_uuid(UUID(self.node1)),
            node2=node_repository.get_by_uuid(UUID(self.node2)),
            type=self.type,
            annotation=self.annotation,
        )


def add(link: LinkIn) -> Link:
    """
    Add a link to the repository
    :param link: link to add
    :return: internal link object
    """
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
    """
    Get all links from the repository
    :return: list of internal link objects
    """
    # Todo: paginate
    return [link.to_internal_model() for link in LinkRepo.scan()]


def get_all_for_node_uuid(node_uuid: UUID4) -> list[Link]:
    """
    Get all links for a given node uuid
    :param node_uuid: node uuid
    :return: all links that link to that node
    """
    # search in both columns
    links_first_node = LinkRepo.node1_gsi.query(str(node_uuid))
    links_second_node = LinkRepo.node2_gsi.query(str(node_uuid))
    # Todo: paginate
    return [link.to_internal_model() for link in links_first_node] + [
        link.to_internal_model() for link in links_second_node
    ]


def get_by_uuid(uuid: UUID4) -> Link:
    """
    Get a link by uuid
    :param uuid: link uuid
    :return: link with uuid
    """
    return LinkRepo.get(str(uuid)).to_internal_model()
