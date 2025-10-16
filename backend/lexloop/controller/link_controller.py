from fastapi import APIRouter, status

from lexloop.model.link_model import LinkOut, LinkIn
from lexloop.repository.link_repository import LinkRepo

from lexloop.service import link_service

from pydantic import UUID4

router = APIRouter()


@router.post(
    "/links", response_model=LinkOut, status_code=status.HTTP_201_CREATED
)
async def add_link(link: LinkIn) -> LinkRepo:
    return link_service.add(link)


@router.get("/links", response_model=list[LinkOut])
async def get_links() -> list[LinkRepo]:
    link_list = link_service.get_all()
    return link_list


@router.get("/links/{uuid}", response_model=LinkOut)
async def get_link(uuid: UUID4) -> LinkRepo:
    link = link_service.get_by_uuid(uuid)
    return link
