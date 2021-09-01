"""Greedy algorithm."""

from typing import Collection

from .. import Player, Scheme, LineUp


class Greedy:
    """Greedy algorithm."""

    def __init__(self, players: Collection[Player]):
        self._players = sorted(players, key=lambda player: player.points, reverse=True)

    def draft(self, scheme: Scheme) -> LineUp:
        """Draft players following an specified scheme."""
        # Make a copy.
        players = list(self._players)

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

        raise ValueError("There are not enough players to form a line-up.")
