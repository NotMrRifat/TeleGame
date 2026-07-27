"""Leaderboard handlers."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.domain_repos import RatingRepository

router = Router(name="leaderboard_router")


@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: Message, db_session: AsyncSession) -> None:
    """Handles /leaderboard command showing top rated players."""
    rating_repo = RatingRepository(db_session)
    top_ratings = await rating_repo.get_global_leaderboard(game_slug="tic_tac_toe", limit=10)

    leaderboard_text = "🏆 *Global Leaderboard - Tic-Tac-Toe (Season 1)*\n━━━━━━━━━━━━━━━━━━━━━━\n"

    if not top_ratings:
        leaderboard_text += "No ranked matches recorded yet. Play games to claim the top spot!\n"
    else:
        for idx, rating in enumerate(top_ratings, 1):
            user_name = rating.user.first_name if rating.user else f"User {rating.user_id}"
            leaderboard_text += (
                f"{idx}. *{user_name}* — `{rating.elo} ELO` (Peak: {rating.peak_elo})\n"
            )

    leaderboard_text += "\n💡 Win games in any group to increase your Elo rating!"
    await message.reply(leaderboard_text, parse_mode="Markdown")
