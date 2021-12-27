"""Helper functions for unit-tests."""

import json
import os
import random
from typing import Any, Dict, List

import cartola_draft as draft

THIS_FOLDER = os.path.dirname(__file__)
PLAYERS_JSON_PATH = os.path.join(THIS_FOLDER, "data", "players.json")
POSITIONS = ["goalkeeper", "fullback", "defender", "midfielder", "forward", "coach"]
SCHEMES_COUNTING = {
    442: {
        "goalkeeper": 1,
        "fullback": 2,
        "defender": 2,
        "midfielder": 4,
        "forward": 2,
        "coach": 1,
    },
    433: {
        "goalkeeper": 1,
        "fullback": 2,
        "defender": 2,
        "midfielder": 3,
        "forward": 3,
        "coach": 1,
    },
    352: {
        "goalkeeper": 1,
        "fullback": 0,
        "defender": 3,
        "midfielder": 5,
        "forward": 2,
        "coach": 1,
    },
    541: {
        "goalkeeper": 1,
        "fullback": 2,
        "defender": 3,
        "midfielder": 4,
        "forward": 1,
        "coach": 1,
    },
}

INVALID_SCHEMES_COUNTING = {
    442: {  # No coach
        "goalkeeper": 1,
        "fullback": 2,
        "defender": 2,
        "midfielder": 4,
        "forward": 2,
        "coach": 0,
    },
    362: {  # Too many midfielders
        "goalkeeper": 1,
        "fullback": 0,
        "defender": 3,
        "midfielder": 6,
        "forward": 2,
        "coach": 1,
    },
    541: {  # No goalkeeper
        "goalkeeper": 0,
        "fullback": 2,
        "defender": 3,
        "midfielder": 4,
        "forward": 1,
        "coach": 1,
    },
    542: {  # Too many players
        "goalkeeper": 1,
        "fullback": 2,
        "defender": 3,
        "midfielder": 4,
        "forward": 1,
        "coach": 2,
    },
}


def load_players_dict() -> List[Dict[str, Any]]:
    """Create line-up players dict."""
    # Load players data from JSON folder.
    with open(PLAYERS_JSON_PATH, mode="r", encoding="utf-8") as file:
        return json.load(file)


def load_players() -> List[draft.Player]:
    """Create line-up players."""
    return [draft.Player(**player) for player in load_players_dict()]


def load_players_by_position() -> Dict[str, List[draft.Player]]:
    """Create line-up players."""
    # Load players.
    players = load_players()
    # Separate players by position.
    return {
        pos: [player for player in players if player.position == pos]
        for pos in POSITIONS
    }


def get_random_players(amount: int, position: str) -> List[draft.Player]:
    """Get some random players."""
    return [random.choice(load_players_by_position()[position]) for _ in range(amount)]


def get_random_players_with_scheme(scheme: draft.Scheme) -> List[draft.Player]:
    """Construct a list random players following a scheme."""
    return [
        player
        for key, val in scheme.positions.items()
        for player in get_random_players(val, key)
    ]
