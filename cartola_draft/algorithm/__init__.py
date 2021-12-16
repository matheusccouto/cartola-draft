"""Cartola FC optimization algorithms."""

import abc
from typing import Collection, Dict, List

from .. import Player, Scheme, LineUp


class DraftError(Exception):
    """Error on drating players."""


class BaseAlgorithm(abc.ABC):
    """Algorithm base class."""

    # pylint: disable=too-few-public-methods

    @abc.abstractmethod
    def __init__(self, players: Collection[Player]):
        """Initializer"""

    @staticmethod
    def _organize_players_by_position(
        players: Collection[Player],
    ) -> Dict[int, List[Player]]:
        """Organize players by position."""
        return {
            i: [player for player in players if player.position == i]
            for i in range(1, 7)
        }

    @abc.abstractmethod
    def draft(self, price: float, scheme: Scheme) -> LineUp:
        """Draft players following an specified scheme."""
