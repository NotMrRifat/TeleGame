"""Security & Anti-Spam Middleware for Aiogram 3."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.services.security_service import RateLimitExceededError, security_service


class SecurityMiddleware(BaseMiddleware):
    """Enforces rate limiting and anti-duplicate callback protection."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = None
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id
            if security_service.is_duplicate_callback(event.id):
                await event.answer("Duplicate request ignored.", show_alert=False)
                return None

        if user_id:
            try:
                security_service.validate_rate_limit(user_id)
            except RateLimitExceededError as err:
                if isinstance(event, Message):
                    await event.reply(str(err))
                elif isinstance(event, CallbackQuery):
                    await event.answer(str(err), show_alert=True)
                return None

        return await handler(event, data)
