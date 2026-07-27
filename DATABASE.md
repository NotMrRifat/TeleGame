# 🗄️ TeleGame Database Schema Documentation

All database tables use PostgreSQL with `UUIDv4` primary keys, UTC timestamp audit columns (`created_at`, `updated_at`), and `is_deleted` soft-delete flags.

## Entity Relationship Summary

### `users`
Stores player profiles, levels, virtual coin balances, cosmetic equipment, and win/loss statistics.
- `id` (UUID, Primary Key)
- `telegram_id` (BigInteger, Unique Index)
- `username` (String)
- `coins`, `xp`, `level`, `wins`, `losses`, `draws`, `daily_streak`
- `avatar`, `title`, `frame`, `theme`
- `role` (player, admin, superadmin, owner)

### `groups`
Stores Telegram group chat metadata and preferences.
- `id` (UUID, Primary Key)
- `telegram_chat_id` (BigInteger, Unique Index)
- `title`, `language_code`, `settings` (JSONB)

### `sessions` & `session_players`
Stores active and historical game sessions.
- `group_id` (ForeignKey -> groups.id)
- `game_slug` (String, Index)
- `status` (LOBBY, PLAYING, PAUSED, FINISHED, CANCELLED, TIMEOUT)
- `state_data` (JSONB)
- `expires_at` (DateTime, UTC Index)

### `ratings`
Elo ratings per player per game.
- `user_id` (ForeignKey -> users.id)
- `game_slug` (String)
- `elo`, `peak_elo`, `season`

### `achievements`, `user_achievements`, `inventory`, `quests`, `clans`
Auxiliary tables for achievements, cosmetics inventory, daily quests, and clan rankings.
