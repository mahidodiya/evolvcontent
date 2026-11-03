import asyncio

from app.modules.moderations.batch_processor import process_batch
from app.modules.moderations.schema import ModerationBatch


async def main():

    batch = ModerationBatch(
        posts=[
            {
                "moderationId": 1,
                "userId": 46,
                "postId": 149,
                "postType": "IMAGE",
                "mediaURL": "https://res.cloudinary.com/demo/image/upload/sample.jpg"
            },
            {
                "moderationId": 2,
                "userId": 47,
                "postId": 150,
                "postType": "TEXT",
                "textContent": "Learning Python and artificial intelligence."
            }
        ],
        totalPosts=2
    )

    result = await process_batch(batch)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())