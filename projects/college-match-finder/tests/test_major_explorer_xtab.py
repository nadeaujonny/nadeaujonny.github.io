"""Tests for Phase 13.1 and 13.2 cross-tab session-state helpers.

Phase 13.1 covers set_major_explorer_cip() in page_modules/major_explorer.py.
Phase 13.2 covers set_school_finder_cip(), initial_cip_filter_index(), and
apply_cip_filter() in page_modules/school_finder.py. These two groups are
kept together because both test the cross-tab handoff session_state mechanics.
"""
import pandas as pd
import pytest
import streamlit as st

from page_modules.major_explorer import set_major_explorer_cip, SELECTED_CIP_KEY
from page_modules.school_finder import (
    apply_cip_filter,
    initial_cip_filter_index,
    set_school_finder_cip,
)


@pytest.fixture(autouse=True)
def clear_session_state():
    """Reset session_state before every test."""
    st.session_state.clear()
    yield
    st.session_state.clear()


# ---------------------------------------------------------------------------
# Phase 13.1 — set_major_explorer_cip helper
# ---------------------------------------------------------------------------

def test_set_major_explorer_cip_writes_session_state():
    """Dot-format CIP4 string is converted to int and written to selected_cip."""
    set_major_explorer_cip("11.07")
    assert st.session_state[SELECTED_CIP_KEY] == 1107


def test_set_major_explorer_cip_handles_string_input_without_dot():
    """Bare int string (no dot) also writes the correct integer."""
    set_major_explorer_cip("1107")
    assert st.session_state[SELECTED_CIP_KEY] == 1107


def test_set_major_explorer_cip_overwrites_prior_selection():
    """Helper replaces whatever was in selected_cip before the call."""
    st.session_state[SELECTED_CIP_KEY] = 2701
    set_major_explorer_cip("11.07")
    assert st.session_state[SELECTED_CIP_KEY] == 1107


def test_set_major_explorer_cip_clears_picker_widget_state():
    """Cross-tab handoff must clear the picker widget's persisted state
    so default_index is honored on next render. Regression test for
    widget-state shadowing bug discovered during 6E verification."""
    st.session_state["major_picker_widget"] = "Accounting (52.03)"

    set_major_explorer_cip("11.07")

    assert "major_picker_widget" not in st.session_state
    assert st.session_state[SELECTED_CIP_KEY] == 1107
    assert st.session_state["_last_xtab_cip"] == "11.07"
    assert st.session_state["_active_tab"] == "major_explorer"


# ---------------------------------------------------------------------------
# Phase 13.2 — set_school_finder_cip helper + initial_cip_filter_index
# ---------------------------------------------------------------------------

def test_set_school_finder_cip_writes_session_state():
    """Dot-format CIP4 is written to cip_filter_widget and fires banner sentinel."""
    st.session_state.pop("cip_filter_widget", None)
    st.session_state.pop("_last_xtab_cip_filter", None)
    set_school_finder_cip("11.07")
    assert st.session_state["cip_filter_widget"] == "11.07"
    assert st.session_state["_last_xtab_cip_filter"] == "11.07"


def test_set_school_finder_cip_handles_no_dot_format():
    """Bare int string is normalized to dot format before writing."""
    st.session_state.pop("cip_filter_widget", None)
    set_school_finder_cip("1107")
    assert st.session_state["cip_filter_widget"] == "11.07"


def test_set_school_finder_cip_overwrites_prior_selection():
    """Helper replaces whatever was in cip_filter_widget before the call."""
    st.session_state["cip_filter_widget"] = "27.01"
    set_school_finder_cip("11.07")
    assert st.session_state["cip_filter_widget"] == "11.07"


def test_initial_cip_filter_index_uses_session_state():
    """Pre-populated session key resolves to its position in the options list."""
    options = ["All majors", "11.07", "27.01"]
    st.session_state["cip_filter_widget"] = "27.01"
    assert initial_cip_filter_index(options) == 2


def test_initial_cip_filter_index_defaults_to_zero_when_unset():
    """No session key → returns 0 ('All majors')."""
    st.session_state.pop("cip_filter_widget", None)
    options = ["All majors", "11.07", "27.01"]
    assert initial_cip_filter_index(options) == 0


def test_initial_cip_filter_index_falls_back_when_value_not_in_options():
    """Stale session value (not in current options) → falls back to 0."""
    st.session_state["cip_filter_widget"] = "99.99"
    options = ["All majors", "11.07", "27.01"]
    assert initial_cip_filter_index(options) == 0


def test_apply_cip_filter_no_op_for_all_majors():
    """'All majors' sentinel leaves the school pool unchanged."""
    fos_df = pd.DataFrame({"cip_code": [1107], "unit_id": [1]})
    schools_df = pd.DataFrame({"unit_id": [1, 2], "school_name": ["MIT", "Caltech"]})
    result = apply_cip_filter(schools_df, "All majors", fos_df)
    assert len(result) == 2


def test_apply_cip_filter_restricts_to_offering_schools():
    """Only schools with a FoS row for the selected CIP survive the filter."""
    fos_df = pd.DataFrame({"cip_code": [1107, 1107, 2701], "unit_id": [1, 3, 2]})
    schools_df = pd.DataFrame({"unit_id": [1, 2, 3], "school_name": ["A", "B", "C"]})
    result = apply_cip_filter(schools_df, "11.07", fos_df)
    assert set(result["unit_id"]) == {1, 3}
    assert 2 not in result["unit_id"].values
