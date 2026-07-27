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


def setup_routers() -> Router:
    """Combines all feature routers into main router."""
    main_router = Router(name="main_router")
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
        r._parent_router = None
        main_router.include_router(r)
    return main_router
