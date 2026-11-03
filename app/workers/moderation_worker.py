import asyncio
import json
import logging

from app.messaging.redis_client import (
    redis_client,
    connect_redis,
    close_redis
)

from app.messaging.consumer import consume_messages

from app.messaging.publisher import publish_moderation_result

from app.messaging.stream_manager import initialize_request_stream

from app.modules.moderations.schema import ModerationBatch

from app.modules.moderations.batch_processor import process_batch

from app.core.config import settings
from app.messaging.recovery import recover_pending_messages


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


DEAD_LETTER_STREAM = "evolv:moderation:dead-letter"


async def send_to_dead_letter(message: dict):
    """
    Preserve malformed messages before acknowledging them.
    """

    await redis_client.xadd(
        DEAD_LETTER_STREAM,
        {
            "payload": json.dumps({
                "original_message_id": message["message_id"],
                "original_payload": message.get("payload"),
                "error": message.get("error")
            })
        }
    )


async def process_message(message: dict):
    """
    Process one Redis request message.
    """

    message_id = message["message_id"]

    try:

        # Handle invalid messages separately.
        if not message["valid"]:

            logger.error(
                "Invalid moderation message: %s",
                message_id
            )

            await send_to_dead_letter(message)

            await redis_client.xack(
                settings.REDIS_MODERATION_REQUEST_STREAM,
                settings.REDIS_MODERATION_REQUEST_GROUP,
                message_id
            )

            return

        # Validate batch.
        batch = ModerationBatch.model_validate(
            message["payload"]
        )

        logger.info(
            "Processing moderation batch: %s",
            message_id
        )

        # Process all posts.
        result = await process_batch(batch)

        # Publish results.
        result_message_id = await publish_moderation_result(result)

        logger.info(
            "Moderation results published: %s",
            result_message_id
        )

        # Acknowledge original request only after publishing.
        await redis_client.xack(
            settings.REDIS_MODERATION_REQUEST_STREAM,
            settings.REDIS_MODERATION_REQUEST_GROUP,
            message_id
        )

        logger.info(
            "Original request acknowledged: %s",
            message_id
        )

    except Exception:

        logger.exception(
            "Failed to process moderation message: %s",
            message_id
        )

        # Do not acknowledge.
        # The message remains pending in Redis.
        # Recovery will be implemented using XAUTOCLAIM.


async def run_worker():

    logger.info("Starting EVOLV moderation worker...")

    recovery_cursor = "0-0"
    last_recovery_time = 0

    try:
        await connect_redis()
        await initialize_request_stream()

        logger.info("Moderation worker is running.")

        loop = asyncio.get_running_loop()

        while True:

            # 1. Consume new messages
            messages = await consume_messages()

            for message in messages:
                await process_message(message)

            # 2. Check for abandoned pending messages
            current_time = loop.time()

            if (
                current_time - last_recovery_time
                >= settings.REDIS_RECOVERY_INTERVAL
            ):

                recovery_cursor, recovered_messages = (
                    await recover_pending_messages(recovery_cursor)
                )

                for message in recovered_messages:
                    await process_message(message)

                # Complete the scan before starting another interval
                if recovery_cursor == "0-0":
                    last_recovery_time = current_time

    except asyncio.CancelledError:

        logger.info("Moderation worker shutdown requested.")
        raise

    except Exception:

        logger.exception("Moderation worker encountered an error.")
        raise

    finally:

        await close_redis()
        logger.info("Redis connection closed.")

if __name__ == "__main__":
    asyncio.run(run_worker())