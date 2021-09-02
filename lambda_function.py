"""AWS lambda function."""

import json
from typing import Callable, Dict, List

from cartola_draft import Player, Scheme
from cartola_draft.algorithm.greedy import Greedy


def parse_scheme(scheme: Dict[int, int]) -> Scheme:
    """Parse scheme argument."""
    sch = Scheme(scheme)
    if not sch.is_valid():
        raise ValueError(f"{scheme} is not a valid scheme.")
    return sch


def parse_algorithm(name: str) -> Callable:
    """Parse algorithm argument."""
    if "greedy" in name.lower():
        return Greedy
    raise ValueError(f"{name} is not a valid algorithm")


def parse_players(players: List[Dict[str, float]]) -> List[Player]:
    """Parse players argument."""
    return [Player(**player) for player in players]


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """AWS lambda handler."""
    # Parse arguments.
    scheme = parse_scheme(event["scheme"])
    algo_class = parse_algorithm(event["algorithm"])
    players = parse_players(event["players"])

    # Create algorithm instance.
    algo = algo_class(players)

    # Draft line-up.
    line_up = algo.draft(scheme)

    return {"statusCode": 200, "body": json.dumps(line_up.players, default=vars)}
