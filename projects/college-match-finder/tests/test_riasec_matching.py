"""Tests for Phase 12.2b riasec_matching engine.

Validates the contracts of compute_holland_code(), compute_correlations(), and
get_top_n_matches() defined in riasec_matching.py. Tests are structural / contract /
range-based or mathematically-derived — no hardcoded numeric correlation values from
the dataset, which would break on source updates. The one exception is the perfect
self-match test, which checks correlation > 0.999 as a mathematical property, not a
data value.
"""
import numpy as np
import pandas as pd
import pytest

from riasec_distribution import get_riasec_for_cip4
from riasec_matching import (
    RIASEC_DIMENSIONS,
    compute_correlations,
    compute_holland_code,
    get_top_n_matches,
)

_DIMS = RIASEC_DIMENSIONS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _flat_vector(value: float) -> dict:
    """Return a RIASEC dict with every dimension set to value."""
    return {d: value for d in _DIMS}


# ---------------------------------------------------------------------------
# Holland Code tests
# ---------------------------------------------------------------------------

def test_holland_code_basic():
    """Standard example: I highest, R second, E third → 'IRE'."""
    vec = {"R": 35.0, "I": 38.0, "A": 12.0, "S": 9.0, "E": 22.0, "C": 14.0}
    assert compute_holland_code(vec) == "IRE"


def test_holland_code_canonical_tiebreak():
    """All dimensions equal → canonical order R > I > A wins → 'RIA'."""
    assert compute_holland_code(_flat_vector(20.0)) == "RIA"


def test_holland_code_partial_tie():
    """A and S tie for second; A wins on canonical order → 'IAS'."""
    vec = {"R": 10.0, "I": 30.0, "A": 20.0, "S": 20.0, "E": 5.0, "C": 5.0}
    assert compute_holland_code(vec) == "IAS"


def test_holland_code_missing_key_raises():
    """Five-key dict must raise ValueError (one RIASEC dimension absent)."""
    incomplete = {d: 20.0 for d in _DIMS if d != "C"}
    with pytest.raises(ValueError):
        compute_holland_code(incomplete)


def test_holland_code_returns_three_letters():
    """Output is always a 3-character string with letters from RIASEC set."""
    code = compute_holland_code({"R": 10.0, "I": 5.0, "A": 30.0, "S": 25.0, "E": 15.0, "C": 20.0})
    assert len(code) == 3
    assert all(ch in set(_DIMS) for ch in code)


# ---------------------------------------------------------------------------
# Correlation tests
# ---------------------------------------------------------------------------

def test_compute_correlations_shape():
    """Output must have 416 rows and 8 columns (cip4, correlation, R-I-A-S-E-C)."""
    df = compute_correlations({"R": 20.0, "I": 30.0, "A": 10.0, "S": 25.0, "E": 15.0, "C": 5.0})
    assert df.shape == (416, 8), f"Expected (416, 8), got {df.shape}"


def test_compute_correlations_columns():
    """Column names and order must match the contract exactly."""
    df = compute_correlations({"R": 20.0, "I": 30.0, "A": 10.0, "S": 25.0, "E": 15.0, "C": 5.0})
    assert list(df.columns) == ["cip4", "correlation", *_DIMS]


def test_compute_correlations_sorted_desc():
    """Non-NaN correlations must be monotonically decreasing (NaN sorted last)."""
    df = compute_correlations({"R": 20.0, "I": 30.0, "A": 10.0, "S": 25.0, "E": 15.0, "C": 5.0})
    non_nan = df["correlation"].dropna()
    assert non_nan.is_monotonic_decreasing, "correlations are not sorted descending"


def test_compute_correlations_range():
    """All non-NaN correlation values must lie in [-1.0, 1.0]."""
    df = compute_correlations({"R": 20.0, "I": 30.0, "A": 10.0, "S": 25.0, "E": 15.0, "C": 5.0})
    non_nan = df["correlation"].dropna()
    assert (non_nan >= -1.0).all() and (non_nan <= 1.0).all()


def test_compute_correlations_perfect_self_match():
    """Social Work (44.07) correlated against its own vector must return correlation > 0.999."""
    profile = get_riasec_for_cip4("44.07")
    assert profile is not None, "44.07 Social Work must be present in RIASEC data"
    user_vec = profile["scores"]  # {R, I, A, S, E, C} on O*NET IRT scale

    df = compute_correlations(user_vec)
    top_row = df.iloc[0]

    assert top_row["cip4"] == "44.07", (
        f"Expected 44.07 as top match for Social Work self-vector, got {top_row['cip4']}"
    )
    corr = top_row["correlation"]
    assert corr > 0.999, f"Self-match correlation for 44.07 is {corr:.6f}, expected > 0.999"


def test_compute_correlations_zero_variance_all_nan():
    """A flat user vector (zero variance) makes Pearson undefined — all correlations must be NaN.

    Rationale: Pearson correlation is the covariance divided by the product of standard
    deviations; a constant vector has std=0, making the denominator zero and the result
    mathematically undefined. Returning NaN rather than raising keeps the UI path clean.
    """
    df = compute_correlations(_flat_vector(20.0))
    assert df["correlation"].isna().all(), "Expected all NaN for zero-variance user vector"


def test_compute_correlations_missing_key_raises():
    """Five-key user dict must raise ValueError."""
    incomplete = {d: 20.0 for d in _DIMS if d != "I"}
    with pytest.raises(ValueError):
        compute_correlations(incomplete)


# ---------------------------------------------------------------------------
# Top-N wrapper tests
# ---------------------------------------------------------------------------

def test_get_top_n_default():
    """Default n=10 must return exactly 10 rows."""
    df = get_top_n_matches({"R": 20.0, "I": 30.0, "A": 10.0, "S": 25.0, "E": 15.0, "C": 5.0})
    assert len(df) == 10


def test_get_top_n_custom():
    """n=40 must return exactly 40 rows (Phase 12.3 badge threshold)."""
    df = get_top_n_matches({"R": 20.0, "I": 30.0, "A": 10.0, "S": 25.0, "E": 15.0, "C": 5.0}, n=40)
    assert len(df) == 40


def test_get_top_n_drops_nan():
    """Returned rows must all have non-NaN correlation values."""
    df = get_top_n_matches({"R": 20.0, "I": 30.0, "A": 10.0, "S": 25.0, "E": 15.0, "C": 5.0})
    assert not df["correlation"].isna().any(), "Top-N result must not contain NaN correlations"


def test_get_top_n_zero_variance_returns_empty():
    """A flat user vector (all NaN correlations) must return an empty DataFrame, not an error."""
    df = get_top_n_matches(_flat_vector(20.0))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# ---------------------------------------------------------------------------
# Sanity test — Realistic user
# ---------------------------------------------------------------------------

def test_known_alignment_realistic_user():
    """A strongly Realistic user vector should surface canonically Realistic CIP families.

    Constructs a max-R, low-everything-else vector and asserts that at least one
    of the top 10 CIP4s begins with '15.' (Engineering Technologies), '01.'
    (Agriculture/Food Sciences), or '46.' (Construction Trades) — the three
    families with the heaviest Realistic loading in O*NET data. This is a soft
    alignment sanity check; if it fails, investigate the data before muting.
    """
    realistic_vec = {"R": 40.0, "I": 5.0, "A": 5.0, "S": 5.0, "E": 5.0, "C": 5.0}
    df = get_top_n_matches(realistic_vec, n=10)

    realistic_prefixes = {"15.", "01.", "46."}
    top_cip4s = df["cip4"].tolist()
    found = any(
        any(cip.startswith(prefix) for prefix in realistic_prefixes)
        for cip in top_cip4s
    )
    assert found, (
        f"Expected at least one Realistic CIP family (15.xx, 01.xx, 46.xx) in top 10, "
        f"got: {top_cip4s}"
    )
