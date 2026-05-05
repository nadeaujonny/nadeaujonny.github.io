"""Loader and scorer for the O*NET Interest Profiler Short Form questionnaire.

Reads riasec_items.yaml (60 items, 10 per RIASEC dimension) via a single
lru_cache load and exposes get_items() for rendering the questionnaire and
get_response_scale() for building Likert widgets. score_responses() converts
a complete set of 60 integer responses (0–4) into a six-dimensional RIASEC
score vector where each dimension value is the sum of its 10 item responses
(range 0.0–40.0 per dimension). validate_responses() runs the same checks
but returns a list of error strings instead of raising, so the Streamlit page
can display all validation errors at once before calling score_responses().
"""
from collections import OrderedDict
from functools import lru_cache
from pathlib import Path
from typing import List

import yaml

from config import RIASEC_DIMENSIONS

_YAML_PATH = Path(__file__).parent / "data" / "riasec_items.yaml"
_SCALE_MIN = 0
_SCALE_MAX = 4


@lru_cache(maxsize=1)
def _load_items_data() -> dict:
    """Load and parse the YAML instrument file once per session."""
    with open(_YAML_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def get_items() -> List[dict]:
    """Return the 60 instrument items in source order (R×10, I×10, …, C×10).

    Each item is a dict with keys: id (str), dimension (str), text (str).
    """
    return _load_items_data()["items"]


def get_response_scale() -> dict:
    """Return the Likert scale config: min, max, and a labels dict (int → str)."""
    raw = _load_items_data()["response_scale"]
    return {
        "min": raw["min"],
        "max": raw["max"],
        "labels": {int(k): v for k, v in raw["labels"].items()},
    }


def validate_responses(responses: dict) -> List[str]:
    """Return a list of validation error messages; empty list means valid.

    Checks:
    - All 60 item IDs are present in responses.
    - No unknown item IDs are present.
    - All values are integers in [0, 4].
    """
    errors: List[str] = []
    valid_ids = {item["id"] for item in get_items()}

    unknown = set(responses.keys()) - valid_ids
    if unknown:
        errors.append(f"Unknown item ID(s): {', '.join(sorted(unknown))}")

    missing = valid_ids - set(responses.keys())
    if missing:
        errors.append(f"Missing response(s) for item ID(s): {', '.join(sorted(missing))}")

    for item_id, value in responses.items():
        if item_id in valid_ids:
            if not isinstance(value, int) or isinstance(value, bool):
                errors.append(f"Response for {item_id} must be an integer, got {value!r}")
            elif value < _SCALE_MIN or value > _SCALE_MAX:
                errors.append(
                    f"Response for {item_id} is {value}, must be in [{_SCALE_MIN}, {_SCALE_MAX}]"
                )

    return errors


def score_responses(responses: dict) -> "OrderedDict[str, float]":
    """Convert 60 Likert responses into a RIASEC score vector.

    Each dimension score is the SUM of the 10 item responses for that
    dimension (range 0.0–40.0). Summing matches the published O*NET
    methodology; Pearson correlation is invariant to this vs. mean.

    Args:
        responses: dict mapping item ID (e.g. 'R01') to integer 0–4.
                   Must contain exactly all 60 item IDs — no more, no less.

    Returns:
        OrderedDict with keys R, I, A, S, E, C (in that order), float values.

    Raises:
        ValueError: if any item ID is missing, unknown, or has an out-of-range value.
    """
    errors = validate_responses(responses)
    if errors:
        raise ValueError("; ".join(errors))

    items = get_items()
    totals: OrderedDict = OrderedDict((dim, 0.0) for dim in RIASEC_DIMENSIONS)
    for item in items:
        totals[item["dimension"]] += float(responses[item["id"]])

    return totals
