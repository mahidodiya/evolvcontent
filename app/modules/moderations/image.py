from openai import OpenAIError

from app.integrations.openai_client import openai_client
from app.core.config import settings
from app.modules.moderations.schema import ModerationResult


async def moderate_image(image_url: str) -> dict:

    if not image_url or not image_url.strip():
        raise ValueError("Image URL cannot be empty")

    try:
        response = await openai_client.moderations.create(
            model=settings.OPENAI_MODERATION_MODEL,
            input=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        )

        result = response.results[0]

        moderation_result = ModerationResult(
            flagged=result.flagged,
            decision=(
                "REJECTED"
                if result.flagged
                else "APPROVED"
            ),
            categories=result.categories.model_dump(),
            scores=result.category_scores.model_dump(),
            applied_input_types=(
                result.category_applied_input_types.model_dump()
                if result.category_applied_input_types
                else {}
            )
        )

        return moderation_result.model_dump()

    except OpenAIError:
        raise