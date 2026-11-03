import json

from app.messaging.redis_client import redis_client
from app.core.config import settings


async def publish_moderation_result(result: dict) -> str:
    """
    Publish completed moderation results to Redis result stream.
    """

    try:
        message_id = await redis_client.xadd(
            settings.REDIS_MODERATION_RESULT_STREAM,
            {
                "payload": json.dumps(
                    result,
                    ensure_ascii=False
                )
            }
        )

        print(
            f"Moderation result published successfully. "
            f"Redis message ID: {message_id}"
        )

        return message_id

    except Exception as error:

        print(f"Failed to publish moderation result: {error}")

        raise