"""Cartola FC optimization algorithms."""

import abc
from typing import Sequence

from .. import Player, Scheme, LineUp, players_by_position


class DraftError(Exception):
    """Error on drating players."""


class BaseAlgorithm(abc.ABC):
    """Algorithm base class."""

    # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def __init__(self, players: Sequence[Player]):
        """Initializer"""
        self.players = players
        self.players_by_position = players_by_position(self.players)

    def _draft_bench(self, line_up: LineUp) -> Sequence[Player]:
        """Draft players for the bench of a given line up."""
        bench = []
        for pos, count in line_up.scheme.items():
            if "coach" in pos:
                continue
            if count > 0:
                price = min([p.price for p in line_up.players_by_position[pos]])
                players = [p for p in self.players_by_position[pos] if p.price < price]
                player = sorted(players, key=lambda p: p.points)[-1]
                bench.append(player)
        return bench

    @abc.abstractmethod
    def draft(self, price: float, scheme: Scheme, max_players_per_club: int) -> LineUp:
        """Draft players following an specified scheme."""
