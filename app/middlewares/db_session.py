"""Database Session Middleware for Aiogram 3."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database.session import AsyncSessionLocal


class DbSessionMiddleware(BaseMiddleware):
    """Injects transactional AsyncSession into handler data dictionary."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["db_session"] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception as err:
                await session.rollback()
                raise err
