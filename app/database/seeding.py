"""Default Data Seeder for TeleGame platform."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.config.settings import settings
from app.models.domain import (
    AchievementModel,
    GameModel,
    QuestModel,
    SystemSettingModel,
    UserModel,
)


async def seed_default_data(session: AsyncSession) -> None:
    """Seeds default games, achievements, quests, admins, and settings into the database."""
    logger.info("Executing database default data seeder...")

    # 1. Seed Games
    default_games = [
        {
            "slug": "tic_tac_toe",
            "title": "Tic-Tac-Toe",
            "description": "Classic 3x3 grid game",
            "min_players": 2,
            "max_players": 2,
            "category": "board",
        },
        {
            "slug": "rock_paper_scissors",
            "title": "Rock Paper Scissors",
            "description": "Quick hand-gesture strategy game",
            "min_players": 2,
            "max_players": 2,
            "category": "casual",
        },
        {
            "slug": "connect_four",
            "title": "Connect Four",
            "description": "Drop discs to connect 4 in a row",
            "min_players": 2,
            "max_players": 2,
            "category": "strategy",
        },
        {
            "slug": "hangman",
            "title": "Hangman",
            "description": "Guess the hidden word before running out of attempts",
            "min_players": 1,
            "max_players": 8,
            "category": "word",
        },
        {
            "slug": "word_chain",
            "title": "Word Chain",
            "description": "Chain words using the last letter of the previous word",
            "min_players": 2,
            "max_players": 10,
            "category": "word",
        },
        {
            "slug": "trivia",
            "title": "Trivia Battle",
            "description": "Test your knowledge against friends in real time",
            "min_players": 1,
            "max_players": 20,
            "category": "quiz",
        },
        {
            "slug": "mafia",
            "title": "Mafia",
            "description": "Social deduction multiplayer game of mystery and deceit",
            "min_players": 4,
            "max_players": 16,
            "category": "party",
        },
        {
            "slug": "uno",
            "title": "UNO",
            "description": "Classic color and number matching card game",
            "min_players": 2,
            "max_players": 8,
            "category": "cards",
        },
        {
            "slug": "chess",
            "title": "Chess",
            "description": "Grand strategy board game",
            "min_players": 2,
            "max_players": 2,
            "category": "strategy",
        },
        {
            "slug": "ludo",
            "title": "Ludo",
            "description": "Classic dice rolling board game",
            "min_players": 2,
            "max_players": 4,
            "category": "board",
        },
    ]

    for g_data in default_games:
        stmt = select(GameModel).where(GameModel.slug == g_data["slug"])
        res = await session.execute(stmt)
        if not res.scalar_one_or_none():
            session.add(GameModel(**g_data))

    # 2. Seed Achievements
    default_achievements = [
        {
            "slug": "first_win",
            "title": "First Victory",
            "description": "Win your very first game",
            "icon": "🏆",
            "reward_coins": 100,
            "reward_xp": 150,
        },
        {
            "slug": "wins_100",
            "title": "Veteran Gamer",
            "description": "Achieve 100 total victories",
            "icon": "👑",
            "reward_coins": 1000,
            "reward_xp": 1500,
        },
        {
            "slug": "daily_player",
            "title": "Daily Player",
            "description": "Maintain a 7-day login streak",
            "icon": "🔥",
            "reward_coins": 500,
            "reward_xp": 700,
        },
        {
            "slug": "trivia_genius",
            "title": "Trivia Genius",
            "description": "Answer 10 trivia questions correctly in a row",
            "icon": "🧠",
            "reward_coins": 300,
            "reward_xp": 400,
        },
        {
            "slug": "master_detective",
            "title": "Master Detective",
            "description": "Win a Mafia game as Detective",
            "icon": "🕵️",
            "reward_coins": 400,
            "reward_xp": 500,
        },
    ]

    for a_data in default_achievements:
        stmt = select(AchievementModel).where(AchievementModel.slug == a_data["slug"])
        res = await session.execute(stmt)
        if not res.scalar_one_or_none():
            session.add(AchievementModel(**a_data))

    # 3. Seed Quests
    default_quests = [
        {
            "slug": "daily_play_3",
            "title": "Daily Gamer",
            "description": "Play 3 matches in any game today",
            "quest_type": "DAILY",
            "target_count": 3,
            "reward_coins": 150,
            "reward_xp": 200,
        },
        {
            "slug": "daily_win_1",
            "title": "Daily Champion",
            "description": "Win 1 game today",
            "quest_type": "DAILY",
            "target_count": 1,
            "reward_coins": 200,
            "reward_xp": 250,
        },
    ]

    for q_data in default_quests:
        stmt = select(QuestModel).where(QuestModel.slug == q_data["slug"])
        res = await session.execute(stmt)
        if not res.scalar_one_or_none():
            session.add(QuestModel(**q_data))

    # 4. Seed Admin Users
    if settings.OWNER_ID:
        stmt = select(UserModel).where(UserModel.telegram_id == settings.OWNER_ID)
        res = await session.execute(stmt)
        owner_user = res.scalar_one_or_none()
        if not owner_user:
            session.add(
                UserModel(
                    telegram_id=settings.OWNER_ID,
                    first_name="Platform Owner",
                    role="owner",
                    coins=10000,
                    level=100,
                )
            )
        else:
            owner_user.role = "owner"

    # 5. System Settings
    system_settings = [
        {
            "key": "maintenance_mode",
            "value": {"enabled": False, "reason": ""},
            "description": "Global maintenance flag",
        },
        {
            "key": "platform_version",
            "value": {"version": "1.0.0"},
            "description": "Platform version",
        },
    ]

    for s_data in system_settings:
        stmt = select(SystemSettingModel).where(SystemSettingModel.key == s_data["key"])
        res = await session.execute(stmt)
        if not res.scalar_one_or_none():
            session.add(SystemSettingModel(**s_data))

    await session.commit()
    logger.info("Default data seeding completed.")


async def main() -> None:
    """CLI entrypoint for running database seeding."""
    from app.database.session import get_db_session

    logger.info("Running standalone database seeding script...")
    async with get_db_session() as session:
        await seed_default_data(session)
    logger.info("Database seeding finished successfully.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
