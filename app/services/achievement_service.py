"""Achievement Service for event-driven achievement tracking and rewards."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.models.domain import AchievementModel, UserAchievementModel
from app.repositories.domain_repos import UserRepository


class AchievementService:
    """Tracks player progress toward unlockable achievements."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)

    async def check_and_unlock(
        self, telegram_id: int, achievement_slug: str
    ) -> AchievementModel | None:
        """Unlocks achievement for user if criteria are met."""
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return None

        # Fetch achievement definition
        stmt_ach = select(AchievementModel).where(AchievementModel.slug == achievement_slug)
        res_ach = await self.db_session.execute(stmt_ach)
        ach = res_ach.scalar_one_or_none()
        if not ach:
            return None

        # Check existing user achievement status
        stmt_ua = select(UserAchievementModel).where(
            UserAchievementModel.user_id == user.id,
            UserAchievementModel.achievement_slug == achievement_slug,
        )
        res_ua = await self.db_session.execute(stmt_ua)
        user_ach = res_ua.scalar_one_or_none()

        if not user_ach:
            user_ach = UserAchievementModel(
                user_id=user.id,
                achievement_slug=achievement_slug,
                progress=1,
                is_unlocked=True,
                unlocked_at=datetime.now(UTC),
            )
            self.db_session.add(user_ach)
            user.coins += ach.reward_coins
            user.xp += ach.reward_xp
            await self.db_session.flush()
            logger.info(f"Unlocked achievement '{achievement_slug}' for user {telegram_id}")
            return ach

        return None
