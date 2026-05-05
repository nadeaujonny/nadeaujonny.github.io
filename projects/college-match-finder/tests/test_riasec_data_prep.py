"""Tests for Phase 12.1 O*NET RIASEC interest-score data prep.

Validates the cleaned cip4_riasec.csv output produced by build_cip4_riasec()
in data_prep_riasec.py.

Run from project root:
    pytest tests/test_riasec_data_prep.py
"""

from pathlib import Path

import pandas as pd
import pytest


CLEANED_PATH = Path("data/cleaned/cip4_riasec.csv")
RIASEC_DIMS = ["R", "I", "A", "S", "E", "C"]
EXPECTED_COLUMNS = {"cip4", "R", "I", "A", "S", "E", "C", "n_socs", "coverage_pct"}

# Source data uses O*NET IRT-derived 1–7 scale.
SCORE_MIN = 1.0
SCORE_MAX = 7.0


@pytest.fixture(scope="module")
def cip4_riasec() -> pd.DataFrame:
    """Load the cleaned RIASEC dataset for all tests."""
    assert CLEANED_PATH.exists(), (
        f"{CLEANED_PATH} not found. Run "
        "`python data_prep_riasec.py` to build it."
    )
    return pd.read_csv(CLEANED_PATH, dtype={"cip4": str})


def test_output_file_exists():
    """data/cleaned/cip4_riasec.csv was produced by data_prep_riasec.py."""
    assert CLEANED_PATH.exists(), (
        f"{CLEANED_PATH} not found. Run `python data_prep_riasec.py`."
    )


def test_expected_columns(cip4_riasec: pd.DataFrame):
    """Output has exactly the 9 required columns, no more, no less."""
    assert set(cip4_riasec.columns) == EXPECTED_COLUMNS, (
        f"Column mismatch. Got: {set(cip4_riasec.columns)}"
    )


def test_expected_shape(cip4_riasec: pd.DataFrame):
    """Row count is in the expected ballpark.

    Rule: all 416 CIP4s in the routing table appear in the output, including
    the 3 with 0% RIASEC coverage (empty-state rows). Tolerance of ±50 allows
    for future crosswalk updates without a test change.

    Baseline (Phase 12.1, May-2024 BLS + O*NET 30.2): 416 rows.
    """
    n = len(cip4_riasec)
    assert 364 <= n <= 466, (
        f"Row count {n} outside expected range 364–466. "
        "Baseline: 416 (including 3 empty-state rows)."
    )


def test_no_duplicate_cip4s(cip4_riasec: pd.DataFrame):
    """Each CIP4 code appears at most once — no aggregation duplicates."""
    dupes = cip4_riasec[cip4_riasec["cip4"].duplicated()]["cip4"].tolist()
    assert not dupes, f"Duplicate CIP4 codes found: {dupes}"


def test_riasec_scores_in_range(cip4_riasec: pd.DataFrame):
    """All non-null RIASEC scores are within the O*NET IRT scale of 1.0–7.0."""
    for dim in RIASEC_DIMS:
        col = cip4_riasec[dim].dropna()
        lo = float(col.min())
        hi = float(col.max())
        assert lo >= SCORE_MIN, (
            f"{dim} has value {lo:.3f} below expected minimum {SCORE_MIN}"
        )
        assert hi <= SCORE_MAX, (
            f"{dim} has value {hi:.3f} above expected maximum {SCORE_MAX}"
        )


def test_coverage_pct_in_range(cip4_riasec: pd.DataFrame):
    """coverage_pct is between 0 and 100 inclusive for every CIP4."""
    lo = float(cip4_riasec["coverage_pct"].min())
    hi = float(cip4_riasec["coverage_pct"].max())
    assert lo >= 0.0, f"coverage_pct has value {lo} below 0"
    assert hi <= 100.0, f"coverage_pct has value {hi} above 100"


def test_n_socs_non_negative(cip4_riasec: pd.DataFrame):
    """n_socs is >= 0 for all rows (0 is valid for empty-state CIP4s)."""
    assert (cip4_riasec["n_socs"] >= 0).all(), (
        "n_socs has negative values, which should never occur"
    )


def test_known_cip4_canary(cip4_riasec: pd.DataFrame):
    """Social Work (44.07) — S (Social) must be the highest RIASEC dimension.

    This CIP4 has unambiguously high Social scores (S=6.47 at baseline) and
    is a stable canary for regression in the aggregation logic. Note: Computer
    Science (11.07) has C as its empirical top dimension (not I), which is a
    valid O*NET finding — the Conventional dimension captures working with data
    and rule-following systems.
    """
    row = cip4_riasec[cip4_riasec["cip4"] == "44.07"]
    assert len(row) == 1, "CIP4 44.07 (Social Work) is missing from the output"
    scores = row.iloc[0][RIASEC_DIMS]
    assert scores.idxmax() == "S", (
        f"Expected S to be the highest dimension for Social Work (44.07), "
        f"got {scores.idxmax()}. Scores: {scores.round(2).to_dict()}"
    )


def test_military_tech_cip4s_have_zero_coverage(cip4_riasec: pd.DataFrame):
    """28.05 and 28.06 (Military Technologies) route to SOCs absent from the
    O*NET Interests file — they appear in the output with n_socs=0 and NaN
    scores. The loader in Phase 12.1d should return None for these."""
    for cip in ["28.05", "28.06"]:
        row = cip4_riasec[cip4_riasec["cip4"] == cip]
        assert len(row) == 1, f"CIP4 {cip} should appear as an empty-state row"
        assert row.iloc[0]["n_socs"] == 0, (
            f"CIP4 {cip} expected n_socs=0, got {row.iloc[0]['n_socs']}"
        )
        assert row.iloc[0]["coverage_pct"] == 0.0, (
            f"CIP4 {cip} expected coverage_pct=0.0, got {row.iloc[0]['coverage_pct']}"
        )


def test_cip4_format(cip4_riasec: pd.DataFrame):
    """CIP4 codes use the XX.XX dot convention (5 chars with period at index 2)."""
    lengths = cip4_riasec["cip4"].str.len()
    assert (lengths == 5).all(), (
        f"Some CIP4 codes are not 5 characters: "
        f"{cip4_riasec[lengths != 5]['cip4'].tolist()}"
    )
    assert (cip4_riasec["cip4"].str[2] == ".").all(), (
        "Some CIP4 codes lack a period at position 2"
    )
