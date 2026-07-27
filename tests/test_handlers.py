"""Unit tests for Aiogram Routers and Command registration."""

from app.handlers import setup_routers
from app.utils.keyboards import get_games_selection_keyboard, get_main_menu_keyboard


def test_router_setup():
    """Verify setup_routers includes all feature routers."""
    main_router = setup_routers()
    assert main_router is not None
    assert len(main_router.sub_routers) >= 8


def test_keyboard_generation():
    """Verify main menu and game selection keyboards generate valid InlineKeyboardMarkup."""
    kb_main = get_main_menu_keyboard("en")
    assert len(kb_main.inline_keyboard) >= 5

    kb_games = get_games_selection_keyboard()
    assert len(kb_games.inline_keyboard) >= 5
