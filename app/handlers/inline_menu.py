"""Inline Main Menu callback query router."""

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.i18n.engine import i18n
from app.models.domain import UserModel
from app.utils.keyboards import get_games_selection_keyboard, get_main_menu_keyboard

router = Router(name="inline_menu_router")


@router.callback_query(F.data == "menu_main")
async def cb_main_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Returns to main menu."""
    lang = db_user.language_code
    text = f"{i18n.get('welcome', lang)}\n\n{i18n.get('main_menu', lang)}"
    kb = get_main_menu_keyboard(lang)
    await query.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_games")
async def cb_games_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Opens games selection menu."""
    kb = get_games_selection_keyboard()
    await query.message.edit_text(
        "🎮 *Choose a Game to Play:*", reply_markup=kb, parse_mode="Markdown"
    )
    await query.answer()


@router.callback_query(F.data == "menu_profile")
async def cb_profile_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views profile via inline button."""
    text = (
        f"👤 *Player Profile*\n\n"
        f"Name: {db_user.first_name}\n"
        f"Title: `{db_user.title}`\n"
        f"Level: {db_user.level} (XP: {db_user.xp})\n"
        f"Coins: 💰 {db_user.coins}\n"
        f"Wins: 🏆 {db_user.wins} | Losses: ❌ {db_user.losses}\n"
        f"Daily Streak: 🔥 {db_user.daily_streak} Days\n"
    )
    await query.message.edit_text(
        text, reply_markup=get_main_menu_keyboard(db_user.language_code), parse_mode="Markdown"
    )
    await query.answer()
