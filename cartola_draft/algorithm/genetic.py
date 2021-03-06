"""Genetic algorithm."""

import random
from typing import List, Sequence

from . import BaseAlgorithm, DraftError
from .. import Player, Scheme, LineUp


class Genetic(BaseAlgorithm):
    """Genetic algorithm."""

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        players: Sequence[Player],
        n_generations: int = 500,
        n_individuals: int = 100,
        tournament_size: int = 100,
        n_tournament_winners: int = 5,
        max_n_mutations: int = 3,
    ):
        # pylint: disable=too-many-arguments
        super().__init__(players)
        self.n_generations = n_generations
        self.n_individuals = n_individuals
        self.tournament_size = tournament_size
        self.n_tournament_winners = n_tournament_winners
        self.max_n_mutations = max_n_mutations
        self.history: List[float] = []

    @staticmethod
    def _create_random_line_up(players: Sequence[Player], scheme: Scheme) -> LineUp:
        """Create a random line up."""
        # Make a copy and shuffle.
        players = list(players)
        random.shuffle(players)

        # Create line-up without any player.
        line_up = LineUp(scheme=scheme, players=[])

        # Iterate over players until it is able to fill the team.
        for player in players:

            # Check if the team has room for this player.
            if line_up.missing(player.position):
                line_up.add_player(player)

            # Check if the team is ready.
            if line_up.is_valid():
                return line_up

        raise DraftError("There are not enough players to form a line-up.")

    @staticmethod
    def _calculate_fitness(
        line_up: LineUp,
        max_price: float,
        max_players_per_club: int,
    ) -> float:
        """Calculate fitness metric. The greater the better"""
        if line_up.price > max_price:
            return max_price - line_up.price
        if max(line_up.players_per_club.values()) > max_players_per_club:
            return 0
        return line_up.points

    def _rank(
        self,
        line_ups: Sequence[LineUp],
        max_price: float,
        max_players_per_club: int,
    ) -> List[LineUp]:
        """Rank line ups based on the fitness."""
        iterable = sorted(
            line_ups,
            key=lambda x: self._calculate_fitness(
                x,
                max_price=max_price,
                max_players_per_club=max_players_per_club,
            ),
            reverse=True,
        )
        return list(iterable)

    def _tournament(
        self,
        line_ups: Sequence[LineUp],
        max_price: float,
        max_players_per_club: int,
    ) -> List[LineUp]:
        """Select best line up."""
        tournament_size = min(len(line_ups), self.tournament_size)
        ranked = self._rank(
            random.sample(line_ups, tournament_size),
            max_price=max_price,
            max_players_per_club=max_players_per_club,
        )
        return ranked[: self.n_tournament_winners]

    def _change_random_player(self, line_up: LineUp):
        """Change a random player from the line up."""
        i = random.randrange(len(line_up))
        new_player = random.choice(self.players_by_position[line_up[i].position])

        if new_player in line_up:
            self._change_random_player(line_up)
        else:
            line_up[i] = new_player

    def _create_offsprings(self, line_ups: Sequence[LineUp], size: int) -> List[LineUp]:
        """Create offsprings for given line ups."""
        offsprings = []
        for _ in range(size):

            line_up = random.choice(line_ups).copy()

            # Sample how many players to mutate.
            n_mutations = round(random.triangular(1, self.max_n_mutations, 0))
            for _ in range(int(n_mutations)):
                self._change_random_player(line_up)

            offsprings.append(line_up)

        return offsprings

    def draft(self, price: float, scheme: Scheme, max_players_per_club: int) -> LineUp:
        """Draft players following an specified scheme."""
        line_ups = [
            self._create_random_line_up(self.players, scheme)
            for _ in range(self.n_individuals)
        ]

        for _ in range(self.n_generations):

            ranked = self._rank(
                line_ups,
                max_price=price,
                max_players_per_club=max_players_per_club,
            )
            best = ranked[:1]
            rest = ranked[1:]
            self.history.append(best[0].points)

            tournament_size = min(len(rest), self.tournament_size)
            selected = self._tournament(
                random.sample(rest, k=min(len(rest), tournament_size)),
                max_price=price,
                max_players_per_club=max_players_per_club,
            )
            offsprings = self._create_offsprings(selected, size=self.n_individuals - 1)
            line_ups = best + offsprings

        best = self._rank(
            line_ups,
            max_price=price,
            max_players_per_club=max_players_per_club,
        )[:1]
        self.history.append(best[0].points)
        best[0].bench = self._draft_bench(best[0])
        return best[0]
