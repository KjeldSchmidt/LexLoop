from fastapi import FastAPI, Response, status
from mangum import Mangum

from lexloop.controller.node_controller import router as word_router
from lexloop.controller.link_controller import router as link_router

app = FastAPI()


@app.get("/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(word_router)
app.include_router(link_router)

aws_handler = Mangum(app)
