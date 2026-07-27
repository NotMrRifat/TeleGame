"""Start and General platform command handlers with detailed step-by-step guidance."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.i18n.engine import i18n
from app.models.domain import UserModel
from app.utils.keyboards import get_main_menu_keyboard

router = Router(name="start_router")


@router.message(Command("start", "menu"))
async def cmd_start(message: Message, db_user: UserModel) -> None:
    """Handles /start and /menu commands with step-by-step instructions."""
    lang = db_user.language_code
    text = f"{i18n.get('welcome', lang)}\n\n{i18n.get('main_menu', lang)}"
    kb = get_main_menu_keyboard(lang)
    await message.reply(text, reply_markup=kb, parse_mode="Markdown")


@router.message(Command("help"))
async def cmd_help(message: Message, db_user: UserModel) -> None:
    """Handles /help command with detailed guides for all feature areas."""
    lang = db_user.language_code
    help_text = (
        f"{i18n.get('how_to_play_title', lang)}\n\n"
        f"{i18n.get('how_to_play_steps', lang)}\n\n"
        "━━━━━━━ 🛠 *Command Categories* ━━━━━━━\n\n"
        "🎮 *Game Commands:*\n"
        "• `/games` — Browse all 10 playable game plugins\n"
        "• `/newgame <name>` — Create a game lobby in a group\n"
        "• `/join` — Join the waiting lobby\n"
        "• `/leave` — Leave the lobby before start\n"
        "• `/startgame` — Host force-starts match\n"
        "• `/endgame` — Cancel current game session\n\n"
        "👤 *Player & Social:*\n"
        "• `/profile` — View stats, XP, level, and items\n"
        "• `/daily` — Claim daily coin streak rewards\n"
        "• `/leaderboard` — View global top rankings\n"
        "• `/clan` — Clan creation & management\n"
        "• `/language` — Switch language (en/bn)\n\n"
        "Need further assistance? Use `/support` to contact our team!"
    )
    await message.reply(help_text, parse_mode="Markdown")


@router.message(Command("about", "rules"))
async def cmd_about(message: Message) -> None:
    """Handles /about and /rules command."""
    about_text = (
        "ℹ️ *About TeleGame Platform*\n\n"
        "TeleGame is a serverless, plugin-based Telegram multiplayer gaming platform.\n\n"
        "📜 *Fair Play Rules:*\n"
        "1. No spamming or macro botting.\n"
        "2. Play turns within turn timeout limits.\n"
        "3. Respect group members during multiplayer games.\n\n"
        "Version: `1.0.0` | Built with Aiogram 3 & Python 3.13"
    )
    await message.reply(about_text, parse_mode="Markdown")


@router.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    """Handles /ping health check."""
    await message.reply("🏓 *Pong!* Platform operational & database ready.", parse_mode="Markdown")
