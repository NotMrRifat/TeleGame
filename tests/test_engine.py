"""Unit tests for Core Game Engine, FSM, and Plugin Manager."""

import pytest

from app.core.engine.fsm import GameFSM, GameState, InvalidStateTransitionError
from app.core.engine.plugin_manager import plugin_manager
from app.games.tic_tac_toe.game import GamePlugin as TicTacToePlugin


def test_plugin_discovery():
    """Verify dynamic discovery of game plugins."""
    plugins = plugin_manager.discover_plugins()
    assert "tic_tac_toe" in plugins
    assert "rock_paper_scissors" in plugins
    assert "connect_four" in plugins
    assert plugins["tic_tac_toe"] == TicTacToePlugin


def test_fsm_valid_transitions():
    """Test valid FSM state transitions."""
    fsm = GameFSM(initial_state=GameState.LOBBY)
    assert fsm.current_state == GameState.LOBBY
    fsm.transition_to(GameState.PLAYING)
    assert fsm.current_state == GameState.PLAYING
    fsm.transition_to(GameState.FINISHED)
    assert fsm.current_state == GameState.FINISHED


def test_fsm_invalid_transition():
    """Test invalid FSM state transition raises exception."""
    fsm = GameFSM(initial_state=GameState.FINISHED)
    with pytest.raises(InvalidStateTransitionError):
        fsm.transition_to(GameState.PLAYING)
