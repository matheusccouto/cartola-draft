"""Cartola FC optimization algorithms."""

import abc
from typing import Sequence

from .. import Player, Scheme, LineUp


class DraftError(Exception):
    """Error on drating players."""


class BaseAlgorithm(abc.ABC):
    """Algorithm base class."""

    # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def __init__(self, players: Sequence[Player]):
        """Initializer"""
        self.players = players

    @abc.abstractmethod
    def draft(self, price: float, scheme: Scheme, max_players_per_club: int) -> LineUp:
        """Draft players following an specified scheme."""
