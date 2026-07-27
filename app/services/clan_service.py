"""Clan Service managing user clans, rankings, and vault resources."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.models.domain import ClanModel
from app.repositories.domain_repos import UserRepository


class ClanService:
    """Manages creation, membership, and ranking of multiplayer clans."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)

    async def create_clan(self, owner_id: int, name: str, tag: str) -> ClanModel | None:
        """Create new clan with owner as leader."""
        user = await self.user_repo.get_by_telegram_id(owner_id)
        if not user or user.clan_id is not None:
            return None

        clan = ClanModel(
            name=name,
            tag=tag.upper(),
            owner_telegram_id=owner_id,
            total_xp=user.xp,
        )
        self.db_session.add(clan)
        await self.db_session.flush()

        user.clan_id = clan.id
        await self.db_session.flush()
        logger.info(f"Created clan '{name}' [{tag}] by User {owner_id}")
        return clan
