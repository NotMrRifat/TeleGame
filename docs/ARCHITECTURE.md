# 🏛️ TeleGame Architecture Overview

## Core Design Principles

1. **Decoupled Engine & Plugin Separation**: The core game engine (`app/core/engine/`) communicates with games solely through the `BaseGame` abstract interface.
2. **Serverless-First Execution**: State is persisted exclusively in PostgreSQL using JSONB fields for game states and UTC `expires_at` for timeouts.
3. **Session Isolation**: Every group chat has a single active `SessionModel` locked to prevent multi-game interference.
4. **Decoupled Event Bus**: Subsystems communicate asynchronously via `event_dispatcher`.

## Data Models Summary
- `users`: Stores statistics, coins, XP, levels, cosmetics equipment.
- `groups`: Stores group chat profiles and group-specific settings.
- `sessions`: Stores active/historical game session state JSONB.
- `ratings`: Elo ratings per game per player.
- `achievements` & `user_achievements`: Track unlockable milestones.
- `clans`: Social clan hierarchy and rankings.
