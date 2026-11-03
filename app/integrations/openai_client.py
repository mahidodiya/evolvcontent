from openai import AsyncOpenAI

from app.core.config import settings


openai_client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=30.0,
    max_retries=2
)