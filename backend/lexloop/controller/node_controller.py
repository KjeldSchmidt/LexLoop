from fastapi import APIRouter, Depends, status
from supabase import Client

from lexloop.auth.dependencies import get_supabase_client
from lexloop.model.link_model import LinkOut
from lexloop.model.node_model import NodeOut, NodeIn
from lexloop.repository.node_repository import Node

from lexloop.service import node_service, link_service

from pydantic import UUID4

router = APIRouter()


@router.post(
    "/nodes", response_model=NodeOut, status_code=status.HTTP_201_CREATED
)
async def node_node(
    node: NodeIn, supabase: Client = Depends(get_supabase_client)
) -> Node:
    return node_service.add(node, supabase)


@router.get(
    "/nodes",
    response_model=list[NodeOut],
)
async def get_nodes(
    supabase: Client = Depends(get_supabase_client),
) -> list[Node]:
    node_list = node_service.get_all(supabase)
    return node_list


@router.get("/nodes/{uuid}", response_model=NodeOut)
async def get_node(
    uuid: UUID4, supabase: Client = Depends(get_supabase_client)
) -> Node:
    node = node_service.get_by_uuid(uuid, supabase)
    return node


@router.get("/nodes/{node_uuid}/links", response_model=list[LinkOut])
async def get_node_links(
    node_uuid: UUID4, supabase: Client = Depends(get_supabase_client)
) -> list[LinkOut]:
    links = link_service.get_all_for_node_uuid(node_uuid, supabase)
    return [LinkOut.from_internal_model(link) for link in links]
