"""Ludo Game Plugin."""

import random
from typing import Any

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Ludo dice-rolling board game plugin."""

    slug = "ludo"
    title = "Ludo"
    description = "Classic dice rolling board game"
    min_players = 2
    max_players = 4

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.last_dice: int = 1
            self.players: list[int] = []
            self.positions: dict[int, int] = {}
            self.turn_index: int = 0
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.players = [p.telegram_id for p in players[:4]]
        self.positions = dict.fromkeys(self.players, 0)
        self.turn_index = 0
        self.is_over = False
        self.winner_id = None
        return self.serialize()

    def join(self, player: GamePlayer) -> bool:
        if len(self.players) >= 4 or player.telegram_id in self.players:
            return False
        self.players.append(player.telegram_id)
        self.positions[player.telegram_id] = 0
        return True

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
            return GameMoveResult(success=False, message="Not your turn to roll dice.")

        dice = random.randint(1, 6)
        self.last_dice = dice
        self.positions[telegram_id] = self.positions.get(telegram_id, 0) + dice

        if self.positions[telegram_id] >= 57:  # Home reached
            self.is_over = True
            self.winner_id = telegram_id
            return GameMoveResult(
                success=True,
                message=f"Player {telegram_id} rolled {dice} and won!",
                is_game_over=True,
                winner_user_id=telegram_id,
            )

        self.turn_index = (self.turn_index + 1) % len(self.players)
        return GameMoveResult(
            success=True,
            message=f"Rolled a {dice}!",
            next_turn_user_id=self.players[self.turn_index],
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
            "last_dice": self.last_dice,
            "players": self.players,
            "positions": {str(k): v for k, v in self.positions.items()},
            "turn_index": self.turn_index,
            "is_over": self.is_over,
            "winner_id": self.winner_id,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.last_dice = state_data.get("last_dice", 1)
        self.players = state_data.get("players", [])
        raw_pos = state_data.get("positions", {})
        self.positions = {int(k): v for k, v in raw_pos.items()}
        self.turn_index = state_data.get("turn_index", 0)
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or not self.players:
            return False
        return telegram_id == self.players[self.turn_index]

    def timeout(self) -> GameMoveResult:
        self.is_over = True
        return GameMoveResult(success=True, message="Ludo match timed out.", is_game_over=True)

    def render(self, language_code: str = "en") -> str:
        if self.is_over:
            return f"🎲 *Ludo*\n\nGame Over!\nWinner: Player {self.winner_id}"
        return f"🎲 *Ludo*\n\nLast Dice Roll: 🎲 *{self.last_dice}*\nTurn: Player {self.players[self.turn_index]}"
