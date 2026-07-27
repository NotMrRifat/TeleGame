"""Unit tests for Game Plugin mechanics and AI Opponent."""

from app.core.engine.ai_opponent import compute_ai_move, get_ai_game_player
from app.core.engine.base_game import GamePlayer
from app.games.connect_four.game import GamePlugin as ConnectFourPlugin
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


def test_ai_opponent_computation():
    """Test AI opponent move computation for Tic-Tac-Toe, RPS, and Connect Four."""
    # Test Tic-Tac-Toe AI
    ttt = TicTacToePlugin()
    p1 = GamePlayer(telegram_id=101)
    ai = get_ai_game_player()
    ttt.join(p1)
    ttt.join(ai)

    ttt.handle_move(101, {"cell": 4})  # Center move by human
    ai_move = compute_ai_move("tic_tac_toe", ttt)
    assert ai_move is not None
    assert "cell" in ai_move
    assert ai_move["cell"] in [0, 2, 6, 8]  # AI prefers corners

    # Test RPS AI
    rps = RPSPlugin()
    rps.join(p1)
    rps.join(ai)
    rps_ai_move = compute_ai_move("rock_paper_scissors", rps)
    assert rps_ai_move is not None
    assert rps_ai_move["choice"] in ["rock", "paper", "scissors"]

    # Test Connect Four AI
    c4 = ConnectFourPlugin()
    c4.join(p1)
    c4.join(ai)
    c4_ai_move = compute_ai_move("connect_four", c4)
    assert c4_ai_move is not None
    assert "col" in c4_ai_move
    assert 0 <= c4_ai_move["col"] <= 6
