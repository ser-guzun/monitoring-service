from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=settings.ECHO_DB
)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
