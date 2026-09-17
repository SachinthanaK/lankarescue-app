from collections.abc import AsyncIterator

from lankarescue_database import Database
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .config import get_settings

settings = get_settings()
database = Database(settings.database_url, echo=settings.database_echo)


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in database.session():
        yield session


async def database_ready() -> bool:
    try:
        async with database.session_factory() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
