"""Inline Main Menu & Dynamic Menu Callback Router."""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.engine.plugin_manager import plugin_manager
from app.i18n.engine import i18n
from app.models.domain import UserModel
from app.repositories.domain_repos import RatingRepository
from app.services.economy_service import EconomyService
from app.utils.game_info import GAME_DETAILS
from app.utils.keyboards import (
    get_back_to_menu_keyboard,
    get_game_details_keyboard,
    get_games_selection_keyboard,
    get_main_menu_keyboard,
)

router = Router(name="inline_menu_router")


@router.callback_query(F.data == "menu_main")
async def cb_main_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Returns to main menu."""
    lang = db_user.language_code
    text = f"{i18n.get('welcome', lang)}\n\n{i18n.get('main_menu', lang)}"
    kb = get_main_menu_keyboard(lang)
    if query.message:
        await query.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_games")
async def cb_games_menu(query: CallbackQuery) -> None:
    """Opens games selection menu."""
    kb = get_games_selection_keyboard()
    if query.message:
        await query.message.edit_text(
            "🎮 *TeleGame Multiplayer Games*\n━━━━━━━━━━━━━━━━━━━━━━\nSelect any game to view details and launch in your group chat!",
            reply_markup=kb,
            parse_mode="Markdown",
        )
    await query.answer()


@router.callback_query(F.data.startswith("select_game_"))
async def cb_select_game(query: CallbackQuery) -> None:
    """Handles individual game plugin selection."""
    slug = query.data.replace("select_game_", "")
    games = plugin_manager.list_available_games()

    if slug not in games:
        await query.answer("Game plugin not found.", show_alert=True)
        return

    info = GAME_DETAILS.get(slug, {})
    game_cls = games[slug]
    title = info.get("title") or getattr(game_cls, "title", slug.replace("_", " ").title())
    description = info.get("description") or getattr(
        game_cls, "description", "Exciting multiplayer game!"
    )
    min_p = info.get("min_players") or getattr(game_cls, "min_players", 2)
    max_p = info.get("max_players") or getattr(game_cls, "max_players", 2)
    rules = info.get("rules", "Play turns according to game rules.")

    detail_text = (
        f"🎮 *{title}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 *Description:* {description}\n"
        f"👥 *Players:* {min_p} - {max_p} Players\n"
        f"🏷 *Category:* `{info.get('category', slug)}`\n\n"
        f"📜 *How to Play & Rules:*\n{rules}\n\n"
        f"📖 *How to Launch in a Group Chat:*\n"
        f"1. Add @TeleGameMasterBot to your group.\n"
        f"2. Type `/newgame {slug}` in the group!\n"
        f"3. Type `/join` to enter the lobby and start playing!"
    )
    kb = get_game_details_keyboard(slug)
    if query.message:
        await query.message.edit_text(detail_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_profile")
async def cb_profile_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views profile via inline button."""
    total_matches = db_user.games_played or 1
    win_rate = (db_user.wins / total_matches) * 100
    text = (
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
        f"• *Win Rate:* 📈 {win_rate:.1f}%\n"
        f"• *Daily Streak:* 🔥 {db_user.daily_streak} Days\n"
    )
    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_leaderboard")
async def cb_leaderboard_menu(query: CallbackQuery, db_user: UserModel, db_session: AsyncSession) -> None:
    """Views global leaderboard inline."""
    rating_repo = RatingRepository(db_session)
    top_ratings = await rating_repo.get_global_leaderboard(game_slug="tic_tac_toe", limit=10)

    leaderboard_text = "🏆 *Global Leaderboard - Season 1*\n━━━━━━━━━━━━━━━━━━━━━━\n"
    if not top_ratings:
        leaderboard_text += "No ranked matches recorded yet. Play games to claim the top spot!\n"
    else:
        for idx, rating in enumerate(top_ratings, 1):
            user_name = rating.user.first_name if rating.user else f"User {rating.user_id}"
            leaderboard_text += f"{idx}. *{user_name}* — `{rating.elo} ELO`\n"

    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(leaderboard_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_rewards")
async def cb_rewards_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views daily rewards & streak."""
    reward_text = (
        f"🎁 *Daily Login Rewards*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔥 *Current Streak:* {db_user.daily_streak} Days\n"
        f"💰 *Current Balance:* {db_user.coins} Coins\n\n"
        f"Claim your daily reward boost to earn extra coins and maintain your streak!"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎁 Claim Daily Reward", callback_data="claim_daily")],
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="menu_main")],
        ]
    )
    if query.message:
        await query.message.edit_text(reward_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "claim_daily")
async def cb_claim_daily(query: CallbackQuery, db_user: UserModel, db_session: AsyncSession) -> None:
    """Claims daily reward directly inline."""
    economy = EconomyService(db_session)
    success, amount, _ = await economy.claim_daily_reward(query.from_user.id)

    if success:
        msg = f"🎉 Claimed +{amount} Coins! Streak: {db_user.daily_streak} Days!"
    else:
        msg = "⚠️ Daily reward already claimed today! Check back tomorrow."

    await query.answer(msg, show_alert=True)
    # Refresh rewards menu view
    await cb_rewards_menu(query, db_user)


@router.callback_query(F.data == "menu_quests")
async def cb_quests_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views active quests inline."""
    quests_text = (
        "🎯 *Active Quests & Objectives*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ *Daily Gamer* (Play 3 matches)\n"
        "   • Progress: [████░░░░░░] (1/3)\n"
        "   • Reward: 💰 150 Coins | ⚡ 200 XP\n\n"
        "2️⃣ *Daily Champion* (Win 1 match)\n"
        "   • Progress: [░░░░░░░░░░] (0/1)\n"
        "   • Reward: 💰 200 Coins | ⚡ 250 XP\n\n"
        "Complete matches in any group to automatically claim rewards!"
    )
    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(quests_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_shop")
async def cb_shop_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views shop items inline."""
    shop_text = (
        f"🛒 *TeleGame Cosmetic Shop*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *Your Coins:* {db_user.coins}\n"
        f"🏷 *Equipped Title:* `{db_user.title}`\n"
        f"🖼 *Equipped Frame:* `{db_user.frame}`\n\n"
        f"🌟 *Available Items:*\n"
        f"1️⃣ Title: `Mastermind` — 💰 500 Coins\n"
        f"2️⃣ Title: `Grandmaster` — 💰 1,500 Coins\n"
        f"3️⃣ Frame: `Gold Neon` — 💰 1,000 Coins\n"
        f"4️⃣ Theme: `Dark Cyberpunk` — 💰 2,000 Coins\n"
    )
    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(shop_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_inventory")
async def cb_inventory_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views inventory inline."""
    inv_text = (
        f"🎒 *Player Inventory*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏷 *Titles:* `{db_user.title}` (Equipped)\n"
        f"🖼 *Frames:* `{db_user.frame}` (Equipped)\n"
        f"🎨 *Themes:* `{db_user.theme}` (Equipped)\n"
        f"👤 *Avatar:* `{db_user.avatar}`\n"
    )
    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(inv_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_friends")
async def cb_friends_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views friends list inline."""
    friends_text = (
        "👥 *Friends & Social Network*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "You currently have 0 active friends.\n\n"
        "💡 Play multiplayer matches in group chats to connect with other players!"
    )
    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(friends_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_clan")
async def cb_clan_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views clan details inline."""
    clan_text = (
        "⚔ *TeleGame Clan System*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Clans allow players to team up, pool XP, and compete in Clan Wars!\n\n"
        "📖 *Creation Guide:*\n"
        "Type `/clan create <name> <tag>` in chat (e.g. `/clan create CyberKnights CKN`)"
    )
    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(clan_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "menu_settings")
async def cb_settings_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views settings & language toggle inline."""
    current_lang = "English" if db_user.language_code == "en" else "বাংলা (Bangla)"
    settings_text = (
        f"⚙️ *Platform Settings*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🌐 *Language:* `{current_lang}`\n"
        f"🔔 *Notifications:* Enabled\n"
    )
    btn_label = "🌐 Switch to English" if db_user.language_code == "bn" else "🌐 বাংলায় পরিবর্তন করুন"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=btn_label, callback_data="toggle_lang")],
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="menu_main")],
        ]
    )
    if query.message:
        await query.message.edit_text(settings_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()


@router.callback_query(F.data == "toggle_lang")
async def cb_toggle_lang(query: CallbackQuery, db_user: UserModel, db_session: AsyncSession) -> None:
    """Toggles user language code inline."""
    new_lang = "en" if db_user.language_code == "bn" else "bn"
    db_user.language_code = new_lang
    await db_session.flush()

    msg = "🌐 Language changed to English!" if new_lang == "en" else "🌐 ভাষা পরিবর্তন করা হয়েছে!"
    await query.answer(msg, show_alert=True)
    await cb_settings_menu(query, db_user)


@router.callback_query(F.data == "menu_help")
async def cb_help_menu(query: CallbackQuery, db_user: UserModel) -> None:
    """Views help guide inline."""
    help_text = (
        "📖 *TeleGame Platform Help & Commands*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎮 `/games` — View 10 available games\n"
        "📌 `/newgame <slug>` — Start game lobby in group\n"
        "👥 `/join` — Enter open lobby\n"
        "🚀 `/startgame` — Host force-starts match\n"
        "🛑 `/cancel` — End active game\n"
        "👤 `/profile` — View player stats\n"
        "🎁 `/daily` — Claim daily rewards\n"
        "🏆 `/leaderboard` — View top ratings"
    )
    kb = get_back_to_menu_keyboard(db_user.language_code)
    if query.message:
        await query.message.edit_text(help_text, reply_markup=kb, parse_mode="Markdown")
    await query.answer()
