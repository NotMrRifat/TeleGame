"""Domain-specific repositories for TeleGame models."""

import uuid

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.domain import (
    GameModel,
    GroupModel,
    RatingModel,
    SessionModel,
    UserModel,
)
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """User data access repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)

    async def get_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        """Get user profile by Telegram User ID."""
        stmt = select(UserModel).where(
            UserModel.telegram_id == telegram_id,
            UserModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_or_create(
        self,
        telegram_id: int,
        first_name: str,
        username: str | None = None,
        language_code: str = "bn",
    ) -> UserModel:
        """Fetch existing user or create a new user profile upon interaction."""
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.create(
                telegram_id=telegram_id,
                first_name=first_name,
                username=username,
                language_code=language_code,
            )
        else:
            # Sync dynamic telegram user fields if changed
            if user.first_name != first_name or user.username != username:
                user.first_name = first_name
                user.username = username
                await self.session.flush()
        return user


class GroupRepository(BaseRepository[GroupModel]):
    """Telegram Group data access repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(GroupModel, session)

    async def get_by_telegram_chat_id(self, chat_id: int) -> GroupModel | None:
        """Fetch group profile by Telegram Chat ID."""
        stmt = select(GroupModel).where(
            GroupModel.telegram_chat_id == chat_id,
            GroupModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_or_create(
        self, chat_id: int, title: str, chat_type: str = "supergroup"
    ) -> GroupModel:
        """Fetch existing group or initialize group profile."""
        group = await self.get_by_telegram_chat_id(chat_id)
        if not group:
            group = await self.create(
                telegram_chat_id=chat_id,
                title=title,
                type=chat_type,
            )
        return group


class SessionRepository(BaseRepository[SessionModel]):
    """Game Session data access repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(SessionModel, session)

    async def get_active_session_by_group(self, group_id: uuid.UUID) -> SessionModel | None:
        """Fetch current non-finished active game session for a group."""
        stmt = (
            select(SessionModel)
            .where(
                SessionModel.group_id == group_id,
                SessionModel.status.in_(["LOBBY", "PLAYING", "PAUSED"]),
                SessionModel.is_deleted.is_(False),
            )
            .options(selectinload(SessionModel.players))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()


class GameRepository(BaseRepository[GameModel]):
    """Game Plugin data access repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(GameModel, session)

    async def get_by_slug(self, slug: str) -> GameModel | None:
        """Fetch registered game by slug."""
        stmt = select(GameModel).where(
            GameModel.slug == slug,
            GameModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()


class RatingRepository(BaseRepository[RatingModel]):
    """Elo Rating repository."""

    def __init__(self, session: AsyncSession):
        super().__init__(RatingModel, session)

    async def get_user_rating(self, user_id: uuid.UUID, game_slug: str) -> RatingModel | None:
        """Fetch user rating for a specific game."""
        stmt = select(RatingModel).where(
            RatingModel.user_id == user_id,
            RatingModel.game_slug == game_slug,
            RatingModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_global_leaderboard(self, game_slug: str, limit: int = 10) -> list[RatingModel]:
        """Fetch top ratings for leaderboard display."""
        stmt = (
            select(RatingModel)
            .where(
                RatingModel.game_slug == game_slug,
                RatingModel.is_deleted.is_(False),
            )
            .order_by(desc(RatingModel.elo))
            .limit(limit)
            .options(selectinload(RatingModel.user))
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
