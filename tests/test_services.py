"""Unit tests for Platform Services."""

import pytest

from app.services.rating_service import RatingService
from app.services.security_service import RateLimitExceededError, security_service


def test_elo_math_calculation():
    """Test expected score formula for Elo calculation."""
    # Equal rating expects 50% score
    exp = RatingService.calculate_expected_score(1200, 1200)
    assert pytest.approx(exp, 0.01) == 0.5

    # Higher rating expects higher win probability
    exp_high = RatingService.calculate_expected_score(1600, 1200)
    assert exp_high > 0.9


def test_security_rate_limiting():
    """Test security rate limit validation."""
    user_id = 999888
    # First call succeeds
    assert security_service.validate_rate_limit(user_id) is True

    # Immediate second call raises RateLimitExceededError
    with pytest.raises(RateLimitExceededError):
        security_service.validate_rate_limit(user_id)
