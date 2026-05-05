"""Tests for Phase 13.3 get_school_all_programs helper.

Covers get_school_all_programs() in page_modules/major_explorer.py:
happy-path sort order, empty-school handling, NaN earnings sort, and
CIP4 dot-format output contract.
"""
import pandas as pd
import pytest
import streamlit as st

from page_modules.major_explorer import get_school_all_programs


@pytest.fixture(autouse=True)
def clear_session_state():
    """Reset session_state before every test."""
    st.session_state.clear()
    yield
    st.session_state.clear()


def test_get_school_all_programs_happy_path():
    """Returns programs for a school, sorted by median_earnings_1yr descending."""
    fos_df = pd.DataFrame({
        "unit_id": [100, 100, 100, 200],
        "cip_code": [1107, 2701, 5138, 1107],
        "cip_description": ["Computer Science", "Math", "Nursing", "Computer Science"],
        "median_earnings_1yr": [70000.0, 55000.0, 65000.0, 60000.0],
        "median_debt": [25000.0, 22000.0, 27000.0, 24000.0],
    })
    result = get_school_all_programs(fos_df, unitid=100)
    assert len(result) == 3
    assert list(result["cip4"]) == ["11.07", "51.38", "27.01"]
    assert list(result["major_name"]) == ["Computer Science", "Nursing", "Math"]


def test_get_school_all_programs_empty_for_unknown_school():
    """Returns empty DataFrame with correct columns for a school not in FoS data."""
    fos_df = pd.DataFrame({
        "unit_id": [100],
        "cip_code": [1107],
        "cip_description": ["CS"],
        "median_earnings_1yr": [70000.0],
        "median_debt": [25000.0],
    })
    result = get_school_all_programs(fos_df, unitid=999)
    assert len(result) == 0
    assert list(result.columns) == ["cip4", "major_name", "median_earnings_1yr", "median_debt"]


def test_get_school_all_programs_sorts_nan_earnings_last():
    """Programs with suppressed median_earnings_1yr (NaN) sort to the bottom."""
    fos_df = pd.DataFrame({
        "unit_id": [100, 100, 100],
        "cip_code": [1107, 2701, 5138],
        "cip_description": ["CS", "Math", "Nursing"],
        "median_earnings_1yr": [70000.0, float("nan"), 65000.0],
        "median_debt": [25000.0, 22000.0, 27000.0],
    })
    result = get_school_all_programs(fos_df, unitid=100)
    assert list(result["cip4"]) == ["11.07", "51.38", "27.01"]


def test_get_school_all_programs_formats_cip4_as_dotted_string():
    """cip_code stored as 4-digit int (1107); output cip4 uses dotted format ('11.07')."""
    fos_df = pd.DataFrame({
        "unit_id": [100],
        "cip_code": [1107],
        "cip_description": ["CS"],
        "median_earnings_1yr": [70000.0],
        "median_debt": [25000.0],
    })
    result = get_school_all_programs(fos_df, unitid=100)
    assert result["cip4"].iloc[0] == "11.07"
