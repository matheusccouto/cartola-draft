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
        n_generations: int = 100,
        n_individuals: int = 100,
        tournament_size: int = 10,
        n_tournament_winners: int = 5,
        max_n_mutations: int = 5,
    ):
        # pylint: disable=too-many-arguments
        super().__init__(players)
        self.n_generations = n_generations
        self.n_individuals = n_individuals
        self.tournament_size = tournament_size
        self.n_tournament_winners = n_tournament_winners
        self.max_n_mutations = max_n_mutations
        self.players_by_position = self._organize_players_by_position(self.players)

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
    def _calculate_fitness(line_up: LineUp, max_price: float) -> float:
        """Calculate fitness metric. The greater the better"""
        if line_up.price > max_price:
            return line_up.price - max_price
        return line_up.points

    def _rank(self, line_ups: Sequence[LineUp], max_price: float) -> List[LineUp]:
        """Rank line ups based on the fitness."""
        return list(
            sorted(
                line_ups,
                key=lambda x: self._calculate_fitness(x, max_price=max_price),
                reverse=True,
            )
        )

    def _tournament(
        self,
        line_ups: Sequence[LineUp],
        max_price: float,
    ) -> List[LineUp]:
        """Select best line up."""
        ranked = self._rank(random.sample(line_ups, self.tournament_size), max_price)
        return ranked[: self.n_tournament_winners]

    @staticmethod
    def _pop_random_player(line_up: LineUp) -> Player:
        """Pop a random player from the line up"""
        player = random.choice(line_up.players)
        line_up.remove_player(player)
        return player

    def _change_random_player(self, line_up: LineUp):
        """Change a random player from the line up."""
        player = self._pop_random_player(line_up)
        line_up.add_player(random.choice(self.players_by_position[player.position]))

    def _create_offsprings(self, line_ups: Sequence[LineUp], size: int) -> List[LineUp]:
        """Create offsprings for given line ups."""
        offsprings = []
        for _ in range(size):

            line_up = random.choice(line_ups)
            line_up = line_up.copy()

            # Sample how many players to mutate.
            n_mutations = round(random.triangular(0, self.max_n_mutations, 0))
            for _ in range(int(n_mutations)):
                self._change_random_player(line_up)

            offsprings.append(line_up)

        return offsprings

    def draft(self, price: float, scheme: Scheme) -> LineUp:
        """Draft players following an specified scheme."""
        line_ups = [
            self._create_random_line_up(self.players, scheme)
            for _ in range(self.n_individuals)
        ]

        for _ in range(self.n_generations):

            best = self._rank(line_ups, max_price=price)[0]

            selected = self._tournament(
                [random.choice(line_ups) for _ in range(self.tournament_size)],
                max_price=price,
            )
            offsprings = self._create_offsprings(selected, size=self.n_individuals - 1)

            line_ups = [best] + offsprings

        return best
