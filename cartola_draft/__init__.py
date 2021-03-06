"""Cartola FC line-up draft."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

POSITIONS = ["goalkeeper", "fullback", "defender", "midfielder", "forward", "coach"]


def players_by_position(players: Sequence["Player"]):
    """Organize players by position."""
    return {
        pos: [player for player in players if player.position == pos]
        for pos in POSITIONS
    }


@dataclass
class Player:
    """Player"""

    id: int  # pylint: disable=invalid-name
    position: str
    price: float
    points: float
    club: int

    def __hash__(self):
        return self.id

    def __iter__(self):
        for key, val in vars(self).items():
            yield key, val


@dataclass
class Scheme:
    """Line-up scheme."""

    positions: Dict[str, int]

    def __getitem__(self, val):
        return self.positions[val]

    def items(self):
        """Iterate of items."""
        return self.positions.items()

    def keys(self):
        """Iterate of keys."""
        return self.positions.keys()

    def values(self):
        """Iterate of values."""
        return self.positions.values()

    def is_valid(self):
        """Check if scheme is valid."""
        players = sum([count for pos, count in self.positions.items() if pos != "coach"])
        coach = self.positions["coach"]
        return players == 11 and coach <= 1


@dataclass
class LineUp:
    """Squad line-up"""

    scheme: Scheme
    players: List[Player]
    bench: Optional[List[Player]] = None

    def __post_init__(self):
        if self.bench is None:
            self.bench = [None]

    def __len__(self):
        return len(self.players)

    def __getitem__(self, index):
        return self.players[index]

    def __setitem__(self, index, value):
        self.players[index] = value

    def __iter__(self):
        for player in self.players:
            yield dict(player)

    def __contains__(self, value):
        return value in self.players

    @property
    def players_by_position(self) -> Dict[str, List[Player]]:
        """Get line-up players by position."""
        return players_by_position(self.players)

    @property
    def points(self):
        """Get line-up points."""
        return sum([player.points for player in self.players])

    @property
    def price(self):
        """Get line-up price."""
        sum_ = 0
        for player in self.players:
            sum_ += player.price
        return sum_

    @property
    def clubs(self):
        """Get amount of different clubs in the line-up."""
        return len({player.club for player in self.players})

    @property
    def players_per_club(self):
        """Get players per club."""
        return {player.club: self.players.count(player) for player in self.players}

    def add_player(self, player: Player):
        """Add player to the line-up."""
        self.players.append(player)

    def remove_player(self, player: Player):
        """Remove player from the line-up."""
        self.players.remove(player)

    def is_valid(self):
        """Check if it follows the scheme."""
        line_up_pos = [player.position for player in self.players]
        ref_pos = [key for key, val in self.scheme.items() for _ in range(val)]
        return sorted(line_up_pos) == sorted(ref_pos)

    def missing(self, position: str) -> bool:
        """Check if line-up still missing players from a certain position."""
        players_from_pos = [p for p in self.players if p.position == position]
        return len(players_from_pos) < self.scheme[position]

    def copy(self) -> "LineUp":
        """Copy this instance."""
        return LineUp(scheme=self.scheme, players=list(self.players))
