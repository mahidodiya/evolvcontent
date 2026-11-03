from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings

from app.messaging.redis_client import (
    connect_redis,
    close_redis
)

from app.messaging.stream_manager import (
    initialize_request_stream
)
from app.messaging.consumer import consume_messages



@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect_redis()

    await initialize_request_stream()

    yield

    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered content safety service for EVOLV",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "EVOLV AI Moderation Service"
    }


@app.get("/")
async def root():

    return {
        "service": "EVOLV AI Moderation",
        "status": "running"
    }


@app.get("/health")
async def health_check():

    return {
        "status": "healthy"
    }

@app.get("/test/redis-consumer")
async def test_redis_consumer():

    messages = await consume_messages()

    return {
        "total_messages": len(messages),
        "messages": messages
    }