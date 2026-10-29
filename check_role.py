
import asyncio

from sqlalchemy import text

from app.database import engine


async def main():
    async with engine.connect() as connection:
        result = await connection.execute(
            text("SELECT role, COUNT(*) FROM users GROUP BY role")
        )

        for role, count in result.all():
            print(f"Role: {role}, Users: {count}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
