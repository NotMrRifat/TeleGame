"""Inventory & Cosmetics Service for equipping avatars, frames, titles, and themes."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.repositories.domain_repos import UserRepository


class InventoryService:
    """Manages player cosmetics inventory and equipped titles/frames/themes."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)

    async def equip_item(self, telegram_id: int, item_type: str, item_slug: str) -> bool:
        """Equip cosmetic item for player."""
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False

        if item_type == "title":
            user.title = item_slug
        elif item_type == "frame":
            user.frame = item_slug
        elif item_type == "theme":
            user.theme = item_slug
        elif item_type == "avatar":
            user.avatar = item_slug
        else:
            return False

        await self.db_session.flush()
        logger.info(f"User {telegram_id} equipped {item_type} '{item_slug}'")
        return True
