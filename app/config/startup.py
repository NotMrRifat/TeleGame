"""Startup validation service for TeleGame platform."""

import sys

from app.config.logging import logger
from app.config.settings import settings


class StartupValidationError(Exception):
    """Exception raised when startup validation fails."""

    pass


async def validate_startup_configuration() -> bool:
    """Validates bot configuration, secrets, Python version, and database connection.

    Returns:
        bool: True if validation succeeds.

    Raises:
        StartupValidationError: If any critical validation check fails.
    """
    logger.info("Initializing platform startup validation checks...")

    # 1. Validate Python Version (3.13+)
    if sys.version_info < (3, 13):
        logger.warning(
            f"Python version {sys.version_info.major}.{sys.version_info.minor} is below 3.13. Python 3.13+ is recommended."
        )

    # 2. Validate Bot Token
    if not settings.BOT_TOKEN or settings.BOT_TOKEN.startswith("123456789:ABCdef"):
        logger.warning(
            "BOT_TOKEN is using default/placeholder value. Real Telegram API calls will fail."
        )

    # 3. Validate Database URL
    if not settings.DATABASE_URL:
        raise StartupValidationError("DATABASE_URL is not specified in configuration.")

    if not settings.DATABASE_URL.startswith(("postgresql+asyncpg://", "sqlite+aiosqlite://")):
        logger.warning(
            f"DATABASE_URL protocol may not support AsyncIO ORM: {settings.DATABASE_URL}"
        )

    # 4. Validate Webhook Config
    if settings.WEBHOOK_URL and not settings.WEBHOOK_URL.startswith(("https://", "http://")):
        raise StartupValidationError(
            f"Invalid WEBHOOK_URL scheme: '{settings.WEBHOOK_URL}'. Must start with http:// or https://"
        )

    # 5. Validate Secrets
    if len(settings.SECRET_KEY) < 16:
        logger.warning(
            "SECRET_KEY length is less than 16 characters. Consider using a stronger key."
        )

    # 6. Validate Languages
    if settings.DEFAULT_LANGUAGE not in settings.SUPPORTED_LANGUAGES:
        raise StartupValidationError(
            f"DEFAULT_LANGUAGE '{settings.DEFAULT_LANGUAGE}' is not in SUPPORTED_LANGUAGES {settings.SUPPORTED_LANGUAGES}"
        )

    # 7. Database Connectivity Check
    try:
        from sqlalchemy import text

        from app.database.session import get_db_session

        async with get_db_session() as session:
            await session.execute(text("SELECT 1"))
        logger.info("Database connectivity check passed.")
    except Exception as e:
        logger.error(
            f"Database connection error: {e}. Please check your DATABASE_URL in .env file."
        )

    logger.info("Startup validation completed successfully. All critical checks passed.")
    return True
