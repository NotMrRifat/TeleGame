"""Unit tests for Settings parsing and Startup validation."""

import pytest

from app.config.settings import Settings
from app.config.startup import validate_startup_configuration


def test_settings_parsing():
    """Verify settings parse comma-separated lists and optional numeric IDs cleanly."""
    settings = Settings(
        ADMIN_IDS="100, 200, 300",
        SUPER_ADMIN_IDS="100",
        SUPPORTED_LANGUAGES="en, bn, es",
        BOT_ID="",
        OWNER_ID="555",
    )
    assert settings.ADMIN_IDS == [100, 200, 300]
    assert settings.SUPER_ADMIN_IDS == [100]
    assert settings.SUPPORTED_LANGUAGES == ["en", "bn", "es"]
    assert settings.BOT_ID == 0
    assert settings.OWNER_ID == 555


@pytest.mark.asyncio
async def test_startup_validation():
    """Verify validate_startup_configuration returns True."""
    res = await validate_startup_configuration()
    assert res is True
