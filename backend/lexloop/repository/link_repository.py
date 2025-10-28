from uuid import uuid4
from pydantic import UUID4

from lexloop.model.link_model import LinkIn, Link, LinkType
from lexloop.model.node_model import Node
from supabase import Client


def add(link: LinkIn, supabase: Client) -> Link:
    """Add a link. user_id is automatically set by RLS based on JWT."""
    link_data = {
        "uuid": str(uuid4()),
        "type": link.type,
        "node1_uuid": link.node1,
        "node2_uuid": link.node2,
        "annotation": link.annotation,
    }
    result = supabase.table("links").insert(link_data).execute()
    data = result.data[0]

    # Fetch the nodes
    node1_result = (
        supabase.table("nodes")
        .select("*")
        .eq("uuid", data["node1_uuid"])
        .execute()
    )
    node2_result = (
        supabase.table("nodes")
        .select("*")
        .eq("uuid", data["node2_uuid"])
        .execute()
    )

    node1 = Node(**node1_result.data[0])
    node2 = Node(**node2_result.data[0])

    return Link(
        uuid=data["uuid"],
        type=LinkType[data["type"]],
        node1=node1,
        node2=node2,
        annotation=data["annotation"],
    )


def get_all(supabase: Client) -> list[Link]:
    """Get all links. RLS automatically filters by user_id."""
    result = (
        supabase.table("links")
        .select("*, node1:nodes!node1_uuid(*), node2:nodes!node2_uuid(*)")
        .execute()
    )

    links = []
    for row in result.data:
        links.append(
            Link(
                uuid=row["uuid"],
                type=LinkType[row["type"]],
                node1=Node(**row["node1"]),
                node2=Node(**row["node2"]),
                annotation=row["annotation"],
            )
        )
    return links


def get_all_for_node_uuid(node_uuid: UUID4, supabase: Client) -> list[Link]:
    """Get all links for a node. RLS automatically filters by user_id."""
    result = (
        supabase.table("links")
        .select("*, node1:nodes!node1_uuid(*), node2:nodes!node2_uuid(*)")
        .or_(f"node1_uuid.eq.{str(node_uuid)},node2_uuid.eq.{str(node_uuid)}")
        .execute()
    )

    links = []
    for row in result.data:
        links.append(
            Link(
                uuid=row["uuid"],
                type=LinkType[row["type"]],
                node1=Node(**row["node1"]),
                node2=Node(**row["node2"]),
                annotation=row["annotation"],
            )
        )
    return links


def get_by_uuid(uuid: UUID4, supabase: Client) -> Link:
    """Get link by UUID. RLS automatically filters by user_id."""
    result = (
        supabase.table("links")
        .select("*, node1:nodes!node1_uuid(*), node2:nodes!node2_uuid(*)")
        .eq("uuid", str(uuid))
        .execute()
    )

    if not result.data:
        raise ValueError(f"Link with uuid {uuid} not found")

    data = result.data[0]
    return Link(
        uuid=data["uuid"],
        type=LinkType[data["type"]],
        node1=Node(**data["node1"]),
        node2=Node(**data["node2"]),
        annotation=data["annotation"],
    )
