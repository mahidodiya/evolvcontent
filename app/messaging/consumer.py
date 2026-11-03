import json

from pydantic import ValidationError

from app.messaging.redis_client import redis_client
from app.core.config import settings
from app.modules.moderations.schema import ModerationBatch


async def consume_messages():

    messages = await redis_client.xreadgroup(
        groupname=settings.REDIS_MODERATION_REQUEST_GROUP,
        consumername=settings.REDIS_CONSUMER_NAME,
        streams={
            settings.REDIS_MODERATION_REQUEST_STREAM: ">"
        },
        count=5,
        block=5000
    )

    if not messages:
        return []

    processed_messages = []

    for stream_name, stream_messages in messages:

        for message_id, fields in stream_messages:

            try:
                raw_payload = json.loads(fields["payload"])

                validated_payload = ModerationBatch.model_validate(
                    raw_payload
                )

                processed_messages.append({
                    "message_id": message_id,
                    "payload": validated_payload.model_dump(mode="json"),
                    "valid": True,
                    "error": None
                })

            except (KeyError, json.JSONDecodeError, ValidationError) as error:

                processed_messages.append({
                    "message_id": message_id,
                    "payload": None,
                    "valid": False,
                    "error": str(error)
                })

    return processed_messages