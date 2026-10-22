"""HTTP endpoints for vocabulary nodes (terms) and their tag/link relations."""

from fastapi import APIRouter, Body, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.principal import Principal, require_principal
from lexloop.controller import get_db
from lexloop.model.link_model import LinkOut
from lexloop.model.node_model import NodeIn, NodeOut
from lexloop.model.pagination import Page, PaginationParams, pagination_params
from lexloop.service import (
    course_access,
    link_service,
    node_service,
    tag_service,
)

router = APIRouter(dependencies=[Depends(require_principal)])


@router.post("/nodes", status_code=status.HTTP_201_CREATED)
async def add_node(
    node: NodeIn = Body(embed=True),
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> NodeOut:
    """Create a node in a course, optionally with initial tags."""
    course_access.ensure_can_view_course(principal, node.course_uuid, session)
    added_node = node_service.add(node, session)
    return NodeOut.from_internal_model(added_node)


@router.post("/nodes/update/{node_uuid}/tags/", status_code=status.HTTP_200_OK)
async def update_tags(
    node_uuid: UUID4,
    tag_uuids: list[UUID4] = Body(embed=True),
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> NodeOut:
    """Replace the full tag set on a node."""
    existing = node_service.get_by_uuid(node_uuid, session)
    course_access.ensure_can_view_course(
        principal, existing.course_uuid, session
    )
    updated_node = node_service.update_tags(node_uuid, tag_uuids, session)
    return NodeOut.from_internal_model(updated_node)


@router.post("/nodes/{node_uuid}/{tag_uuid}", status_code=status.HTTP_200_OK)
async def add_tag_to_node(
    node_uuid: UUID4,
    tag_uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> NodeOut:
    """Attach a single tag to a node."""
    existing = node_service.get_by_uuid(node_uuid, session)
    course_access.ensure_can_view_course(
        principal, existing.course_uuid, session
    )
    updated_node = node_service.add_tag_to_node(node_uuid, tag_uuid, session)
    return NodeOut.from_internal_model(updated_node)


@router.get("/course/{course_uuid}/nodes")
async def get_nodes(
    course_uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[NodeOut]:
    """List nodes belonging to a course (paginated)."""
    course_access.ensure_can_view_course(principal, course_uuid, session)
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
async def get_node(
    uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> NodeOut:
    """Fetch a single node by UUID."""
    node = node_service.get_by_uuid(uuid, session)
    course_access.ensure_can_view_course(principal, node.course_uuid, session)
    return NodeOut.from_internal_model(node)


@router.get("/nodes/{node_uuid}/links")
async def get_node_links(
    node_uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[LinkOut]:
    """List links that involve the given node (paginated)."""
    node = node_service.get_by_uuid(node_uuid, session)
    course_access.ensure_can_view_course(principal, node.course_uuid, session)
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
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[NodeOut]:
    """List nodes that have the given tag (paginated)."""
    tag = tag_service.get_by_uuid(tag_uuid, session)
    course_access.ensure_can_view_course(principal, tag.course_uuid, session)
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
