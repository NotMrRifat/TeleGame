"""Asynchronous Event Bus for loose module coupling."""

import asyncio
from collections.abc import Callable, Coroutine
from typing import Any

from pydantic import BaseModel

from app.config.logging import logger


class PlatformEvent(BaseModel):
    """Base event payload structure."""

    event_name: str
    payload: dict[str, Any] = {}


EventHandler = Callable[[PlatformEvent], Coroutine[Any, Any, None]]


class EventDispatcher:
    """Decoupled Async Event Dispatcher."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Register listener callback for specific event."""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(handler)

    async def dispatch(self, event_name: str, payload: dict[str, Any]) -> None:
        """Emits event to all registered listeners asynchronously."""
        event = PlatformEvent(event_name=event_name, payload=payload)
        handlers = self._listeners.get(event_name, [])

        if not handlers:
            return

        logger.debug(f"Dispatching event '{event_name}' to {len(handlers)} handler(s)")
        tasks = [asyncio.create_task(handler(event)) for handler in handlers]
        await asyncio.gather(*tasks, return_exceptions=True)


event_dispatcher = EventDispatcher()
