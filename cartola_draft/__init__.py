"""Cartola FC line-up draft."""

from dataclasses import dataclass
from typing import Collection, Tuple

from . import exceptions


@dataclass
class Player:
    """Player"""

    id: int
    position: int
    price: float
    points: float
    club: int


@dataclass
class Scheme:
    """Line-up scheme."""

    goalkeepers: int
    fullbacks: int
    defenders: int
    midfielders: int
    forwards: int
    coaches: int


@dataclass
class LineUp:
    """Squad line-up"""

    scheme: Scheme
    goalkeepers: Collection[Player]
    fullbacks: Collection[Player]
    defenders: Collection[Player]
    midfielders: Collection[Player]
    forwards: Collection[Player]
    coaches: Collection[Player]

    def __post_init__(self):
        does_not_follow_scheme = (
            len(self.goalkeepers) != self.scheme.goalkeepers,
            len(self.fullbacks) != self.scheme.fullbacks,
            len(self.defenders) != self.scheme.defenders,
            len(self.midfielders) != self.scheme.midfielders,
            len(self.forwards) != self.scheme.forwards,
            len(self.coaches) != self.scheme.coaches,
        )
        if any(does_not_follow_scheme):
            raise exceptions.LineUpSchemeError("Line-up does not follow the scheme.")

    @property
    def players(self) -> Tuple[Player]:
        """Get line-up players"""
        return (
            *self.goalkeepers,
            *self.fullbacks,
            *self.defenders,
            *self.midfielders,
            *self.forwards,
            *self.coaches,
        )

    @property
    def points(self):
        """Get line-up points."""
        return sum([player.points for player in self.players])

    @property
    def price(self):
        """Get line-up price."""
        return sum([player.price for player in self.players])

    @property
    def clubs(self):
        """Get amount of different clubs in the line-up."""
        return len({player.club for player in self.players})
