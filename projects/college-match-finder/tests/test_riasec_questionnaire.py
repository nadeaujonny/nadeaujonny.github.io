"""Tests for Phase 12.2a riasec_questionnaire loader and scorer.

Validates the contract of get_items(), get_response_scale(), score_responses(),
and validate_responses() defined in riasec_questionnaire.py. Tests are
structural / contract / range-based — no hardcoded item text, which comes
from a public-domain source and may be revised independently of this module.
"""
import collections

import pytest

from riasec_questionnaire import (
    _load_items_data,
    get_items,
    get_response_scale,
    score_responses,
    validate_responses,
)

_DIMENSIONS = ["R", "I", "A", "S", "E", "C"]
_ITEMS_PER_DIM = 10
_TOTAL_ITEMS = 60
_SCALE_MIN = 0
_SCALE_MAX = 4


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _full_responses(value: int) -> dict:
    """Return a complete 60-item response dict with every item set to value."""
    return {item["id"]: value for item in get_items()}


# ---------------------------------------------------------------------------
# File presence
# ---------------------------------------------------------------------------

def test_yaml_file_exists():
    from pathlib import Path
    yaml_path = Path(__file__).parent.parent / "data" / "raw" / "riasec_items.yaml"
    assert yaml_path.exists(), f"Missing: {yaml_path}"


# ---------------------------------------------------------------------------
# get_items
# ---------------------------------------------------------------------------

def test_get_items_returns_60():
    assert len(get_items()) == _TOTAL_ITEMS


def test_get_items_dimension_balance():
    counts = collections.Counter(item["dimension"] for item in get_items())
    for dim in _DIMENSIONS:
        assert counts[dim] == _ITEMS_PER_DIM, (
            f"Dimension {dim} has {counts[dim]} items, expected {_ITEMS_PER_DIM}"
        )


def test_get_items_unique_ids():
    ids = [item["id"] for item in get_items()]
    assert len(ids) == len(set(ids)), "Duplicate item IDs found"


def test_get_items_schema():
    valid_dims = set(_DIMENSIONS)
    for item in get_items():
        assert set(item.keys()) == {"id", "dimension", "text"}, (
            f"Unexpected keys for item {item.get('id')}: {set(item.keys())}"
        )
        assert item["dimension"] in valid_dims, (
            f"Invalid dimension '{item['dimension']}' for item {item['id']}"
        )
        assert isinstance(item["text"], str) and item["text"].strip(), (
            f"Empty or non-string text for item {item['id']}"
        )


# ---------------------------------------------------------------------------
# get_response_scale
# ---------------------------------------------------------------------------

def test_get_response_scale_shape():
    scale = get_response_scale()
    assert scale["min"] == 0
    assert scale["max"] == 4
    assert isinstance(scale["labels"], dict)
    assert len(scale["labels"]) == 5
    assert all(isinstance(k, int) for k in scale["labels"])


# ---------------------------------------------------------------------------
# score_responses — happy path
# ---------------------------------------------------------------------------

def test_score_responses_all_zeros():
    result = score_responses(_full_responses(0))
    assert list(result.keys()) == _DIMENSIONS
    for dim in _DIMENSIONS:
        assert result[dim] == 0.0
        assert isinstance(result[dim], float)


def test_score_responses_all_max():
    result = score_responses(_full_responses(_SCALE_MAX))
    expected = float(_ITEMS_PER_DIM * _SCALE_MAX)  # 40.0
    for dim in _DIMENSIONS:
        assert result[dim] == expected


def test_score_responses_dimension_isolation():
    """Setting only R items to max and others to 0 must yield R=40, others=0."""
    responses = {}
    for item in get_items():
        responses[item["id"]] = _SCALE_MAX if item["dimension"] == "R" else 0
    result = score_responses(responses)
    assert result["R"] == float(_ITEMS_PER_DIM * _SCALE_MAX)
    for dim in ["I", "A", "S", "E", "C"]:
        assert result[dim] == 0.0


# ---------------------------------------------------------------------------
# score_responses — error cases
# ---------------------------------------------------------------------------

def test_score_responses_missing_id_raises():
    responses = _full_responses(2)
    dropped_id = list(responses.keys())[0]
    del responses[dropped_id]
    with pytest.raises(ValueError, match=dropped_id):
        score_responses(responses)


def test_score_responses_out_of_range_raises():
    responses = _full_responses(2)
    first_id = list(responses.keys())[0]
    responses[first_id] = 5
    with pytest.raises(ValueError):
        score_responses(responses)


def test_score_responses_negative_out_of_range_raises():
    responses = _full_responses(2)
    first_id = list(responses.keys())[0]
    responses[first_id] = -1
    with pytest.raises(ValueError):
        score_responses(responses)


def test_score_responses_unknown_id_raises():
    responses = _full_responses(2)
    responses["Z99"] = 2
    with pytest.raises(ValueError, match="Z99"):
        score_responses(responses)


# ---------------------------------------------------------------------------
# validate_responses
# ---------------------------------------------------------------------------

def test_validate_responses_returns_errors_not_raises():
    responses = _full_responses(2)
    first_id = list(responses.keys())[0]
    responses[first_id] = 99
    errors = validate_responses(responses)
    assert isinstance(errors, list)
    assert len(errors) > 0


def test_validate_responses_valid_input_empty_list():
    assert validate_responses(_full_responses(2)) == []


# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------

def test_loader_caching():
    _load_items_data.cache_clear()
    get_items()   # first call — populates cache
    get_items()   # second call — should hit cache
    info = _load_items_data.cache_info()
    assert info.hits >= 1, f"Expected cache hit, got: {info}"
