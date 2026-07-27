"""Clan commands handler."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import UserModel
from app.services.clan_service import ClanService

router = Router(name="clan_router")


@router.message(Command("clan"))
async def cmd_clan(message: Message, db_user: UserModel, db_session: AsyncSession) -> None:
    """Handles /clan command with step-by-step clan guide."""
    args = message.text.split()

    if len(args) > 3 and args[1].lower() == "create":
        name = args[2]
        tag = args[3]
        clan_service = ClanService(db_session)
        clan = await clan_service.create_clan(message.from_user.id, name, tag)
        if clan:
            await message.reply(
                f"⚔ *Clan '{name}' [{tag}] Created!* You are now the Clan Leader.",
                parse_mode="Markdown",
            )
        else:
            await message.reply(
                "⚠️ Could not create clan. You may already belong to a clan.", parse_mode="Markdown"
            )
        return

    clan_text = (
        "⚔ *TeleGame Clan System*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Clans allow players to team up, pool XP, and compete in Clan Wars!\n\n"
        "📖 *How to Create a Clan:*\n"
        "Type `/clan create <name> <tag>` (e.g. `/clan create CyberKnights CKN`)\n\n"
        "💡 Members of a clan share XP bonuses during multiplayer matches!"
    )
    await message.reply(clan_text, parse_mode="Markdown")
