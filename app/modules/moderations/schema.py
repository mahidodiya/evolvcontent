from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PostType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    TEXT = "TEXT"


class ModerationPost(BaseModel):
    model_config = ConfigDict(extra="ignore")

    userId: int
    postId: int
    postType: PostType

    mediaURL: Optional[str] = None
    textContent: Optional[str] = None

    # Recommended for reliable retries and duplicate prevention.
    # Ask Ankit to add this to the NestJS payload.
    moderationId: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_content(self):

        if self.postType in (PostType.IMAGE, PostType.VIDEO):
            if not self.mediaURL:
                raise ValueError(
                    f"{self.postType.value} post requires mediaURL"
                )

        if self.postType == PostType.TEXT:
            if not self.textContent or not self.textContent.strip():
                raise ValueError("TEXT post requires textContent")

        return self


class ModerationBatch(BaseModel):
    posts: list[ModerationPost] = Field(min_length=1)
    totalPosts: int

    @model_validator(mode="after")
    def validate_total_posts(self):

        if self.totalPosts != len(self.posts):
            raise ValueError(
                "totalPosts does not match the number of posts"
            )

        return self

class ModerationResult(BaseModel):
    flagged: bool
    decision: str
    categories: dict[str, bool]
    scores: dict[str, float]
    applied_input_types: dict[str, Any]

    provider: str = "openai"
    model: str = "omni-moderation-latest"
    error: Optional[str] = None