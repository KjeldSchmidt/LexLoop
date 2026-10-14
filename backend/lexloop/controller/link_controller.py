"""HTTP endpoints for links between vocabulary nodes."""

from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.orm import Session

from lexloop.controller import get_db
from lexloop.model.link_model import LinkOut, LinkIn, LinkType, LinkTypeInfo
from lexloop.model.pagination import Page, PaginationParams, pagination_params

from lexloop.service import link_service

from pydantic import UUID4

router = APIRouter()


@router.post("/links", status_code=status.HTTP_201_CREATED)
async def add_link(
    link: LinkIn = Body(embed=True), session: Session = Depends(get_db)
) -> LinkOut:
    """Create a typed link between two nodes."""
    added_link = link_service.add(link, session)
    return LinkOut.from_internal_model(added_link)


@router.get("/course/{course_uuid}/links")
async def get_links(
    course_uuid: UUID4,
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[LinkOut]:
    """List links belonging to a course (paginated)."""
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
async def get_link(uuid: UUID4, session: Session = Depends(get_db)) -> LinkOut:
    """Fetch a single link by UUID."""
    link = link_service.get_by_uuid(uuid, session)
    return LinkOut.from_internal_model(link)
