"""Core package initialization."""

from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer
from app.core.engine.fsm import GameFSM, GameState, InvalidStateTransitionError
from app.core.engine.plugin_manager import plugin_manager
from app.core.engine.session_manager import ActiveSessionConflictError, SessionManager
from app.core.events.dispatcher import event_dispatcher
from app.core.scheduler.timer import LazyTimerEngine, cleanup_expired_sessions

__all__ = [
    "BaseGame",
    "GamePlayer",
    "GameMoveResult",
    "GameState",
    "GameFSM",
    "InvalidStateTransitionError",
    "plugin_manager",
    "SessionManager",
    "ActiveSessionConflictError",
    "event_dispatcher",
    "LazyTimerEngine",
    "cleanup_expired_sessions",
]
