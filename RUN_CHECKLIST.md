# 📋 TeleGame Real Execution & Run Checklist

This checklist documents the exact commands, expected outputs, database tables, API responses, and troubleshooting steps for verifying the **TeleGame** platform.

---

## 1. Commands to Run & Verification Workflow

### Step 1: Environment Setup
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate
```

### Step 2: Install Package in Editable Mode
```bash
python -m pip install -e .[dev]
```
**Expected Output:** `Successfully installed telegame-1.0.0`

### Step 3: Dependency Check
```bash
python -m pip check
```
**Expected Output:** `No broken requirements found.`

### Step 4: Code Quality & Linting
```bash
python -m ruff check .
python -m black --check .
```
**Expected Output:** `All checks passed!` & `All done! 74 files would be left unchanged.`

### Step 5: Test Suite Execution
```bash
python -m pytest -v --asyncio-mode=auto
```
**Expected Output:** `11 passed in X.XXs`

---

## 2. Expected Database Tables

Running `alembic upgrade head` or starting `app.main` auto-initializes the following 15 PostgreSQL ORM tables:

1. `users` — Player profiles, levels, coins, cosmetic titles/frames/themes.
2. `groups` — Group chat configurations and settings.
3. `games` — Registered game plugins registry.
4. `sessions` — Active and historical game session JSONB state.
5. `session_players` — Junction connecting users to active game sessions.
6. `moves` — History of played moves.
7. `ratings` — Elo ratings per game per player.
8. `achievements` — Registry of unlockable platform achievements.
9. `user_achievements` — Unlocked milestones per user.
10. `inventory` — Player cosmetics inventory.
11. `quests` — Daily and weekly quest definitions.
12. `clans` — Social clan rankings and vaults.
13. `friendships` — Friend relationships and pending invites.
14. `settings` — Dynamic system key-value configuration.
15. `analytics_logs` — System telemetry and play counts.

---

## 3. Expected API & Health Responses

### `GET http://localhost:8000/`
```json
{
  "status": "online",
  "app": "TeleGame",
  "version": "1.0.0",
  "environment": "development"
}
```

### `GET http://localhost:8000/health`
```json
{
  "status": "ok",
  "uptime_seconds": 120
}
```

### `GET http://localhost:8000/readiness`
```json
{
  "status": "ready",
  "database": "connected"
}
```

### `GET http://localhost:8000/metrics`
```json
{
  "loaded_games_count": 10,
  "available_plugins": [
    "chess",
    "connect_four",
    "hangman",
    "ludo",
    "mafia",
    "rock_paper_scissors",
    "tic_tac_toe",
    "trivia",
    "uno",
    "word_chain"
  ],
  "uptime_seconds": 120
}
```

---

## 4. Expected Telegram Slash Command Responses

| Command | Expected Telegram Response |
| :--- | :--- |
| `/start` | Welcome menu with numbered onboarding guide and dynamic Inline Keyboard buttons |
| `/games` | Interactive list of all 10 game plugins with step-by-step start guide |
| `/newgame tic_tac_toe` | Lobby initialized message with instructions for players to `/join` and host to `/startgame` |
| `/join` | Confirmation of player entry and updated player capacity count |
| `/profile` | Detailed player card showing level, XP, coins, wins, losses, and win rate |
| `/daily` | Daily streak claim notification showing earned coins and streak counter |
| `/leaderboard` | Top 10 seasonal Elo rating leaderboard |
| `/admin` | Admin dashboard listing moderation tools |

---

## 5. Common Errors & Solutions

### Issue: `DATABASE_URL` Connection Failed
- **Cause**: PostgreSQL is not running or credentials in `.env` are incorrect.
- **Solution**: Ensure PostgreSQL container or Supabase is running, then verify `DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname`.

### Issue: Bot token validation warning on boot
- **Cause**: `BOT_TOKEN` in `.env` is set to placeholder value.
- **Solution**: Obtain a real bot token from [@BotFather](https://t.me/BotFather) and update `.env`.
