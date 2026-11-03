import json
import logging

from app.messaging.redis_client import redis_client
from app.core.config import settings

logger = logging.getLogger(__name__)


async def recover_pending_messages(start_id="0-0"):
    """
    Recover idle messages from the Redis Pending Entries List
    using XAUTOCLAIM.
    """

    response = await redis_client.xautoclaim(
        name=settings.REDIS_MODERATION_REQUEST_STREAM,
        groupname=settings.REDIS_MODERATION_REQUEST_GROUP,
        consumername=settings.REDIS_CONSUMER_NAME,
        min_idle_time=settings.REDIS_PENDING_IDLE_TIME,
        start_id=start_id,
        count=settings.REDIS_RECOVERY_BATCH_SIZE
    )

    next_cursor = response[0]
    stream_messages = response[1]

    recovered_messages = []

    for message_id, fields in stream_messages:
        try:
            raw_payload = json.loads(fields["payload"])

            recovered_messages.append({
                "message_id": message_id,
                "payload": raw_payload,
                "valid": True,
                "error": None
            })

        except (KeyError, json.JSONDecodeError) as error:

            recovered_messages.append({
                "message_id": message_id,
                "payload": None,
                "valid": False,
                "error": str(error)
            })

    if recovered_messages:
        logger.info(
            "Recovered %s pending moderation messages",
            len(recovered_messages)
        )

    return next_cursor, recovered_messages