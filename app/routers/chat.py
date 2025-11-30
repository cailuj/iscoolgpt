from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_client import generate_answer
from app.config import settings

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode ser vazia.")

    try:
        answer = generate_answer(req.question, req.context)
        return ChatResponse(answer=answer, model=settings.GEMMA_MODEL_NAME)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar resposta com Gemma 2: {str(e)}",
        )