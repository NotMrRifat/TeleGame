"""Economy, shop, inventory, and quest handlers."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import UserModel
from app.services.economy_service import EconomyService

router = Router(name="economy_router")


@router.message(Command("daily"))
async def cmd_daily(message: Message, db_user: UserModel, db_session: AsyncSession) -> None:
    """Handles /daily reward claim with step-by-step streak guide."""
    economy = EconomyService(db_session)
    success, amount, msg_key = await economy.claim_daily_reward(message.from_user.id)

    if success:
        reward_msg = (
            f"🎁 *Daily Login Reward Claimed!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔥 *Daily Streak:* {db_user.daily_streak} Days\n"
            f"💰 *Coins Earned:* +{amount} Coins\n"
            f"💳 *New Balance:* 💰 {db_user.coins} Coins\n\n"
            f"💡 *Tip:* Maintain your login streak daily to earn exponentially higher rewards!"
        )
    else:
        reward_msg = (
            f"⚠️ *Daily Reward Already Claimed Today!*\n\n"
            f"🔥 Current Streak: `{db_user.daily_streak}` Days\n"
            f"Please return tomorrow to claim your next reward boost!"
        )
    await message.reply(reward_msg, parse_mode="Markdown")


@router.message(Command("shop", "inventory"))
async def cmd_shop(message: Message, db_user: UserModel) -> None:
    """Handles /shop and /inventory commands with item list."""
    shop_text = (
        f"🛒 *TeleGame Cosmetic Shop & Inventory*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *Your Coins:* {db_user.coins}\n"
        f"🏷 *Equipped Title:* `{db_user.title}`\n"
        f"🖼 *Equipped Frame:* `{db_user.frame}`\n\n"
        f"🌟 *Available Items to Unlock:*\n"
        f"1️⃣ Title: `Mastermind` — 💰 500 Coins\n"
        f"2️⃣ Title: `Grandmaster` — 💰 1,500 Coins\n"
        f"3️⃣ Frame: `Gold Neon` — 💰 1,000 Coins\n"
        f"4️⃣ Theme: `Dark Cyberpunk` — 💰 2,000 Coins\n\n"
        f"💡 Win matches and claim `/daily` rewards to earn coins!"
    )
    await message.reply(shop_text, parse_mode="Markdown")


@router.message(Command("quests"))
async def cmd_quests(message: Message, db_user: UserModel) -> None:
    """Handles /quests command displaying daily and weekly objectives."""
    quests_text = (
        "🎯 *Active Quests & Objectives*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ *Daily Gamer* (Play 3 matches)\n"
        "   • Progress: [████░░░░░░] (1/3)\n"
        "   • Reward: 💰 150 Coins | ⚡ 200 XP\n\n"
        "2️⃣ *Daily Champion* (Win 1 match)\n"
        "   • Progress: [░░░░░░░░░░] (0/1)\n"
        "   • Reward: 💰 200 Coins | ⚡ 250 XP\n\n"
        "Complete matches in any group to automatically earn rewards!"
    )
    await message.reply(quests_text, parse_mode="Markdown")
