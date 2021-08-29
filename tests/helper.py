"""Helper functions for unit-tests."""

import json
import os
import random
from typing import Dict, List

import cartola_draft as draft

THIS_FOLDER = os.path.dirname(__file__)
PLAYERS_JSON_PATH = os.path.join(THIS_FOLDER, "data", "players.json")

INT2POS = {
    1: "goalkeepers",
    2: "fullbacks",
    3: "defenders",
    4: "midfielders",
    5: "forwards",
    6: "coaches",
}

SCHEMES_COUNTING = {
    442: {1: 1, 2: 2, 3: 2, 4: 4, 5: 2, 6: 1},
    352: {1: 1, 2: 0, 3: 3, 4: 5, 5: 2, 6: 1},
    541: {1: 1, 2: 2, 3: 3, 4: 4, 5: 1, 6: 1},
}


def load_players() -> Dict[int, draft.Player]:
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


def get_random_players_by_scheme(scheme: Dict[int, int]) -> Dict[str, draft.Player]:
    """Construct a dict with the position name and a list of random players."""
    return {
        INT2POS[key]: get_random_players(amount=val, position=key)
        for key, val in scheme.items()
    }
