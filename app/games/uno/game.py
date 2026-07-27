"""UNO Game Plugin."""

from typing import Any

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """UNO card game plugin."""

    slug = "uno"
    title = "UNO"
    description = "Classic color and number matching card game"
    min_players = 2
    max_players = 8

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.top_card: str = "RED_7"
            self.players: list[int] = []
            self.turn_index: int = 0
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.top_card = "RED_7"
        self.players = [p.telegram_id for p in players]
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
        if p_id not in self.players:
            self.players.append(p_id)
            return True
        return False

    def leave(self, telegram_id: int) -> bool:
        if telegram_id in self.players:
            self.players.remove(telegram_id)
            return True
        return False

    def start(self) -> dict[str, Any]:
        self.is_over = False
        return self.serialize()

    def handle_move(self, telegram_id: int, move_data: dict[str, Any]) -> GameMoveResult:
        if not self.validate(telegram_id, move_data):
            return GameMoveResult(success=False, message="Invalid card played.")
        card = move_data["card"]
        self.top_card = card
        self.turn_index = (self.turn_index + 1) % len(self.players)
        return GameMoveResult(
            success=True, message=f"Played {card}!", next_turn_user_id=self.players[self.turn_index]
        )

    def next_turn(self) -> int | None:
        return self.players[self.turn_index] if self.players else None

    def pause(self) -> bool:
        return True

    def resume(self) -> bool:
        return True

    def end(self, reason: str = "COMPLETED") -> dict[str, Any]:
        self.is_over = True
        return self.serialize()

    def serialize(self) -> dict[str, Any]:
        return {
            "top_card": self.top_card,
            "players": self.players,
            "turn_index": self.turn_index,
            "is_over": self.is_over,
            "winner_id": self.winner_id,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.top_card = state_data.get("top_card", "RED_7")
        self.players = state_data.get("players", [])
        self.turn_index = state_data.get("turn_index", 0)
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or not self.players or telegram_id != self.players[self.turn_index]:
            return False
        return bool(move_data.get("card"))

    def timeout(self) -> GameMoveResult:
        self.is_over = True
        return GameMoveResult(success=True, message="UNO match timed out.", is_game_over=True)

    def render(self, language_code: str = "en") -> str:
        if self.is_over:
            return f"🎴 *UNO*\n\nGame Over!\nWinner: Player {self.winner_id}"
        return (
            f"🎴 *UNO*\n\nTop Card: `{self.top_card}`\nTurn: Player {self.players[self.turn_index]}"
        )
