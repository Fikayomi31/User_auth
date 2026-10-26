import asyncio

from app.database import Base, engine
from app.model.user import User


async def init_db():
    async with engine.begin() as connection:
        # creates tables that are defined in the metadata but do not already exist.
        await connection.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("Database table crated successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())

