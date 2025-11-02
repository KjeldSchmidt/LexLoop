from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from lexloop.controller import get_db
from lexloop.model.tag_model import TagIn, TagOut

from lexloop.service import tag_service

from pydantic import UUID4

router = APIRouter()


@router.post("/tags", status_code=status.HTTP_201_CREATED)
async def add_tag(tag: TagIn, session: Session = Depends(get_db)) -> TagOut:
    return TagOut.from_internal_model(tag_service.add(tag, session))


@router.get("/tags")
async def get_tags(session: Session = Depends(get_db)) -> list[TagOut]:
    tag_list = tag_service.get_all(session)
    return [TagOut.from_internal_model(tag) for tag in tag_list]


@router.get("/tags/{uuid}")
async def get_tag(uuid: UUID4, session: Session = Depends(get_db)) -> TagOut:
    tag = tag_service.get_by_uuid(uuid, session)
    return TagOut.from_internal_model(tag)
