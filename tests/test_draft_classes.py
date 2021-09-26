"""Test classes."""

import random

import cartola_draft as draft
from . import helper


class TestLineUp:
    """LineUp class tests."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        cls.schemes = {
            442: draft.Scheme(helper.SCHEMES_COUNTING[442]),
            352: draft.Scheme(helper.SCHEMES_COUNTING[352]),
            541: draft.Scheme(helper.SCHEMES_COUNTING[541]),
        }

    def test_points(self):
        """Test points sum with some different formations."""
        for scheme in self.schemes.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_with_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme, players)

            # Calculate the points sum and compare with the property.
            points = sum([player.points for player in players])
            assert line_up.points == points

    def test_price(self):
        """Test price sum with some different schemes."""
        for scheme in self.schemes.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_with_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme, players)

            # Calculate the price sum and compare with the property.
            price = sum([player.price for player in players])
            assert line_up.price == price

    def test_unique_clubs(self):
        """Test unique clubs with some different schemes."""
        for scheme in self.schemes.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_with_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme, players)

            # Calculate the price sum and compare with the property.
            clubs = len({player.club for player in players})
            assert line_up.clubs == clubs

    def test_players(self):
        """Test players with some different schemes."""
        for scheme in self.schemes.values():
            # Construct a dict with the position name and a list of random players.
            players = helper.get_random_players_with_scheme(scheme)

            # Create line up object.
            line_up = draft.LineUp(scheme, players)

            # Get players list and compare with the property.
            players_test = {player.id for player in players}
            players_prop = {player.id for player in line_up.players}
            assert players_prop == players_test

    def test_is_valid(self):
        """Assert that it raises when the scheme is wrong."""
        # Construct a dict with the position name and a list of random players.
        players = helper.get_random_players_with_scheme(self.schemes[541])

        # Create line up object and check if it valid.
        line_up = draft.LineUp(self.schemes[541], players)
        assert line_up.is_valid()

    def test_is_not_valid(self):
        """Assert that it raises when the scheme is wrong."""
        # Construct a dict with the position name and a list of random players.
        players = helper.get_random_players_with_scheme(self.schemes[442])

        # Create line up object and check if it valid.
        line_up = draft.LineUp(self.schemes[352], players)
        assert not line_up.is_valid()

    def test_add(self):
        """Test adding players."""
        # Create empty line up.
        line_up = draft.LineUp(self.schemes[442], players=[])
        assert len(line_up.players) == 0

        # Add a random player.
        player = helper.get_random_players(amount=1, position="goalkeeper")
        line_up.add_player(player)
        assert len(line_up.players) == 1

        # Add another random player.
        player = helper.get_random_players(amount=1, position="coach")
        line_up.add_player(player)
        assert len(line_up.players) == 2

    def test_needs_position(self):
        """Test adding players."""
        # Construct a dict with the position name and a list of random players.
        players = helper.get_random_players_with_scheme(self.schemes[442])

        # Drop a player from the line-up.
        dropped = players.pop(random.choice(range(len(players))))

        # Create line-up with missing player.
        line_up = draft.LineUp(self.schemes[442], players)

        # Check if it needs only the missing position.
        for position in helper.POSITIONS:
            missing = line_up.missing(position)

            if position == dropped.position:
                assert missing
            else:
                assert not missing

    def test_list(self):
        """Test converting to a list."""
        # Construct a dict with the position name and a list of random players.
        players = helper.get_random_players_with_scheme(self.schemes[442])

        # Create line up object and check if it valid.
        line_up = draft.LineUp(self.schemes[442], players)
        # Convert to list
        line_up_list = list(line_up)
        # Make sure convertion was good.
        assert isinstance(line_up_list, list)
        # Check if inner objects are dict.
        for obj in line_up_list:
            assert isinstance(obj, dict)


class TestScheme:
    """Test Scheme class."""

    @staticmethod
    def test_is_valid():
        """Test is valid method."""
        for args in helper.SCHEMES_COUNTING.values():
            scheme = draft.Scheme(args)
            assert scheme.is_valid()

    @staticmethod
    def test_is_not_valid():
        """Test is not valid method."""
        for args in helper.INVALID_SCHEMES_COUNTING.values():
            scheme = draft.Scheme(args)
            assert not scheme.is_valid()


class TestPlayer:
    """Test Player class."""

    @staticmethod
    def test_dict():
        """Test converting to dict."""
        args = dict(id=1, position=2, price=3, points=4, club=5)
        player = draft.Player(**args)
        assert dict(player) == args
