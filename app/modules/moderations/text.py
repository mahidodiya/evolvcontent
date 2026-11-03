from openai import OpenAIError

from app.integrations.openai_client import openai_client
from app.core.config import settings
from app.modules.moderations.schema import ModerationResult


async def moderate_text(text_content: str) -> dict:

    if not text_content or not text_content.strip():
        raise ValueError("Text content cannot be empty")

    response = await openai_client.moderations.create(
        model=settings.OPENAI_MODERATION_MODEL,
        input=text_content
    )

    result = response.results[0]

    return ModerationResult(
        flagged=result.flagged,
        decision="REVIEW_REQUIRED" if result.flagged else "APPROVED",
        categories=result.categories.model_dump(),
        scores=result.category_scores.model_dump(),
        applied_input_types=(
            result.category_applied_input_types.model_dump()
            if result.category_applied_input_types
            else {}
        )
    ).model_dump()