"""Initial database schema.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-07-27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

revision: str = "001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Clans table
    op.create_table(
        "clans",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(64), unique=True, nullable=False, index=True),
        sa.Column("tag", sa.String(10), unique=True, nullable=False),
        sa.Column("owner_telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("total_xp", sa.Integer(), default=0, nullable=False),
        sa.Column("coins_vault", sa.Integer(), default=0, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 2. Users table
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), unique=True, nullable=False, index=True),
        sa.Column("username", sa.String(64), nullable=True, index=True),
        sa.Column("first_name", sa.String(64), nullable=False),
        sa.Column("last_name", sa.String(64), nullable=True),
        sa.Column("language_code", sa.String(10), default="bn", nullable=False),
        sa.Column("coins", sa.Integer(), default=100, nullable=False),
        sa.Column("xp", sa.Integer(), default=0, nullable=False),
        sa.Column("level", sa.Integer(), default=1, nullable=False),
        sa.Column("wins", sa.Integer(), default=0, nullable=False),
        sa.Column("losses", sa.Integer(), default=0, nullable=False),
        sa.Column("draws", sa.Integer(), default=0, nullable=False),
        sa.Column("games_played", sa.Integer(), default=0, nullable=False),
        sa.Column("daily_streak", sa.Integer(), default=0, nullable=False),
        sa.Column("last_daily_claim", sa.DateTime(timezone=True), nullable=True),
        sa.Column("avatar", sa.String(128), default="default", nullable=False),
        sa.Column("title", sa.String(128), default="Novice", nullable=False),
        sa.Column("frame", sa.String(128), default="default", nullable=False),
        sa.Column("theme", sa.String(128), default="classic", nullable=False),
        sa.Column("favorite_game", sa.String(64), nullable=True),
        sa.Column("role", sa.String(32), default="player", nullable=False),
        sa.Column(
            "clan_id",
            UUID(as_uuid=True),
            sa.ForeignKey("clans.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 3. Groups table
    op.create_table(
        "groups",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("telegram_chat_id", sa.BigInteger(), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("type", sa.String(32), default="supergroup", nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("language_code", sa.String(10), default="bn", nullable=False),
        sa.Column("settings", JSONB, default=dict, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 4. Games table
    op.create_table(
        "games",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(64), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("min_players", sa.Integer(), default=2, nullable=False),
        sa.Column("max_players", sa.Integer(), default=2, nullable=False),
        sa.Column("is_enabled", sa.Boolean(), default=True, nullable=False),
        sa.Column("category", sa.String(64), default="casual", nullable=False),
        sa.Column("version", sa.String(32), default="1.0.0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 5. Sessions table
    op.create_table(
        "sessions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "group_id",
            UUID(as_uuid=True),
            sa.ForeignKey("groups.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("game_slug", sa.String(64), nullable=False, index=True),
        sa.Column("status", sa.String(32), default="LOBBY", nullable=False, index=True),
        sa.Column("current_turn_user_id", sa.BigInteger(), nullable=True),
        sa.Column("state_data", JSONB, default=dict, nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("winner_user_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 6. Session Players table
    op.create_table(
        "session_players",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "session_id",
            UUID(as_uuid=True),
            sa.ForeignKey("sessions.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False, index=True),
        sa.Column("username", sa.String(64), nullable=True),
        sa.Column("role", sa.String(32), default="player", nullable=False),
        sa.Column("score", sa.Integer(), default=0, nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("player_data", JSONB, default=dict, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 7. Moves table
    op.create_table(
        "moves",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "session_id",
            UUID(as_uuid=True),
            sa.ForeignKey("sessions.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("move_type", sa.String(64), nullable=False),
        sa.Column("move_payload", JSONB, default=dict, nullable=False),
        sa.Column("turn_number", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 8. Ratings table
    op.create_table(
        "ratings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("game_slug", sa.String(64), nullable=False, index=True),
        sa.Column("elo", sa.Integer(), default=1200, nullable=False, index=True),
        sa.Column("peak_elo", sa.Integer(), default=1200, nullable=False),
        sa.Column("season", sa.Integer(), default=1, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 9. Achievements table
    op.create_table(
        "achievements",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(64), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("icon", sa.String(32), default="🏆", nullable=False),
        sa.Column("reward_coins", sa.Integer(), default=50, nullable=False),
        sa.Column("reward_xp", sa.Integer(), default=100, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 10. User Achievements table
    op.create_table(
        "user_achievements",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("achievement_slug", sa.String(64), nullable=False, index=True),
        sa.Column("progress", sa.Integer(), default=0, nullable=False),
        sa.Column("is_unlocked", sa.Boolean(), default=False, nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 11. Inventory table
    op.create_table(
        "inventory",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("item_type", sa.String(32), nullable=False),
        sa.Column("item_slug", sa.String(64), nullable=False),
        sa.Column("is_equipped", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 12. Quests table
    op.create_table(
        "quests",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(64), unique=True, nullable=False, index=True),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("quest_type", sa.String(32), default="DAILY", nullable=False),
        sa.Column("target_count", sa.Integer(), default=1, nullable=False),
        sa.Column("reward_coins", sa.Integer(), default=100, nullable=False),
        sa.Column("reward_xp", sa.Integer(), default=200, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 13. Friendships table
    op.create_table(
        "friendships",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_telegram_id", sa.BigInteger(), nullable=False, index=True),
        sa.Column("friend_telegram_id", sa.BigInteger(), nullable=False, index=True),
        sa.Column("status", sa.String(32), default="PENDING", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 14. System Settings table
    op.create_table(
        "settings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("key", sa.String(128), unique=True, nullable=False, index=True),
        sa.Column("value", JSONB, default=dict, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )

    # 15. Analytics Logs table
    op.create_table(
        "analytics_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("event_name", sa.String(64), nullable=False, index=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=True),
        sa.Column("group_id", UUID(as_uuid=True), nullable=True),
        sa.Column("payload", JSONB, default=dict, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), default=False, nullable=False),
    )


def downgrade() -> None:
    tables = [
        "analytics_logs",
        "settings",
        "friendships",
        "quests",
        "inventory",
        "user_achievements",
        "achievements",
        "ratings",
        "moves",
        "session_players",
        "sessions",
        "games",
        "groups",
        "users",
        "clans",
    ]
    for t in tables:
        op.drop_table(t, if_exists=True)
