from fastapi import APIRouter, status

from lexloop.model.tag_model import TagIn, TagOut

from lexloop.service import tag_service

from pydantic import UUID4

router = APIRouter()


@router.post("/tags", status_code=status.HTTP_201_CREATED)
async def add_tag(tag: TagIn) -> TagOut:
    return TagOut.from_internal_model(tag_service.add(tag))


@router.get("/tags")
async def get_tags() -> list[TagOut]:
    tag_list = tag_service.get_all()
    return [TagOut.from_internal_model(tag) for tag in tag_list]


@router.get("/tags/{uuid}")
async def get_tag(uuid: UUID4) -> TagOut:
    tag = tag_service.get_by_uuid(uuid)
    return TagOut.from_internal_model(tag)
