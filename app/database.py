from sqlalchemy.orm import declarative_base
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

AsyncSesionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provides an asynchronous database session to an API request
    and ensures it closes safely afterward.
    """
    async with AsyncSesionLocal() as session:
        yield session

