import asyncio

from app.modules.moderations.dispatcher import dispatch_moderation
from app.modules.moderations.schema import ModerationPost


async def main():

    post = ModerationPost(
        moderationId=1,
        userId=46,
        postId=149,
        postType="IMAGE",
        mediaURL=(
            "https://res.cloudinary.com/demo/"
            "image/upload/sample.jpg"
        )
    )

    result = await dispatch_moderation(post)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())