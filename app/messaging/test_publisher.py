import asyncio

from app.messaging.publisher import publish_moderation_result
from app.messaging.redis_client import close_redis, connect_redis


async def main():

    await connect_redis()

    test_result = {
        "event": "CONTENT_SAFETY_COMPLETED",
        "results": [
            {
                "moderationId": 1,
                "userId": 46,
                "postId": 149,
                "postType": "IMAGE",
                "status": "COMPLETED",
                "decision": "APPROVED",
                "moderation_result": {
                    "flagged": False,
                    "categories": {},
                    "scores": {}
                },
                "error": None
            }
        ],
        "totalPosts": 1,
        "processedPosts": 1,
        "failedPosts": 0
    }

    try:
        message_id = await publish_moderation_result(test_result)

        print("Published Redis message:", message_id)

    finally:
        await close_redis()


if __name__ == "__main__":
    asyncio.run(main())