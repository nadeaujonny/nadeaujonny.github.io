"""
school_finder.py — Phase 13.2 cross-tab helpers for the School Finder tab.

Contains session-state manipulation used by other page modules (e.g., the
Major Explorer's 'See schools strong in this major' button) and the ranking
pipeline's CIP filter step. Deliberately imports only streamlit + pandas to
avoid circular imports with major_explorer.
"""

import pandas as pd
import streamlit as st

from utils import normalize_cip4, parse_cip_code


def set_school_finder_cip(cip4_str: str) -> None:
    """Pre-apply a CIP filter on the School Finder tab and fire the cross-tab banner.

    Used by the Major Explorer's 'See schools strong in this major' button (Phase 13.2).
    Mirror of set_major_explorer_cip from page_modules/major_explorer.py.

    Accepts both dot format ("11.07") and bare int string ("1107").
    """
    normalized = normalize_cip4(cip4_str)
    st.session_state["cip_filter_widget"] = normalized
    st.session_state["_last_xtab_cip_filter"] = normalized
    st.session_state["_active_tab"] = "school_finder"


def initial_cip_filter_index(options: list[str]) -> int:
    """Compute the initial index for the CIP filter selectbox.

    If a cross-tab handoff pre-populated cip_filter_widget, honor it.
    Falls back to 0 ('All majors') when the key is absent or stale (value not
    in options). Also removes stale keys so Streamlit doesn't raise a conflict
    when it tries to reconcile session state with the widget's option list.
    """
    target = st.session_state.get("cip_filter_widget")
    if target and target in options:
        return options.index(target)
    st.session_state.pop("cip_filter_widget", None)
    return 0


def apply_cip_filter(
    df: pd.DataFrame,
    cip_filter: str | None,
    fos_df: pd.DataFrame,
) -> pd.DataFrame:
    """Filter the school pool to schools offering a specific CIP4 major.

    fos_df is passed in rather than loaded here to avoid a circular import
    with major_explorer and to keep this function directly unit-testable.

    Args:
        df: Institution-level school pool (post apply_filters).
        cip_filter: CIP4 dot-format string ("11.07") or "All majors" / None.
        fos_df: Field-of-Study DataFrame (from major_explorer.load_field_of_study).

    Returns:
        Filtered DataFrame restricted to schools offering cip_filter, or
        the original DataFrame unchanged when no filter is active.
    """
    if not cip_filter or cip_filter == "All majors":
        return df

    if "unit_id" not in df.columns:
        return df

    cip_int = parse_cip_code(cip_filter)
    offering_unit_ids = set(
        fos_df.loc[fos_df["cip_code"] == cip_int, "unit_id"]
        .dropna()
        .astype(int)
    )
    return df[df["unit_id"].isin(offering_unit_ids)]
