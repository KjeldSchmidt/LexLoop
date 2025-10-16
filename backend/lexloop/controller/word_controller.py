from fastapi import APIRouter, status

from lexloop.model.word_model import WordOut, WordIn
from lexloop.repository.word_repository import Word

from lexloop.service import word_service

from pydantic import UUID4

router = APIRouter()


@router.post(
    "/words", response_model=WordOut, status_code=status.HTTP_201_CREATED
)
async def add_word(word: WordIn) -> Word:
    return word_service.add(word)


@router.get(
    "/words",
    response_model=list[WordOut],
)
async def get_words() -> list[Word]:
    word_list = word_service.get_all()
    return word_list


@router.get("/words/{uuid}", response_model=WordOut)
async def get_word(uuid: UUID4) -> Word:
    word = word_service.get_by_uuid(uuid)
    return word
