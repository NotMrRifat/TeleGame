"""BaseGame abstract class defining the universal interface for all TeleGame plugins."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class GamePlayer(BaseModel):
    """Player representation within an active game instance."""

    telegram_id: int
    username: str | None = None
    role: str = "player"
    score: int = 0
    is_active: bool = True
    player_state: dict[str, Any] = {}


class GameMoveResult(BaseModel):
    """Result returned after processing a game move."""

    success: bool
    message: str
    state_changed: bool = True
    next_turn_user_id: int | None = None
    is_game_over: bool = False
    winner_user_id: int | None = None
    is_draw: bool = False
    extra_data: dict[str, Any] = {}


class BaseGame(ABC):
    """Universal abstract base class for all game plugins."""

    slug: str
    title: str
    description: str
    min_players: int = 2
    max_players: int = 2

    def __init__(self, state_data: dict[str, Any] | None = None):
        self.state_data: dict[str, Any] = state_data or {}

    @abstractmethod
    def initialize(self, players: list[GamePlayer]) -> dict[str, Any]:
        """Initialize new game session state given participating players."""
        pass

    @abstractmethod
    def join(self, player: GamePlayer) -> bool:
        """Add a player to the pending game lobby."""
        pass

    @abstractmethod
    def leave(self, telegram_id: int) -> bool:
        """Remove a player from the game session."""
        pass

    @abstractmethod
    def start(self) -> dict[str, Any]:
        """Transition game from LOBBY to PLAYING state."""
        pass

    @abstractmethod
    def handle_move(self, telegram_id: int, move_data: dict[str, Any]) -> GameMoveResult:
        """Process player move and return updated state result."""
        pass

    @abstractmethod
    def next_turn(self) -> int | None:
        """Determine and return Telegram User ID of the next player."""
        pass

    @abstractmethod
    def pause(self) -> bool:
        """Pause active game session."""
        pass

    @abstractmethod
    def resume(self) -> bool:
        """Resume paused game session."""
        pass

    @abstractmethod
    def end(self, reason: str = "COMPLETED") -> dict[str, Any]:
        """Finalize game session and return final results summary."""
        pass

    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Serialize current in-memory game state to JSON-compatible dict."""
        pass

    @abstractmethod
    def deserialize(self, state_data: dict[str, Any]) -> None:
        """Restore in-memory game state from JSON-compatible dict."""
        pass

    @abstractmethod
    def validate(self, telegram_id: int, move_data: dict[str, Any]) -> bool:
        """Validate if a move is legal according to game rules."""
        pass

    @abstractmethod
    def timeout(self) -> GameMoveResult:
        """Handle turn timeout when time limit expires."""
        pass

    @abstractmethod
    def render(self, language_code: str = "en") -> str:
        """Render formatted Telegram markdown message for current game board state."""
        pass
