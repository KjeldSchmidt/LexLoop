from fastapi import APIRouter, status

from lexloop.model.link_model import LinkOut, LinkIn

from lexloop.service import link_service

from pydantic import UUID4

router = APIRouter()


@router.post("/links", status_code=status.HTTP_201_CREATED)
async def add_link(link: LinkIn) -> LinkOut:
    added_link = link_service.add(link)
    return LinkOut.from_internal_model(added_link)


@router.get("/links")
async def get_links() -> list[LinkOut]:
    link_list = link_service.get_all()
    return [LinkOut.from_internal_model(link) for link in link_list]


@router.get("/links/{uuid}")
async def get_link(uuid: UUID4) -> LinkOut:
    link = link_service.get_by_uuid(uuid)
    return LinkOut.from_internal_model(link)
