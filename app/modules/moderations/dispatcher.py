from app.modules.moderations.schema import ModerationPost, PostType
from app.modules.moderations.image import moderate_image
from app.modules.moderations.text import moderate_text


async def dispatch_moderation(post: ModerationPost) -> dict:
    """
    Route a post to the appropriate moderation module.
    """

    if post.postType == PostType.IMAGE:

        moderation_result = await moderate_image(
            post.mediaURL
        )

    elif post.postType == PostType.TEXT:

        moderation_result = await moderate_text(
            post.textContent
        )

    elif post.postType == PostType.VIDEO:

        raise NotImplementedError(
            "Video moderation has not been implemented yet."
        )

    else:
        raise ValueError(
            f"Unsupported post type: {post.postType}"
        )

    return {
        "moderationId": post.moderationId,
        "userId": post.userId,
        "postId": post.postId,
        "postType": post.postType.value,
        "status": "COMPLETED",
        "decision": (
            "REJECTED"
            if moderation_result["flagged"]
            else "APPROVED"
        ),
        "flagged": moderation_result["flagged"],
        "moderation_result": moderation_result,
        "error": None
    }