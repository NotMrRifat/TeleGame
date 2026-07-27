"""Database Migration Manager."""

from app.config.logging import logger
from app.database.seeding import seed_default_data
from app.database.session import get_db_session, init_db


async def run_auto_migrations() -> None:
    """Ensures database tables are initialized and default seed data is inserted."""
    logger.info("Checking database migrations & schema readiness...")
    await init_db()
    async with get_db_session() as session:
        await seed_default_data(session)
    logger.info("Database auto-migration & seeding routine completed successfully.")
