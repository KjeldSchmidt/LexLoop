from uuid import uuid4
from lexloop.model.node_model import NodeIn, Node
from pydantic import UUID4
from supabase import Client


def add(node: NodeIn, supabase: Client) -> Node:
    """Add a node. user_id is automatically set by RLS based on JWT."""
    node_data = {
        "uuid": str(uuid4()),
        "term": node.term,
        "definition": node.definition,
    }
    result = supabase.table("nodes").insert(node_data).execute()
    data = result.data[0]
    return Node(
        uuid=data["uuid"],
        term=data["term"],
        definition=data["definition"],
    )


def get_all(supabase: Client) -> list[Node]:
    """Get all nodes. RLS automatically filters by user_id."""
    result = supabase.table("nodes").select("*").execute()
    return [
        Node(
            uuid=row["uuid"],
            term=row["term"],
            definition=row["definition"],
        )
        for row in result.data
    ]


def get_by_uuid(uuid: UUID4, supabase: Client) -> Node:
    """Get node by UUID. RLS automatically filters by user_id."""
    result = supabase.table("nodes").select("*").eq("uuid", str(uuid)).execute()
    if not result.data:
        raise ValueError(f"Node with uuid {uuid} not found")
    data = result.data[0]
    return Node(
        uuid=data["uuid"],
        term=data["term"],
        definition=data["definition"],
    )
