"""
Major Explorer tab — Phase 8 of the College Match Finder.

Renders the major-first product surface: pick a CIP-coded major, see
aggregated outcomes, and view the schools that are strongest in that major.

Phase 8 status:
  - 8.1: Tab scaffolding (DONE)
  - 8.2: CIP-coded major picker (THIS STEP)
  - 8.3: Outcomes panel (next)
  - 8.4: "Schools strong in this major" table
  - 8.5: Cross-tab backfill into School Finder detail cards
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import DATA_CLEANED_DIR, LQ_CAP_FOR_CHOROPLETH, PALETTE
from utils import format_cip_code, make_button_key, parse_cip_code
from major_descriptions import get_description
from page_modules.school_finder import set_school_finder_cip
from page_modules.about_the_data import render_about_the_data, OLDEST_DATE, NEWEST_DATE
from nyfed_outcomes import get_nyfed_outcomes
from naics_distribution import get_naics_distribution
from riasec_matching import get_top_n_matches

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FOS_CSV_PATH = DATA_CLEANED_DIR / "field_of_study_cleaned.csv"

# Phase 9 paths
OCCUPATIONS_MASTER_PATH = DATA_CLEANED_DIR / "occupations_master.csv"
CIP4_TO_SOC_PATH = DATA_CLEANED_DIR / "cip4_to_soc.csv"
MAJOR_OUTCOMES_PATH = DATA_CLEANED_DIR / "major_outcomes.csv"

# Phase 10.4 path
CIP4_STATE_EMPLOYMENT_PATH = DATA_CLEANED_DIR / "cip4_state_employment.csv"

# Phase 10.5 path
CIP4_WORK_CONTEXT_PATH = DATA_CLEANED_DIR / "cip4_work_context.csv"

# Session-state key for the currently selected CIP code (stored as int to
# match the dtype in the source CSV). Read by Steps 8.3-8.5 and by the
# School Finder tab in Step 8.5.
SELECTED_CIP_KEY = "selected_cip"

# Maximum number of institutions shown in the "Schools strong in this major"
# table. Sparse-data majors may render fewer rows. Tunable.
TOP_N_SCHOOLS = 25


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_field_of_study() -> pd.DataFrame:
    """
    Load the cleaned Field of Study dataset.

    All rows are bachelor's-level (credential_level == 3). The Scorecard
    suppresses earnings/debt cells where the institutional cohort had fewer
    than 30 federally-aided graduates, so non-null earnings values already
    satisfy the addendum's "sample-size floor of 30" requirement. No
    explicit sample-size column is present in the cleaned CSV.
    """
    df = pd.read_csv(FOS_CSV_PATH, low_memory=False)
    # unit_id is float64 in the CSV (NaN-tolerant); cast to nullable Int64
    # so it joins cleanly to the institution-level UNITID column later.
    df["unit_id"] = df["unit_id"].astype("Int64")
    return df


@st.cache_data(show_spinner=False)
def _load_career_paths_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load occupations_master and cip4_to_soc CSVs.

    Both files are produced by data_prep_majors.py (Phase 9). Cached for the
    Streamlit session lifetime — the files are static on disk.

    Returns:
        (occupations_master, cip4_to_soc) tuple of DataFrames.
    """
    occ = pd.read_csv(OCCUPATIONS_MASTER_PATH, dtype={"soc_code": str})
    cip4_to_soc = pd.read_csv(
        CIP4_TO_SOC_PATH,
        dtype={"cip4": str, "SOC2018Code": str},
    )
    return occ, cip4_to_soc


@st.cache_data(show_spinner=False)
def _load_major_outcomes() -> pd.DataFrame:
    """Load major_outcomes.csv (per-CIP4 employment-weighted aggregates).

    Produced by data_prep_majors.py (Step 9.3). One row per CIP4.
    """
    return pd.read_csv(MAJOR_OUTCOMES_PATH, dtype={"cip4": str})


@st.cache_data(show_spinner=False)
def _load_cip4_state_employment() -> pd.DataFrame:
    """Load cip4_state_employment.csv (state-level employment + LQ by CIP4).

    Produced by data_prep_majors.py (Phase 10.3). ~21K rows.
    dtype={'cip4': str} preserves leading zeros on CIP codes.
    """
    return pd.read_csv(CIP4_STATE_EMPLOYMENT_PATH, dtype={"cip4": str})


@st.cache_data(show_spinner=False)
def _load_cip4_work_context() -> pd.DataFrame:
    """Load cip4_work_context.csv (per-CIP4 O*NET work-context aggregates).

    Produced by data_prep_majors.py (Phase 10.3B). One row per CIP4.
    dtype={'cip4': str} preserves leading zeros on CIP codes.
    """
    return pd.read_csv(CIP4_WORK_CONTEXT_PATH, dtype={"cip4": str})


@st.cache_data
def _compute_work_context_quartiles(cip4_work_context: pd.DataFrame) -> dict:
    """
    Pre-compute quartile thresholds per work-context element across all CIP4s.

    Returns a dict mapping element_name -> dict with keys
    'q25', 'q50', 'q75' (the three threshold values that
    separate the four quartiles).

    Computed once per session and cached. Used to assign each
    bar a quartile color when rendering the work environment panel.
    """
    diagnostic_cols = {'cip4', 'n_routing_socs', 'n_routing_socs_with_context', 'pct_routing_emp_with_context'}
    element_cols = [c for c in cip4_work_context.columns if c not in diagnostic_cols]

    quartiles = {}
    for col in element_cols:
        valid = cip4_work_context[col].dropna()
        if len(valid) > 0:
            quartiles[col] = {
                'q25': valid.quantile(0.25),
                'q50': valid.quantile(0.50),
                'q75': valid.quantile(0.75),
            }
    return quartiles


@st.cache_data(show_spinner=False)
def build_major_picker_options(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the deduplicated picker dataframe.

    Returns a DataFrame with columns:
      - cip_code         (int64): the integer CIP code
      - cip_label        (str):   major name, trailing period stripped
      - cip_code_display (str):   formatted CIP code, e.g. "11.07"
      - display_name     (str):   "Computer Science (11.07)" — the dropdown label

    Sorted alphabetically by cip_label.
    """
    options = (
        df[["cip_code", "cip_description"]]
        .drop_duplicates()
        .copy()
    )
    options["cip_label"] = options["cip_description"].str.rstrip(".").str.strip()
    options["cip_code_display"] = options["cip_code"].apply(format_cip_code)
    options["display_name"] = (
        options["cip_label"] + " (" + options["cip_code_display"] + ")"
    )
    options = options.sort_values("cip_label", kind="stable").reset_index(drop=True)
    return options


# ---------------------------------------------------------------------------
# Outcomes aggregation (Step 8.3)
# ---------------------------------------------------------------------------

# Display config for each outcome metric. Order matters — drives column layout.
OUTCOME_METRICS = [
    {
        "column": "median_earnings_1yr",
        "label": "Median earnings, 1 year out",
        "kind": "currency",
    },
    {
        "column": "median_earnings_4yr",
        "label": "Median earnings, 4 years out",
        "kind": "currency",
    },
    {
        "column": "median_earnings_5yr",
        "label": "Median earnings, 5 years out",
        "kind": "currency",
    },
    {
        "column": "median_debt",
        "label": "Median student debt at graduation",
        "kind": "currency",
    },
]


def aggregate_major_outcomes(fos_df: pd.DataFrame, cip_code: int) -> dict:
    """
    Compute median-of-medians outcomes for the selected major.

    For each metric in OUTCOME_METRICS, returns the median value across all
    institutions offering the major where the metric is non-null. Each
    institution is weighted equally. The Scorecard's own n>=30 suppression
    rule means non-null values already satisfy the addendum's sample-size
    floor.

    Returns a dict keyed by column name, each value a sub-dict with:
        value         : float or None (None if no institutions report)
        n_reporting   : int            (institutions with non-null value)
        n_total       : int            (institutions offering the major)
    """
    subset = fos_df.loc[fos_df["cip_code"] == cip_code]
    n_total = len(subset)

    results = {}
    for metric in OUTCOME_METRICS:
        col = metric["column"]
        non_null = subset[col].dropna()
        results[col] = {
            "value": float(non_null.median()) if len(non_null) else None,
            "n_reporting": int(len(non_null)),
            "n_total": int(n_total),
        }
    return results


def _format_currency(value: float | None) -> str:
    """Format a float as '$NN,NNN' or return the not-reported sentinel."""
    if value is None:
        return "Not reported"
    return f"${value:,.0f}"


def _format_completeness_caption(n_reporting: int, n_total: int) -> str:
    """Render the 'reported for X of Y institutions (Z%)' line."""
    if n_total == 0:
        return "No institutions offer this major."
    if n_reporting == 0:
        return f"Not reported by any of {n_total:,} institutions"
    pct = 100.0 * n_reporting / n_total
    return f"Reported by {n_reporting:,} of {n_total:,} institutions ({pct:.0f}%)"


# ---------------------------------------------------------------------------
# Schools-strong-in-this-major (Step 8.4)
# ---------------------------------------------------------------------------

def get_top_schools_for_major(
    fos_df: pd.DataFrame,
    cip_code: int,
    top_n: int = TOP_N_SCHOOLS,
) -> pd.DataFrame:
    """
    Return the top N schools offering the selected major, ranked by
    median_earnings_5yr descending.

    Schools with NaN median_earnings_5yr are excluded from the ranking — they
    cannot be sorted on the chosen metric. Ties broken alphabetically by
    school name. Returns an empty DataFrame if no school in this major
    reports 5yr earnings.

    Output columns:
        unit_id, school_name, median_earnings_5yr,
        median_earnings_1yr, median_debt
    """
    cols = [
        "unit_id",
        "school_name",
        "median_earnings_5yr",
        "median_earnings_1yr",
        "median_debt",
    ]
    subset = fos_df.loc[fos_df["cip_code"] == cip_code, cols].copy()
    ranked = (
        subset.dropna(subset=["median_earnings_5yr"])
        .sort_values(
            ["median_earnings_5yr", "school_name"],
            ascending=[False, True],
            kind="stable",
        )
        .head(top_n)
        .reset_index(drop=True)
    )
    return ranked


def _pin_school_callback(school_name: str) -> None:
    """
    Append school_name to st.session_state['pinned_schools'] if not already
    present. This callback fires before the next rerun's widgets render,
    which is the only safe time to mutate the multiselect-bound state.
    """
    pinned = st.session_state.get("pinned_schools", [])
    if school_name not in pinned:
        st.session_state["pinned_schools"] = pinned + [school_name]
    # Track the most recent cross-tab pin for the instruction banner
    st.session_state["_last_xtab_pinned"] = school_name


def set_major_explorer_cip(cip4_str: str) -> None:
    """Pre-select a CIP4 in the Major Explorer tab.

    Called from Find Your Fit (Phase 13.1) via button on_click=. Writes the
    integer-encoded CIP to the shared session key and sets a sentinel so the
    caller's next render can show a tab-switch affordance banner.

    Accepts both dot format ("11.07") and bare int string ("1107") — the
    replace(".", "") is a no-op when the dot is already absent.
    """
    st.session_state[SELECTED_CIP_KEY] = parse_cip_code(cip4_str)
    st.session_state["_last_xtab_cip"] = cip4_str
    st.session_state["_active_tab"] = "major_explorer"
    st.session_state.pop("major_picker_widget", None)


def get_school_program_outcomes(
    fos_df: pd.DataFrame, unit_id: int, cip_code: int
) -> dict | None:
    """
    Look up a single school's program-level outcomes for one major.

    Returns:
        None if the school does not offer the major at all.
        A dict with the four outcome columns otherwise. Individual values
        may be NaN if the Scorecard suppressed them (n < 30).
    """
    match = fos_df.loc[
        (fos_df["unit_id"] == unit_id) & (fos_df["cip_code"] == cip_code)
    ]
    if match.empty:
        return None
    row = match.iloc[0]
    return {
        "median_earnings_1yr": row["median_earnings_1yr"],
        "median_earnings_4yr": row["median_earnings_4yr"],
        "median_earnings_5yr": row["median_earnings_5yr"],
        "median_debt": row["median_debt"],
    }


def get_school_all_programs(fos_df: pd.DataFrame, unitid: int) -> pd.DataFrame:
    """Return all programs offered at a given school, sorted by median earnings descending.

    Used by render_detail_card's 'Programs offered' expander (Phase 13.3).

    Args:
        fos_df: The full Field-of-Study DataFrame as loaded by load_field_of_study().
        unitid: The school's unit_id (integer).

    Returns:
        DataFrame with columns: cip4, major_name, median_earnings_1yr, median_debt.
        Sorted by median_earnings_1yr descending, NaN last. Empty DataFrame (with
        correct columns) if the school has no programs in the FoS dataset.
    """
    _EMPTY_COLS = ["cip4", "major_name", "median_earnings_1yr", "median_debt"]

    school_rows = fos_df[fos_df["unit_id"] == unitid]
    if school_rows.empty:
        return pd.DataFrame(columns=_EMPTY_COLS)

    out = pd.DataFrame({
        "cip4": school_rows["cip_code"].apply(format_cip_code),
        "major_name": school_rows["cip_description"].str.rstrip(".").str.strip(),
        "median_earnings_1yr": school_rows["median_earnings_1yr"].values,
        "median_debt": school_rows["median_debt"].values,
    })

    return out.sort_values(
        "median_earnings_1yr", ascending=False, na_position="last"
    ).reset_index(drop=True)


def get_selected_major_label(fos_df: pd.DataFrame, cip_code: int) -> str | None:
    """
    Return the display-friendly major label for a CIP code, e.g.
    'Computer Science (11.07)'. Returns None if cip_code is not in fos_df.
    Used by app.py to title the program-level outcomes section.
    """
    match = fos_df.loc[fos_df["cip_code"] == cip_code, "cip_description"]
    if match.empty:
        return None
    label = match.iloc[0].rstrip(".").strip()
    return f"{label} ({format_cip_code(cip_code)})"


# ---------------------------------------------------------------------------
# Wages and projections summary panel (Step 9.5)
# ---------------------------------------------------------------------------

def _render_wages_projections_summary(cip4_str: str) -> None:
    """Render the per-major wage and projections summary.

    Shows employment-weighted median wage, 25th-75th percentile wage range,
    10-year projected growth %, total employment in routing occupations,
    and the count of routing occupations behind these numbers.

    Args:
        cip4_str: the CIP4 in XX.XX format, e.g. '11.07'.
    """
    if not cip4_str:
        return  # Nothing to render until a major is selected.

    st.markdown("### Wages and projections")
    st.caption(
        "Aggregated across BLS-defined routing occupations for this major, "
        "weighted by 2024 employment. See methodology in About the Data."
    )

    major_outcomes = _load_major_outcomes()
    row = major_outcomes[major_outcomes["cip4"] == cip4_str]

    if len(row) == 0:
        st.info(
            f"BLS occupational data is not available for this major "
            f"(CIP {cip4_str})."
        )
        return

    row = row.iloc[0]

    median_wage = (
        f"${row['weighted_annual_median']:,.0f}"
        if pd.notna(row["weighted_annual_median"])
        else "—"
    )
    pct25 = (
        f"${row['weighted_annual_pct25']:,.0f}"
        if pd.notna(row["weighted_annual_pct25"])
        else "—"
    )
    pct75 = (
        f"${row['weighted_annual_pct75']:,.0f}"
        if pd.notna(row["weighted_annual_pct75"])
        else "—"
    )
    growth = (
        f"{row['weighted_employment_change_percent']:+.1f}%"
        if pd.notna(row["weighted_employment_change_percent"])
        else "—"
    )
    total_emp = (
        f"{int(row['total_employment_routing']):,}"
        if pd.notna(row["total_employment_routing"])
        else "—"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Median annual wage",
            value=median_wage,
        )
        st.caption(f"25th–75th: {pct25} – {pct75}")

    with col2:
        st.metric(
            label="10-year projected growth",
            value=growth,
        )
        st.caption("BLS 2024–2034 projections")

    with col3:
        st.metric(
            label="Total employment (routing)",
            value=total_emp,
        )
        st.caption("Across all routing occupations, 2024")

    with col4:
        n_routing = int(row["n_routing_socs"])
        n_with_wage = int(row["n_socs_with_wage_data"])
        st.metric(
            label="Routing occupations",
            value=str(n_routing),
        )
        st.caption(f"{n_with_wage} of {n_routing} with wage data")


# ---------------------------------------------------------------------------
# Work environment panel (Phase 10.5)
# ---------------------------------------------------------------------------

def render_work_environment_panel(
    selected_cip4: str,
    cip4_work_context: pd.DataFrame,
    quartile_thresholds: dict,
) -> None:
    """
    Render the work environment panel: a horizontal bar chart showing
    all 13 O*NET work-context elements for the selected CIP4, sorted
    by value descending, colored by quartile rank across all CIP4s.

    Inputs:
        selected_cip4: The CIP4 code currently selected in the major picker.
        cip4_work_context: DataFrame loaded from cip4_work_context.csv.
        quartile_thresholds: Dict from _compute_work_context_quartiles.

    Returns:
        None (renders directly via Streamlit).
    """

    def _quartile_color(value: float, thresholds: dict) -> str:
        if pd.isna(value) or thresholds is None:
            return PALETTE["quartile_below_avg"]
        if value >= thresholds['q75']:
            return PALETTE["quartile_top"]
        if value >= thresholds['q50']:
            return PALETTE["quartile_above_avg"]
        if value >= thresholds['q25']:
            return PALETTE["quartile_below_avg"]
        return PALETTE["quartile_bottom"]

    def _quartile_label(value: float, thresholds: dict) -> str:
        if pd.isna(value) or thresholds is None:
            return 'No data'
        if value >= thresholds['q75']:
            return 'Top quartile across all majors'
        if value >= thresholds['q50']:
            return 'Above average across all majors'
        if value >= thresholds['q25']:
            return 'Below average across all majors'
        return 'Bottom quartile across all majors'

    row_df = cip4_work_context[cip4_work_context["cip4"] == selected_cip4]

    if row_df.empty:
        st.info(
            "ℹ️ Work environment data is not available for this major. "
            "This typically happens when most routing occupations lack O*NET work-context coverage."
        )
        return

    row = row_df.iloc[0]
    diagnostic_cols = {'cip4', 'n_routing_socs', 'n_routing_socs_with_context', 'pct_routing_emp_with_context'}
    element_cols = [c for c in cip4_work_context.columns if c not in diagnostic_cols]

    pct_coverage = row.get('pct_routing_emp_with_context', float('nan'))
    all_nan = all(pd.isna(row[c]) for c in element_cols)

    if pd.isna(pct_coverage) or all_nan:
        st.info(
            "ℹ️ Work environment data is not available for this major. "
            "This typically happens when most routing occupations lack O*NET work-context coverage."
        )
        return

    st.markdown("### Work environment")
    st.caption(
        "Characteristics of the typical workday for graduates of this major, based on O*NET 30.2 "
        "work-context ratings (1-5 scale, employment-weighted across the major's routing occupations)."
    )

    plot_data = []
    for col in element_cols:
        val = row[col]
        if pd.isna(val):
            continue
        thresholds = quartile_thresholds.get(col)
        plot_data.append({
            'element': col,
            'value': float(val),
            'color': _quartile_color(float(val), thresholds),
            'quartile_label': _quartile_label(float(val), thresholds),
        })

    plot_df = pd.DataFrame(plot_data).sort_values('value', ascending=False).reset_index(drop=True)

    if plot_df.empty:
        st.info(
            "ℹ️ Work environment data is not available for this major. "
            "This typically happens when most routing occupations lack O*NET work-context coverage."
        )
        return

    # Reverse order for Plotly (renders bottom-up, so last item appears at top)
    plot_df_rev = plot_df.iloc[::-1].reset_index(drop=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=plot_df_rev['element'].tolist(),
        x=plot_df_rev['value'].tolist(),
        orientation='h',
        marker_color=plot_df_rev['color'].tolist(),
        text=[f'{v:.1f}' for v in plot_df_rev['value'].tolist()],
        textposition='outside',
        customdata=plot_df_rev['quartile_label'].tolist(),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Score: %{x:.1f}<br>'
            '%{customdata}'
            '<extra></extra>'
        ),
    ))
    fig.update_layout(
        xaxis_range=[0, 5.3],
        xaxis_title='Score (1-5 scale)',
        yaxis_title='',
        height=450,
        margin=dict(l=10, r=20, t=20, b=40),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Bars colored by where each element falls across all 414 majors: "
        "**dark blue** = top 25%, **light blue** = above average, "
        "**light gray** = below average, **medium gray** = bottom 25%. "
        "Source: O*NET 30.2 Work Context (CC BY 4.0)."
    )


# ---------------------------------------------------------------------------
# Geographic concentration panel (Phase 10.4)
# ---------------------------------------------------------------------------

def render_geographic_concentration_panel(
    selected_cip4: str,
    cip4_state_employment: pd.DataFrame,
) -> None:
    """
    Render the side-by-side choropleth panel showing total employment
    and location quotient by state for the selected CIP4.

    Filters cip4_state_employment to the selected CIP4, renders two
    Plotly choropleths in side-by-side columns, and includes a
    methodology caption.

    Inputs:
        selected_cip4: The CIP4 code currently selected in the major picker.
        cip4_state_employment: DataFrame loaded from cip4_state_employment.csv.

    Returns:
        None (renders directly via Streamlit).
    """
    df = cip4_state_employment[cip4_state_employment["cip4"] == selected_cip4].copy()

    # Empty-state guard
    if df.empty or (df["total_employment"].isna().all() and df["location_quotient"].isna().all()):
        st.info(
            "ℹ️ Geographic distribution data is not available for this major. "
            "This typically happens when most routing occupations have suppressed "
            "state-level employment data (BLS confidentiality protections)."
        )
        return

    st.markdown("### Where these jobs are")
    st.caption(
        "State-by-state distribution of jobs that graduates of this major typically pursue."
    )

    col1, col2 = st.columns(2)

    _choropleth_layout = dict(
        geo_scope="usa",
        geo_bgcolor="rgba(0,0,0,0)",
        geo_landcolor=PALETTE["choropleth_land"],
        geo_subunitcolor=PALETTE["choropleth_borders"],
        margin=dict(l=0, r=0, t=20, b=0),
        height=400,
    )

    # ------------------------------------------------------------------
    # Left: Total Employment
    # ------------------------------------------------------------------
    with col1:
        st.markdown("**Total Employment**")

        emp_df = df.dropna(subset=["total_employment"])
        if emp_df.empty:
            st.info("No state employment data available for this major.")
        else:
            fig_emp = go.Figure()
            fig_emp.add_trace(go.Choropleth(
                locations=emp_df["state"],
                locationmode="USA-states",
                z=emp_df["total_employment"],
                colorscale=PALETTE["choropleth_scale"],
                colorbar_title="Jobs",
                customdata=emp_df[["coverage_pct", "n_observed_socs", "n_routing_socs"]].values,
                hovertemplate=(
                    "<b>%{location}</b><br>"
                    "Total employment: %{z:,.0f}<br>"
                    "Coverage: %{customdata[0]:.1f}%<br>"
                    "SOCs observed: %{customdata[1]:.0f} of %{customdata[2]:.0f}"
                    "<extra></extra>"
                ),
            ))
            fig_emp.update_layout(**_choropleth_layout)
            st.plotly_chart(fig_emp, use_container_width=True)
            st.caption(
                "USA state choropleth showing total employment in occupations entered by graduates "
                "of this major. Darker = higher employment. Source: BLS OEWS State-Level, May 2024."
            )

    # ------------------------------------------------------------------
    # Right: Location Quotient
    # ------------------------------------------------------------------
    with col2:
        st.markdown("**Concentration (LQ)**")

        lq_df = df.dropna(subset=["location_quotient"])
        if lq_df.empty:
            st.info("No location quotient data available for this major.")
        else:
            z_capped = np.minimum(lq_df["location_quotient"].values, LQ_CAP_FOR_CHOROPLETH)

            fig_lq = go.Figure()
            fig_lq.add_trace(go.Choropleth(
                locations=lq_df["state"],
                locationmode="USA-states",
                z=z_capped,
                customdata=lq_df[["location_quotient", "coverage_pct", "n_observed_socs", "n_routing_socs"]].values,
                colorscale=PALETTE["choropleth_scale"],
                zmin=0,
                zmax=LQ_CAP_FOR_CHOROPLETH,
                colorbar_title="LQ",
                hovertemplate=(
                    "<b>%{location}</b><br>"
                    "Location quotient: %{customdata[0]:.2f}<br>"
                    "Coverage: %{customdata[1]:.1f}%<br>"
                    "SOCs observed: %{customdata[2]:.0f} of %{customdata[3]:.0f}"
                    "<extra></extra>"
                ),
            ))
            fig_lq.update_layout(**_choropleth_layout)
            st.plotly_chart(fig_lq, use_container_width=True)
            st.caption(
                f"Color scale capped at LQ = {LQ_CAP_FOR_CHOROPLETH} for readability. "
                "Hover for true values."
            )

    st.caption(
        "Location quotient measures concentration relative to the national average. "
        "LQ = 1.0 means the major's careers are represented at the national rate; "
        "LQ = 2.0 means twice the national concentration. "
        "Light gray states have insufficient data (less than 50% of routing occupations "
        "observed at state level)."
    )


# ---------------------------------------------------------------------------
# Career paths panel (Step 9.4)
# ---------------------------------------------------------------------------

def _render_career_paths_panel(cip4_str: str) -> None:
    """Render the 'Career paths and occupations' panel for the selected CIP4.

    Shows a table of the BLS-defined routing occupations for this major,
    sorted by 2024 total employment descending. Three rendering states:
      1. No routing SOCs found: info banner.
      2. Routing SOCs found but all lack wage/projection data: warning banner.
      3. Normal: full table with completeness caption.
    """
    st.markdown("### Career paths and occupations")
    st.caption(
        "Occupations that graduates of this major typically enter, based on "
        "the NCES CIP–SOC crosswalk. Sorted by 2024 total employment."
    )

    if not cip4_str:
        st.info("Select a major above to see its career paths.")
        return

    occ_master, cip4_to_soc = _load_career_paths_data()

    routing = cip4_to_soc[cip4_to_soc["cip4"] == cip4_str]
    if len(routing) == 0:
        st.info(
            f"No BLS-defined routing occupations were found for this major "
            f"(CIP {cip4_str}). This is rare and usually means the major "
            f"maps to occupations that BLS doesn't publish at the detailed "
            f"level."
        )
        return

    # Inner-join routing pairs to per-SOC data.
    # Some routing SOCs may not be in occ_master (aggregation-level codes).
    # Drop them silently.
    merged = routing.merge(
        occ_master,
        left_on="SOC2018Code",
        right_on="soc_code",
        how="inner",
    )

    if len(merged) == 0:
        st.warning(
            f"This major routes to {len(routing)} occupations in the "
            f"crosswalk, but none of them have wage or projection data "
            f"available at the detailed SOC level."
        )
        return

    merged = merged.sort_values(
        by="total_employment_oews",
        ascending=False,
        na_position="last",
    )

    display = pd.DataFrame({
        "Occupation": merged["occupation_title"],
        "Median annual wage": merged["annual_median"],
        "10yr growth %": merged["employment_change_percent"],
        "Annual openings (000s)": merged["annual_openings_avg"],
        "Typical entry education": merged["typical_education"],
    })

    display_formatted = display.copy()
    display_formatted["Median annual wage"] = display["Median annual wage"].map(
        lambda v: f"${v:,.0f}" if pd.notna(v) else "—"
    )
    display_formatted["10yr growth %"] = display["10yr growth %"].map(
        lambda v: f"{v:+.1f}%" if pd.notna(v) else "—"
    )
    display_formatted["Annual openings (000s)"] = display["Annual openings (000s)"].map(
        lambda v: f"{v:,.1f}" if pd.notna(v) else "—"
    )
    display_formatted["Typical entry education"] = display["Typical entry education"].fillna("—")

    st.dataframe(
        display_formatted,
        hide_index=True,
        use_container_width=True,
    )

    n_total = len(routing)
    n_in_table = len(merged)
    n_with_wage = int(merged["annual_median"].notna().sum())
    n_with_growth = int(merged["employment_change_percent"].notna().sum())
    if n_in_table < n_total:
        gap_note = (
            f" ({n_total - n_in_table} additional crosswalk occupations are "
            f"aggregation-level codes that BLS splits into the detailed "
            f"occupations shown here.)"
        )
    else:
        gap_note = ""
    st.caption(
        f"Showing {n_in_table} routing occupations. "
        f"Wage data available for {n_with_wage} of {n_in_table}; "
        f"growth projections available for {n_with_growth} of {n_in_table}."
        + gap_note
    )


# ---------------------------------------------------------------------------
# Major description panel (Phase 11.1A / 11.1C)
# ---------------------------------------------------------------------------

def _render_stub_description(entry: dict) -> None:
    """Render a minimal description for a major not yet in the authored library."""
    st.info(
        "This major isn't yet covered by a detailed description in our library. "
        "The summary below is the official NCES classification text — accurate but "
        "less detailed than our featured majors. The federal data on this page "
        "(earnings, employment, geographic concentration) is unaffected."
    )
    st.markdown(f"*{entry['name']}*")
    st.caption(
        "Source: [NCES CIP Classification]"
        "(https://nces.ed.gov/ipeds/cipcode/Default.aspx?y=56)"
    )


def _render_major_description(cip_code: str, fallback_name: str) -> None:
    """Render the hand-authored major description block, or a stub if not yet authored.

    Args:
        cip_code: CIP4 string in XX.XX format, e.g. '11.07'.
        fallback_name: Major name from FoS data, used when no description exists.
    """
    desc = get_description(cip_code)

    if desc is None:
        return  # graceful no-op for unknown CIP4
    if desc.get("is_stub"):
        _render_stub_description(desc)
        return

    st.markdown(f"### {desc['name']}")
    st.markdown(desc["overview"])

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("**What you'll learn**")
        for item in desc.get("what_youll_learn", []):
            st.markdown(f"- {item}")
    with col_right:
        st.markdown("**Typical classes**")
        for item in desc.get("typical_classes", []):
            st.markdown(f"- {item}")

    related = desc.get("related_majors", [])
    if related:
        st.markdown(f"**Related majors:** {', '.join(related)}")


# ---------------------------------------------------------------------------
# NY Fed labor market outcomes panel (Phase 11.2B.3)
# ---------------------------------------------------------------------------

def _render_nyfed_outcomes(cip4: str) -> None:
    outcomes = get_nyfed_outcomes(cip4)

    st.markdown("### Labor Market Outcomes (NY Fed)")

    if outcomes is None:
        st.info(
            "Labor market outcomes are not available for this major. "
            "The Federal Reserve Bank of New York publishes data for ~73 broad "
            "major categories; this major falls outside that set."
        )
        return

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Unemployment Rate",
            f"{outcomes['unemployment_rate']:.1f}%",
            help="Share of recent graduates (ages 22–27) actively looking for work but unable to find it.",
        )

    with col2:
        st.metric(
            "Underemployment Rate",
            f"{outcomes['underemployment_rate']:.1f}%",
            help="Share of recent graduates working in jobs that do not typically require a college degree.",
        )

    with col3:
        st.metric(
            "Median Wage (Early Career)",
            f"${outcomes['median_wage_early_career']:,.0f}",
            help="Median annual wage for full-time workers ages 22–27 with this major.",
        )

    with col4:
        st.metric(
            "Median Wage (Mid-Career)",
            f"${outcomes['median_wage_mid_career']:,.0f}",
            help="Median annual wage for full-time workers ages 35–45 with this major.",
        )

    with col5:
        st.metric(
            "Share with Graduate Degree",
            f"{outcomes['share_with_graduate_degree']:.1f}%",
            help="Share of workers with this undergraduate major who have also earned a graduate degree.",
        )

    st.caption(
        "Source: Federal Reserve Bank of New York, *The Labor Market for Recent "
        "College Graduates*, February 2026 release. Metrics shown reflect the "
        "broader NY Fed major category that includes this CIP."
    )


# ---------------------------------------------------------------------------
# Industry distribution panel (Phase 11.3.3)
# ---------------------------------------------------------------------------

# Display constants
_NAICS_TITLE_TRUNCATE_AT = 50
_NAICS_TOP_N = 10


def _truncate_title(title: str, limit: int = _NAICS_TITLE_TRUNCATE_AT) -> str:
    if len(title) <= limit:
        return title
    return title[:limit].rstrip() + "…"


def _render_naics_distribution_panel(cip4: str) -> None:
    """Render the 'Industries that hire this major' panel.

    Top 10 NAICS3 industries by employment-weighted share, with an
    'Other (N industries combined)' row appended at the bottom in a
    muted color when there are >10 NAICS for this CIP4 AND the combined
    Other share is at least 0.1%.
    """
    st.markdown("### Industries that hire this major")

    dist = get_naics_distribution(cip4)
    if dist is None:
        st.info(
            "Industry distribution is not available for this major. "
            "The federal occupation-to-industry data does not publish "
            "detail at the level needed for these specialized programs."
        )
        return

    # Build the display dataframe: top 10 + optional Other row
    top_n = dist.head(_NAICS_TOP_N).copy()
    n_other = len(dist) - len(top_n)
    other_share = dist.iloc[_NAICS_TOP_N:]["share_in_naics3"].sum() if n_other > 0 else 0.0

    # Title-axis labels: truncated for display, full for hover
    top_n["display_title"] = top_n["naics3_title"].apply(_truncate_title)
    top_n["hover_title"] = top_n["naics3_title"]
    top_n["bar_color"] = PALETTE["categorical_primary"]

    if n_other > 0 and other_share >= 0.001:  # ≥0.1%
        other_row = pd.DataFrame([{
            "naics3": "OTHER",
            "naics3_title": f"Other ({n_other} industries combined)",
            "weighted_emp": int(dist.iloc[_NAICS_TOP_N:]["weighted_emp"].sum()),
            "share_in_naics3": other_share,
            "display_title": f"Other ({n_other} industries combined)",
            "hover_title": f"{n_other} additional industries, each <{top_n['share_in_naics3'].min():.1%}",
            "bar_color": PALETTE["categorical_other"],
        }])
        plot_df = pd.concat([top_n, other_row], ignore_index=True)
    else:
        plot_df = top_n

    # Plotly draws horizontal bars bottom-up by default, so reverse the
    # dataframe so the largest share appears at the TOP of the chart,
    # with Other (if present) pinned at the bottom.
    plot_df = plot_df.iloc[::-1].reset_index(drop=True)

    fig = go.Figure(go.Bar(
        x=plot_df["share_in_naics3"] * 100,  # render as percent
        y=plot_df["display_title"],
        orientation="h",
        marker_color=plot_df["bar_color"].tolist(),
        customdata=plot_df[["hover_title", "weighted_emp"]].values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Share: %{x:.1f}%<br>"
            "Weighted employment: %{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
    ))
    fig.update_layout(
        height=max(280, 30 * len(plot_df) + 80),
        margin=dict(l=10, r=10, t=10, b=40),
        xaxis_title="Share of employment (%)",
        yaxis_title=None,
        showlegend=False,
        plot_bgcolor=PALETTE["naics_chart_bg"],
    )
    fig.update_xaxes(showgrid=True, gridcolor=PALETTE["gridline_light"])
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Top 10 industries (3-digit NAICS) employing workers in occupations entered by graduates "
        "of this major. Source: BLS OEWS NAICS-by-SOC, May 2024."
    )


# ---------------------------------------------------------------------------
# RIASEC alignment helper (Phase 12.3)
# ---------------------------------------------------------------------------

def _get_aligned_cip4_set() -> set | None:
    """Return the set of CIP4 codes (dot format, e.g. '11.07') aligned with the
    user's RIASEC profile, or None if the questionnaire hasn't been taken.

    Top 40 by Pearson correlation. Cached per session so we don't re-run the
    correlation matrix on every Streamlit rerun.

    Returns:
        None  — user has not taken the questionnaire
        set() — user took the quiz but zero-variance vector produced no matches
        set of 40 CIP4 strings — normal case
    """
    user_vector = st.session_state.get("riasec_user_vector")
    if user_vector is None:
        return None

    fingerprint = tuple(sorted(user_vector.items()))
    cached_set = st.session_state.get("_aligned_cip4_set_cache")
    cached_fp = st.session_state.get("_aligned_cip4_set_cache_vector")

    if cached_set is not None and cached_fp == fingerprint:
        return cached_set

    top_40 = get_top_n_matches(user_vector, n=40)
    aligned_set = set(top_40["cip4"].tolist())

    st.session_state["_aligned_cip4_set_cache"] = aligned_set
    st.session_state["_aligned_cip4_set_cache_vector"] = fingerprint

    return aligned_set


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render() -> None:
    """Render the Major Explorer tab. Called from app.py inside the tab context."""
    st.header("Major Explorer")
    st.caption(
        "Pick a major to see earnings, debt, and the schools that are "
        "strongest in that field."
    )

    # Load data (cached after first call)
    fos_df = load_field_of_study()
    picker_df = build_major_picker_options(fos_df)

    # Phase 12.3: compute alignment set once per session rerun
    aligned_set = _get_aligned_cip4_set()

    # ------------------------------------------------------------------
    # Alignment context banner (Phase 12.3)
    # ------------------------------------------------------------------
    if aligned_set is None:
        st.info(
            "💡 **Tip:** Take the **Find Your Fit** questionnaire to see which "
            "majors align with your interests. Aligned majors will be marked "
            "with ⭐ in the picker below."
        )
    elif len(aligned_set) > 0:
        holland_code = st.session_state.get("fyf_holland_code", "?")
        st.success(
            f"⭐ Showing {len(aligned_set)} majors aligned with your interests "
            f"(Holland Code: **{holland_code}**). All {len(picker_df):,} majors are still "
            f"available — the star just marks the top alignments by Pearson correlation."
        )
    # Case 3: aligned_set is empty (zero-variance vector) — no banner

    # Determine the default index. If a major has already been selected
    # (e.g. via cross-tab navigation in Step 8.5), preserve that selection;
    # otherwise default to the first option (alphabetical).
    default_cip = st.session_state.get(SELECTED_CIP_KEY)
    if default_cip is not None and default_cip in picker_df["cip_code"].values:
        default_index = int(
            picker_df.index[picker_df["cip_code"] == default_cip][0]
        )
    else:
        default_index = 0

    # Build annotated options list — aligned CIP4s get a ⭐ prefix
    base_options = picker_df["display_name"].tolist()
    cip4_display_list = picker_df["cip_code_display"].tolist()
    if aligned_set:
        annotated_options = [
            f"⭐ {label}" if cip4 in aligned_set else label
            for label, cip4 in zip(base_options, cip4_display_list)
        ]
    else:
        annotated_options = base_options

    selection = st.selectbox(
        "Select a major",
        options=annotated_options,
        index=default_index,
        key="major_picker_widget",
        help=(
            f"All {len(picker_df):,} bachelor's-level majors with at least one "
            "U.S. institution offering the program in the most recent College "
            "Scorecard release."
        ),
    )

    # Strip alignment prefix before looking up the row in picker_df
    lookup_name = selection.removeprefix("⭐ ")

    # Persist the integer CIP for downstream consumers (Steps 8.3-8.5).
    selected_row = picker_df.loc[picker_df["display_name"] == lookup_name].iloc[0]
    st.session_state[SELECTED_CIP_KEY] = int(selected_row["cip_code"])

    # ------------------------------------------------------------------
    # Major description — Phase 11.1A
    # ------------------------------------------------------------------
    st.divider()
    _render_major_description(
        selected_row["cip_code_display"],
        selected_row["cip_label"],
    )

    # Phase 13.2 — cross-tab handoff button
    st.button(
        "See schools strong in this major →",
        key=make_button_key("see_schools", selected_row["cip_code_display"]),
        on_click=set_school_finder_cip,
        args=(selected_row["cip_code_display"],),
        help=(
            f"Pre-filters School Finder to schools offering "
            f"{selected_row['cip_label']}. Switch to the School Finder tab "
            "after clicking — the sidebar filter will be set for you."
        ),
    )

    # ------------------------------------------------------------------
    # NY Fed labor market outcomes — Phase 11.2B.3
    # ------------------------------------------------------------------
    st.divider()
    cip4_str_for_nyfed = selected_row["cip_code_display"]
    _render_nyfed_outcomes(cip4_str_for_nyfed)

    # ------------------------------------------------------------------
    # Outcomes panel — Step 8.3
    # ------------------------------------------------------------------

    cip_code = int(selected_row["cip_code"])
    outcomes = aggregate_major_outcomes(fos_df, cip_code)
    n_total = outcomes[OUTCOME_METRICS[0]["column"]]["n_total"]

    st.subheader(
        f"{selected_row['cip_label']} — Outcomes "
        f"(CIP {selected_row['cip_code_display']})"
    )
    st.caption(
        f"Aggregated across {n_total:,} U.S. institutions offering this major "
        f"in the most recent College Scorecard release."
    )

    cols = st.columns(len(OUTCOME_METRICS))
    for col_widget, metric in zip(cols, OUTCOME_METRICS):
        result = outcomes[metric["column"]]
        with col_widget:
            st.metric(
                label=metric["label"],
                value=_format_currency(result["value"]),
            )
            st.caption(
                _format_completeness_caption(
                    result["n_reporting"], result["n_total"]
                )
            )

    # Persistent methodology footer
    with st.expander("About these numbers", expanded=False):
        st.markdown(
            "- **Aggregation:** Each value is the median across institutions "
            "that report the metric for this major. Schools are weighted "
            "equally regardless of program size.\n"
            "- **Sample size:** The College Scorecard suppresses any cell "
            "where the institutional cohort had fewer than 30 "
            "federally-aided graduates, so every value shown reflects at "
            "least 30 graduates per institution.\n"
            "- **Earnings scope:** Earnings reflect federally-aided "
            "graduates only — students who received federal grants or "
            "loans. Self-funded students are not represented in these "
            "figures.\n"
            "- **Source:** U.S. Department of Education College Scorecard, "
            "Field of Study file."
        )

    # ------------------------------------------------------------------
    # Wages and projections summary — Step 9.5
    # ------------------------------------------------------------------
    st.divider()
    cip4_str = format_cip_code(cip_code)
    _render_wages_projections_summary(cip4_str)

    # ------------------------------------------------------------------
    # Career paths and occupations — Step 9.4
    # ------------------------------------------------------------------
    st.divider()
    _render_career_paths_panel(cip4_str)

    # ------------------------------------------------------------------
    # Industries that hire this major — Phase 11.3.3
    # ------------------------------------------------------------------
    st.divider()
    _render_naics_distribution_panel(cip4_str)

    # ------------------------------------------------------------------
    # Work environment — Phase 10.5
    # ------------------------------------------------------------------
    st.divider()
    cip4_work_context = _load_cip4_work_context()
    work_context_quartiles = _compute_work_context_quartiles(cip4_work_context)
    render_work_environment_panel(cip4_str, cip4_work_context, work_context_quartiles)

    # ------------------------------------------------------------------
    # Geographic concentration — Phase 10.4
    # ------------------------------------------------------------------
    st.divider()
    cip4_state_emp = _load_cip4_state_employment()
    render_geographic_concentration_panel(cip4_str, cip4_state_emp)

    # ------------------------------------------------------------------
    # Schools strong in this major — Step 8.4
    # ------------------------------------------------------------------
    st.divider()
    st.subheader("Schools strong in this major")

    top_schools = get_top_schools_for_major(fos_df, cip_code)
    n_total_for_cip = outcomes[OUTCOME_METRICS[0]["column"]]["n_total"]

    if top_schools.empty:
        st.info(
            f"No institutions report 5-year graduate earnings for this major "
            f"in the most recent Scorecard release. {n_total_for_cip:,} "
            "schools offer the program, but their cohort sizes fell below "
            "the Scorecard's reporting threshold (n < 30 federally-aided "
            "graduates)."
        )
    else:
        st.caption(
            f"Top {len(top_schools)} of {n_total_for_cip:,} institutions, "
            "ranked by median earnings 5 years after graduation. "
            "Use the pin buttons to send a school to the School Finder tab."
        )

        # Cross-tab instruction banner — shown once after a pin click
        last_pinned = st.session_state.pop("_last_xtab_pinned", None)
        if last_pinned is not None:
            st.success(
                f"📌 **{last_pinned}** is now pinned in the School Finder. "
                "Switch to the School Finder tab to see its full detail card."
            )

        # Header row
        header = st.columns([1, 5, 2, 2, 2, 2])
        for col, label in zip(
            header,
            ["#", "School", "5yr earnings", "1yr earnings", "Median debt", ""],
        ):
            col.markdown(f"**{label}**")

        # Data rows
        for rank_idx, (_, row) in enumerate(top_schools.iterrows(), start=1):
            cols = st.columns([1, 5, 2, 2, 2, 2])
            cols[0].write(rank_idx)
            cols[1].write(row["school_name"])
            cols[2].write(_format_currency(row["median_earnings_5yr"]))
            cols[3].write(_format_currency(row["median_earnings_1yr"]))
            cols[4].write(_format_currency(row["median_debt"]))
            cols[5].button(
                "📌 Pin",
                key=make_button_key("pin_btn", int(row["unit_id"]), cip_code),
                on_click=_pin_school_callback,
                args=(row["school_name"],),
                use_container_width=True,
                help=(
                    f"Pin {row['school_name']} in the School Finder tab "
                    "to see its full detail card with cross-major data."
                ),
            )

    st.caption(
        f"Data through {OLDEST_DATE}, with some sources updated as recently as "
        f"{NEWEST_DATE}. See About the Data for per-source dates."
    )
    render_about_the_data()
