from fastapi import APIRouter, status

from lexloop.model.link_model import LinkOut
from lexloop.model.node_model import NodeOut, NodeIn

from lexloop.service import node_service, link_service

from pydantic import UUID4

router = APIRouter()


@router.post("/nodes", status_code=status.HTTP_201_CREATED)
async def add_node(node: NodeIn) -> NodeOut:
    added_node = node_service.add(node)
    return NodeOut.from_internal_model(added_node)


@router.get("/nodes")
async def get_nodes() -> list[NodeOut]:
    node_list = node_service.get_all()
    return [NodeOut.from_internal_model(node) for node in node_list]


@router.get("/nodes/{uuid}")
async def get_node(uuid: UUID4) -> NodeOut:
    node = node_service.get_by_uuid(uuid)
    return NodeOut.from_internal_model(node)


@router.get("/nodes/{node_uuid}/links")
async def get_node_links(node_uuid: UUID4) -> list[LinkOut]:
    links = link_service.get_all_for_node_uuid(node_uuid)
    return [LinkOut.from_internal_model(link) for link in links]


@router.get("/nodes/tag/{tag_uuid}")
async def get_tag_nodes(tag_uuid: UUID4) -> list[NodeOut]:
    nodes = node_service.get_all_for_tag_uuid(tag_uuid)
    return [NodeOut.from_internal_model(node) for node in nodes]
