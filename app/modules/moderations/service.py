from openai import APIError, APITimeoutError, APIConnectionError

from app.integrations.openai_client import openai_client
from app.core.config import settings


async def moderate_image(image_url: str):

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

        decision = (
            "REJECTED"
            if result.flagged
            else "APPROVED"
        )

        return {
            "success": True,
            "flagged": result.flagged,
            "decision": decision,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
            "applied_input_types": (
                result.category_applied_input_types.model_dump()
                if result.category_applied_input_types
                else {}
            )
        }

    except (APITimeoutError, APIConnectionError):
        raise

    except APIError:
        raise

    except Exception as error:

        print(f"Image moderation error: {error}")

        raise