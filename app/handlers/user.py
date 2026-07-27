"""User profile, statistics, and settings handlers."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import UserModel

router = Router(name="user_router")


@router.message(Command("profile", "stats", "rank"))
async def cmd_profile(message: Message, db_user: UserModel) -> None:
    """Handles /profile, /stats, and /rank commands with detailed stat breakdown."""
    total_matches = db_user.games_played or 1
    win_rate = (db_user.wins / total_matches) * 100

    profile_text = (
        f"👤 *Player Profile & Telemetry*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• *Name:* {db_user.first_name}\n"
        f"• *Title:* `{db_user.title}`\n"
        f"• *Level:* {db_user.level} (XP: {db_user.xp})\n"
        f"• *Coins:* 💰 {db_user.coins}\n\n"
        f"📊 *Game Statistics:*\n"
        f"• *Wins:* 🏆 {db_user.wins}\n"
        f"• *Losses:* ❌ {db_user.losses}\n"
        f"• *Draws:* 🤝 {db_user.draws}\n"
        f"• *Total Matches:* 🎮 {db_user.games_played}\n"
        f"• *Win Rate:* 📈 {win_rate:.1f}%\n"
        f"• *Daily Streak:* 🔥 {db_user.daily_streak} Days\n\n"
        f"💡 *Tip:* Use `/shop` to purchase new titles and frames using your coins!"
    )
    await message.reply(profile_text, parse_mode="Markdown")


@router.message(Command("language"))
async def cmd_language(message: Message, db_user: UserModel, db_session: AsyncSession) -> None:
    """Handles /language command to toggle between English and Bangla."""
    new_lang = "en" if db_user.language_code == "bn" else "bn"
    db_user.language_code = new_lang
    await db_session.flush()

    if new_lang == "bn":
        msg = "🌐 *ভাষা সফলভাবে বাংলায় পরিবর্তন করা হয়েছে!*"
    else:
        msg = "🌐 *Language successfully updated to English!*"

    await message.reply(msg, parse_mode="Markdown")
