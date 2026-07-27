"""Unit tests for Game Plugin mechanics."""

from app.core.engine.base_game import GamePlayer
from app.games.rock_paper_scissors.game import GamePlugin as RPSPlugin
from app.games.tic_tac_toe.game import GamePlugin as TicTacToePlugin


def test_tic_tac_toe_mechanics():
    """Test Tic-Tac-Toe move validation, turns, and win detection."""
    game = TicTacToePlugin()
    p1 = GamePlayer(telegram_id=101, username="Player1")
    p2 = GamePlayer(telegram_id=102, username="Player2")

    game.initialize([p1, p2])
    assert game.next_turn() == 101

    # Row 0 win for P1: 0, 1, 2
    game.handle_move(101, {"cell": 0})  # P1
    game.handle_move(102, {"cell": 3})  # P2
    game.handle_move(101, {"cell": 1})  # P1
    game.handle_move(102, {"cell": 4})  # P2
    res = game.handle_move(101, {"cell": 2})  # P1 wins

    assert res.is_game_over is True
    assert res.winner_user_id == 101


def test_rps_win_mechanics():
    """Test Rock Paper Scissors winner determination."""
    game = RPSPlugin()
    p1 = GamePlayer(telegram_id=101)
    p2 = GamePlayer(telegram_id=102)

    game.initialize([p1, p2])
    game.handle_move(101, {"choice": "rock"})
    res = game.handle_move(102, {"choice": "scissors"})

    assert res.is_game_over is True
    assert res.winner_user_id == 101
