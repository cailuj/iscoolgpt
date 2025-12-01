import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "IsCoolGPT - Gemma 2B API"
    HF_TOKEN: str | None = os.getenv("HF_TOKEN")
    GEMMA_MODEL_NAME: str = os.getenv("GEMMA_MODEL_NAME", "google/gemma-2b-it")

    MAX_NEW_TOKENS: int = int(os.getenv("MAX_NEW_TOKENS", "256"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P: float = float(os.getenv("TOP_P", "0.9"))

settings = Settings()