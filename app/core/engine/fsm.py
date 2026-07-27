"""Generic Finite State Machine for game session state transitions."""

from enum import Enum


class GameState(str, Enum):
    """Universal game states supported across all plugins."""

    WAITING = "WAITING"
    LOBBY = "LOBBY"
    PREPARING = "PREPARING"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    VOTING = "VOTING"
    NIGHT = "NIGHT"
    DAY = "DAY"
    ROUND = "ROUND"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"


# Valid State Transitions
ALLOWED_TRANSITIONS: dict[GameState, set[GameState]] = {
    GameState.WAITING: {GameState.LOBBY, GameState.CANCELLED},
    GameState.LOBBY: {
        GameState.PREPARING,
        GameState.PLAYING,
        GameState.CANCELLED,
        GameState.TIMEOUT,
    },
    GameState.PREPARING: {GameState.PLAYING, GameState.CANCELLED},
    GameState.PLAYING: {
        GameState.PAUSED,
        GameState.VOTING,
        GameState.NIGHT,
        GameState.DAY,
        GameState.ROUND,
        GameState.FINISHED,
        GameState.CANCELLED,
        GameState.TIMEOUT,
    },
    GameState.PAUSED: {GameState.PLAYING, GameState.CANCELLED},
    GameState.VOTING: {GameState.DAY, GameState.NIGHT, GameState.FINISHED, GameState.CANCELLED},
    GameState.NIGHT: {GameState.DAY, GameState.VOTING, GameState.FINISHED, GameState.CANCELLED},
    GameState.DAY: {GameState.NIGHT, GameState.VOTING, GameState.FINISHED, GameState.CANCELLED},
    GameState.ROUND: {GameState.PLAYING, GameState.FINISHED, GameState.CANCELLED},
    GameState.FINISHED: set(),
    GameState.CANCELLED: set(),
    GameState.TIMEOUT: set(),
}


class InvalidStateTransitionError(Exception):
    """Error thrown when attempting an unauthorized state transition."""

    pass


class GameFSM:
    """Finite State Machine for managing game session state validity."""

    def __init__(self, initial_state: GameState = GameState.LOBBY):
        self._current_state: GameState = initial_state

    @property
    def current_state(self) -> GameState:
        """Get current state."""
        return self._current_state

    def transition_to(self, new_state: GameState) -> GameState:
        """Transitions to new state if valid.

        Raises:
            InvalidStateTransitionError: If the transition is prohibited.
        """
        allowed = ALLOWED_TRANSITIONS.get(self._current_state, set())
        if new_state not in allowed:
            raise InvalidStateTransitionError(
                f"Cannot transition from {self._current_state.value} to {new_state.value}"
            )
        self._current_state = new_state
        return self._current_state

    def can_transition_to(self, new_state: GameState) -> bool:
        """Check if transition is valid without executing it."""
        allowed = ALLOWED_TRANSITIONS.get(self._current_state, set())
        return new_state in allowed
