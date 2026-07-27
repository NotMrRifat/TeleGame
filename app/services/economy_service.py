"""Economy Service managing virtual coins, daily claims, and balance adjustments."""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.repositories.domain_repos import UserRepository


class InsufficientCoinsError(Exception):
    """Raised when user balance is lower than transaction cost."""

    pass


class EconomyService:
    """Manages virtual economy transactions and daily streaks."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)

    async def add_coins(self, telegram_id: int, amount: int, reason: str = "REWARD") -> int:
        """Add coins to user account and return new balance."""
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise ValueError(f"User {telegram_id} not found.")

        user.coins += amount
        await self.db_session.flush()
        logger.info(
            f"Added {amount} coins to User {telegram_id} (Reason: {reason}). New balance: {user.coins}"
        )
        return user.coins

    async def deduct_coins(self, telegram_id: int, amount: int, reason: str = "PURCHASE") -> int:
        """Deduct coins from user balance.

        Raises:
            InsufficientCoinsError: If user balance is insufficient.
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise ValueError(f"User {telegram_id} not found.")

        if user.coins < amount:
            raise InsufficientCoinsError(
                f"Required {amount} coins, but user only has {user.coins}."
            )

        user.coins -= amount
        await self.db_session.flush()
        logger.info(
            f"Deducted {amount} coins from User {telegram_id} (Reason: {reason}). New balance: {user.coins}"
        )
        return user.coins

    async def claim_daily_reward(self, telegram_id: int) -> tuple[bool, int, str]:
        """Claim daily streak reward.

        Returns:
            Tuple[bool, int, str]: (claimed_success, reward_amount, message)
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise ValueError(f"User {telegram_id} not found.")

        now = datetime.now(UTC)
        if user.last_daily_claim:
            delta = now - user.last_daily_claim
            if delta.total_seconds() < 86400:  # Less than 24h
                return False, 0, "already_claimed"

            if delta.total_seconds() > 172800:  # More than 48h -> streak breaks
                user.daily_streak = 1
            else:
                user.daily_streak += 1
        else:
            user.daily_streak = 1

        reward_coins = 100 + (user.daily_streak * 10)
        user.coins += reward_coins
        user.last_daily_claim = now
        await self.db_session.flush()

        return True, reward_coins, "daily_claimed"
