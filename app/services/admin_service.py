"""Admin Service handling platform administrative actions."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.repositories.domain_repos import SessionRepository, UserRepository


class AdminService:
    """Manages administrative operations including moderation, roles, and force-ending sessions."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)
        self.session_repo = SessionRepository(db_session)

    async def set_user_role(self, telegram_id: int, new_role: str) -> bool:
        """Assign role to target user."""
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False
        user.role = new_role
        await self.db_session.flush()
        logger.info(f"Assigned role '{new_role}' to User {telegram_id}")
        return True

    async def force_end_session(
        self, session_id: uuid.UUID, reason: str = "ADMIN_FORCE_END"
    ) -> bool:
        """Force end an active game session."""
        session = await self.session_repo.get_by_id(session_id)
        if not session or session.status in ["FINISHED", "CANCELLED"]:
            return False

        session.status = "CANCELLED"
        await self.db_session.flush()
        logger.info(f"Force-ended session '{session_id}' (Reason: {reason})")
        return True
