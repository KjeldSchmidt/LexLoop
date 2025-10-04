from fastapi import FastAPI, Response, status

from lexloop.model import WordOut, WordIn
from lexloop.repositories.word_repository import WordRepo

from lexloop.service import word_service

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
