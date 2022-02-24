"""Azure function."""

import json
import logging
from typing import Any, Callable, Dict, List

import azure.functions as func

from cartola_draft import Player, Scheme
from cartola_draft.algorithm import DraftError
from cartola_draft.algorithm.greedy import Greedy
from cartola_draft.algorithm.genetic import Genetic


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
    if "genetic" in name.lower():
        return Genetic
    raise ValueError(f"{name} is not a valid algorithm")


def parse_players(players: List[Dict[str, Any]]) -> List[Player]:
    """Parse players argument."""
    return [Player(**player) for player in players]


def parse_price(price: float) -> float:
    """Parse price."""
    if price <= 0:
        raise ValueError("Price should be positve")
    return price


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure function execution."""
    logging.info("Python HTTP trigger function processed a request.")

    # Load arguments
    args = req.get_json()

    # Parse arguments.
    scheme = parse_scheme(args["scheme"])
    algo_class = parse_algorithm(args["algorithm"])
    players = parse_players(args["players"])
    price = parse_price(args["price"])

    # Create algorithm instance.
    algo = algo_class(players)

    # Draft line-up.
    try:
        line_up = algo.draft(price, scheme)
    except DraftError as error:
        return func.HttpResponse(
            str(error),
            status_code=400,
        )

    return func.HttpResponse(json.dumps(line_up.players, default=vars), status_code=200)
