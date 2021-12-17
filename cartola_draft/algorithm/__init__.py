"""Cartola FC optimization algorithms."""

import abc
from typing import Dict, List, Sequence

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

    @staticmethod
    def _organize_players_by_position(
        players: Sequence[Player],
    ) -> Dict[int, List[Player]]:
        """Organize players by position."""
        positions = {player.position for player in players}
        return {
            pos: [player for player in players if player.position == pos]
            for pos in positions
        }

    @abc.abstractmethod
    def draft(self, price: float, scheme: Scheme) -> LineUp:
        """Draft players following an specified scheme."""
