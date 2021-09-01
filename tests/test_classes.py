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
            442: draft.Scheme({1: 1, 2: 2, 3: 2, 4: 4, 5: 2, 6: 1}),
            352: draft.Scheme({1: 1, 2: 0, 3: 3, 4: 5, 5: 2, 6: 1}),
            541: draft.Scheme({1: 1, 2: 2, 3: 3, 4: 4, 5: 1, 6: 1}),
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
        player = helper.get_random_players(amount=1, position=1)
        line_up.add_player(player)
        assert len(line_up.players) == 1

        # Add another random player.
        player = helper.get_random_players(amount=1, position=6)
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
        for position in range(1, 7):
            missing = line_up.missing(position)

            if position == dropped.position:
                assert missing
            else:
                assert not missing


class TestScheme:
    """Test Scheme class."""

    @staticmethod
    def test_is_valid():
        """Test is valid method."""
        args_list = [
            {1: 1, 2: 2, 3: 2, 4: 4, 5: 2, 6: 1},  # 442
            {1: 1, 2: 0, 3: 3, 4: 5, 5: 2, 6: 1},  # 352
            {1: 1, 2: 2, 3: 2, 4: 5, 5: 1, 6: 1},  # 451
            {1: 1, 2: 2, 3: 3, 4: 3, 5: 2, 6: 1},  # 532
            {1: 1, 2: 2, 3: 3, 4: 4, 5: 1, 6: 1},  # 541
        ]
        for args in args_list:
            scheme = draft.Scheme(args)
            assert scheme.is_valid()

    @staticmethod
    def test_is_valid():
        """Test is not valid method."""
        args_list = [
            {1: 1, 2: 2, 3: 2, 4: 4, 5: 2, 6: 0},  # No coach
            {1: 1, 2: 0, 3: 3, 4: 6, 5: 2, 6: 1},  # Too many midfielders
            {1: 0, 2: 2, 3: 2, 4: 5, 5: 1, 6: 1},  # No goalkeeper
            {1: 1, 2: 2, 3: 3, 4: 4, 5: 2, 6: 1},  # Too many players
        ]
        for args in args_list:
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
