"""Unit tests for greedy algorithm."""

import timeit

import pytest

from cartola_draft import Scheme
from cartola_draft.algorithm import DraftError
from cartola_draft.algorithm.greedy import Greedy
from . import helper

MAX_EXEC_TIME = 0.1  # seconds
SCHEMES = {442: Scheme(helper.SCHEMES_COUNTING[442])}


class TestTypicalDraft:
    """Test draft method from Greedy class."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        cls.algo = Greedy(helper.load_players())

    def test_line_up_is_valid(self):
        """Test if line up is valid.."""
        line_up = self.algo.draft(100, SCHEMES[442], 12)
        assert line_up.is_valid()

    def test_max_players_per_club(self):
        """Test if max players per club is respected."""
        line_up = self.algo.draft(100, SCHEMES[442], 3)
        assert max(line_up.players_per_club.values()) <= 3

    def test_speed(self):
        """Test if draft is fast."""
        # Time-it receive a string or a callable, so it is simpler to use lamda.
        times = timeit.timeit(
            lambda: self.algo.draft(100, SCHEMES[442], 12), number=100
        )
        assert times < MAX_EXEC_TIME * 100


class TestExtremeCases:
    """Test exceptions."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def test_few_players():
        """Test trying to use few players."""
        algo = Greedy(helper.load_players()[:10])
        with pytest.raises(DraftError):
            algo.draft(100, SCHEMES[442], 12)
