"""User Auto-Sync Middleware for Aiogram 3."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.domain_repos import UserRepository


class UserSyncMiddleware(BaseMiddleware):
    """Automatically registers or updates Telegram user profile in PostgreSQL."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event_user: User = data.get("event_from_user")
        db_session: AsyncSession = data.get("db_session")

        if event_user and db_session:
            user_repo = UserRepository(db_session)
            raw_lang = event_user.language_code or "bn"
            lang = raw_lang.split("-")[0].lower() if raw_lang else "bn"
            if lang not in ["en", "bn"]:
                lang = "bn"
            first_name = event_user.first_name or "Player"
            db_user = await user_repo.get_or_create(
                telegram_id=event_user.id,
                first_name=first_name,
                username=event_user.username,
                language_code=lang,
            )
            data["db_user"] = db_user

        return await handler(event, data)
