from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.orm import Session

from lexloop.controller import get_db
from lexloop.model.link_model import LinkOut, LinkIn, LinkType, LinkTypeInfo

from lexloop.service import link_service

from pydantic import UUID4

router = APIRouter()


@router.post("/links", status_code=status.HTTP_201_CREATED)
async def add_link(
    link: LinkIn = Body(embed=True), session: Session = Depends(get_db)
) -> LinkOut:
    added_link = link_service.add(link, session)
    return LinkOut.from_internal_model(added_link)


@router.get("/course/{course_uuid}/links")
async def get_links(
    course_uuid: UUID4, session: Session = Depends(get_db)
) -> list[LinkOut]:
    link_list = link_service.get_by_course_uuid(session, course_uuid)
    return [LinkOut.from_internal_model(link) for link in link_list]


@router.get("/links/types")
async def get_link_types() -> list[LinkTypeInfo]:
    return [
        LinkTypeInfo(value=link_type.value, display_name=link_type.display_name)
        for link_type in LinkType
    ]


@router.get("/links/{uuid}")
async def get_link(uuid: UUID4, session: Session = Depends(get_db)) -> LinkOut:
    link = link_service.get_by_uuid(uuid, session)
    return LinkOut.from_internal_model(link)
