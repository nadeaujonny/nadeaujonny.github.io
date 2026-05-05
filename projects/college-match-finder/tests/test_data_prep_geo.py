"""
test_data_prep_geo.py — Tests for data_prep_geo.py.

Run with:
    pytest tests/ -v

Tests 1-9 read the actual raw file via load_oews_state() and build_state_occupations().
Test 10 uses monkeypatch to redirect output and verify the full write-read cycle.
"""

import pandas as pd
import pytest

import data_prep_geo as dpg
from data_prep_geo import (
    _filter_state_df,
    load_oews_state,
    build_state_occupations,
    OEWS_SUPPRESSION_VALUES,
)


# ============================================================
# Filter logic
# ============================================================

def test_load_oews_state_filters_to_detailed_cross_industry():
    """Filter must keep only O_GROUP=='detailed', NAICS=='000000', AREA_TYPE=='2'."""
    synthetic = pd.DataFrame({
        "NAICS": ["000000", "000000", "999999", "000000", "000000"],
        "O_GROUP": ["detailed", "detailed", "detailed", "major", "detailed"],
        "AREA_TYPE": ["2", "1", "2", "2", "2"],
        "OCC_CODE": ["15-1252", "15-1253", "15-1254", "15-1255", "15-1256"],
        "OCC_TITLE": ["A", "B", "C", "D", "E"],
        "TOT_EMP": ["100", "200", "300", "400", "500"],
    })
    result = _filter_state_df(synthetic)
    assert len(result) == 2
    assert set(result["OCC_CODE"]) == {"15-1252", "15-1256"}
    assert (result["NAICS"] == "000000").all()
    assert (result["O_GROUP"] == "detailed").all()
    assert (result["AREA_TYPE"] == "2").all()


# ============================================================
# Suppression handling
# ============================================================

def test_suppression_sentinels_become_nan():
    """After load_oews_state(), suppression strings must be NaN, not literal strings.

    load_oews_state() returns original BLS column names (TOT_EMP, LOC_QUOTIENT);
    renaming to snake_case happens later in build_state_occupations().
    """
    state = load_oews_state()
    for sentinel in OEWS_SUPPRESSION_VALUES:
        assert sentinel not in state["TOT_EMP"].astype(str).values
        assert sentinel not in state["LOC_QUOTIENT"].astype(str).values


# ============================================================
# String dtype — FIPS and state abbr
# ============================================================

def test_dtype_str_preserves_leading_zero_fips():
    """state_fips must be string-typed and preserve leading zeros (e.g., '01')."""
    state = load_oews_state()
    cleaned = build_state_occupations(state)
    assert pd.api.types.is_string_dtype(cleaned["state_fips"])
    # Alabama FIPS is '01' — would be 1 if coerced to int
    assert "01" in cleaned["state_fips"].values


def test_state_abbr_is_two_letter_string():
    """All state_abbr values must be exactly 2-character uppercase strings."""
    state = load_oews_state()
    cleaned = build_state_occupations(state)
    assert pd.api.types.is_string_dtype(cleaned["state_abbr"])
    lengths = cleaned["state_abbr"].str.len()
    assert (lengths == 2).all(), f"Found non-2-char abbr: {cleaned.loc[lengths != 2, 'state_abbr'].unique()}"


# ============================================================
# Uniqueness
# ============================================================

def test_unique_state_soc_pairs():
    """Each (state_fips, soc_code) pair must appear exactly once in the cleaned output."""
    state = load_oews_state()
    cleaned = build_state_occupations(state)
    dupes = cleaned.duplicated(subset=["state_fips", "soc_code"])
    assert not dupes.any(), f"Duplicate state-SOC pairs found: {dupes.sum()}"


# ============================================================
# Location quotient range
# ============================================================

def test_location_quotient_range():
    """Non-NaN location_quotient values must be positive; median should be near 1.0."""
    state = load_oews_state()
    cleaned = build_state_occupations(state)
    non_null_lq = cleaned["location_quotient"].dropna()
    assert (non_null_lq > 0).all(), "All LQ values must be positive"
    # LQ is a ratio (state share / national share); the employment-weighted median
    # should fall between 0.5 and 1.5 across the full state universe
    median_lq = non_null_lq.median()
    assert 0.5 <= median_lq <= 1.5, f"Unexpected median LQ: {median_lq:.3f}"


# ============================================================
# Colorado spot-check
# ============================================================

def test_colorado_present():
    """Colorado must have at least 500 SOC rows in the cleaned output."""
    state = load_oews_state()
    cleaned = build_state_occupations(state)
    co_rows = (cleaned["state_name"] == "Colorado").sum()
    assert co_rows >= 500, f"Expected >=500 Colorado rows, got {co_rows}"


# ============================================================
# Column order
# ============================================================

def test_column_order():
    """Cleaned output columns must appear in the documented order."""
    state = load_oews_state()
    cleaned = build_state_occupations(state)
    expected = [
        "state_fips", "state_abbr", "state_name",
        "soc_code", "occupation_title",
        "total_employment", "location_quotient", "jobs_per_1000",
        "annual_median", "annual_mean",
        "annual_pct10", "annual_pct25", "annual_pct75", "annual_pct90",
        "hourly_median", "hourly_mean",
    ]
    assert list(cleaned.columns) == expected


# ============================================================
# Numeric dtype
# ============================================================

def test_numeric_columns_are_float():
    """Wage and employment columns must be numeric after cleaning."""
    state = load_oews_state()
    cleaned = build_state_occupations(state)
    numeric_cols = [
        "total_employment", "location_quotient", "jobs_per_1000",
        "annual_median", "annual_mean",
        "annual_pct10", "annual_pct25", "annual_pct75", "annual_pct90",
        "hourly_median", "hourly_mean",
    ]
    for col in numeric_cols:
        assert pd.api.types.is_numeric_dtype(cleaned[col]), \
            f"Expected numeric dtype for {col}, got {cleaned[col].dtype}"


# ============================================================
# Integration: write and read back
# ============================================================

def test_cleaned_file_writes_and_reads_back(tmp_path, monkeypatch):
    """main() must write state_occupations.csv; it must read back with correct row count."""
    out_path = tmp_path / "state_occupations.csv"
    monkeypatch.setattr(dpg, "CLEANED_DIR", tmp_path)
    monkeypatch.setattr(dpg, "STATE_OCCUPATIONS_PATH", out_path)

    dpg.main()

    assert out_path.exists(), "state_occupations.csv was not written"
    result = pd.read_csv(out_path)
    assert len(result) > 30000, f"Expected >30k rows, got {len(result):,}"
    assert "state_fips" in result.columns
    assert "location_quotient" in result.columns
