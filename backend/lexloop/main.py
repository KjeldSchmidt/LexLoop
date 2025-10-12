from fastapi import FastAPI, Response, status

from lexloop.model.link_model import LinkOut, LinkIn
from lexloop.model.word_model import WordOut, WordIn
from lexloop.repositories.link_repository import LinkRepo
from lexloop.repositories.word_repository import WordRepo

from lexloop.service import word_service, link_service

from pydantic import UUID4

app = FastAPI()


@app.get("/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/words", response_model=WordOut, status_code=status.HTTP_201_CREATED)
async def add_word(word: WordIn) -> WordRepo:
    return word_service.add(word)


@app.get(
    "/words",
    response_model=list[WordOut],
)
async def get_words() -> list[WordRepo]:
    word_list = word_service.get_all()
    return word_list


@app.get("/words/{uuid}", response_model=WordOut)
async def get_word(uuid: UUID4) -> WordRepo:
    word = word_service.get_by_uuid(uuid)
    return word


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
