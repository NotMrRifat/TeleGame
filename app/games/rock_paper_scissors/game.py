"""Rock Paper Scissors Game Plugin."""

from typing import Any

from app.core.engine.ai_opponent import BOT_AI_ID
from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Rock Paper Scissors game plugin."""

    slug = "rock_paper_scissors"
    title = "Rock Paper Scissors"
    description = "Quick hand-gesture strategy game"
    min_players = 2
    max_players = 2

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.players: list[int] = []
            self.choices: dict[int, str] = {}
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.players = [p.telegram_id for p in players[:2]]
        self.choices = {}
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
            return GameMoveResult(success=False, message="Invalid choice or move.")

        choice = move_data["choice"].lower()  # rock, paper, scissors
        self.choices[telegram_id] = choice

        if len(self.choices) < 2:
            return GameMoveResult(
                success=True,
                message="Choice submitted! Waiting for opponent...",
                state_changed=True,
            )

        # Both players selected choices
        p1, p2 = self.players[0], self.players[1]
        c1, c2 = self.choices[p1], self.choices[p2]

        self.is_over = True
        if c1 == c2:
            return GameMoveResult(
                success=True, message=f"Both chose {c1}! Draw!", is_game_over=True, is_draw=True
            )

        win_rules = {("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")}
        if (c1, c2) in win_rules:
            self.winner_id = p1
        else:
            self.winner_id = p2

        return GameMoveResult(
            success=True,
            message=f"Game Over! Winner: {self.winner_id}",
            is_game_over=True,
            winner_user_id=self.winner_id,
        )

    def next_turn(self) -> int | None:
        for p in self.players:
            if p not in self.choices:
                return p
        return None

    def pause(self) -> bool:
        return True

    def resume(self) -> bool:
        return True

    def end(self, reason: str = "COMPLETED") -> dict[str, Any]:
        self.is_over = True
        return self.serialize()

    def serialize(self) -> dict[str, Any]:
        return {
            "players": self.players,
            "choices": {str(k): v for k, v in self.choices.items()},
            "is_over": self.is_over,
            "winner_id": self.winner_id,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.players = state_data.get("players", [])
        raw_c = state_data.get("choices", {})
        self.choices = {int(k): v for k, v in raw_c.items()}
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or telegram_id not in self.players:
            return False
        if telegram_id in self.choices:
            return False
        choice = move_data.get("choice", "").lower()
        return choice in ["rock", "paper", "scissors"]

    def timeout(self) -> GameMoveResult:
        self.is_over = True
        return GameMoveResult(success=True, message="RPS match timed out.", is_game_over=True)

    def render(self, language_code: str = "en") -> str:
        rps_emoji = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        if self.is_over:
            # Build choices summary
            lines = []
            for pid, ch in self.choices.items():
                label = "🤖 Computer" if pid == BOT_AI_ID else f"Player {pid}"
                lines.append(f"{label}: {rps_emoji.get(ch, ch)} *{ch.capitalize()}*")
            choices_text = "\n".join(lines) if lines else ""
            if self.winner_id:
                winner_label = "🤖 Computer" if self.winner_id == BOT_AI_ID else f"Player {self.winner_id}"
                return (
                    f"✊✌✋ *Rock Paper Scissors — Result!*\n\n"
                    f"{choices_text}\n\n"
                    f"🏆 Winner: {winner_label}!"
                )
            return (
                f"✊✌✋ *Rock Paper Scissors — Result!*\n\n"
                f"{choices_text}\n\n"
                f"🤝 Match ended in a Draw!"
            )
        submitted = len(self.choices)
        remaining = len(self.players) - submitted
        return (
            f"✊✌✋ *Rock Paper Scissors*\n\n"
            f"{'✅' * submitted}{'⏳' * remaining} ({submitted}/{len(self.players)} choices submitted)\n"
            f"Tap a button below to make your choice!"
        )
