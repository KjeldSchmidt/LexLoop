from lexloop.model.link_model import LinkIn
from lexloop.repository import link_repository
from lexloop.repository.link_repository import Link
from supabase import Client
from pydantic import UUID4


def add(link: LinkIn, supabase: Client) -> Link:
    return link_repository.add(link, supabase)


def get_all(supabase: Client) -> list[Link]:
    return link_repository.get_all(supabase)


def get_by_uuid(uuid: UUID4, supabase: Client) -> Link:
    return link_repository.get_by_uuid(uuid, supabase)


def get_all_for_node_uuid(node_uuid: UUID4, supabase: Client) -> list[Link]:
    return link_repository.get_all_for_node_uuid(node_uuid, supabase)
