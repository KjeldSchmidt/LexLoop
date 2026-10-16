"""HTTP endpoints for vocabulary nodes (terms) and their tag/link relations."""

from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.orm import Session

from lexloop.auth.principal import require_principal
from lexloop.controller import get_db
from lexloop.model.link_model import LinkOut
from lexloop.model.node_model import NodeOut, NodeIn
from lexloop.model.pagination import Page, PaginationParams, pagination_params

from lexloop.service import node_service, link_service

from pydantic import UUID4

router = APIRouter(dependencies=[Depends(require_principal)])


@router.post("/nodes", status_code=status.HTTP_201_CREATED)
async def add_node(
    node: NodeIn = Body(embed=True), session: Session = Depends(get_db)
) -> NodeOut:
    """Create a node in a course, optionally with initial tags."""
    added_node = node_service.add(node, session)
    return NodeOut.from_internal_model(added_node)


@router.post("/nodes/update/{node_uuid}/tags/", status_code=status.HTTP_200_OK)
async def update_tags(
    node_uuid: UUID4,
    tag_uuids: list[UUID4] = Body(embed=True),
    session: Session = Depends(get_db),
) -> NodeOut:
    """Replace the full tag set on a node."""
    updated_node = node_service.update_tags(node_uuid, tag_uuids, session)
    return NodeOut.from_internal_model(updated_node)


@router.post("/nodes/{node_uuid}/{tag_uuid}", status_code=status.HTTP_200_OK)
async def add_tag_to_node(
    node_uuid: UUID4, tag_uuid: UUID4, session: Session = Depends(get_db)
) -> NodeOut:
    """Attach a single tag to a node."""
    updated_node = node_service.add_tag_to_node(node_uuid, tag_uuid, session)
    return NodeOut.from_internal_model(updated_node)


@router.get("/course/{course_uuid}/nodes")
async def get_nodes(
    course_uuid: UUID4,
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[NodeOut]:
    """List nodes belonging to a course (paginated)."""
    nodes, total = node_service.get_by_course_uuid(
        session,
        course_uuid,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return Page(
        items=[NodeOut.from_internal_model(node) for node in nodes],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/nodes/{uuid}")
async def get_node(uuid: UUID4, session: Session = Depends(get_db)) -> NodeOut:
    """Fetch a single node by UUID."""
    node = node_service.get_by_uuid(uuid, session)
    return NodeOut.from_internal_model(node)


@router.get("/nodes/{node_uuid}/links")
async def get_node_links(
    node_uuid: UUID4,
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[LinkOut]:
    """List links that involve the given node (paginated)."""
    links, total = link_service.get_all_for_node_uuid(
        node_uuid,
        session,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return Page(
        items=[LinkOut.from_internal_model(link) for link in links],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/nodes/tag/{tag_uuid}")
async def get_tag_nodes(
    tag_uuid: UUID4,
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[NodeOut]:
    """List nodes that have the given tag (paginated)."""
    nodes, total = node_service.get_all_for_tag_uuid(
        tag_uuid,
        session,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return Page(
        items=[NodeOut.from_internal_model(node) for node in nodes],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )
