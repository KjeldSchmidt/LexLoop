from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from lexloop.controller import get_db
from lexloop.model.link_model import LinkOut
from lexloop.model.node_model import NodeOut, NodeIn

from lexloop.service import node_service, link_service

from pydantic import UUID4

router = APIRouter()


@router.post("/nodes", status_code=status.HTTP_201_CREATED)
async def add_node(node: NodeIn, session: Session = Depends(get_db)) -> NodeOut:
    added_node = node_service.add(node, session)
    return NodeOut.from_internal_model(added_node)


@router.post("/nodes/{node_uuid}/{tag_uuid}", status_code=status.HTTP_200_OK)
async def add_tag_to_node(
    node_uuid: UUID4, tag_uuid: UUID4, session: Session = Depends(get_db)
) -> NodeOut:
    updated_node = node_service.add_tag_to_node(node_uuid, tag_uuid, session)
    return NodeOut.from_internal_model(updated_node)


@router.get("/nodes")
async def get_nodes(session: Session = Depends(get_db)) -> list[NodeOut]:
    node_list = node_service.get_all(session)
    return [NodeOut.from_internal_model(node) for node in node_list]


@router.get("/nodes/{uuid}")
async def get_node(uuid: UUID4, session: Session = Depends(get_db)) -> NodeOut:
    node = node_service.get_by_uuid(uuid, session)
    return NodeOut.from_internal_model(node)


@router.get("/nodes/{node_uuid}/links")
async def get_node_links(
    node_uuid: UUID4, session: Session = Depends(get_db)
) -> list[LinkOut]:
    links = link_service.get_all_for_node_uuid(node_uuid, session)
    return [LinkOut.from_internal_model(link) for link in links]


@router.get("/nodes/tag/{tag_uuid}")
async def get_tag_nodes(
    tag_uuid: UUID4, session: Session = Depends(get_db)
) -> list[NodeOut]:
    nodes = node_service.get_all_for_tag_uuid(tag_uuid, session)
    return [NodeOut.from_internal_model(node) for node in nodes]
