# 🛠️ TeleGame Local Development Setup Guide

Follow these steps to set up TeleGame locally on your machine.

## Prerequisites

- **Python**: 3.13 or higher
- **PostgreSQL**: Local PostgreSQL instance or Supabase
- **Git**

## Step-by-Step Setup

### 1. Clone Repository
```bash
git clone https://github.com/telegame/telegame.git
cd TeleGame
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Package in Editable Mode
```bash
python -m pip install -e .[dev]
```

### 4. Create Environment Configuration
```bash
copy .env.example .env  # On Windows
cp .env.example .env    # On Linux/macOS
```
Fill in your `BOT_TOKEN` and `DATABASE_URL`.

### 5. Run Migrations & Seeder
```bash
alembic upgrade head
python -m app.database.seeding
```

### 6. Start Development Server
```bash
python -m uvicorn app.main:app --reload
```
The platform is now active and listening on `http://localhost:8000`.
