"""HTTP endpoints for links between vocabulary nodes."""

from uuid import UUID

from fastapi import APIRouter, Body, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.principal import Principal, require_principal
from lexloop.controller import get_db
from lexloop.model.link_model import LinkIn, LinkOut, LinkType, LinkTypeInfo
from lexloop.model.pagination import Page, PaginationParams, pagination_params
from lexloop.service import course_access, link_service, node_service

router = APIRouter(dependencies=[Depends(require_principal)])


@router.post("/links", status_code=status.HTTP_201_CREATED)
async def add_link(
    link: LinkIn = Body(embed=True),
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> LinkOut:
    """Create a typed link between two nodes."""
    node = node_service.get_by_uuid(UUID(link.node1), session)
    course_access.ensure_can_view_course(principal, node.course_uuid, session)
    added_link = link_service.add(link, session)
    return LinkOut.from_internal_model(added_link)


@router.get("/course/{course_uuid}/links")
async def get_links(
    course_uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[LinkOut]:
    """List links belonging to a course (paginated)."""
    course_access.ensure_can_view_course(principal, course_uuid, session)
    links, total = link_service.get_by_course_uuid(
        session,
        course_uuid,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return Page(
        items=[LinkOut.from_internal_model(link) for link in links],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/links/types")
async def get_link_types() -> list[LinkTypeInfo]:
    """Return the allowed link type values and display names."""
    return [
        LinkTypeInfo(value=link_type.value, display_name=link_type.display_name)
        for link_type in LinkType
    ]


@router.get("/links/{uuid}")
async def get_link(
    uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> LinkOut:
    """Fetch a single link by UUID."""
    link = link_service.get_by_uuid(uuid, session)
    course_access.ensure_can_view_course(
        principal, link.node1.course_uuid, session
    )
    return LinkOut.from_internal_model(link)
