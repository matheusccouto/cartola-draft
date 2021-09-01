"""Cartola FC line-up draft."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Player:
    """Player"""

    id: int
    position: int
    price: float
    points: float
    club: int

    def __iter__(self):
        for key, val in vars(self).items():
            yield key, val


@dataclass
class Scheme:
    """Line-up scheme."""

    positions: Dict[int, int]

    def __getitem__(self, val):
        return self.positions[val]

    def is_valid(self):
        """Check if scheme is valid."""
        return sum(self.positions.values()) == 12


@dataclass
class LineUp:
    """Squad line-up"""

    scheme: Scheme
    players: List[Player]

    def __iter__(self):
        for player in sorted(self.players, key=lambda player: player.position):
            yield dict(player)

    @property
    def players_by_position(self) -> Dict[int, List[Player]]:
        """Get line-up players by position."""
        return {i: [p for p in self.players if p.position == i] for i in range(1, 7)}

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

    def add_player(self, player: Player):
        """Add player to the line-up."""
        self.players.append(player)

    def is_valid(self):
        """Check if it follows the scheme."""
        valid = (
            len(self.players_by_position[i]) == self.scheme[i] for i in range(1, 7)
        )
        return all(valid)

    def missing(self, position: int) -> bool:
        """Check if line-up still missing players from a certain position."""
        return len(self.players_by_position[position]) < self.scheme[position]
