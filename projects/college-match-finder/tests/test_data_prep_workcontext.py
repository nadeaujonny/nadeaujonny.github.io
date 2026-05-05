"""
test_data_prep_workcontext.py — Tests for data_prep_workcontext.py.

Run with:
    pytest tests/ -v

All tests use synthetic DataFrames rather than reading the real 297k-row Excel
file, following the convention established in test_data_prep_majors.py for
filter/computation tests.
"""

import numpy as np
import pandas as pd
import pytest

from data_prep_workcontext import (
    clean_work_context,
    aggregate_to_bls_soc,
    pivot_to_wide,
    NUMERIC_SCALES,
    ELEMENTS_TO_KEEP,
)


# ============================================================
# Helpers for building synthetic raw DataFrames
# ============================================================

def _make_raw_row(
    onet_soc="15-1252.00",
    title="Software Developers",
    element_name="Time Pressure",
    scale_id="CX",
    data_value="3.5",
    n="20",
    recommend_suppress="N",
    not_relevant="N",
) -> dict:
    """Build one row matching the raw Work Context Excel column layout."""
    return {
        "O*NET-SOC Code": onet_soc,
        "Title": title,
        "Element ID": "4.C.1.a.1",
        "Element Name": element_name,
        "Scale ID": scale_id,
        "Scale Name": "Context",
        "Category": "",
        "Data Value": data_value,
        "N": n,
        "Standard Error": "0.05",
        "Lower CI Bound": "3.0",
        "Upper CI Bound": "4.0",
        "Recommend Suppress": recommend_suppress,
        "Not Relevant": not_relevant,
        "Date": "04/2026",
        "Domain Source": "Analyst",
    }


def _make_raw_df(rows: list[dict]) -> pd.DataFrame:
    """Convert a list of row dicts into a dtype=str DataFrame (mimics dtype=str read)."""
    return pd.DataFrame(rows).astype(str)


# ============================================================
# clean_work_context — filter to numeric scales
# ============================================================

def test_filter_to_numeric_scales_only():
    """Only CX and CT rows survive; CXP and CTP rows are dropped."""
    rows = [
        _make_raw_row(scale_id="CX"),
        _make_raw_row(scale_id="CT"),
        _make_raw_row(scale_id="CXP"),
        _make_raw_row(scale_id="CTP"),
    ]
    raw = _make_raw_df(rows)
    result = clean_work_context(raw)
    assert set(result["scale_id"]) == {"CX", "CT"}
    assert len(result) == 2


# ============================================================
# clean_work_context — suppress / not-relevant drops
# ============================================================

def test_drop_recommend_suppress():
    """Rows with Recommend Suppress == 'Y' are dropped; 'N' rows are kept."""
    rows = [
        _make_raw_row(recommend_suppress="Y"),
        _make_raw_row(recommend_suppress="N"),
    ]
    raw = _make_raw_df(rows)
    result = clean_work_context(raw)
    assert len(result) == 1
    # Verify the kept row is the non-suppressed one (rating coerces to 3.5)
    assert result.iloc[0]["rating"] == pytest.approx(3.5)


def test_drop_not_relevant():
    """Rows with Not Relevant == 'Y' are dropped."""
    rows = [
        _make_raw_row(not_relevant="Y"),
        _make_raw_row(not_relevant="N"),
    ]
    raw = _make_raw_df(rows)
    result = clean_work_context(raw)
    assert len(result) == 1


# ============================================================
# clean_work_context — element subset filter
# ============================================================

def test_only_kept_elements_pass_filter():
    """Only elements listed in ELEMENTS_TO_KEEP survive the filter."""
    kept_elem = "Time Pressure"
    dropped_elem = "Exposed to Whole Body Vibration"  # real O*NET element not in our list
    rows = [
        _make_raw_row(element_name=kept_elem),
        _make_raw_row(element_name=dropped_elem),
    ]
    raw = _make_raw_df(rows)
    result = clean_work_context(raw)
    assert len(result) == 1
    assert result.iloc[0]["element_name"] == kept_elem


def test_element_short_label_mapping():
    """'Duration of Typical Work Week' must map to 'hours_per_week'."""
    rows = [_make_raw_row(element_name="Duration of Typical Work Week", scale_id="CT")]
    raw = _make_raw_df(rows)
    result = clean_work_context(raw)
    assert len(result) == 1
    assert result.iloc[0]["element_short"] == "hours_per_week"


# ============================================================
# aggregate_to_bls_soc — SOC stripping
# ============================================================

def _make_clean_row(
    onet_soc: str,
    element_short: str,
    rating: float,
    sample_size: float,
    element_name: str = "Time Pressure",
) -> dict:
    return {
        "onet_soc_code": onet_soc,
        "occupation_title": "Test",
        "element_name": element_name,
        "element_short": element_short,
        "scale_id": "CX",
        "rating": rating,
        "sample_size": sample_size,
    }


def test_onet_soc_strips_to_6_digit():
    """'15-1252.00' and '15-1252.01' both produce soc_code '15-1252'."""
    rows = [
        _make_clean_row("15-1252.00", "time_pressure", 4.0, 20.0),
        _make_clean_row("15-1252.01", "time_pressure", 2.0, 10.0),
    ]
    clean = pd.DataFrame(rows)
    result = aggregate_to_bls_soc(clean)
    assert set(result["soc_code"]) == {"15-1252"}


# ============================================================
# aggregate_to_bls_soc — weighted mean math
# ============================================================

def test_weighted_mean_with_two_variants():
    """Weighted mean: (4.0*20 + 2.0*10) / 30 == 3.333..."""
    rows = [
        _make_clean_row("15-1252.00", "time_pressure", 4.0, 20.0),
        _make_clean_row("15-1252.01", "time_pressure", 2.0, 10.0),
    ]
    clean = pd.DataFrame(rows)
    result = aggregate_to_bls_soc(clean)
    row = result[result["soc_code"] == "15-1252"].iloc[0]
    expected = (4.0 * 20 + 2.0 * 10) / 30
    assert row["rating"] == pytest.approx(expected)


def test_weighted_mean_falls_back_to_unweighted_when_n_missing():
    """When all sample_size values are NaN, fall back to simple mean of ratings."""
    rows = [
        _make_clean_row("15-1252.00", "time_pressure", 4.0, np.nan),
        _make_clean_row("15-1252.01", "time_pressure", 2.0, np.nan),
    ]
    clean = pd.DataFrame(rows)
    result = aggregate_to_bls_soc(clean)
    row = result[result["soc_code"] == "15-1252"].iloc[0]
    # Simple mean: (4.0 + 2.0) / 2 = 3.0
    assert row["rating"] == pytest.approx(3.0)


# ============================================================
# pivot_to_wide — structural invariants
# ============================================================

def _make_multi_soc_agg() -> pd.DataFrame:
    """Build a minimal aggregated DataFrame with 3 SOCs and all 13 elements."""
    soc_codes = ["15-1252", "11-1011", "13-1081"]
    rows = []
    for soc in soc_codes:
        for elem_short in ELEMENTS_TO_KEEP.values():
            rows.append({
                "soc_code": soc,
                "element_short": elem_short,
                "rating": 3.0,
                "n_onet_soc_variants": 1,
                "total_sample_size": 20,
            })
    return pd.DataFrame(rows)


def test_pivot_one_row_per_soc():
    """After pivot, each soc_code appears in exactly one row."""
    agg = _make_multi_soc_agg()
    wide = pivot_to_wide(agg)
    assert wide["soc_code"].is_unique
    assert len(wide) == 3


def test_pivot_columns_match_elements_to_keep():
    """Element columns in wide output are exactly the values from ELEMENTS_TO_KEEP."""
    agg = _make_multi_soc_agg()
    wide = pivot_to_wide(agg)
    expected_elements = set(ELEMENTS_TO_KEEP.values())
    actual_elements = set(wide.columns) - {"soc_code", "elements_with_data", "avg_sample_size"}
    assert actual_elements == expected_elements


def test_coverage_columns_present():
    """Wide output must include elements_with_data and avg_sample_size columns."""
    agg = _make_multi_soc_agg()
    wide = pivot_to_wide(agg)
    assert "elements_with_data" in wide.columns
    assert "avg_sample_size" in wide.columns


# ============================================================
# clean_work_context — Data Value coercion
# ============================================================

def test_data_value_coercion_drops_non_numeric():
    """Rows with non-numeric Data Value (e.g., 'n/a') are dropped after coercion."""
    rows = [
        _make_raw_row(data_value="n/a"),
        _make_raw_row(data_value="3.5"),
    ]
    raw = _make_raw_df(rows)
    result = clean_work_context(raw)
    assert len(result) == 1
    assert result.iloc[0]["rating"] == pytest.approx(3.5)
