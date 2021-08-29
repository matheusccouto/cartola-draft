"""Test classes."""

import pytest

import cartola_draft as draft
from . import helper


class TestLineUp:
    """LineUp class tests."""

    @staticmethod
    def test_points():
        """Test points sum with some different formations."""
        for scheme in helper.SCHEMES_COUNTING.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_by_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme=draft.Scheme(*scheme.values()), **players)

            # Calculate the points sum and compare with the property.
            points = sum([play.points for pos in players.values() for play in pos])
            assert line_up.points == points

    @staticmethod
    def test_price():
        """Test price sum with some different schemes."""
        for scheme in helper.SCHEMES_COUNTING.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_by_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme=draft.Scheme(*scheme.values()), **players)

            # Calculate the price sum and compare with the property.
            price = sum([play.price for pos in players.values() for play in pos])
            assert line_up.price == price

    @staticmethod
    def test_unique_clubs():
        """Test unique clubs with some different schemes."""
        for scheme in helper.SCHEMES_COUNTING.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_by_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme=draft.Scheme(*scheme.values()), **players)

            # Calculate the price sum and compare with the property.
            clubs = len({play.club for pos in players.values() for play in pos})
            assert line_up.clubs == clubs

    @staticmethod
    def test_players():
        """Test players with some different schemes."""
        for scheme in helper.SCHEMES_COUNTING.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_by_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme=draft.Scheme(*scheme.values()), **players)

            # Get players list and compare with the property.
            players_test = {play.id for pos in players.values() for play in pos}
            players_prop = {play.id for play in line_up.players}
            assert players_prop == players_test

    @staticmethod
    def test_does_not_follow_scheme():
        """Assert that it raises when the scheme is wrong."""
        scheme1 = helper.SCHEMES_COUNTING[442]
        scheme2 = helper.SCHEMES_COUNTING[352]
        # Construct a dict with the position name and a list of random players.
        players = helper.get_random_players_by_scheme(scheme1)

        # Create line up object.
        with pytest.raises(draft.exceptions.LineUpSchemeError):
            draft.LineUp(scheme=draft.Scheme(*scheme2), **players)
