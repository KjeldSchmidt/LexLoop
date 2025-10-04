from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/health")
async def health():
    return Response(status_code=status.HTTP_204_NO_CONTENT)
