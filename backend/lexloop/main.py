from fastapi import FastAPI, Response, status

from lexloop.controller.word_controller import router as word_router


app = FastAPI()


@app.get("/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(word_router)
