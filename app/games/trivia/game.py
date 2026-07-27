"""Trivia Battle Game Plugin."""

from typing import Any

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Trivia Battle quiz game plugin."""

    slug = "trivia"
    title = "Trivia Battle"
    description = "Test your knowledge against friends in real time"
    min_players = 1
    max_players = 20

    QUESTIONS = [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Madrid"],
            "answer": 1,
        },
        {
            "question": "Which programming language was created by Guido van Rossum?",
            "options": ["Java", "C++", "Python", "JavaScript"],
            "answer": 2,
        },
        {
            "question": "How many bits are in a byte?",
            "options": ["4", "8", "16", "32"],
            "answer": 1,
        },
    ]

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.current_q_index: int = 0
            self.scores: dict[int, int] = {}
            self.players: list[int] = []
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.current_q_index = 0
        self.players = [p.telegram_id for p in players]
        self.scores = dict.fromkeys(self.players, 0)
        self.is_over = False
        self.winner_id = None
        return self.serialize()

    def join(self, player: GamePlayer) -> bool:
        if player.telegram_id not in self.players:
            self.players.append(player.telegram_id)
            self.scores[player.telegram_id] = 0
            return True
        return False

    def leave(self, telegram_id: int) -> bool:
        if telegram_id in self.players:
            self.players.remove(telegram_id)
            return True
        return False

    def start(self) -> dict[str, Any]:
        self.is_over = False
        self.current_q_index = 0
        return self.serialize()

    def handle_move(self, telegram_id: int, move_data: dict[str, Any]) -> GameMoveResult:
        if not self.validate(telegram_id, move_data):
            return GameMoveResult(success=False, message="Invalid option selected.")

        option = int(move_data["option"])
        curr_q = self.QUESTIONS[self.current_q_index]

        if option == curr_q["answer"]:
            self.scores[telegram_id] = self.scores.get(telegram_id, 0) + 10
            msg = "Correct answer! +10 Points"
        else:
            msg = "Wrong answer!"

        # Advance to next question
        self.current_q_index += 1
        if self.current_q_index >= len(self.QUESTIONS):
            self.is_over = True
            max_score = -1
            for p, sc in self.scores.items():
                if sc > max_score:
                    max_score = sc
                    self.winner_id = p
            return GameMoveResult(
                success=True,
                message=f"Trivia Battle Finished! Winner: {self.winner_id}",
                is_game_over=True,
                winner_user_id=self.winner_id,
            )

        return GameMoveResult(success=True, message=msg)

    def next_turn(self) -> int | None:
        return self.players[0] if self.players else None

    def pause(self) -> bool:
        return True

    def resume(self) -> bool:
        return True

    def end(self, reason: str = "COMPLETED") -> dict[str, Any]:
        self.is_over = True
        return self.serialize()

    def serialize(self) -> dict[str, Any]:
        return {
            "current_q_index": self.current_q_index,
            "scores": {str(k): v for k, v in self.scores.items()},
            "players": self.players,
            "is_over": self.is_over,
            "winner_id": self.winner_id,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.current_q_index = state_data.get("current_q_index", 0)
        raw_sc = state_data.get("scores", {})
        self.scores = {int(k): v for k, v in raw_sc.items()}
        self.players = state_data.get("players", [])
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or telegram_id not in self.players:
            return False
        opt = move_data.get("option")
        return opt is not None and 0 <= int(opt) <= 3

    def timeout(self) -> GameMoveResult:
        self.is_over = True
        return GameMoveResult(success=True, message="Trivia match timed out.", is_game_over=True)

    def render(self, language_code: str = "en") -> str:
        if self.is_over:
            return f"🧠 *Trivia Battle*\n\nGame Over!\nWinner: Player {self.winner_id}"
        q = self.QUESTIONS[self.current_q_index]
        opts = "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(q["options"])])
        return f"🧠 *Trivia Battle* (Q{self.current_q_index + 1}/{len(self.QUESTIONS)})\n\n*{q['question']}*\n\n{opts}"
