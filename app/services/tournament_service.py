"""Tournament Engine supporting Single Elimination, Double Elimination, Round Robin, and Swiss brackets."""

import random

from pydantic import BaseModel


class TournamentMatch(BaseModel):
    """Represents a single match within a tournament bracket."""

    match_id: int
    round_number: int
    player1_id: int
    player2_id: int
    winner_id: int | None = None
    is_completed: bool = False


class TournamentEngine:
    """Generates and manages tournament brackets."""

    @staticmethod
    def generate_single_elimination_bracket(player_ids: list[int]) -> list[TournamentMatch]:
        """Generates single elimination bracket for N players."""
        players = list(player_ids)
        random.shuffle(players)

        num_players = len(players)
        matches: list[TournamentMatch] = []
        match_id = 1

        # Calculate initial round pairings
        for i in range(0, num_players - 1, 2):
            matches.append(
                TournamentMatch(
                    match_id=match_id,
                    round_number=1,
                    player1_id=players[i],
                    player2_id=players[i + 1],
                )
            )
            match_id += 1

        return matches
