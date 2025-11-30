from functools import lru_cache
from loguru import logger
import torch
from transformers import pipeline
from huggingface_hub import login
from app.config import settings


def _login_to_hf():
    """Autentica no Hugging Face Hub usando HF_TOKEN."""
    if settings.HF_TOKEN:
        try:
            login(settings.HF_TOKEN)
            logger.info("Autenticado no Hugging Face Hub com HF_TOKEN.")
        except Exception as e:
            logger.error(f"Falha ao autenticar no Hugging Face Hub: {e}")
    else:
        logger.warning("HF_TOKEN não definido!")


def _build_prompt(question: str, context: str | None = None) -> str:
    system = (
        "Você é o IsCoolGPT, um assistente didático para ajudar estudantes em cloud computing."
    )

    if context:
        return f"{system}\n\nContexto:\n{context}\n\nPergunta:\n{question}\n\nResposta:"
    return f"{system}\n\nPergunta:\n{question}\n\nResposta:"


@lru_cache(maxsize=1)
def _get_pipeline():
    """Carrega o modelo Gemma-2B-IT (leve, roda no CPU)."""
    _login_to_hf()

    device = -1 
    torch_dtype = torch.float32

    logger.info(f"Carregando modelo {settings.GEMMA_MODEL_NAME} no CPU...")

    pipe = pipeline(
        "text-generation",
        model=settings.GEMMA_MODEL_NAME,
        device=device,
        torch_dtype=torch_dtype,
    )

    logger.info("Pipeline carregado com sucesso.")
    return pipe


def generate_answer(question: str, context: str | None = None) -> str:
    pipe = _get_pipeline()
    prompt = _build_prompt(question, context)

    logger.info("Gerando resposta com Gemma-2B-IT...")

    outputs = pipe(
        prompt,
        max_new_tokens=settings.MAX_NEW_TOKENS,
        temperature=settings.TEMPERATURE,
        top_p=settings.TOP_P,
        do_sample=True,
        return_full_text=False,
    )

    answer = outputs[0]["generated_text"].strip()
    return answer