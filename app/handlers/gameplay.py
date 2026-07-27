"""Active gameplay move handlers for interactive games with AI Opponent support and victory announcements."""

from typing import Any

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.engine.ai_opponent import BOT_AI_ID, compute_ai_move
from app.core.engine.session_manager import SessionManager
from app.models.domain import UserModel
from app.repositories.domain_repos import UserRepository
from app.services.rating_service import RatingService
from app.utils.keyboards import (
    get_connect_four_keyboard,
    get_rps_keyboard,
    get_tic_tac_toe_keyboard,
)

router = Router(name="gameplay_router")


async def format_game_over_message(
    result: Any, game_inst: Any, db_session: AsyncSession, current_user: Any, board_text: str
) -> str:
    """Renders congratulatory victory message with winner name or draw notification."""
    if result.winner_user_id:
        if result.winner_user_id == BOT_AI_ID:
            return (
                f"🤖 *COMPUTER WON THE MATCH!* 🤖\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Better luck next time! Keep practicing to defeat the Computer!\n\n"
                f"{board_text}"
            )

        winner_name = "Player"
        if result.winner_user_id == current_user.id:
            winner_name = current_user.first_name or "Player"
        else:
            user_repo = UserRepository(db_session)
            w_user = await user_repo.get_by_telegram_id(result.winner_user_id)
            if w_user:
                winner_name = w_user.first_name or f"User {result.winner_user_id}"

        return (
            f"🎉 *CONGRATULATIONS {winner_name.upper()}!* 🏆\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 You won the match! High score & Elo rating updated!\n\n"
            f"{board_text}"
        )
    elif result.is_draw:
        return (
            f"🤝 *MATCH ENDED IN A DRAW!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Both players played exceptionally well!\n\n"
            f"{board_text}"
        )
    return f"🏁 *GAME OVER!*\n\n{board_text}"


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

    # If vs Computer AI and not over, AI takes counter-move
    if BOT_AI_ID in game_inst.players and not result.is_game_over:
        ai_move = compute_ai_move("tic_tac_toe", game_inst)
        if ai_move:
            result = game_inst.handle_move(BOT_AI_ID, ai_move)
            await session_mgr.save_game_instance(session_rec, game_inst)

    board_text = game_inst.render(db_user.language_code)
    board_kb = get_tic_tac_toe_keyboard(game_inst.board)

    if result.is_game_over:
        session_rec.status = "FINISHED"
        session_rec.winner_user_id = result.winner_user_id
        await db_session.flush()

        if (
            result.winner_user_id
            and result.winner_user_id != BOT_AI_ID
            and game_inst.players
            and len(game_inst.players) >= 2
        ):
            loser_id = [p for p in game_inst.players if p != result.winner_user_id][0]
            if loser_id != BOT_AI_ID:
                rating_service = RatingService(db_session)
                await rating_service.update_1v1_ratings(
                    result.winner_user_id, loser_id, session_rec.game_slug
                )

        final_msg = await format_game_over_message(
            result, game_inst, db_session, query.from_user, board_text
        )
        if query.message:
            await query.message.edit_text(final_msg, parse_mode="Markdown")
    else:
        if query.message:
            await query.message.edit_text(board_text, reply_markup=board_kb, parse_mode="Markdown")

    await query.answer(result.message)


@router.callback_query(F.data.startswith("rps_move_"))
async def cb_rps_move(query: CallbackQuery, db_user: UserModel, db_session: AsyncSession) -> None:
    """Handles Rock Paper Scissors gesture choice callbacks."""
    choice = query.data.replace("rps_move_", "")
    session_mgr = SessionManager(db_session)
    active_session = await session_mgr.get_active_session(query.message.chat.id)

    if not active_session:
        await query.answer("No active RPS match found.", show_alert=True)
        return

    session_rec, game_inst = await session_mgr.load_game_instance(active_session.id)
    result = game_inst.handle_move(query.from_user.id, {"choice": choice})

    if not result.success:
        await query.answer(result.message, show_alert=True)
        return

    await session_mgr.save_game_instance(session_rec, game_inst)

    # If vs Computer AI and not over, AI submits choice
    if BOT_AI_ID in game_inst.players and not result.is_game_over:
        ai_move = compute_ai_move("rock_paper_scissors", game_inst)
        if ai_move:
            result = game_inst.handle_move(BOT_AI_ID, ai_move)
            await session_mgr.save_game_instance(session_rec, game_inst)

    board_text = game_inst.render(db_user.language_code)

    if result.is_game_over:
        session_rec.status = "FINISHED"
        session_rec.winner_user_id = result.winner_user_id
        await db_session.flush()

        if (
            result.winner_user_id
            and result.winner_user_id != BOT_AI_ID
            and game_inst.players
            and len(game_inst.players) >= 2
        ):
            loser_id = [p for p in game_inst.players if p != result.winner_user_id][0]
            if loser_id != BOT_AI_ID:
                rating_service = RatingService(db_session)
                await rating_service.update_1v1_ratings(
                    result.winner_user_id, loser_id, session_rec.game_slug
                )

        final_msg = await format_game_over_message(
            result, game_inst, db_session, query.from_user, board_text
        )
        if query.message:
            await query.message.edit_text(final_msg, parse_mode="Markdown")
    else:
        board_kb = get_rps_keyboard()
        if query.message:
            await query.message.edit_text(board_text, reply_markup=board_kb, parse_mode="Markdown")

    await query.answer(f"Selected {choice.capitalize()}!")


@router.callback_query(F.data.startswith("c4_drop_"))
async def cb_c4_drop(query: CallbackQuery, db_user: UserModel, db_session: AsyncSession) -> None:
    """Handles Connect Four column drop callbacks."""
    col = int(query.data.split("_")[-1])
    session_mgr = SessionManager(db_session)
    active_session = await session_mgr.get_active_session(query.message.chat.id)

    if not active_session:
        await query.answer("No active Connect Four match found.", show_alert=True)
        return

    session_rec, game_inst = await session_mgr.load_game_instance(active_session.id)
    result = game_inst.handle_move(query.from_user.id, {"col": col})

    if not result.success:
        await query.answer(result.message, show_alert=True)
        return

    await session_mgr.save_game_instance(session_rec, game_inst)

    # If vs Computer AI and not over, AI drops disc
    if BOT_AI_ID in game_inst.players and not result.is_game_over:
        ai_move = compute_ai_move("connect_four", game_inst)
        if ai_move:
            result = game_inst.handle_move(BOT_AI_ID, ai_move)
            await session_mgr.save_game_instance(session_rec, game_inst)

    board_text = game_inst.render(db_user.language_code)

    if result.is_game_over:
        session_rec.status = "FINISHED"
        session_rec.winner_user_id = result.winner_user_id
        await db_session.flush()

        if (
            result.winner_user_id
            and result.winner_user_id != BOT_AI_ID
            and game_inst.players
            and len(game_inst.players) >= 2
        ):
            loser_id = [p for p in game_inst.players if p != result.winner_user_id][0]
            if loser_id != BOT_AI_ID:
                rating_service = RatingService(db_session)
                await rating_service.update_1v1_ratings(
                    result.winner_user_id, loser_id, session_rec.game_slug
                )

        final_msg = await format_game_over_message(
            result, game_inst, db_session, query.from_user, board_text
        )
        if query.message:
            await query.message.edit_text(final_msg, parse_mode="Markdown")
    else:
        board_kb = get_connect_four_keyboard(game_inst.board)
        if query.message:
            await query.message.edit_text(board_text, reply_markup=board_kb, parse_mode="Markdown")

    await query.answer(f"Dropped disc in Column {col + 1}!")
