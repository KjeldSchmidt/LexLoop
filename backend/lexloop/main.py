from fastapi import FastAPI, Response, status

from lexloop.model import Word
from lexloop.repositories.word_repository import WordModel

from lexloop.service import word_service

app = FastAPI()


@app.get("/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/words")
async def add_word(word: Word) -> Response:
    word_service.add(word)
    return Response(status_code=status.HTTP_201_CREATED)


@app.get(
    "/words",
    response_model=list[Word],
)
async def get_words() -> list[WordModel]:
    word_list = word_service.get_all()
    return word_list
