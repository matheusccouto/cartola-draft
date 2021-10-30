"""Azure function."""

import json
import logging
from typing import Any, Callable, Dict, List

from cartola_draft import Player, Scheme
from cartola_draft.algorithm.greedy import Greedy

import azure.functions as func


def parse_scheme(scheme: Dict[str, int]) -> Scheme:
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


def parse_players(players: List[Dict[str, Any]]) -> List[Player]:
    """Parse players argument."""
    return [Player(**player) for player in players]


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure function execution."""
    logging.info("Python HTTP trigger function processed a request.")

    # Load arguments
    args = req.get_json()

    # Parse arguments.
    scheme = parse_scheme(args["scheme"])
    algo_class = parse_algorithm(args["algorithm"])
    players = parse_players(args["players"])

    # Create algorithm instance.
    algo = algo_class(players)

    # Draft line-up.
    line_up = algo.draft(scheme)

    return func.HttpResponse(json.dumps(line_up.players, default=vars), status_code=200)