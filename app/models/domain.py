"""Domain ORM models for TeleGame platform."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class UserModel(Base):
    """User profile model storing player statistics, virtual balance, and cosmetic equipment."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), default="bn", nullable=False)

    # Economics & Stats
    coins: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    wins: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    losses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    draws: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    daily_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_daily_claim: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Cosmetics & Customization
    avatar: Mapped[str] = mapped_column(String(128), default="default", nullable=False)
    title: Mapped[str] = mapped_column(String(128), default="Novice", nullable=False)
    frame: Mapped[str] = mapped_column(String(128), default="default", nullable=False)
    theme: Mapped[str] = mapped_column(String(128), default="classic", nullable=False)
    favorite_game: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Roles & Clan
    role: Mapped[str] = mapped_column(
        String(32), default="player", nullable=False
    )  # player, admin, owner
    clan_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clans.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    ratings: Mapped[list["RatingModel"]] = relationship(
        "RatingModel", back_populates="user", cascade="all, delete-orphan"
    )
    inventory: Mapped[list["InventoryModel"]] = relationship(
        "InventoryModel", back_populates="user", cascade="all, delete-orphan"
    )
    achievements: Mapped[list["UserAchievementModel"]] = relationship(
        "UserAchievementModel", back_populates="user", cascade="all, delete-orphan"
    )


class GroupModel(Base):
    """Telegram Group/Chat model."""

    __tablename__ = "groups"

    telegram_chat_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    type: Mapped[str] = mapped_column(String(32), default="supergroup", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    language_code: Mapped[str] = mapped_column(String(10), default="bn", nullable=False)
    settings: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)


class GameModel(Base):
    """Game Plugin Registry Model."""

    __tablename__ = "games"

    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    min_players: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    max_players: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    category: Mapped[str] = mapped_column(String(64), default="casual", nullable=False)
    version: Mapped[str] = mapped_column(String(32), default="1.0.0", nullable=False)


class SessionModel(Base):
    """Active or Completed Game Session Model for a Telegram Group."""

    __tablename__ = "sessions"

    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True
    )
    game_slug: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(32), default="LOBBY", nullable=False, index=True
    )  # LOBBY, PLAYING, PAUSED, FINISHED, CANCELLED, TIMEOUT
    current_turn_user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    state_data: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    winner_user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    players: Mapped[list["PlayerSessionModel"]] = relationship(
        "PlayerSessionModel", back_populates="session", cascade="all, delete-orphan"
    )
    moves: Mapped[list["MoveModel"]] = relationship(
        "MoveModel", back_populates="session", cascade="all, delete-orphan"
    )


class PlayerSessionModel(Base):
    """Junction model connecting Users to Game Sessions."""

    __tablename__ = "session_players"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    role: Mapped[str] = mapped_column(String(32), default="player", nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    player_data: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="players")


class MoveModel(Base):
    """History of moves played in game sessions."""

    __tablename__ = "moves"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    move_type: Mapped[str] = mapped_column(String(64), nullable=False)
    move_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    turn_number: Mapped[int] = mapped_column(Integer, nullable=False)

    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="moves")


class RatingModel(Base):
    """Elo Rating per game per user."""

    __tablename__ = "ratings"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    game_slug: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    elo: Mapped[int] = mapped_column(Integer, default=1200, nullable=False, index=True)
    peak_elo: Mapped[int] = mapped_column(Integer, default=1200, nullable=False)
    season: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="ratings")


class AchievementModel(Base):
    """Global Registry of Unlockable Achievements."""

    __tablename__ = "achievements"

    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(32), default="🏆", nullable=False)
    reward_coins: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    reward_xp: Mapped[int] = mapped_column(Integer, default=100, nullable=False)


class UserAchievementModel(Base):
    """User Unlocked Achievements model."""

    __tablename__ = "user_achievements"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    achievement_slug: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_unlocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    unlocked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="achievements")


class InventoryModel(Base):
    """User Cosmetics Inventory."""

    __tablename__ = "inventory"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    item_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # avatar, frame, title, theme
    item_slug: Mapped[str] = mapped_column(String(64), nullable=False)
    is_equipped: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="inventory")


class QuestModel(Base):
    """Daily/Weekly/Seasonal Quests."""

    __tablename__ = "quests"

    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quest_type: Mapped[str] = mapped_column(
        String(32), default="DAILY", nullable=False
    )  # DAILY, WEEKLY, SEASONAL
    target_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    reward_coins: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    reward_xp: Mapped[int] = mapped_column(Integer, default=200, nullable=False)


class ClanModel(Base):
    """Social Clans Model."""

    __tablename__ = "clans"

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    tag: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    owner_telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    total_xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    coins_vault: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class FriendshipModel(Base):
    """Friendship & Friend Requests."""

    __tablename__ = "friendships"

    user_telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    friend_telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(32), default="PENDING", nullable=False
    )  # PENDING, ACCEPTED, BLOCKED


class SystemSettingModel(Base):
    """Dynamic key-value settings storage."""

    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    value: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class AnalyticsLogModel(Base):
    """Telemetry and system log storage."""

    __tablename__ = "analytics_logs"

    event_name: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    group_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
