import asyncio

from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from app.core.config import settings
from app.workers.moderation_worker import run_worker


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start Redis moderation worker
    worker_task = asyncio.create_task(
        run_worker(),
        name="evolv-moderation-worker"
    )

    print("EVOLV moderation worker started.")

    yield

    # Gracefully stop worker during application shutdown
    print("Shutting down EVOLV moderation worker...")

    worker_task.cancel()

    with suppress(asyncio.CancelledError):
        await worker_task

    print("EVOLV moderation worker stopped.")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered content safety service for EVOLV",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():

    return {
        "service": "EVOLV AI Moderation",
        "status": "running"
    }


@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "service": "EVOLV AI Moderation Service"
    }