from app.modules.moderations.schema import ModerationBatch
from app.modules.moderations.dispatcher import dispatch_moderation


async def process_batch(batch: ModerationBatch) -> dict:
    """
    Process all posts in a moderation batch independently.
    """

    results = []

    for post in batch.posts:

        try:
            moderation_result = await dispatch_moderation(post)

            results.append(moderation_result)

        except Exception as error:

            results.append({
                "moderationId": post.moderationId,
                "userId": post.userId,
                "postId": post.postId,
                "postType": post.postType.value,
                "status": "FAILED",
                "decision": None,
                "flagged": None,
                "moderation_result": None,
                "error": str(error)
            })

    completed_posts = sum(
        1 for result in results
        if result["status"] == "COMPLETED"
    )

    failed_posts = sum(
        1 for result in results
        if result["status"] == "FAILED"
    )

    return {
        "event": "CONTENT_SAFETY_COMPLETED",
        "results": results,
        "totalPosts": batch.totalPosts,
        "processedPosts": completed_posts,
        "failedPosts": failed_posts
    }