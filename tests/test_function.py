"""Unit tests for AWS lambda function."""

import json

import pytest

import function
from cartola_draft import Player, Scheme
from cartola_draft.algorithm.greedy import Greedy
from . import helper


class TestScheme:
    """Test scheme parsing."""

    @staticmethod
    def test_valid():
        """Test valid values."""
        for args in helper.SCHEMES_COUNTING.values():
            scheme = function.parse_scheme(args)
            assert isinstance(scheme, Scheme)

    @staticmethod
    def test_not_valid():
        """Test not valid values."""
        for args in helper.INVALID_SCHEMES_COUNTING.values():
            with pytest.raises(ValueError):
                function.parse_scheme(args)


class TestAlgorithm:
    """Test algorithm argument passing."""

    @staticmethod
    def test_greedy():
        """Test parsing greedy algorithm."""
        for name in ["Greedy", "greedy", "GREEDY", "gReEdy", "greedy algorithm"]:
            # Create instance.
            algo = function.parse_algorithm(name)(helper.load_players())
            assert isinstance(algo, Greedy)

    @staticmethod
    def test_genetic():
        """Test parsing genetic algorithm."""
        for name in ["Genetic", "genetic", "GENETIC", "GeNeTic", "genetic algorithm"]:
            with pytest.raises(ValueError):
                function.parse_algorithm(name)

    @staticmethod
    def test_strange_name():
        """Make sure it raises when receiving invalid values.."""
        for name in ["algorithm", "protest", "pepper", "wall", "football"]:
            with pytest.raises(ValueError):
                function.parse_algorithm(name)


class TestPlayers:
    """Test players arguments parsing."""

    @staticmethod
    def test_valid():
        """Test parsing valid values."""
        players = helper.load_players_dict()
        for player in function.parse_players(players):
            isinstance(player, Player)

    @staticmethod
    def test_missing_keys():
        """Test if it raises when missing keys.."""
        players = helper.load_players_dict()
        players[-1].pop("points")  # Remove the key 'points' from a single dict
        with pytest.raises(TypeError):
            function.parse_players(players)

    @staticmethod
    def test_too_many_keys():
        """Test if it raises when missing keys.."""
        players = helper.load_players_dict()
        # Remove the key 'points'
        players[0]["extra"] = 0.0  # Add the key 'extra' to a single dict
        with pytest.raises(TypeError):
            function.parse_players(players)


# class TestLambdaFunction:
#     """Test AWS lambda function."""

#     # pylint: disable=too-few-public-methods

#     @staticmethod
#     def _test(event=None, context=None):
#         """General testig."""
#         res = function.main(event=event, context=context)
#         # Read JSON
#         res_body = json.loads(res["body"])
#         # Assert that status ig good.
#         assert res["statusCode"] == 200
#         # Make sure the reutn has the correct length.
#         assert len(res_body) == 12
#         # Make sure it has the right scheme.
#         event_body = json.loads(event["body"])
#         for pos, amount in event_body["scheme"].items():
#             players_from_pos = [item for item in res_body if item["position"] == pos]
#             assert len(players_from_pos) == amount

#     def test_greedy(self):
#         """Test draft using greedy algorithm."""
#         body = {
#             "scheme": helper.SCHEMES_COUNTING[442],
#             "players": helper.load_players_dict(),
#             "algorithm": "greedy",
#         }
#         self._test(event={"body": json.dumps(body)})