"""Admin and moderation commands router."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.models.domain import UserModel
from app.services.security_service import security_service

router = Router(name="admin_router")


@router.message(Command("admin", "dashboard"))
async def cmd_admin_dashboard(message: Message, db_user: UserModel) -> None:
    """Handles /admin dashboard command."""
    if not security_service.is_admin(message.from_user.id, db_user.role):
        await message.reply("🚫 Access Denied: Admin privileges required.", parse_mode="Markdown")
        return

    dashboard_text = (
        "🛠 *TeleGame Admin Dashboard*\n\n"
        "• /endgame <session_id> - Force end game\n"
        "• /givecoins <user_id> <amount> - Add coins\n"
        "• /setrole <user_id> <role> - Assign role\n"
        "• /broadcast <message> - System broadcast\n"
    )
    await message.reply(dashboard_text, parse_mode="Markdown")
