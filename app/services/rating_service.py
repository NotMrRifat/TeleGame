"""Elo Rating Service for competitive game ranking updates."""

import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logging import logger
from app.repositories.domain_repos import RatingRepository, UserRepository


class RatingService:
    """Calculates and persists Elo rating adjustments for 1v1 and multiplayer matches."""

    DEFAULT_K_FACTOR = 32

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.rating_repo = RatingRepository(db_session)
        self.user_repo = UserRepository(db_session)

    @staticmethod
    def calculate_expected_score(rating_a: int, rating_b: int) -> float:
        """Calculate expected score of Player A against Player B using standard Elo formula."""
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))

    async def update_1v1_ratings(
        self,
        winner_id: int,
        loser_id: int,
        game_slug: str,
        is_draw: bool = False,
        k_factor: int = DEFAULT_K_FACTOR,
    ) -> tuple[int, int]:
        """Update Elo ratings for two competing players after a match.

        Returns:
            Tuple[int, int]: (winner_new_elo, loser_new_elo)
        """
        winner_user = await self.user_repo.get_by_telegram_id(winner_id)
        loser_user = await self.user_repo.get_by_telegram_id(loser_id)

        if not winner_user or not loser_user:
            return 1200, 1200

        r_winner = await self.rating_repo.get_user_rating(winner_user.id, game_slug)
        if not r_winner:
            r_winner = await self.rating_repo.create(
                user_id=winner_user.id, game_slug=game_slug, elo=1200
            )

        r_loser = await self.rating_repo.get_user_rating(loser_user.id, game_slug)
        if not r_loser:
            r_loser = await self.rating_repo.create(
                user_id=loser_user.id, game_slug=game_slug, elo=1200
            )

        e_winner = self.calculate_expected_score(r_winner.elo, r_loser.elo)
        e_loser = self.calculate_expected_score(r_loser.elo, r_winner.elo)

        s_winner = 0.5 if is_draw else 1.0
        s_loser = 0.5 if is_draw else 0.0

        r_winner.elo = max(100, int(r_winner.elo + k_factor * (s_winner - e_winner)))
        r_loser.elo = max(100, int(r_loser.elo + k_factor * (s_loser - e_loser)))

        # Update peak elo
        r_winner.peak_elo = max(r_winner.peak_elo, r_winner.elo)
        r_loser.peak_elo = max(r_loser.peak_elo, r_loser.elo)

        # Update global user win/loss statistics
        if not is_draw:
            winner_user.wins += 1
            loser_user.losses += 1
        else:
            winner_user.draws += 1
            loser_user.draws += 1

        winner_user.games_played += 1
        loser_user.games_played += 1

        await self.db_session.flush()

        logger.info(
            f"Updated Ratings ({game_slug}): Winner {winner_id} -> {r_winner.elo}, Loser {loser_id} -> {r_loser.elo}"
        )
        return r_winner.elo, r_loser.elo
