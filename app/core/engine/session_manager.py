"""Session Manager for managing active group sessions, locking, and conflict prevention."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.core.engine.base_game import BaseGame
from app.core.engine.plugin_manager import plugin_manager
from app.models.domain import GroupModel, PlayerSessionModel, SessionModel
from app.repositories.domain_repos import GroupRepository, SessionRepository


class ActiveSessionConflictError(Exception):
    """Exception raised when attempting to start a second game session in a group."""

    pass


class SessionManager:
    """Manages group game sessions, state isolation, locking, and recovery."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.session_repo = SessionRepository(db_session)
        self.group_repo = GroupRepository(db_session)

    async def get_or_create_group(self, telegram_chat_id: int, title: str) -> GroupModel:
        """Fetch or register Telegram group."""
        return await self.group_repo.get_or_create(telegram_chat_id, title)

    async def get_active_session(self, telegram_chat_id: int) -> SessionModel | None:
        """Fetch active non-finished session for a group if any."""
        group = await self.group_repo.get_by_telegram_chat_id(telegram_chat_id)
        if not group:
            return None
        return await self.session_repo.get_active_session_by_group(group.id)

    async def create_game_session(
        self,
        telegram_chat_id: int,
        title: str,
        game_slug: str,
        host_telegram_id: int,
        host_username: str | None,
    ) -> SessionModel:
        """Creates a new game lobby for a group if no active game exists.

        Raises:
            ActiveSessionConflictError: If a session is already active.
        """
        group = await self.get_or_create_group(telegram_chat_id, title)

        active = await self.session_repo.get_active_session_by_group(group.id)
        if active:
            raise ActiveSessionConflictError("An active game session already exists in this group.")

        # Instantiate Game plugin to get initial state
        game_cls = plugin_manager.get_game_class(game_slug)
        game_inst = game_cls()

        session = await self.session_repo.create(
            group_id=group.id,
            game_slug=game_slug,
            status="LOBBY",
            current_turn_user_id=host_telegram_id,
            state_data=game_inst.serialize(),
        )

        # Add host as first player
        host_player = PlayerSessionModel(
            session_id=session.id,
            telegram_id=host_telegram_id,
            username=host_username,
            role="host",
            score=0,
            is_active=True,
        )
        self.db_session.add(host_player)
        await self.db_session.flush()

        logger.info(f"Created new '{game_slug}' session ({session.id}) in chat {telegram_chat_id}")
        return session

    async def load_game_instance(self, session_id: uuid.UUID) -> tuple[SessionModel, BaseGame]:
        """Load session record and construct initialized BaseGame instance."""
        session_record = await self.session_repo.get_by_id(session_id)
        if not session_record:
            raise ValueError(f"Session '{session_id}' not found.")

        game_cls = plugin_manager.get_game_class(session_record.game_slug)
        game_inst = game_cls()
        game_inst.deserialize(session_record.state_data or {})
        return session_record, game_inst

    async def save_game_instance(self, session_record: SessionModel, game_inst: BaseGame) -> None:
        """Persist updated game instance state data to PostgreSQL."""
        session_record.state_data = game_inst.serialize()
        await self.db_session.flush()
