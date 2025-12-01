from functools import lru_cache
from loguru import logger
import torch
from transformers import pipeline
from huggingface_hub import login
from app.config import settings


if settings.HF_TOKEN:
    try:
        login(settings.HF_TOKEN)
        logger.info("Autenticado no Hugging Face Hub com HF_TOKEN.")
    except Exception as e:
        logger.error(f"Falha ao autenticar no Hugging Face Hub: {e}")
else:
    logger.warning("HF_TOKEN não definido! Continuando sem autenticação.")


def _build_prompt(question: str, context: str | None = None) -> str:
    """
    Flan-T5 usa prompts do tipo "instrução → resposta".
    Aqui criamos um prompt com instrução + contexto + pergunta.
    """

    system = (
        "Você é o IsCoolGPT, um assistente didático que explica conceitos de Cloud Computing "
        "de forma simples, clara e objetiva, usando exemplos quando necessário."
    )

    if context:
        return (
            f"{system}\n\n"
            f"Contexto adicional fornecido:\n{context}\n\n"
            f"Pergunta do aluno: {question}\n\n"
            "Explique passo a passo e de forma bem didática.\n\n"
            "Resposta:"
        )

    return (
        f"{system}\n\n"
        f"Pergunta do aluno: {question}\n\n"
        "Explique a resposta com clareza e em detalhes.\n\n"
        "Resposta:"
    )


@lru_cache(maxsize=1)
def _get_pipeline():
    """Carrega o modelo FLAN-T5 (super leve e rápido para CPU)."""

    device = -1  # CPU
    dtype = torch.float32

    logger.info(f"Carregando modelo {settings.MODEL_NAME} no modo CPU...")

    pipe = pipeline(
        "text2text-generation",
        model=settings.MODEL_NAME,
        device=device,
        dtype=dtype,
    )

    logger.info("Pipeline carregado com sucesso para Flan-T5.")
    return pipe


def generate_answer(question: str, context: str | None = None) -> str:
    """
    Gera a resposta usando FLAN-T5.
    """
    pipe = _get_pipeline()
    prompt = _build_prompt(question, context)

    logger.info("Gerando resposta com FLAN-T5...")

    outputs = pipe(
        prompt,
        max_new_tokens=settings.MAX_NEW_TOKENS,
        temperature=settings.TEMPERATURE,
        top_p=settings.TOP_P,
        do_sample=True,                 
    )

    answer = outputs[0]["generated_text"].strip()
    logger.info("Resposta gerada com sucesso.")

    return answer