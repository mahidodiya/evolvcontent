from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "EVOLV AI Moderation Service"
    APP_ENV: str = "development"
    DEBUG: bool = True

    OPENAI_API_KEY: str
    OPENAI_MODERATION_MODEL: str = "omni-moderation-latest"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Redis
    REDIS_URL: str

    REDIS_MODERATION_REQUEST_STREAM: str = (
        "evolv:moderation:requests"
    )

    REDIS_MODERATION_RESULT_STREAM: str = (
        "evolv:moderation:results"
    )

    REDIS_MODERATION_REQUEST_GROUP: str = (
        "moderation_workers"
    )

    REDIS_CONSUMER_NAME: str = "fastapi_worker_1"

    REDIS_BATCH_SIZE: int = 5

    REDIS_BLOCK_TIMEOUT: int = 5000

    REDIS_PENDING_IDLE_TIME: int = 60000

    REDIS_RECOVERY_BATCH_SIZE: int = 5

    REDIS_RECOVERY_INTERVAL: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()