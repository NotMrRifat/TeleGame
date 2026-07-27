"""Mafia Game Plugin."""

import random
from typing import Any

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Mafia social deduction multi-role game plugin."""

    slug = "mafia"
    title = "Mafia"
    description = "Social deduction multiplayer game of mystery and deceit"
    min_players = 4
    max_players = 16

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.phase: str = "NIGHT"  # NIGHT, DAY, VOTING
            self.roles: dict[int, str] = {}  # {id: "mafia"/"detective"/"civilian"}
            self.alive_players: list[int] = []
            self.night_kills: dict[int, int] = {}  # {target: count}
            self.is_over: bool = False
            self.winning_team: str | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.alive_players = [p.telegram_id for p in players]
        num_mafia = max(1, len(self.alive_players) // 3)

        shuffled = list(self.alive_players)
        random.shuffle(shuffled)

        self.roles = {}
        for i, pid in enumerate(shuffled):
            if i < num_mafia:
                self.roles[pid] = "mafia"
            elif i == num_mafia:
                self.roles[pid] = "detective"
            else:
                self.roles[pid] = "civilian"

        self.phase = "NIGHT"
        self.is_over = False
        self.winning_team = None
        return self.serialize()

    def join(self, player: GamePlayer) -> bool:
        if player.telegram_id not in self.alive_players:
            self.alive_players.append(player.telegram_id)
            return True
        return False

    def leave(self, telegram_id: int) -> bool:
        if telegram_id in self.alive_players:
            self.alive_players.remove(telegram_id)
            return True
        return False

    def start(self) -> dict[str, Any]:
        self.is_over = False
        self.phase = "NIGHT"
        return self.serialize()

    def handle_move(self, telegram_id: int, move_data: dict[str, Any]) -> GameMoveResult:
        if not self.validate(telegram_id, move_data):
            return GameMoveResult(success=False, message="Invalid action or target.")

        action = move_data["action"]  # kill, investigate, vote
        target_id = int(move_data["target_id"])

        if self.phase == "NIGHT":
            if action == "kill" and self.roles.get(telegram_id) == "mafia":
                self.night_kills[target_id] = self.night_kills.get(target_id, 0) + 1
                self.phase = "DAY"
                if target_id in self.alive_players:
                    self.alive_players.remove(target_id)
                return GameMoveResult(
                    success=True, message=f"Night ended. Player {target_id} was killed!"
                )

        elif self.phase == "DAY":
            if action == "vote":
                if target_id in self.alive_players:
                    self.alive_players.remove(target_id)
                self.phase = "NIGHT"
                return GameMoveResult(
                    success=True, message=f"Day ended. Player {target_id} was lynched!"
                )

        return GameMoveResult(success=True, message="Action processed.")

    def next_turn(self) -> int | None:
        return self.alive_players[0] if self.alive_players else None

    def pause(self) -> bool:
        return True

    def resume(self) -> bool:
        return True

    def end(self, reason: str = "COMPLETED") -> dict[str, Any]:
        self.is_over = True
        return self.serialize()

    def serialize(self) -> dict[str, Any]:
        return {
            "phase": self.phase,
            "roles": {str(k): v for k, v in self.roles.items()},
            "alive_players": self.alive_players,
            "is_over": self.is_over,
            "winning_team": self.winning_team,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.phase = state_data.get("phase", "NIGHT")
        raw_r = state_data.get("roles", {})
        self.roles = {int(k): v for k, v in raw_r.items()}
        self.alive_players = state_data.get("alive_players", [])
        self.is_over = state_data.get("is_over", False)
        self.winning_team = state_data.get("winning_team")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or telegram_id not in self.alive_players:
            return False
        target = move_data.get("target_id")
        return target is not None and int(target) in self.roles

    def timeout(self) -> GameMoveResult:
        self.is_over = True
        return GameMoveResult(success=True, message="Mafia game timed out.", is_game_over=True)

    def render(self, language_code: str = "en") -> str:
        if self.is_over:
            return f"🕵️ *Mafia*\n\nGame Over!\nWinning Team: {self.winning_team}"
        return (
            f"🕵️ *Mafia*\n\nCurrent Phase: *{self.phase}*\nAlive Players: {len(self.alive_players)}"
        )
