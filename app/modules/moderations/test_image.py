import asyncio

from app.modules.moderations.image import moderate_image


async def main():

    image_url = (
        "https://res.cloudinary.com/demo/image/upload/sample.jpg"
    )

    result = await moderate_image(image_url)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())