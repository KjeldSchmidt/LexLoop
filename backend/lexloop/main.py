from fastapi import FastAPI, Response, status

from lexloop.model.link_model import LinkOut, LinkIn
from lexloop.repository.link_repository import LinkRepo

from lexloop.service import link_service

from pydantic import UUID4

from lexloop.controller.word_controller import router as word_router

app = FastAPI()


@app.get("/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/links", response_model=LinkOut, status_code=status.HTTP_201_CREATED)
async def add_link(link: LinkIn) -> LinkRepo:
    return link_service.add(link)


@app.get("/links", response_model=list[LinkOut])
async def get_links() -> list[LinkRepo]:
    link_list = link_service.get_all()
    return link_list


@app.get("/links/{uuid}", response_model=LinkOut)
async def get_link(uuid: UUID4) -> LinkRepo:
    link = link_service.get_by_uuid(uuid)
    return link


app.include_router(word_router)
