"""AI Opponent Engine for Single-Player / Vs Computer Game Sessions."""

import random
from typing import Any

from app.core.engine.base_game import GamePlayer

BOT_AI_ID = 999999999
BOT_AI_NAME = "🤖 TeleGame Computer"


def is_ai_player(telegram_id: int) -> bool:
    """Checks if a telegram_id represents the AI Computer player."""
    return telegram_id == BOT_AI_ID


def get_ai_game_player() -> GamePlayer:
    """Returns a GamePlayer object for the AI Computer."""
    return GamePlayer(
        telegram_id=BOT_AI_ID,
        username="TeleGameComputer",
        role="bot",
    )


def compute_ai_move(game_slug: str, game_inst: Any) -> dict[str, Any] | None:
    """Computes intelligent AI move payload based on game type and current board state."""
    if game_slug == "tic_tac_toe":
        board = getattr(game_inst, "board", [" "] * 9)
        open_cells = [i for i, cell in enumerate(board) if cell == " "]
        if not open_cells:
            return None

        ai_symbol = getattr(game_inst, "symbols", {}).get(BOT_AI_ID, "⭕")
        human_symbol = "❌" if ai_symbol == "⭕" else "⭕"

        winning_combos = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        # 1. Check if AI can win in 1 move
        for a, b, c in winning_combos:
            line = [board[a], board[b], board[c]]
            if line.count(ai_symbol) == 2 and line.count(" ") == 1:
                idx = [a, b, c][line.index(" ")]
                return {"cell": idx}

        # 2. Check if AI needs to block Human from winning in 1 move
        for a, b, c in winning_combos:
            line = [board[a], board[b], board[c]]
            if line.count(human_symbol) == 2 and line.count(" ") == 1:
                idx = [a, b, c][line.index(" ")]
                return {"cell": idx}

        # 3. Prefer center cell
        if 4 in open_cells:
            return {"cell": 4}

        # 4. Prefer corners
        corners = [c for c in [0, 2, 6, 8] if c in open_cells]
        if corners:
            return {"cell": random.choice(corners)}

        # 5. Pick random open cell
        return {"cell": random.choice(open_cells)}

    elif game_slug == "rock_paper_scissors":
        choices = ["rock", "paper", "scissors"]
        return {"choice": random.choice(choices)}

    elif game_slug == "connect_four":
        board = getattr(game_inst, "board", [[" "] * 7 for _ in range(6)])
        valid_cols = [c for c in range(7) if board[0][c] == " "]
        if not valid_cols:
            return None

        ai_symbol = getattr(game_inst, "symbols", {}).get(BOT_AI_ID, "🟡")
        human_symbol = "🔴" if ai_symbol == "🟡" else "🔴"

        # Check if any column gives immediate win for AI
        for col in valid_cols:
            for r in range(5, -1, -1):
                if board[r][col] == " ":
                    board[r][col] = ai_symbol
                    if hasattr(game_inst, "_check_win") and game_inst._check_win(r, col, ai_symbol):
                        board[r][col] = " "
                        return {"col": col}
                    board[r][col] = " "
                    break

        # Check if any column blocks human win
        for col in valid_cols:
            for r in range(5, -1, -1):
                if board[r][col] == " ":
                    board[r][col] = human_symbol
                    if hasattr(game_inst, "_check_win") and game_inst._check_win(
                        r, col, human_symbol
                    ):
                        board[r][col] = " "
                        return {"col": col}
                    board[r][col] = " "
                    break

        # Prefer center columns
        for col in [3, 2, 4, 1, 5, 0, 6]:
            if col in valid_cols:
                return {"col": col}

        return {"col": random.choice(valid_cols)}

    return None
