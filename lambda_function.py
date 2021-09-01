"""AWS lambda function."""

import json

from cartola_draft import Player, Scheme
from cartola_draft.algorithm.greedy import Greedy


def lambda_handler(event, context):
    """AWS lambda handler."""
    # Parse scheme.
    scheme = Scheme(event["scheme"])
    if not scheme.is_valid():
        raise ValueError(f"The scheme {event['scheme']} is not valid.")

    # Parse algorithm.
    if "greedy" in event["algorithm"]:
        algo_class = Greedy
    else:
        raise ValueError(f"{event['algorithm']} is not a supported algorithm")

    # Create players instances.
    players = [Player(**player) for player in event["players"]]

    # Get instance.
    algo = algo_class(players)

    # Draft line-up.
    line_up = algo.draft(scheme)

    return {"statusCode": 200, "body": json.dumps(line_up, default=vars)}
