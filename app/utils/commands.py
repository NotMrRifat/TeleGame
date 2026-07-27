"""Automatic Telegram Bot Command Registration."""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.config.logging import logger


async def setup_bot_commands(bot: Bot) -> None:
    """Registers official platform slash commands with Telegram API."""
    commands = [
        BotCommand(command="start", description="Start TeleGame & open main menu"),
        BotCommand(command="help", description="View help & full command list"),
        BotCommand(command="menu", description="Open interactive main menu"),
        BotCommand(command="vsbot", description="Play instant match vs Computer AI (Solo)"),
        BotCommand(command="games", description="Browse 10 playable game plugins"),
        BotCommand(command="newgame", description="Create a game lobby in a group"),
        BotCommand(command="join", description="Join waiting group game lobby"),
        BotCommand(command="startgame", description="Start match when lobby is ready"),
        BotCommand(command="cancel", description="Cancel or end active game session"),
        BotCommand(command="profile", description="View stats, level & XP"),
        BotCommand(command="balance", description="View coin & gem wallet balance"),
        BotCommand(command="daily", description="Claim daily coin streak rewards"),
        BotCommand(command="shop", description="Open items shop & cosmetics"),
        BotCommand(command="inventory", description="View inventory & equipped items"),
        BotCommand(command="leaderboard", description="View global player rankings"),
        BotCommand(command="clan", description="Create or manage a clan"),
        BotCommand(command="language", description="Switch language (English/Bangla)"),
        BotCommand(command="about", description="About TeleGame platform & rules"),
        BotCommand(command="ping", description="Check bot latency & status"),
    ]

    try:
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
        logger.info(f"Successfully registered {len(commands)} bot slash commands with Telegram.")
    except Exception as e:
        logger.error(f"Failed to register bot commands: {e}")
