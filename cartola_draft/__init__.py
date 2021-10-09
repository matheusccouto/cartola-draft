"""Cartola FC line-up draft."""

from dataclasses import dataclass
from typing import Dict, List

POSITIONS = ["goalkeeper", "fullback", "defender", "midfielder", "forward", "coach"]


@dataclass
class Player:
    """Player"""

    id: int  # pylint: disable=invalid-name
    position: str
    price: float
    points: float
    club: int

    def __iter__(self):
        for key, val in vars(self).items():
            yield key, val


@dataclass
class Scheme:
    """Line-up scheme."""

    positions: Dict[str, int]

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
    def players_by_position(self) -> Dict[str, List[Player]]:
        """Get line-up players by position."""
        return {
            pos: [player for player in self.players if player.position == pos]
            for pos in POSITIONS
        }

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
            len(self.players_by_position[pos]) == self.scheme[pos] for pos in POSITIONS
        )
        return all(valid)

    def missing(self, position: str) -> bool:
        """Check if line-up still missing players from a certain position."""
        return len(self.players_by_position[position]) < self.scheme[position]
