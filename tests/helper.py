"""Helper functions for unit-tests."""

import json
import os
import random
from typing import Dict, List

import cartola_draft as draft

THIS_FOLDER = os.path.dirname(__file__)
PLAYERS_JSON_PATH = os.path.join(THIS_FOLDER, "data", "players.json")

SCHEMES_COUNTING = {
    442: {1: 1, 2: 2, 3: 2, 4: 4, 5: 2, 6: 1},
    352: {1: 1, 2: 0, 3: 3, 4: 5, 5: 2, 6: 1},
    541: {1: 1, 2: 2, 3: 3, 4: 4, 5: 1, 6: 1},
}


def load_players() -> Dict[int, List[draft.Player]]:
    """Create line-up players."""
    # Load players data from JSON folder.
    with open(PLAYERS_JSON_PATH, mode="r", encoding="utf-8") as file:
        players = json.load(file)

    # Separate players by position.
    return {
        i: [draft.Player(**play) for play in players if play["position"] == i]
        for i in range(1, 7, 1)
    }


def get_random_players(amount: int, position: int) -> List[draft.Player]:
    """Get some random players."""
    return [random.choice(load_players()[position]) for _ in range(amount)]


def get_random_players_with_scheme(scheme: draft.Scheme) -> List[draft.Player]:
    """Construct a list random players following a scheme."""
    return [
        player
        for key, val in scheme.positions.items()
        for player in get_random_players(val, key)
    ]
