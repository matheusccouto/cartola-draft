"""Greedy algorithm."""

from typing import Sequence

from . import BaseAlgorithm, DraftError
from .. import Player, Scheme, LineUp


class Greedy(BaseAlgorithm):
    """Greedy algorithm."""

    # pylint: disable=too-few-public-methods

    def __init__(self, players: Sequence[Player]):
        super().__init__(players)
        self.players = sorted(players, key=lambda player: player.points, reverse=True)

    def draft(self, price: float, scheme: Scheme, max_players_per_club: int) -> LineUp:
        """Draft players following an specified scheme."""
        # Make a copy.
        players = list(self.players)

        # Create line-up without any player.
        line_up = LineUp(scheme=scheme, players=[])

        # Iterate over players until it is able to fill the team.
        for player in players:

            # Check if the team has room for this player.
            if line_up.missing(player.position) and player.price <= price:
                line_up.add_player(player)
                price -= player.price

                # If the addition breaks the max players per club rule, undo it.
                if max(line_up.players_per_club.values()) > max_players_per_club:
                    line_up.remove_player(player)
                    price += player.price

            # Check if the team is ready.
            if line_up.is_valid():
                return line_up

        raise DraftError("There are not enough players to form a line-up.")
