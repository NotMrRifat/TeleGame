"""Word Chain Game Plugin."""

from typing import Any

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Word Chain multiplayer word matching plugin."""

    slug = "word_chain"
    title = "Word Chain"
    description = "Chain words using the last letter of the previous word"
    min_players = 2
    max_players = 10

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.used_words: list[str] = ["PYTHON"]
            self.last_letter: str = "N"
            self.players: list[int] = []
            self.turn_index: int = 0
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.used_words = ["PYTHON"]
        self.last_letter = "N"
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
        self.turn_index = 0
        return self.serialize()

    def handle_move(self, telegram_id: int, move_data: dict[str, Any]) -> GameMoveResult:
        if not self.validate(telegram_id, move_data):
            return GameMoveResult(
                success=False,
                message=f"Word must start with letter '{self.last_letter}' and be unused.",
            )

        word = move_data["word"].upper()
        self.used_words.append(word)
        self.last_letter = word[-1]

        # Rotate turn to next player
        self.turn_index = (self.turn_index + 1) % len(self.players)
        return GameMoveResult(
            success=True,
            message=f"Accepted word '{word}'! Next word must start with '{self.last_letter}'.",
            next_turn_user_id=self.players[self.turn_index],
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
            "used_words": self.used_words,
            "last_letter": self.last_letter,
            "players": self.players,
            "turn_index": self.turn_index,
            "is_over": self.is_over,
            "winner_id": self.winner_id,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.used_words = state_data.get("used_words", ["PYTHON"])
        self.last_letter = state_data.get("last_letter", "N")
        self.players = state_data.get("players", [])
        self.turn_index = state_data.get("turn_index", 0)
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or not self.players:
            return False
        if telegram_id != self.players[self.turn_index]:
            return False
        word = move_data.get("word", "").upper()
        if not word or word in self.used_words:
            return False
        return word[0] == self.last_letter

    def timeout(self) -> GameMoveResult:
        if not self.players:
            return GameMoveResult(success=True, message="Game timed out.", is_game_over=True)
        eliminated_id = self.players[self.turn_index]
        self.players.remove(eliminated_id)
        if len(self.players) <= 1:
            self.is_over = True
            self.winner_id = self.players[0] if self.players else None
            return GameMoveResult(
                success=True,
                message=f"Player {eliminated_id} timed out. Game Over!",
                is_game_over=True,
                winner_user_id=self.winner_id,
            )
        self.turn_index = self.turn_index % len(self.players)
        return GameMoveResult(
            success=True,
            message=f"Player {eliminated_id} timed out and was eliminated.",
            next_turn_user_id=self.players[self.turn_index],
        )

    def render(self, language_code: str = "en") -> str:
        last_word = self.used_words[-1] if self.used_words else "NONE"
        if self.is_over:
            return (
                f"📝 *Word Chain*\n\nWinner: {self.winner_id}\nTotal Words: {len(self.used_words)}"
            )
        return f"📝 *Word Chain*\n\nLast Word: `{last_word}`\nNext Letter: *{self.last_letter}*\nTurn: Player {self.players[self.turn_index]}"
