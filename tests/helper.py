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

INVALID_SCHEMES_COUNTING = {
    442: {1: 1, 2: 2, 3: 2, 4: 4, 5: 2, 6: 0},  # No coach
    362: {1: 1, 2: 0, 3: 3, 4: 6, 5: 2, 6: 1},  # Too many midfielders
    541: {1: 0, 2: 2, 3: 2, 4: 5, 5: 1, 6: 1},  # No goalkeeper
    542: {1: 1, 2: 2, 3: 3, 4: 4, 5: 2, 6: 1},  # Too many players
}


def load_players_dict() -> List[Dict[str, int]]:
    """Create line-up players dict."""
    # Load players data from JSON folder.
    with open(PLAYERS_JSON_PATH, mode="r", encoding="utf-8") as file:
        return json.load(file)


def load_players() -> List[draft.Player]:
    """Create line-up players."""
    return [draft.Player(**player) for player in load_players_dict()]


def load_players_by_position() -> Dict[int, List[draft.Player]]:
    """Create line-up players."""
    # Load players.
    players = load_players()
    # Separate players by position.
    return {
        i: [player for player in players if player.position == i]
        for i in range(1, 7, 1)
    }


def get_random_players(amount: int, position: int) -> List[draft.Player]:
    """Get some random players."""
    return [random.choice(load_players_by_position()[position]) for _ in range(amount)]


def get_random_players_with_scheme(scheme: draft.Scheme) -> List[draft.Player]:
    """Construct a list random players following a scheme."""
    return [
        player
        for key, val in scheme.positions.items()
        for player in get_random_players(val, key)
    ]
