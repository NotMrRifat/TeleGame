"""Analytics & Telemetry Service."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.models.domain import AnalyticsLogModel


class AnalyticsService:
    """Tracks platform event telemetry and analytics."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def log_event(
        self, event_name: str, telegram_id: int | None = None, payload: dict[str, Any] | None = None
    ) -> None:
        """Log event telemetry to analytics_logs table."""
        entry = AnalyticsLogModel(
            event_name=event_name,
            telegram_id=telegram_id,
            payload=payload or {},
        )
        self.db_session.add(entry)
        await self.db_session.flush()
        logger.debug(f"Logged analytics event: {event_name}")
