# 🎮 TeleGame: Telegram Multiplayer Gaming Platform (Serverless & Plugin-Based)

[![CI Status](https://github.com/telegame/telegame/workflows/CI/badge.svg)](https://github.com/telegame/telegame/actions)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![Aiogram Version](https://img.shields.io/badge/aiogram-3.x-green.svg)](https://docs.aiogram.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TeleGame** is a production-quality, modular, serverless-ready Telegram Multiplayer Gaming Platform built with **Python 3.13**, **Aiogram 3.x**, **SQLAlchemy 2.x Async**, **PostgreSQL**, and **Pydantic v2**.

---

## 🌟 Key Features

- **Dynamic Game Plugin Architecture**: Add new games simply by dropping a folder into `app/games/`. No core engine code edits required!
- **Serverless & VPS-Free**: Designed for **Vercel Functions**, Railway, Render, Docker, or local ASGI execution.
- **Lazy Timer Engine**: Game turn timeouts and expirations are saved as PostgreSQL `expires_at` timestamps—no continuous background VPS `asyncio.sleep` loops needed!
- **State Machine & Group Isolation**: Supports multiple concurrent groups and sessions with single-active-game session locks per group.
- **10 Built-In Games**:
  1. ❌⭕ **Tic-Tac-Toe**
  2. ✊✌✋ **Rock Paper Scissors**
  3. 🔴🟡 **Connect Four**
  4. 🔤 **Hangman**
  5. 📝 **Word Chain**
  6. 🧠 **Trivia Battle**
  7. 🕵️ **Mafia**
  8. 🎴 **UNO**
  9. ♟️ **Chess**
  10. 🎲 **Ludo**
- **Rich Systems**: Elo Rating Engine, Virtual Economy & Daily Streaks, Cosmetic Inventory, Achievements, Daily Quests, Clans, and Telemetry Analytics.
- **Multi-Language Support**: Dynamic English and Bangla (`en`/`bn`) dynamic localization.
- **Built-in Security**: Anti-spam flood protection, rate limiting, and duplicate callback query replay protection.

---

## 🏗️ Architecture Layout

```
TeleGame/
├── api/                   # Vercel Serverless Gateway (api/index.py)
├── app/
│   ├── config/            # Pydantic Settings v2, Startup Validation, Loggers
│   ├── core/              # BaseGame Engine, FSM, Plugin Manager, Session Manager, Lazy Timers
│   ├── database/          # Async Engine, Migration Runner, Default Seeder
│   ├── games/             # Dynamic Game Plugins (Tic-Tac-Toe, Mafia, Trivia, etc.)
│   ├── handlers/          # Aiogram 3 Routers & Controllers
│   ├── i18n/              # Dynamic Localization Engine (en.json, bn.json)
│   ├── middlewares/       # Security, DbSession, UserSync, i18n
│   ├── models/            # SQLAlchemy 2.x Async ORM (UUID Primary Keys)
│   ├── repositories/      # Async Repositories
│   ├── services/          # Business Logic (Economy, Elo Rating, Quests, Admin)
│   └── utils/             # Keyboard Builders & Command Auto-Registration
├── docs/                  # Architecture, Plugin Development & Deployment Guides
├── tests/                 # Comprehensive Pytest suite
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```

---

## 🚀 Quick Start & Local Execution

### 1. Configure Environment
```bash
cp .env.example .env
# Edit .env and supply your BOT_TOKEN and DATABASE_URL
```

### 2. Standard 5-Step Execution Workflow
```bash
python -m venv .venv
python -m pip install -e .[dev]
alembic upgrade head
python -m app.database.seeding
python -m uvicorn app.main:app --reload
```

### 3. Running Unit Tests & Quality Verification
```bash
pytest -v
ruff check .
ruff format --check .
```


---

## 📜 License
Distributed under the MIT License. See `LICENSE` for details.
