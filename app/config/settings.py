"""Application configuration module using Pydantic Settings."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Platform configuration settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # Bot Configuration
    BOT_TOKEN: str = Field(default="123456789:ABCdefGHIjklMNOpqrSTUvwxYZ_sample_token")
    BOT_USERNAME: str = Field(default="TeleGameMasterBot")
    BOT_ID: int = Field(default=123456789)

    # Webhook & Serverless Settings
    WEBHOOK_SECRET: str = Field(default="super_secret_webhook_token_32_chars_long")
    WEBHOOK_URL: str = Field(default="https://elitetelegame.vercel.app")
    WEBHOOK_PATH: str = Field(default="/webhook")

    # Environment
    APP_ENV: str = Field(default="development")
    ENVIRONMENT: str = Field(default="development")
    APP_NAME: str = Field(default="TeleGame")
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")

    # Database & Storage
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/telegame"
    )
    SUPABASE_URL: str = Field(default="https://xyzcompany.supabase.co")
    SUPABASE_KEY: str = Field(default="sample_supabase_key")
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # Security
    SECRET_KEY: str = Field(default="super-secret-key-change-this-in-production-min-32-chars")
    SESSION_SECRET: str = Field(default="session-secret-key-change-this-in-production-min-32-chars")
    JWT_SECRET: str = Field(default="jwt-secret-key-change-this-in-production-min-32-chars")
    ENCRYPTION_KEY: str = Field(default="encryption-secret-key-change-this-32b")

    # Access Control Lists
    ADMIN_IDS: list[int] | str = Field(default_factory=lambda: [12345678, 87654321])
    SUPER_ADMIN_IDS: list[int] | str = Field(default_factory=lambda: [12345678])
    OWNER_ID: int | str = Field(default=12345678)
    BOT_ID: int | str = Field(default=123456789)

    # Localization
    SUPPORTED_LANGUAGES: list[str] | str = Field(default_factory=lambda: ["en", "bn"])
    DEFAULT_LANGUAGE: str = Field(default="bn")
    TIMEZONE: str = Field(default="Asia/Dhaka")
    DEFAULT_CURRENCY: str = Field(default="COINS")
    DEFAULT_THEME: str = Field(default="classic")
    DEFAULT_AVATAR: str = Field(default="default")

    # Game & Session Timeouts (Seconds)
    TURN_TIMEOUT: int = Field(default=60)
    LOBBY_TIMEOUT: int = Field(default=180)
    GAME_TIMEOUT: int = Field(default=1800)
    SESSION_TIMEOUT: int = Field(default=3600)
    MAX_ACTIVE_GAMES_PER_GROUP: int = Field(default=1)
    MAX_PLAYERS_PER_GAME: int = Field(default=32)
    RATE_LIMIT_SECONDS: int = Field(default=2)

    # Feature Flags
    ENABLE_ANALYTICS: bool = Field(default=True)
    ENABLE_LEADERBOARD: bool = Field(default=True)
    ENABLE_QUESTS: bool = Field(default=True)
    ENABLE_CLANS: bool = Field(default=True)
    ENABLE_ECONOMY: bool = Field(default=True)
    ENABLE_SHOP: bool = Field(default=True)
    ENABLE_NOTIFICATIONS: bool = Field(default=True)
    ENABLE_LOGGING: bool = Field(default=True)
    ENABLE_DEBUG_COMMANDS: bool = Field(default=False)

    @field_validator("WEBHOOK_URL", mode="before")
    @classmethod
    def parse_webhook_url(cls, val: object) -> str:
        """Ensure WEBHOOK_URL has https:// or http:// scheme."""
        if not val:
            return "https://elitetelegame.vercel.app"
        s_val = str(val).strip()
        if not s_val.startswith(("https://", "http://")):
            return f"https://{s_val}"
        return s_val

    @field_validator("ADMIN_IDS", "SUPER_ADMIN_IDS", mode="before")
    @classmethod
    def parse_int_list(cls, val: object) -> list[int]:
        """Convert comma-separated strings or list values to integer lists."""
        if val is None or val == "":
            return []
        if isinstance(val, str):
            if val.startswith("[") and val.endswith("]"):
                import json

                try:
                    parsed = json.loads(val)
                    return [int(x) for x in parsed if x is not None]
                except Exception:
                    pass
            items = [item.strip() for item in val.split(",") if item.strip()]
            return [int(x) for x in items]
        if isinstance(val, (list, tuple)):
            return [int(x) for x in val if x is not None]
        return [int(val)]

    @field_validator("SUPPORTED_LANGUAGES", mode="before")
    @classmethod
    def parse_str_list(cls, val: object) -> list[str]:
        """Convert comma-separated strings or list values to string lists."""
        if val is None or val == "":
            return ["en"]
        if isinstance(val, str):
            if val.startswith("[") and val.endswith("]"):
                import json

                try:
                    parsed = json.loads(val)
                    return [str(x).strip() for x in parsed if str(x).strip()]
                except Exception:
                    pass
            return [x.strip() for x in val.split(",") if x.strip()]
        if isinstance(val, (list, tuple)):
            return [str(x).strip() for x in val if str(x).strip()]
        return [str(val).strip()]

    @field_validator("BOT_ID", "OWNER_ID", mode="before")
    @classmethod
    def parse_int_val(cls, val: object) -> int:
        """Convert string or empty values to int safely."""
        if val is None or val == "":
            return 0
        return int(val)

    @property
    def full_webhook_url(self) -> str:
        """Returns the complete webhook URL."""
        import os

        base = self.WEBHOOK_URL.rstrip("/")
        vercel_url = os.getenv("VERCEL_URL")
        if vercel_url and ("telegame.vercel.app" in base or not base):
            base = f"https://{vercel_url}"
        path = self.WEBHOOK_PATH if self.WEBHOOK_PATH.startswith("/") else f"/{self.WEBHOOK_PATH}"
        return f"{base}{path}"


settings = Settings()
