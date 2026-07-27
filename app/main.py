"""FastAPI Webhook & Bot ASGI Application Gateway."""

import asyncio
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
from app.database.session import engine, get_db_session
from app.handlers import setup_routers
from app.middlewares import DbSessionMiddleware, SecurityMiddleware, UserSyncMiddleware
from app.utils.commands import setup_bot_commands

# Singleton Bot & Dispatcher instances
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Register Middlewares
dp.update.middleware(DbSessionMiddleware())
dp.update.middleware(UserSyncMiddleware())
dp.update.middleware(SecurityMiddleware())

# Register Main Router
dp.include_router(setup_routers())

start_time = time.time()
_initialized = False
_webhook_checked = False
_init_lock = asyncio.Lock()


async def ensure_bot_session(bot_inst: Bot) -> None:
    """Ensures bot's aiohttp ClientSession is active and bound to the current running event loop."""
    try:
        current_loop = asyncio.get_running_loop()
        session = getattr(bot_inst.session, "_session", None)
        if session is not None:
            session_loop = getattr(session, "_loop", None)
            if (
                session.closed
                or session_loop is None
                or session_loop.is_closed()
                or session_loop is not current_loop
            ):
                logger.debug("Recreating bot aiohttp ClientSession for current event loop.")
                if not session.closed:
                    await session.close()
                bot_inst.session._session = None
    except Exception as e:
        logger.warning(f"Error checking bot session loop compatibility: {e}")


async def setup_telegram_webhook(bot_inst: Bot) -> bool:
    """Checks and registers Telegram webhook automatically with secret token if missing or changed."""
    global _webhook_checked
    if _webhook_checked:
        return True

    if not settings.BOT_TOKEN or settings.BOT_TOKEN.startswith("123456789:ABCdef"):
        logger.warning("Skipping webhook setup: BOT_TOKEN is default placeholder.")
        return False

    target_url = settings.full_webhook_url
    if not target_url.startswith("https://"):
        logger.warning(
            f"Skipping webhook setup: WEBHOOK_URL must start with https:// (got '{target_url}')"
        )
        return False

    try:
        await ensure_bot_session(bot_inst)
        current_info = await bot_inst.get_webhook_info()
        secret = settings.WEBHOOK_SECRET if settings.WEBHOOK_SECRET else None

        if current_info.url == target_url:
            logger.info(f"Webhook already registered & active: {target_url}")
            _webhook_checked = True
            return True

        logger.info(f"Registering Telegram Webhook to {target_url}...")
        allowed_types = dp.resolve_used_update_types() or [
            "message",
            "edited_message",
            "callback_query",
            "inline_query",
            "my_chat_member",
        ]

        success = await bot_inst.set_webhook(
            url=target_url,
            secret_token=secret,
            drop_pending_updates=False,
            allowed_updates=allowed_types,
        )
        if success:
            logger.info(f"Webhook registered successfully: {target_url}")
            _webhook_checked = True
        else:
            logger.error(f"Failed to register Telegram Webhook to {target_url}")
        return success
    except Exception as e:
        logger.error(f"Error checking/setting Telegram Webhook: {e}")
        return False


async def ensure_initialized() -> None:
    """Thread-safe & async-safe application initialization routine for serverless execution."""
    global _initialized
    if _initialized:
        return

    async with _init_lock:
        if _initialized:
            return

        logger.info("Booting TeleGame Platform Production Engine...")

        # 1. Validate environment & settings
        await validate_startup_configuration()

        # 2. Discover game plugins
        plugins = plugin_manager.discover_plugins()
        logger.info(f"Plugins loaded: {list(plugins.keys())}")

        # 3. Database migrations & seed
        await run_auto_migrations()
        logger.info("Database connected & verified.")

        # 4. Sync BotFather Slash Commands (non-blocking failure)
        try:
            await setup_bot_commands(bot)
            logger.info("Bot commands synced.")
        except Exception as e:
            logger.warning(f"Non-fatal error syncing bot commands: {e}")

        # 5. Register Telegram Webhook automatically
        await setup_telegram_webhook(bot)

        logger.info("Dispatcher ready.")
        logger.info("Startup complete — TeleGame Platform operational!")
        _initialized = True


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application boot and shutdown lifespan context."""
    await ensure_initialized()
    yield
    logger.info("Shutting down TeleGame Platform...")
    try:
        await bot.session.close()
        logger.info("Bot client session closed successfully.")
    except Exception as e:
        logger.warning(f"Error closing bot session: {e}")

    try:
        await engine.dispose()
        logger.info("Database engine connections closed successfully.")
    except Exception as e:
        logger.warning(f"Error disposing database engine: {e}")

    logger.info("Teardown complete.")


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
        "webhook_url": settings.full_webhook_url,
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


async def handle_telegram_update(request: Request) -> Response:
    """Core webhook update processor for Telegram Serverless Gateway."""
    start_ts = time.time()
    await ensure_initialized()
    await ensure_bot_session(bot)

    # Verify secret token header if configured
    if settings.WEBHOOK_SECRET and settings.WEBHOOK_SECRET != "super_secret_webhook_token_32_chars_long":
        secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret_header != settings.WEBHOOK_SECRET:
            logger.warning("Unauthorized Telegram update: secret token mismatch.")
            raise HTTPException(status_code=401, detail="Unauthorized: Webhook secret token invalid")

    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Invalid JSON payload in Telegram webhook: {e}")
        return Response(status_code=400, content="Invalid JSON payload")

    # Log incoming telemetry details
    update_id = data.get("update_id", "unknown")
    msg_obj = data.get("message") or data.get("edited_message") or {}
    cb_obj = data.get("callback_query") or {}
    from_user = msg_obj.get("from") or cb_obj.get("from") or {}
    user_id = from_user.get("id", "unknown")
    username = from_user.get("username", "anonymous")
    command = msg_obj.get("text") or cb_obj.get("data") or "event"

    logger.info(
        f"Incoming Telegram Update ID: {update_id} | User ID: {user_id} | Username: @{username} | Command: '{command}'"
    )

    try:
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot=bot, update=update)
        exec_time_ms = round((time.time() - start_ts) * 1000, 2)
        logger.info(
            f"Successfully processed Update ID: {update_id} | User ID: {user_id} | Execution Time: {exec_time_ms}ms | Response Sent: HTTP 200"
        )
        return Response(status_code=200)
    except Exception as e:
        exec_time_ms = round((time.time() - start_ts) * 1000, 2)
        logger.error(
            f"Exception processing Update ID {update_id} after {exec_time_ms}ms: {e}",
            exc_info=True,
        )
        # Always return HTTP 200 to Telegram so bad updates are acknowledged and not retried endlessly
        return Response(status_code=200, content="OK")


# Register webhook routes for /webhook, /api/webhook, and settings.WEBHOOK_PATH
webhook_routes = sorted({"/webhook", "/api/webhook", settings.WEBHOOK_PATH})
for path in webhook_routes:
    app.post(path)(handle_telegram_update)


@app.get("/api/cron/cleanup")
async def cron_lazy_timer_cleanup():
    """Serverless cron endpoint for cleaning up expired sessions."""
    async with get_db_session() as session:
        count = await cleanup_expired_sessions(session)
    return {"status": "ok", "cleaned_sessions": count}
