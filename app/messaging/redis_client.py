import redis.asyncio as redis

from app.core.config import settings


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=10,
    socket_timeout=None,
    health_check_interval=30
)


async def connect_redis():

    try:
        await redis_client.ping()
        print("Redis connection established")

    except Exception as error:
        print(f"Redis connection failed: {error}")
        raise


async def close_redis():

    await redis_client.aclose()