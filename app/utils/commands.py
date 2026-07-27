"""Automatic Telegram Bot Command Registration."""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.config.logging import logger


async def setup_bot_commands(bot: Bot) -> None:
    """Registers official platform slash commands with Telegram API."""
    commands = [
        BotCommand(command="start", description="Start TeleGame & view welcome menu"),
        BotCommand(command="help", description="View help & command guides"),
        BotCommand(command="menu", description="Open interactive inline menu"),
        BotCommand(command="profile", description="View player profile & stats"),
        BotCommand(command="games", description="Browse available game plugins"),
        BotCommand(command="newgame", description="Start a new game lobby in group"),
        BotCommand(command="join", description="Join current group game lobby"),
        BotCommand(command="leave", description="Leave active game session"),
        BotCommand(command="startgame", description="Force start pending game lobby"),
        BotCommand(command="endgame", description="End current game session"),
        BotCommand(command="leaderboard", description="View global leaderboards"),
        BotCommand(command="stats", description="View detailed game statistics"),
        BotCommand(command="history", description="View match history"),
        BotCommand(command="shop", description="Open cosmetics shop"),
        BotCommand(command="inventory", description="View equipped inventory"),
        BotCommand(command="daily", description="Claim daily coin streak"),
        BotCommand(command="quests", description="View daily quests"),
        BotCommand(command="clan", description="Manage or join a clan"),
        BotCommand(command="tournament", description="View or join tournaments"),
        BotCommand(command="settings", description="Adjust user settings"),
        BotCommand(command="report", description="Report an issue or player"),
        BotCommand(command="support", description="Contact platform support"),
        BotCommand(command="about", description="About TeleGame Platform"),
        BotCommand(command="ping", description="Check bot latency"),
        BotCommand(command="admin", description="Admin dashboard"),
    ]

    try:
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
        logger.info("Successfully registered all 25+ bot slash commands with Telegram.")
    except Exception as e:
        logger.error(f"Failed to register bot commands: {e}")
