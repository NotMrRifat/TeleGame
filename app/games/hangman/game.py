"""Hangman Game Plugin."""

from typing import Any

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    """Hangman word guessing game plugin."""

    slug = "hangman"
    title = "Hangman"
    description = "Guess the hidden word before running out of attempts"
    min_players = 1
    max_players = 8

    def __init__(self, state_data: dict[str, Any] | None = None):
        super().__init__(state_data)
        if not self.state_data:
            self.target_word: str = "TELEGRAM"
            self.guessed_letters: list[str] = []
            self.max_attempts: int = 6
            self.wrong_attempts: int = 0
            self.players: list[int] = []
            self.is_over: bool = False
            self.winner_id: int | None = None
        else:
            self.deserialize(self.state_data)

    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        self.target_word = "TELEGRAM"
        self.guessed_letters = []
        self.wrong_attempts = 0
        self.players = [p.telegram_id for p in players]
        self.is_over = False
        self.winner_id = None
        return self.serialize()

    def join(self, player: GamePlayer) -> bool:
        if player.telegram_id not in self.players:
            self.players.append(player.telegram_id)
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
            return GameMoveResult(success=False, message="Invalid letter choice.")

        letter = move_data["letter"].upper()
        self.guessed_letters.append(letter)

        if letter not in self.target_word:
            self.wrong_attempts += 1

        # Check win condition
        if all(ch in self.guessed_letters for ch in self.target_word):
            self.is_over = True
            self.winner_id = telegram_id
            return GameMoveResult(
                success=True,
                message=f"Word guessed correctly! The word was {self.target_word}",
                is_game_over=True,
                winner_user_id=telegram_id,
            )

        # Check loss condition
        if self.wrong_attempts >= self.max_attempts:
            self.is_over = True
            return GameMoveResult(
                success=True,
                message=f"Out of attempts! The word was {self.target_word}",
                is_game_over=True,
            )

        return GameMoveResult(success=True, message=f"Letter '{letter}' processed.")

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
            "target_word": self.target_word,
            "guessed_letters": self.guessed_letters,
            "wrong_attempts": self.wrong_attempts,
            "max_attempts": self.max_attempts,
            "players": self.players,
            "is_over": self.is_over,
            "winner_id": self.winner_id,
        }

    def deserialize(self, state_data: dict[str, Any]) -> None:
        self.target_word = state_data.get("target_word", "TELEGRAM")
        self.guessed_letters = state_data.get("guessed_letters", [])
        self.wrong_attempts = state_data.get("wrong_attempts", 0)
        self.max_attempts = state_data.get("max_attempts", 6)
        self.players = state_data.get("players", [])
        self.is_over = state_data.get("is_over", False)
        self.winner_id = state_data.get("winner_id")

    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        if self.is_over or telegram_id not in self.players:
            return False
        letter = move_data.get("letter", "").upper()
        return len(letter) == 1 and letter.isalpha() and letter not in self.guessed_letters

    def timeout(self) -> GameMoveResult:
        self.is_over = True
        return GameMoveResult(success=True, message="Hangman game timed out.", is_game_over=True)

    def render(self, language_code: str = "en") -> str:
        word_display = " ".join(
            [ch if ch in self.guessed_letters else "_" for ch in self.target_word]
        )
        stages = ["🪢", "😐", "👕", "👖", "👟", "💀"]
        stage = stages[min(self.wrong_attempts, len(stages) - 1)]
        if self.is_over:
            return f"🔤 *Hangman*\n\nWord: {self.target_word}\n\nGame Over!"
        return f"🔤 *Hangman*\n\nWord: {word_display}\nAttempts Left: {self.max_attempts - self.wrong_attempts} {stage}"
