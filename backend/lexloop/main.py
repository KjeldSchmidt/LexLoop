from fastapi import FastAPI, Response
from fastapi import status, Depends
from mangum import Mangum
from sqlalchemy import text
from sqlalchemy.orm import Session

from lexloop.auth.auth_controller import router as auth_router
from lexloop.controller import get_db
from lexloop.controller.course_controller import router as course_router
from lexloop.controller.link_controller import router as link_router
from lexloop.controller.node_controller import router as word_router
from lexloop.controller.tag_controller import router as tag_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/health/database")
async def db_health(session: Session = Depends(get_db)) -> Response:
    session.execute(text("SELECT 1"))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(course_router)
app.include_router(word_router)
app.include_router(link_router)
app.include_router(tag_router)
app.include_router(auth_router)

aws_handler = Mangum(app)
