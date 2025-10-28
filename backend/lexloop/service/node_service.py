from lexloop.model.node_model import NodeIn, Node
from lexloop.repository import node_repository
from supabase import Client
from pydantic import UUID4


def add(word: NodeIn, supabase: Client) -> Node:
    return node_repository.add(word, supabase)


def get_all(supabase: Client) -> list[Node]:
    return node_repository.get_all(supabase)


def get_by_uuid(uuid: UUID4, supabase: Client) -> Node:
    return node_repository.get_by_uuid(uuid, supabase)
