from fastapi import APIRouter, Depends, status
from supabase import Client

from lexloop.auth.dependencies import get_supabase_client
from lexloop.model.link_model import LinkOut, LinkIn

from lexloop.service import link_service

from pydantic import UUID4

router = APIRouter()


@router.post("/links", status_code=status.HTTP_201_CREATED)
async def add_link(
    link: LinkIn, supabase: Client = Depends(get_supabase_client)
) -> LinkOut:
    added_link = link_service.add(link, supabase)
    return LinkOut.from_internal_model(added_link)


@router.get("/links")
async def get_links(
    supabase: Client = Depends(get_supabase_client),
) -> list[LinkOut]:
    link_list = link_service.get_all(supabase)
    return [LinkOut.from_internal_model(link) for link in link_list]


@router.get("/links/{uuid}")
async def get_link(
    uuid: UUID4, supabase: Client = Depends(get_supabase_client)
) -> LinkOut:
    link = link_service.get_by_uuid(uuid, supabase)
    return LinkOut.from_internal_model(link)
