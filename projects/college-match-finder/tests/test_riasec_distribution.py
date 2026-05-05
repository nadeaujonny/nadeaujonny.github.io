"""Tests for Phase 12.1d riasec_distribution loader.

Validates the contract of get_riasec_for_cip4() and get_all_cip4_vectors()
defined in riasec_distribution.py. All tests are structural / contract /
range-based — no hardcoded numeric RIASEC values, which would break on
source updates.
"""
import pandas as pd
import pytest

from riasec_distribution import (
    _load_riasec_data,
    get_all_cip4_vectors,
    get_riasec_for_cip4,
)
from utils import normalize_cip4 as _normalize_cip4

_RIASEC_KEYS = {"R", "I", "A", "S", "E", "C"}


# ---------------------------------------------------------------------------
# Normalization helper
# ---------------------------------------------------------------------------

def test_normalize_dotted_format_passthrough():
    assert _normalize_cip4("11.07") == "11.07"


def test_normalize_4digit_to_dotted():
    assert _normalize_cip4("1107") == "11.07"


def test_normalize_3digit_pads_and_dots():
    """E.g., CIP 01.07 passed as raw int string '107' → '01.07'."""
    assert _normalize_cip4("107") == "01.07"


def test_normalize_float_input_zero_pads():
    """str(float(1.0)) == '1.0' — must become '01.00'."""
    assert _normalize_cip4(1.0) == "01.00"


# ---------------------------------------------------------------------------
# get_riasec_for_cip4 — happy path
# ---------------------------------------------------------------------------

def test_get_riasec_for_known_cip4():
    """Social Work (44.07) — canary from Phase 12.1c — returns full dict."""
    result = get_riasec_for_cip4("44.07")
    assert result is not None
    assert set(result.keys()) == {"cip4", "scores", "n_socs", "coverage_pct"}
    assert result["cip4"] == "44.07"
    assert _RIASEC_KEYS == set(result["scores"].keys())
    assert isinstance(result["n_socs"], int)
    assert isinstance(result["coverage_pct"], float)


def test_riasec_scores_in_range():
    """All six RIASEC scores must be on the O*NET IRT [1.0, 7.0] scale."""
    result = get_riasec_for_cip4("44.07")
    assert result is not None
    for key, val in result["scores"].items():
        assert isinstance(val, float), f"{key} is not float: {val!r}"
        assert 1.0 <= val <= 7.0, f"{key}={val} outside [1.0, 7.0]"


# ---------------------------------------------------------------------------
# get_riasec_for_cip4 — empty-state contract
# ---------------------------------------------------------------------------

def test_get_riasec_for_unknown_cip4_returns_none():
    """CIP4 not in the dataset returns None (not an exception)."""
    assert get_riasec_for_cip4("55.55") is None


def test_empty_state_liberal_arts_returns_none():
    """Liberal Arts 24.01 is in the CSV but has zero O*NET coverage → None."""
    assert get_riasec_for_cip4("24.01") is None


# ---------------------------------------------------------------------------
# get_riasec_for_cip4 — dual-format normalization
# ---------------------------------------------------------------------------

def test_dot_and_no_dot_formats_equivalent():
    """'11.07' and '1107' must return identical dicts."""
    dotted = get_riasec_for_cip4("11.07")
    nodot = get_riasec_for_cip4("1107")
    assert dotted is not None and nodot is not None
    assert dotted == nodot


# ---------------------------------------------------------------------------
# get_all_cip4_vectors
# ---------------------------------------------------------------------------

def test_get_all_cip4_vectors_shape():
    """Full RIASEC matrix must be 416 rows × 7 columns."""
    df = get_all_cip4_vectors()
    assert df.shape == (416, 7), f"Expected (416, 7), got {df.shape}"


def test_get_all_cip4_vectors_columns():
    """Column order is exactly ['cip4', 'R', 'I', 'A', 'S', 'E', 'C']."""
    df = get_all_cip4_vectors()
    assert list(df.columns) == ["cip4", "R", "I", "A", "S", "E", "C"]


# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------

def test_loader_caching():
    """lru_cache must record at least one hit after a second call."""
    _load_riasec_data.cache_clear()
    get_riasec_for_cip4("44.07")  # first call — populates cache
    get_riasec_for_cip4("44.07")  # second call — should hit cache
    info = _load_riasec_data.cache_info()
    assert info.hits >= 1, f"Expected cache hit, got: {info}"
