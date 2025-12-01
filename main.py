from fastapi import FastAPI

from app.config import settings
from app.routers import chat

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API FastAPI usando google/flan-t5 como LLM.",
)


@app.get("/health")
async def health():
    return {"status": "ok", "model": settings.MODEL_NAME}


app.include_router(chat.router)