"""Active gameplay move handlers."""

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.engine.session_manager import SessionManager
from app.models.domain import UserModel
from app.services.rating_service import RatingService
from app.utils.keyboards import get_tic_tac_toe_keyboard

router = Router(name="gameplay_router")


@router.callback_query(F.data.startswith("ttt_move_"))
async def cb_ttt_move(query: CallbackQuery, db_user: UserModel, db_session: AsyncSession) -> None:
    """Handles Tic-Tac-Toe grid move callbacks."""
    cell = int(query.data.split("_")[-1])
    session_mgr = SessionManager(db_session)
    active_session = await session_mgr.get_active_session(query.message.chat.id)

    if not active_session:
        await query.answer("No active game session found.", show_alert=True)
        return

    session_rec, game_inst = await session_mgr.load_game_instance(active_session.id)
    result = game_inst.handle_move(query.from_user.id, {"cell": cell})

    if not result.success:
        await query.answer(result.message, show_alert=True)
        return

    await session_mgr.save_game_instance(session_rec, game_inst)

    board_text = game_inst.render(db_user.language_code)
    board_kb = get_tic_tac_toe_keyboard(game_inst.board)

    if result.is_game_over:
        session_rec.status = "FINISHED"
        session_rec.winner_user_id = result.winner_user_id
        await db_session.flush()

        if result.winner_user_id and game_inst.players and len(game_inst.players) >= 2:
            loser_id = [p for p in game_inst.players if p != result.winner_user_id][0]
            rating_service = RatingService(db_session)
            await rating_service.update_1v1_ratings(
                result.winner_user_id, loser_id, session_rec.game_slug
            )

        await query.message.edit_text(board_text, parse_mode="Markdown")
    else:
        await query.message.edit_text(board_text, reply_markup=board_kb, parse_mode="Markdown")

    await query.answer(result.message)
