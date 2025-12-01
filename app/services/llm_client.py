from functools import lru_cache
from loguru import logger
from transformers import pipeline
from huggingface_hub import login
from app.config import settings


if settings.HF_TOKEN:
    try:
        login(settings.HF_TOKEN)
        logger.info("Authenticated to Hugging Face Hub.")
    except Exception as e:
        logger.error(f"HF authentication error: {e}")
else:
    logger.warning("HF_TOKEN not set! Proceeding without authentication.")


def build_prompt(question: str, context: str | None = None) -> str:
    system = (
        "You are IsCoolGPT, a helpful assistant for cloud computing students. "
        "Respond concisely, clearly, and in English."
    )

    if context:
        return f"{system}\n\nContext:\n{context}\n\nQuestion:\n{question}\nAnswer:"

    return f"{system}\n\nQuestion:\n{question}\nAnswer:"


@lru_cache(maxsize=1)
def get_pipeline():
    logger.info(f"Loading model {settings.MODEL_NAME} on CPU...")

    pipe = pipeline(
        "text2text-generation",
        model=settings.MODEL_NAME,
        device=-1,
    )

    logger.info("Pipeline successfully loaded.")
    return pipe


def generate_answer(question: str, context: str | None = None) -> str:
    pipe = get_pipeline()
    prompt = build_prompt(question, context)

    logger.info("Generating answer with FLAN-T5-Small...")

    try:
        outputs = pipe(
            prompt,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            temperature=settings.TEMPERATURE,
            top_p=settings.TOP_P,
        )

        answer = outputs[0]["generated_text"].strip()
        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "An internal error occurred while generating the response."