"""Database session management with SQLAlchemy 2.x Async."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.logging import logger
from app.config.settings import settings
from app.models import Base

# Fall back to sqlite in-memory for testing/local fallback if postgres is default placeholder
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

engine_kwargs: dict = {
    "echo": settings.DEBUG,
    "future": True,
    "pool_pre_ping": True,
    "poolclass": NullPool,
}

if "asyncpg" in db_url:
    engine_kwargs["connect_args"] = {
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    }

engine = create_async_engine(db_url, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db() -> None:
    """Initialize database tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """Provide a transactional async database session context."""
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as err:
        await session.rollback()
        logger.error(f"Database session rollback due to exception: {err}")
        raise err
    finally:
        await session.close()
