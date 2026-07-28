"""Active gameplay move handlers for interactive games with AI Opponent support and victory announcements."""

from typing import Any

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.engine.ai_opponent import BOT_AI_ID, compute_ai_move
from app.core.engine.session_manager import SessionManager
from app.models.domain import UserModel
from app.repositories.domain_repos import UserRepository
from app.services.rating_service import RatingService
from app.utils.keyboards import (
    get_connect_four_keyboard,
    get_group_post_game_keyboard,
    get_post_game_keyboard,
    get_rps_keyboard,
    get_tic_tac_toe_keyboard,
)

router = Router(name="gameplay_router")

# ─── helpers ──────────────────────────────────────────────────────────────────

def _is_vs_ai(game_inst: Any) -> bool:
    """Returns True when the game session contains the Computer AI player."""
    return BOT_AI_ID in getattr(game_inst, "players", [])


async def _resolve_winner_name(
    winner_id: int,
    current_user_telegram_id: int,
    current_user_first_name: str,
    db_session: AsyncSession,
) -> str:
    """Resolve a human-readable winner name from a telegram_id."""
    if winner_id == BOT_AI_ID:
        return "🤖 Computer"
    if winner_id == current_user_telegram_id:
        return current_user_first_name or "Player"
    user_repo = UserRepository(db_session)
    w_user = await user_repo.get_by_telegram_id(winner_id)
    if w_user:
        return w_user.first_name or f"User {winner_id}"
    return f"Player {winner_id}"


async def format_game_over_message(
    result: Any,
    game_inst: Any,
    db_session: AsyncSession,
    current_user_telegram_id: int,
    current_user_first_name: str,
    board_text: str,
) -> str:
    """Renders congratulatory victory message with winner name or draw notification."""
    if result.winner_user_id:
        winner_name = await _resolve_winner_name(
            result.winner_user_id, current_user_telegram_id, current_user_first_name, db_session
        )

        if result.winner_user_id == BOT_AI_ID:
            return (
                f"🤖 *COMPUTER WON THE MATCH!* 🤖\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Better luck next time! Keep practicing to defeat the Computer!\n\n"
                f"{board_text}"
            )

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


async def _finalize_game(
    session_rec: Any,
    result: Any,
    game_inst: Any,
    db_session: AsyncSession,
    current_user_telegram_id: int,
    current_user_first_name: str,
    board_text: str,
) -> tuple[str, InlineKeyboardMarkup]:
    """Marks session FINISHED, updates ratings. Returns (final_message, post_game_keyboard)."""
    session_rec.status = "FINISHED"
    session_rec.winner_user_id = result.winner_user_id
    await db_session.flush()

    # Only update ratings for PvP (no AI involved)
    if (
        result.winner_user_id
        and result.winner_user_id != BOT_AI_ID
        and game_inst.players
        and len(game_inst.players) >= 2
    ):
        non_ai_players = [p for p in game_inst.players if p != BOT_AI_ID]
        if len(non_ai_players) >= 2:
            loser_ids = [p for p in non_ai_players if p != result.winner_user_id]
            if loser_ids:
                rating_service = RatingService(db_session)
                await rating_service.update_1v1_ratings(
                    result.winner_user_id, loser_ids[0], session_rec.game_slug
                )

    final_msg = await format_game_over_message(
        result, game_inst, db_session,
        current_user_telegram_id, current_user_first_name, board_text
    )

    # Choose appropriate post-game keyboard
    if _is_vs_ai(game_inst):
        kb = get_post_game_keyboard(session_rec.game_slug)
    else:
        kb = get_group_post_game_keyboard()

    return final_msg, kb


# ─── Tic-Tac-Toe ──────────────────────────────────────────────────────────────

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

    # Validate before processing (gives friendly turn messages)
    if not game_inst.validate(query.from_user.id, {"cell": cell}):
        current_turn = game_inst.next_turn()
        if current_turn and current_turn != query.from_user.id:
            msg = "🤖 It's the Computer's turn!" if current_turn == BOT_AI_ID else "⏳ It's not your turn yet!"
        elif game_inst.is_over:
            msg = "🏁 This game has already ended!"
        else:
            msg = "❌ That cell is already taken!"
        await query.answer(msg, show_alert=True)
        return

    result = game_inst.handle_move(query.from_user.id, {"cell": cell})
    if not result.success:
        await query.answer(result.message, show_alert=True)
        return

    await session_mgr.save_game_instance(session_rec, game_inst)

    # AI counter-move (if vs Computer and game still going)
    if _is_vs_ai(game_inst) and not result.is_game_over:
        ai_move = compute_ai_move("tic_tac_toe", game_inst)
        if ai_move:
            ai_result = game_inst.handle_move(BOT_AI_ID, ai_move)
            await session_mgr.save_game_instance(session_rec, game_inst)
            if ai_result.is_game_over:
                result = ai_result

    board_text = game_inst.render(db_user.language_code)

    if result.is_game_over:
        final_msg, post_kb = await _finalize_game(
            session_rec, result, game_inst, db_session,
            query.from_user.id, query.from_user.first_name or "Player", board_text
        )
        if query.message:
            await query.message.edit_text(final_msg, reply_markup=post_kb, parse_mode="Markdown")
    else:
        board_kb = get_tic_tac_toe_keyboard(game_inst.board)
        if query.message:
            await query.message.edit_text(board_text, reply_markup=board_kb, parse_mode="Markdown")

    await query.answer(result.message)


# ─── Rock Paper Scissors ───────────────────────────────────────────────────────

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

    # Check player eligibility
    if query.from_user.id not in game_inst.players:
        await query.answer("❌ You are not in this game!", show_alert=True)
        return

    if game_inst.is_over:
        await query.answer("🏁 This game has already ended!", show_alert=True)
        return

    if query.from_user.id in game_inst.choices:
        await query.answer("✅ Choice submitted! Waiting for opponent...", show_alert=True)
        return

    result = game_inst.handle_move(query.from_user.id, {"choice": choice})
    if not result.success:
        await query.answer(result.message, show_alert=True)
        return

    await session_mgr.save_game_instance(session_rec, game_inst)

    # AI submits its choice immediately after human
    if _is_vs_ai(game_inst) and not result.is_game_over:
        ai_move = compute_ai_move("rock_paper_scissors", game_inst)
        if ai_move:
            ai_result = game_inst.handle_move(BOT_AI_ID, ai_move)
            await session_mgr.save_game_instance(session_rec, game_inst)
            if ai_result.is_game_over:
                result = ai_result

    # Build RPS result reveal text when both players have chosen
    rps_emoji = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    board_text = game_inst.render(db_user.language_code)

    # For vs-AI games, add reveal of both choices to board text
    if _is_vs_ai(game_inst) and result.is_game_over and len(game_inst.choices) == 2:
        human_choice = game_inst.choices.get(query.from_user.id, "?")
        ai_choice = game_inst.choices.get(BOT_AI_ID, "?")
        board_text = (
            f"✊✌✋ *Rock Paper Scissors — Result!*\n\n"
            f"👤 You: {rps_emoji.get(human_choice, human_choice)} *{human_choice.capitalize()}*\n"
            f"🤖 Computer: {rps_emoji.get(ai_choice, ai_choice)} *{ai_choice.capitalize()}*\n"
        )

    if result.is_game_over:
        final_msg, post_kb = await _finalize_game(
            session_rec, result, game_inst, db_session,
            query.from_user.id, query.from_user.first_name or "Player", board_text
        )
        if query.message:
            await query.message.edit_text(final_msg, reply_markup=post_kb, parse_mode="Markdown")
    else:
        board_kb = get_rps_keyboard()
        if query.message:
            await query.message.edit_text(
                f"✊✌✋ *Rock Paper Scissors*\n\n"
                f"✅ You chose *{rps_emoji.get(choice, choice)} {choice.capitalize()}*!\n"
                f"⏳ Waiting for opponent to choose...",
                reply_markup=board_kb,
                parse_mode="Markdown",
            )

    await query.answer(f"Selected {choice.capitalize()}!")


# ─── Connect Four ──────────────────────────────────────────────────────────────

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

    # Validate turn and column
    if game_inst.is_over:
        await query.answer("🏁 This game has already ended!", show_alert=True)
        return

    if not game_inst.validate(query.from_user.id, {"col": col}):
        current_turn = game_inst.next_turn()
        if current_turn and current_turn != query.from_user.id:
            msg = "🤖 It's the Computer's turn!" if current_turn == BOT_AI_ID else "⏳ It's not your turn yet!"
        elif game_inst.board[0][col] != " ":
            msg = f"❌ Column {col + 1} is full! Choose another column."
        else:
            msg = "❌ Invalid move!"
        await query.answer(msg, show_alert=True)
        return

    result = game_inst.handle_move(query.from_user.id, {"col": col})
    if not result.success:
        await query.answer(result.message, show_alert=True)
        return

    await session_mgr.save_game_instance(session_rec, game_inst)

    # AI drops its disc after the human
    if _is_vs_ai(game_inst) and not result.is_game_over:
        ai_move = compute_ai_move("connect_four", game_inst)
        if ai_move:
            ai_result = game_inst.handle_move(BOT_AI_ID, ai_move)
            await session_mgr.save_game_instance(session_rec, game_inst)
            if ai_result.is_game_over:
                result = ai_result

    board_text = game_inst.render(db_user.language_code)

    if result.is_game_over:
        final_msg, post_kb = await _finalize_game(
            session_rec, result, game_inst, db_session,
            query.from_user.id, query.from_user.first_name or "Player", board_text
        )
        if query.message:
            await query.message.edit_text(final_msg, reply_markup=post_kb, parse_mode="Markdown")
    else:
        board_kb = get_connect_four_keyboard(game_inst.board)
        if query.message:
            await query.message.edit_text(board_text, reply_markup=board_kb, parse_mode="Markdown")

    await query.answer(f"Dropped disc in Column {col + 1}!")
