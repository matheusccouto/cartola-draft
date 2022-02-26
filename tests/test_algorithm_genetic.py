"""Unit tests for genetic algorithm."""

import cProfile
import timeit

import pytest

from cartola_draft import Scheme
from cartola_draft.algorithm import DraftError
from cartola_draft.algorithm.genetic import Genetic
from . import helper

MAX_EXEC_TIME = 10  # seconds
SCHEMES = {442: Scheme(helper.SCHEMES_COUNTING[442])}


class TestTypicalDraft:
    """Test draft method from Genetic class."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        cls.algo = Genetic(helper.load_players())

    def test_line_up_is_valid(self):
        """Test if line up is valid.."""
        line_up = self.algo.draft(100, SCHEMES[442], 12)
        assert line_up.is_valid()

    def test_max_players_per_club(self):
        """Test if max players per club is respected."""
        line_up = self.algo.draft(100, SCHEMES[433], 4)
        assert max(line_up.players_per_club.values()) <= 4

    def test_speed(self):
        """Test if draft is fast."""
        # Time-it receive a string or a callable, so it is simpler to use lamda.
        times = timeit.timeit(lambda: self.algo.draft(100, SCHEMES[442], 12), number=5)
        assert times < MAX_EXEC_TIME * 5


class TestExtremeCases:
    """Test exceptions."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def test_few_players():
        """Test trying to use few players."""
        algo = Genetic(helper.load_players()[:10])
        with pytest.raises(DraftError):
            algo.draft(100, SCHEMES[442], 12)


if __name__ == "__main__":
    # Profiling.
    cProfile.run("Genetic(helper.load_players()).draft(100, SCHEMES[442])")
