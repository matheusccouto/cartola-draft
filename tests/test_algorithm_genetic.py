"""Unit tests for genetic algorithm."""

import cProfile
import timeit

import pytest

from cartola_draft import Scheme
from cartola_draft.algorithm import DraftError
from cartola_draft.algorithm.genetic import Genetic
from . import helper

MAX_EXEC_TIME = 30  # seconds. Needs to be improved
SCHEMES = {
    442: Scheme(helper.SCHEMES_COUNTING[442]),
    352: Scheme(helper.SCHEMES_COUNTING[352]),
}


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
        line_up = self.algo.draft(100, SCHEMES[442], 4)
        assert max(line_up.players_per_club.values()) <= 4

    def test_speed(self):
        """Test if draft is fast."""
        # Time-it receive a string or a callable, so it is simpler to use lamda.
        times = timeit.timeit(lambda: self.algo.draft(100, SCHEMES[442], 12), number=5)
        assert times < MAX_EXEC_TIME * 5

    def test_bench_amount(self):
        """Test if bench was drafted correctly."""
        line_up = self.algo.draft(100, SCHEMES[442], 3)
        assert len(line_up.bench) == 5
        assert len({p.position for p in line_up.bench}) == 5

    def test_bench_amount_when_position_does_not_exist(self):
        """Test if bench was drafted correctly when a position does not exist."""
        line_up = self.algo.draft(100, SCHEMES[352], 3)
        assert len(line_up.bench) == 4
        assert len({p.position for p in line_up.bench}) == 4

    def test_bench_prices(self):
        """Test if bench prices are lower than startes."""
        line_up = self.algo.draft(100, SCHEMES[442], 3)
        for player in line_up.bench:
            for pos, starters in line_up.players_by_position.items():
                if pos == player.position:
                    for starter in starters:
                        assert player.price < starter.price

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
