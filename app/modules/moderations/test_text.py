import asyncio

from app.modules.moderations.text import moderate_text


async def main():
    result = await moderate_text(
        "Today I learned how Redis Streams work."
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())