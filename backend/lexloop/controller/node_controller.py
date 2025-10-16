from fastapi import APIRouter, status

from lexloop.model.node_model import NodeOut, NodeIn
from lexloop.repository.node_repository import Node

from lexloop.service import node_service

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
