"""Connect Four Game Plugin."""

from typing import Any

from app.core.engine.ai_opponent import BOT_AI_ID
from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Connect Four (6x7 grid) game plugin."""

    slug = "connect_four"
    title = "Connect Four"
    description = "Drop discs to connect 4 in a row"
    min_players = 2
    max_players = 2

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.board: list[list[str]] = [[" "] * 7 for _ in range(6)]
            self.players: list[int] = []
            self.symbols: dict[int, str] = {}
            self.turn_index: int = 0
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.board = [[" "] * 7 for _ in range(6)]
        self.players = [p.telegram_id for p in players[:2]]
        self.symbols = {self.players[0]: "🔴", self.players[1]: "🟡"}
        self.turn_index = 0
        self.is_over = False
        self.winner_id = None
        return self.serialize()

    def join(self, player: Any) -> bool:
        p_id = (
            player.telegram_id
            if hasattr(player, "telegram_id")
            else (player.id if hasattr(player, "id") else int(player))
        )
        if len(self.players) >= 2 or p_id in self.players:
            return False
        self.players.append(p_id)
        if len(self.players) == 2:
            self.symbols = {self.players[0]: "🔴", self.players[1]: "🟡"}
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
            return GameMoveResult(success=False, message="Invalid column choice.")

        col = int(move_data["col"])
        symbol = self.symbols[telegram_id]

        # Drop disc to lowest available row
        target_row = -1
        for r in range(5, -1, -1):
            if self.board[r][col] == " ":
                self.board[r][col] = symbol
                target_row = r
                break

        # Check win condition
        if self._check_win(target_row, col, symbol):
            self.is_over = True
            self.winner_id = telegram_id
            return GameMoveResult(
                success=True,
                message=f"Player {symbol} connected four!",
                is_game_over=True,
                winner_user_id=telegram_id,
            )

        # Switch turn
        self.turn_index = 1 - self.turn_index
        return GameMoveResult(
            success=True,
            message="Disc dropped.",
            next_turn_user_id=self.players[self.turn_index],
        )

    def _check_win(self, r: int, c: int, s: str) -> bool:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            # Check positive direction
            nr, nc = r + dr, c + dc
            while 0 <= nr < 6 and 0 <= nc < 7 and self.board[nr][nc] == s:
                count += 1
                nr += dr
                nc += dc
            # Check negative direction
            nr, nc = r - dr, c - dc
            while 0 <= nr < 6 and 0 <= nc < 7 and self.board[nr][nc] == s:
                count += 1
                nr -= dr
                nc -= dc
            if count >= 4:
                return True
        return False

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
        self.board = state_data.get("board", [[" "] * 7 for _ in range(6)])
        self.players = state_data.get("players", [])
        raw_s = state_data.get("symbols", {})
        self.symbols = {int(k): v for k, v in raw_s.items()}
        self.turn_index = state_data.get("turn_index", 0)
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or not self.players or len(self.players) < 2:
            return False
        if telegram_id != self.players[self.turn_index]:
            return False
        col = move_data.get("col")
        if col is None or not (0 <= int(col) <= 6):
            return False
        return self.board[0][int(col)] == " "

    def timeout(self) -> GameMoveResult:
        self.is_over = True
        return GameMoveResult(
            success=True, message="Connect Four match timed out.", is_game_over=True
        )

    def render(self, language_code: str = "en") -> str:
        lines = []
        for r in self.board:
            row_str = "".join([cell if cell != " " else "⚪" for cell in r])
            lines.append(row_str)
        grid = "\n".join(lines) + "\n1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
        if self.is_over:
            if self.winner_id:
                sym = self.symbols.get(self.winner_id, "")
                winner_label = "🤖 Computer" if self.winner_id == BOT_AI_ID else f"Player {sym}"
                return f"🔴🟡 *Connect Four*\n\n{grid}\n\n🏆 Winner: {winner_label}!"
            return f"🔴🟡 *Connect Four*\n\n{grid}\n\n🤝 It's a Draw!"
        current_id = self.players[self.turn_index] if self.players else None
        if current_id == BOT_AI_ID:
            turn_text = "🤖 Computer's turn"
        else:
            sym = self.symbols.get(current_id, "Current") if current_id else "Current"
            turn_text = f"Your turn: {sym}"
        return f"🔴🟡 *Connect Four*\n\n{grid}\n\n▶️ {turn_text}"
