from redis.exceptions import ResponseError

from app.messaging.redis_client import redis_client
from app.core.config import settings


async def initialize_request_stream():

    try:
        await redis_client.xgroup_create(
            name=settings.REDIS_MODERATION_REQUEST_STREAM,
            groupname=settings.REDIS_MODERATION_REQUEST_GROUP,
            id="0",
            mkstream=True
        )

        print("Moderation request stream and consumer group created")

    except ResponseError as error:

        if "BUSYGROUP" in str(error):
            print("Moderation request consumer group already exists")
        else:
            raise