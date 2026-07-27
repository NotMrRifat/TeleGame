"""Game Lobby & Session control handlers with step-by-step instructions."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.engine.plugin_manager import plugin_manager
from app.core.engine.session_manager import ActiveSessionConflictError, SessionManager
from app.utils.keyboards import get_games_selection_keyboard

router = Router(name="game_lobby_router")


@router.message(Command("games"))
async def cmd_games(message: Message) -> None:
    """Handles /games command displaying list and step-by-step start guide."""
    games_text = (
        "🎮 *TeleGame Available Game Plugins*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ ❌⭕ `tic_tac_toe` — Classic 3x3 strategy\n"
        "2️⃣ ✊✌✋ `rock_paper_scissors` — Quick gesture match\n"
        "3️⃣ 🔴🟡 `connect_four` — 4-in-a-row drop discs\n"
        "4️⃣ 🔤 `hangman` — Guess the hidden word\n"
        "5️⃣ 📝 `word_chain` — Letter chain word match\n"
        "6️⃣ 🧠 `trivia` — Real-time quiz battle\n"
        "7️⃣ 🕵️ `mafia` — Multi-role social deduction\n"
        "8️⃣ 🎴 `uno` — Color/number matching cards\n"
        "9️⃣ ♟️ `chess` — Grand strategy chess\n"
        "🔟 🎲 `ludo` — Dice rolling board game\n\n"
        "📖 *How to start in this group:*\n"
        "Type `/newgame <slug>` (e.g. `/newgame tic_tac_toe`)"
    )
    kb = get_games_selection_keyboard()
    await message.reply(games_text, reply_markup=kb, parse_mode="Markdown")


@router.message(Command("newgame"))
async def cmd_newgame(message: Message, db_session: AsyncSession) -> None:
    """Handles /newgame command to start a session in group with step-by-step guide."""
    if message.chat.type in ["private"]:
        await message.reply(
            "⚠️ *Games must be played in a Telegram Group!*\n\n"
            "Add @TeleGameMasterBot to a group chat and type `/newgame` to play with friends.",
            parse_mode="Markdown",
        )
        return

    args = message.text.split()
    game_slug = args[1] if len(args) > 1 else "tic_tac_toe"

    if game_slug not in plugin_manager.list_available_games():
        await message.reply(
            f"❌ Game plugin `{game_slug}` not found. Type `/games` to view available games.",
            parse_mode="Markdown",
        )
        return

    session_mgr = SessionManager(db_session)
    try:
        await session_mgr.create_game_session(
            telegram_chat_id=message.chat.id,
            title=message.chat.title or "Group Game",
            game_slug=game_slug,
            host_telegram_id=message.from_user.id,
            host_username=message.from_user.username,
        )
        await message.reply(
            f"🎮 *{game_slug.replace('_', ' ').title()} Lobby Initialized!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 *Host:* {message.from_user.first_name}\n"
            f"📌 *Status:* Waiting for players to join...\n\n"
            f"📍 *Next Steps for Players:*\n"
            f"1️⃣ Group members type `/join` to enter the game.\n"
            f"2️⃣ Host types `/startgame` when ready to begin!\n"
            f"3️⃣ Type `/cancel` to abort the lobby.",
            parse_mode="Markdown",
        )
    except ActiveSessionConflictError:
        await message.reply(
            "⚠️ *Active Session Already Running!*\n\n"
            "An active game is currently running in this group. Finish the match or type `/cancel` to force end it.",
            parse_mode="Markdown",
        )


@router.message(Command("join"))
async def cmd_join(message: Message, db_session: AsyncSession) -> None:
    """Handles /join command for entering open game lobby."""
    session_mgr = SessionManager(db_session)
    active_session = await session_mgr.get_active_session(message.chat.id)

    if not active_session or active_session.status != "LOBBY":
        await message.reply(
            "ℹ️ No open game lobby found. Type `/newgame` to create one!", parse_mode="Markdown"
        )
        return

    session_rec, game_inst = await session_mgr.load_game_instance(active_session.id)
    joined = game_inst.join(message.from_user.id)

    if not joined:
        await message.reply(
            "⚠️ You are already in this lobby, or the lobby is full!", parse_mode="Markdown"
        )
        return

    await session_mgr.save_game_instance(session_rec, game_inst)
    player_count = len(game_inst.players)

    await message.reply(
        f"✅ *{message.from_user.first_name} joined the lobby!*\n\n"
        f"👥 Total Players: `{player_count}/{game_inst.max_players}`\n"
        f"Host type `/startgame` when ready!",
        parse_mode="Markdown",
    )


@router.message(Command("cancel", "endgame", "forfeit"))
async def cmd_cancel(message: Message, db_session: AsyncSession) -> None:
    """Handles cancelling or forfeiting active group match."""
    session_mgr = SessionManager(db_session)
    active_session = await session_mgr.get_active_session(message.chat.id)

    if not active_session:
        await message.reply("ℹ️ No active session to cancel.", parse_mode="Markdown")
        return

    active_session.status = "CANCELLED"
    await db_session.flush()
    await message.reply(
        "🛑 *Game session has been cancelled.* You can now start a new game with `/newgame`!",
        parse_mode="Markdown",
    )
