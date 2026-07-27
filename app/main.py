"""FastAPI Webhook & Bot ASGI Application Gateway."""

import time
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, HTTPException, Request, Response
from sqlalchemy import text

from app.config.logging import logger
from app.config.settings import settings
from app.config.startup import validate_startup_configuration
from app.core.engine.plugin_manager import plugin_manager
from app.core.scheduler.timer import cleanup_expired_sessions
from app.database.migrator import run_auto_migrations
from app.database.session import get_db_session
from app.handlers import setup_routers
from app.middlewares import DbSessionMiddleware, SecurityMiddleware, UserSyncMiddleware
from app.utils.commands import setup_bot_commands

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Register Middlewares
dp.update.middleware(DbSessionMiddleware())
dp.update.middleware(UserSyncMiddleware())
dp.update.middleware(SecurityMiddleware())

# Register Routers
dp.include_router(setup_routers())

start_time = time.time()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application boot and shutdown lifespan context."""
    logger.info("Booting TeleGame Platform...")
    await validate_startup_configuration()
    plugin_manager.discover_plugins()
    await run_auto_migrations()
    await setup_bot_commands(bot)
    logger.info("TeleGame Platform is fully initialized and operational!")
    yield
    logger.info("Shutting down TeleGame Platform...")


app = FastAPI(
    title="TeleGame Platform",
    description="Serverless, Plugin-Based Telegram Multiplayer Gaming Platform",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root_endpoint():
    """Root platform metadata endpoint."""
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health_check():
    """Liveness health check endpoint."""
    return {"status": "ok", "uptime_seconds": int(time.time() - start_time)}


@app.get("/readiness")
async def readiness_check():
    """Readiness check verifying database connectivity."""
    try:
        async with get_db_session() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Database connection unready") from e


@app.get("/metrics")
async def system_metrics():
    """System telemetry & metrics endpoint."""
    games = list(plugin_manager.list_available_games().keys())
    return {
        "loaded_games_count": len(games),
        "available_plugins": games,
        "uptime_seconds": int(time.time() - start_time),
    }


@app.post(settings.WEBHOOK_PATH)
async def bot_webhook_endpoint(request: Request) -> Response:
    """Telegram Webhook handler endpoint."""
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot=bot, update=update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing webhook update: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/cron/cleanup")
async def cron_lazy_timer_cleanup():
    """Serverless cron endpoint for cleaning up expired sessions."""
    async with get_db_session() as session:
        count = await cleanup_expired_sessions(session)
    return {"status": "ok", "cleaned_sessions": count}
