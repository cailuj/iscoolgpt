import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "IsCoolGPT - Flan T5 API"
    HF_TOKEN: str | None = os.getenv("HF_TOKEN")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "google/flan-t5-small")

    MAX_NEW_TOKENS: int = int(os.getenv("MAX_NEW_TOKENS", "256"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    TOP_P: float = float(os.getenv("TOP_P", "0.9"))

settings = Settings()