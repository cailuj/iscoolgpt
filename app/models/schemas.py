from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., description="Pergunta do usuário")
    context: str | None = Field(
        default=None,
        description="Contexto opcional (ex: resumo da aula, tópico, etc.)"
    )

class ChatResponse(BaseModel):
    answer: str
    model: str