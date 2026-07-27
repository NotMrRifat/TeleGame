# 📜 TeleGame Changelog

All notable changes to the TeleGame platform will be documented in this file.

## [1.0.0] - 2026-07-27

### Added
- **Plugin Architecture**: Dynamic discovery engine supporting 10 built-in game plugins.
- **Serverless & Lazy Timer**: PostgreSQL-backed `expires_at` lazy timer engine eliminating VPS dependencies.
- **Database Layer**: SQLAlchemy 2.x Async schema with UUID primary keys and Alembic migration suite.
- **Security**: Anti-spam flood protection, rate limiting, duplicate callback query prevention.
- **Multi-Language Support**: Dynamic English and Bangla (`en`/`bn`) dynamic translations.
- **FastAPI Endpoints**: `/health`, `/readiness`, `/metrics`, `/webhook`, and `/api/cron/cleanup`.
- **Packaging & Deployment**: Setuptools packaging configuration, Dockerfile, docker-compose, and Vercel handler.
