"""Unit tests for Database models and Seeding."""

from app.models.domain import GameModel, UserModel


def test_user_model_instantiation():
    """Test UserModel field attributes."""
    user = UserModel(
        telegram_id=123456789,
        first_name="Test",
        username="testuser",
        coins=100,
        role="player",
    )
    assert user.telegram_id == 123456789
    assert user.coins == 100
    assert user.role == "player"
    user_dict = user.to_dict()
    assert user_dict["first_name"] == "Test"


def test_game_model_instantiation():
    """Test GameModel field attributes."""
    game = GameModel(
        slug="test_game",
        title="Test Game",
        description="A game for testing",
        min_players=2,
        is_enabled=True,
    )
    assert game.slug == "test_game"
    assert game.min_players == 2
    assert game.is_enabled is True
