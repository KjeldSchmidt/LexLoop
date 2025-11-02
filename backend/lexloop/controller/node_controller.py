from fastapi import APIRouter, status

from lexloop.model.link_model import LinkOut
from lexloop.model.node_model import NodeOut, NodeIn
from lexloop.repository.node_repository import Node

from lexloop.service import node_service, link_service

from pydantic import UUID4

router = APIRouter()


@router.post(
    "/nodes", response_model=NodeOut, status_code=status.HTTP_201_CREATED
)
async def node_node(node: NodeIn) -> Node:
    return node_service.add(node)


@router.get(
    "/nodes",
    response_model=list[NodeOut],
)
async def get_nodes() -> list[Node]:
    node_list = node_service.get_all()
    return node_list


@router.get("/nodes/{uuid}", response_model=NodeOut)
async def get_node(uuid: UUID4) -> Node:
    node = node_service.get_by_uuid(uuid)
    return node


@router.get("/nodes/{node_uuid}/links", response_model=list[LinkOut])
async def get_node_links(node_uuid: UUID4) -> list[LinkOut]:
    links = link_service.get_all_for_node_uuid(node_uuid)
    return [LinkOut.from_internal_model(link) for link in links]
