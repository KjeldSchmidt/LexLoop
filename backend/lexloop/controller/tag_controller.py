"""HTTP endpoints for tags within a course."""

from fastapi import APIRouter, Body, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.principal import Principal, require_principal
from lexloop.controller import get_db
from lexloop.model.pagination import Page, PaginationParams, pagination_params
from lexloop.model.tag_model import TagIn, TagOut
from lexloop.service import course_access, node_service, tag_service

router = APIRouter(dependencies=[Depends(require_principal)])


@router.post("/tags", status_code=status.HTTP_201_CREATED)
async def add_tag(
    tag: TagIn = Body(embed=True),
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> TagOut:
    """Create a tag in a course."""
    course_access.ensure_can_view_course(principal, tag.course_uuid, session)
    return TagOut.from_internal_model(tag_service.add(tag, session))


@router.get("/course/{course_uuid}/tags")
async def get_tags(
    course_uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
) -> Page[TagOut]:
    """List tags belonging to a course (paginated)."""
    course_access.ensure_can_view_course(principal, course_uuid, session)
    tags, total = tag_service.get_by_course_uuid(
        session,
        course_uuid,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return Page(
        items=[TagOut.from_internal_model(tag) for tag in tags],
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/tags/{uuid}")
async def get_tag(
    uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> TagOut:
    """Fetch a single tag by UUID."""
    tag = tag_service.get_by_uuid(uuid, session)
    course_access.ensure_can_view_course(principal, tag.course_uuid, session)
    return TagOut.from_internal_model(tag)


@router.get("/tags/node/{node_uuid}")
async def get_node_tags(
    node_uuid: UUID4,
    principal: Principal = Depends(require_principal),
    session: Session = Depends(get_db),
) -> list[TagOut]:
    """List tags attached to a node (unpaginated; typically few)."""
    node = node_service.get_by_uuid(node_uuid, session)
    course_access.ensure_can_view_course(principal, node.course_uuid, session)
    tags = tag_service.get_all_for_node_uuid(node_uuid, session)
    return [TagOut.from_internal_model(tag) for tag in tags]
