"""Handlers package initialization combining all router modules."""

from aiogram import Router

from app.handlers import (
    admin,
    clan,
    economy,
    game_lobby,
    gameplay,
    inline_menu,
    leaderboard,
    start,
    user,
)

_main_router: Router | None = None


def setup_routers() -> Router:
    """Combines all feature routers into main router singleton."""
    global _main_router
    if _main_router is not None:
        return _main_router

    _main_router = Router(name="main_router")
    sub_routers = [
        start.router,
        inline_menu.router,
        user.router,
        game_lobby.router,
        gameplay.router,
        economy.router,
        leaderboard.router,
        clan.router,
        admin.router,
    ]
    for r in sub_routers:
        _main_router.include_router(r)
    return _main_router
