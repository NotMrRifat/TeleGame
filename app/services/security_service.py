"""Security Service handling flood protection, rate limiting, and permission validation."""

import time

from app.config.logging import logger
from app.config.settings import settings


class RateLimitExceededError(Exception):
    """Exception raised when a user exceeds rate limit threshold."""

    pass


class SecurityService:
    """Security manager enforcing anti-spam, duplicate callback protection, and permission validation."""

    def __init__(self) -> None:
        self._last_user_activity: dict[int, float] = {}
        self._processed_callbacks: dict[str, float] = {}

    def validate_rate_limit(self, telegram_id: int) -> bool:
        """Enforces rate limit per user.

        Raises:
            RateLimitExceededError: If requests are sent too rapidly.
        """
        now = time.time()
        last_time = self._last_user_activity.get(telegram_id, 0)
        cooldown = settings.RATE_LIMIT_SECONDS

        if now - last_time < cooldown:
            logger.warning(f"Rate limit triggered by Telegram ID {telegram_id}")
            raise RateLimitExceededError("You are sending requests too quickly! Please slow down.")

        self._last_user_activity[telegram_id] = now
        return True

    def is_duplicate_callback(self, callback_id: str) -> bool:
        """Prevents replay attacks by checking duplicate callback query IDs."""
        now = time.time()
        # Clean expired callback entries (older than 60s)
        self._processed_callbacks = {
            k: v for k, v in self._processed_callbacks.items() if now - v < 60
        }

        if callback_id in self._processed_callbacks:
            return True

        self._processed_callbacks[callback_id] = now
        return False

    @staticmethod
    def is_admin(telegram_id: int, user_role: str = "player") -> bool:
        """Checks if a user is an Admin or Owner."""
        if (
            telegram_id in settings.ADMIN_IDS
            or telegram_id in settings.SUPER_ADMIN_IDS
            or telegram_id == settings.OWNER_ID
        ):
            return True
        return user_role in ["admin", "superadmin", "owner"]

    @staticmethod
    def is_owner(telegram_id: int, user_role: str = "player") -> bool:
        """Checks if a user is the Owner."""
        if telegram_id == settings.OWNER_ID or telegram_id in settings.SUPER_ADMIN_IDS:
            return True
        return user_role == "owner"


security_service = SecurityService()
