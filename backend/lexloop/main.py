from fastapi import FastAPI, Response, status
from mangum import Mangum

from lexloop.controller.node_controller import router as word_router
from lexloop.controller.link_controller import router as link_router
from lexloop.controller.tag_controller import router as tag_router
from lexloop.auth.auth_controller import router as auth_router

app = FastAPI()


@app.get("/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(word_router)
app.include_router(link_router)
app.include_router(tag_router)
app.include_router(auth_router)

aws_handler = Mangum(app)
