"""Lazy Timer Architecture for serverless-safe turn and session timeout evaluation."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.config.settings import settings
from app.core.engine.base_game import GameMoveResult
from app.core.engine.plugin_manager import plugin_manager
from app.models.domain import SessionModel


class LazyTimerEngine:
    """Evaluates timeouts lazily on inbound requests or cron invocation."""

    @staticmethod
    def calculate_turn_expiration(seconds: int | None = None) -> datetime:
        """Returns future expiration timestamp for active turn."""
        timeout_sec = seconds or settings.TURN_TIMEOUT
        return datetime.now(UTC).replace(microsecond=0) + datetime.timedelta(seconds=timeout_sec)

    @staticmethod
    def is_session_expired(session: SessionModel) -> bool:
        """Checks if session expiration timestamp has elapsed."""
        if not session.expires_at:
            return False
        return datetime.now(UTC) >= session.expires_at

    @classmethod
    async def evaluate_and_handle_timeout(
        self, session: SessionModel, db_session: AsyncSession
    ) -> tuple[bool, GameMoveResult | None]:
        """Evaluates whether session has expired and processes timeout logic if needed.

        Returns:
            Tuple[bool, Optional[GameMoveResult]]: (has_expired, timeout_result)
        """
        if not self.is_session_expired(session) or session.status not in ["LOBBY", "PLAYING"]:
            return False, None

        logger.info(f"Session '{session.id}' timed out lazily.")
        game_cls = plugin_manager.get_game_class(session.game_slug)
        game_inst = game_cls()
        game_inst.deserialize(session.state_data or {})

        timeout_result = game_inst.timeout()
        session.state_data = game_inst.serialize()

        if timeout_result.is_game_over:
            session.status = "TIMEOUT"
            session.winner_user_id = timeout_result.winner_user_id

        await db_session.flush()
        return True, timeout_result


async def cleanup_expired_sessions(db_session: AsyncSession) -> int:
    """Cron cleanup function to forfeit expired sessions without long-running VPS tasks."""
    now = datetime.now(UTC)
    stmt = select(SessionModel).where(
        SessionModel.status.in_(["LOBBY", "PLAYING"]),
        SessionModel.expires_at <= now,
        SessionModel.is_deleted.is_(False),
    )
    res = await db_session.execute(stmt)
    expired_sessions = list(res.scalars().all())

    count = 0
    for sess in expired_sessions:
        await LazyTimerEngine.evaluate_and_handle_timeout(sess, db_session)
        count += 1

    await db_session.commit()
    logger.info(f"Lazy timer cleanup evaluated {count} expired session(s).")
    return count
