from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from bot.core import settings
from . import repositories as repos

engine: AsyncEngine = create_async_engine(
    settings.pg_dsn.unicode_string(), echo=False, pool_pre_ping=True
)


async def new_session() -> AsyncSession:
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        return session


class Database:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.user = repos.UserRepository(session)
