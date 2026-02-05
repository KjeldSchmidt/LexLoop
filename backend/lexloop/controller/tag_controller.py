from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.orm import Session

from lexloop.controller import get_db
from lexloop.model.tag_model import TagIn, TagOut

from lexloop.service import tag_service

from pydantic import UUID4

router = APIRouter()


@router.post("/tags", status_code=status.HTTP_201_CREATED)
async def add_tag(
    tag: TagIn = Body(embed=True), session: Session = Depends(get_db)
) -> TagOut:
    return TagOut.from_internal_model(tag_service.add(tag, session))


@router.get("/course/{course_uuid}/tags")
async def get_tags(
    course_uuid: UUID4, session: Session = Depends(get_db)
) -> list[TagOut]:
    tag_list = tag_service.get_by_course_uuid(session, course_uuid)
    return [TagOut.from_internal_model(tag) for tag in tag_list]


@router.get("/tags/{uuid}")
async def get_tag(uuid: UUID4, session: Session = Depends(get_db)) -> TagOut:
    tag = tag_service.get_by_uuid(uuid, session)
    return TagOut.from_internal_model(tag)


@router.get("/tags/node/{node_uuid}")
async def get_node_tags(
    node_uuid: UUID4, session: Session = Depends(get_db)
) -> list[TagOut]:
    tags = tag_service.get_all_for_node_uuid(node_uuid, session)
    return [TagOut.from_internal_model(tag) for tag in tags]
