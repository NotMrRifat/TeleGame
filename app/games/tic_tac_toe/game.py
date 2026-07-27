"""Tic Tac Toe Game Plugin."""

from typing import Any

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Tic Tac Toe (3x3 grid) game plugin."""

    slug = "tic_tac_toe"
    title = "Tic-Tac-Toe"
    description = "Classic 3x3 grid strategy game"
    min_players = 2
    max_players = 2

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.board: list[str] = [" "] * 9  # Index 0-8
            self.players: list[int] = []  # [X_id, O_id]
            self.symbols: dict[int, str] = {}
            self.turn_index: int = 0
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        if len(players) < 2:
            raise ValueError("Tic-Tac-Toe requires 2 players.")
        self.board = [" "] * 9
        self.players = [players[0].telegram_id, players[1].telegram_id]
        self.symbols = {self.players[0]: "❌", self.players[1]: "⭕"}
        self.turn_index = 0
        self.is_over = False
        self.winner_id = None
        return self.serialize()

    def join(self, player: GamePlayer) -> bool:
        if len(self.players) >= 2 or player.telegram_id in self.players:
            return False
        self.players.append(player.telegram_id)
        if len(self.players) == 2:
            self.symbols = {self.players[0]: "❌", self.players[1]: "⭕"}
        return True

    def leave(self, telegram_id: int) -> bool:
        if telegram_id in self.players:
            self.players.remove(telegram_id)
            return True
        return False

    def start(self) -> dict[str, Any]:
        self.is_over = False
        self.turn_index = 0
        return self.serialize()

    def handle_move(self, telegram_id: int, move_data: dict[str, Any]) -> GameMoveResult:
        if not self.validate(telegram_id, move_data):
            return GameMoveResult(success=False, message="Invalid move or not your turn.")

        cell = int(move_data["cell"])
        symbol = self.symbols[telegram_id]
        self.board[cell] = symbol

        # Check win condition
        win_patterns = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # Rows
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # Columns
            [0, 4, 8],
            [2, 4, 6],  # Diagonals
        ]

        for p in win_patterns:
            if self.board[p[0]] == self.board[p[1]] == self.board[p[2]] == symbol:
                self.is_over = True
                self.winner_id = telegram_id
                return GameMoveResult(
                    success=True,
                    message=f"Player {symbol} wins!",
                    is_game_over=True,
                    winner_user_id=telegram_id,
                )

        # Check draw condition
        if " " not in self.board:
            self.is_over = True
            return GameMoveResult(
                success=True,
                message="Game ended in a draw!",
                is_game_over=True,
                is_draw=True,
            )

        # Switch turn
        self.turn_index = 1 - self.turn_index
        next_id = self.players[self.turn_index]

        return GameMoveResult(
            success=True,
            message="Move accepted.",
            next_turn_user_id=next_id,
        )

    def next_turn(self) -> int | None:
        if self.is_over or not self.players:
            return None
        return self.players[self.turn_index]

    def pause(self) -> bool:
        return True

    def resume(self) -> bool:
        return True

    def end(self, reason: str = "COMPLETED") -> dict[str, Any]:
        self.is_over = True
        return self.serialize()

    def serialize(self) -> dict[str, Any]:
        return {
            "board": self.board,
            "players": self.players,
            "symbols": {str(k): v for k, v in self.symbols.items()},
            "turn_index": self.turn_index,
            "is_over": self.is_over,
            "winner_id": self.winner_id,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.board = state_data.get("board", [" "] * 9)
        self.players = state_data.get("players", [])
        raw_symbols = state_data.get("symbols", {})
        self.symbols = {int(k): v for k, v in raw_symbols.items()}
        self.turn_index = state_data.get("turn_index", 0)
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or not self.players or len(self.players) < 2:
            return False
        if telegram_id != self.players[self.turn_index]:
            return False
        cell = move_data.get("cell")
        if cell is None or not (0 <= int(cell) <= 8):
            return False
        return self.board[int(cell)] == " "

    def timeout(self) -> GameMoveResult:
        if not self.players or len(self.players) < 2:
            return GameMoveResult(success=True, message="Game timed out.", is_game_over=True)
        current_id = self.players[self.turn_index]
        winner_id = self.players[1 - self.turn_index]
        self.is_over = True
        self.winner_id = winner_id
        return GameMoveResult(
            success=True,
            message=f"Player {current_id} timed out. Winner is {winner_id}!",
            is_game_over=True,
            winner_user_id=winner_id,
        )

    def render(self, language_code: str = "en") -> str:
        b = [x if x != " " else "⬜" for x in self.board]
        grid = f"{b[0]} | {b[1]} | {b[2]}\n{b[3]} | {b[4]} | {b[5]}\n{b[6]} | {b[7]} | {b[8]}"
        if self.is_over:
            if self.winner_id:
                return f"🎮 *Tic-Tac-Toe*\n\n{grid}\n\n🏆 Winner: Player {self.symbols.get(self.winner_id, 'Winner')}"
            return f"🎮 *Tic-Tac-Toe*\n\n{grid}\n\n🤝 Match ended in a Draw!"
        turn_symbol = self.symbols.get(self.players[self.turn_index], "Current")
        return f"🎮 *Tic-Tac-Toe*\n\n{grid}\n\nTurn: {turn_symbol}"
