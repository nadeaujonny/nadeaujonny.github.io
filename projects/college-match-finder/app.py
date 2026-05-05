"""
app.py — College Match Finder (Step 5.4 — Map View) — Phase 5 complete

Phase 5 features:
  - Step 5.1: Side-by-side comparison view for 2-4 pinned schools
  - Step 5.2: CSV export of ranked results
  - Step 5.3: PDF export with cover page + ranked-list cards
              (text sanitized to Latin-1 for Helvetica compatibility —
              en-dashes, smart quotes, accented chars all handled)
  - Step 5.4: Geographic map of matching schools, color-coded by match
              score (RdYlGn). Renders in a collapsible expander above
              the comparison view. Defaults to a continental-US view when
              no state filter is set; auto-fits to the data extent when
              one or more states are selected. Capped at 2,000 markers
              for render performance.

Phase 6 (next): Polish & Accessibility
  - Dark mode verification
  - Mobile responsiveness pass
  - Accessibility: keyboard navigation, color contrast, chart alt text
  - Data freshness badge + "About the Data" transparency section

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import unicodedata

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from fpdf import FPDF

import config
import profiles
from page_modules import major_explorer
from page_modules import find_your_fit
from page_modules import school_finder
from page_modules import about_the_data
from scoring import compute_scores, compute_sensitivity, generate_explainer
from url_state import decode_tab, decode_riasec
from utils import classify_acceptance, format_acceptance_badge, make_button_key


# ============================================================
# MISSION TYPE → column name mapping (used by sidebar + apply_filters)
# ============================================================
MISSION_TYPE_OPTIONS = {
    "HBCU":                                          "is_hbcu",
    "Hispanic-Serving (HSI)":                        "is_hsi",
    "Asian American/Pacific Islander-Serving (AANAPII)": "is_aanapii",
    "Predominantly Black (PBI)":                     "is_pbi",
    "Tribal":                                        "is_tribal",
    "Alaska Native/Native Hawaiian-Serving (ANNHI)": "is_annhi",
    "Native American Non-Tribal-Serving (NANTI)":    "is_nanti",
}


# CSV export column mapping (Step 5.2).
# Maps internal snake_case column names to human-readable CSV headers.
# Order here is the order columns appear in the file.
# match_score_margin replaces margin_str (raw number > formatted string).
CSV_EXPORT_COLUMNS: dict[str, str] = {
    "rank":                 "Rank",
    "school_name":          "School",
    "match_score":          "Match Score",
    "match_score_margin":   "Score Margin (±)",
    "match_score_lower":    "Match Score Lower (95% CI)",
    "match_score_upper":    "Match Score Upper (95% CI)",
    "state":                "State",
    "city":                 "City",
    "control_label":        "Type",
    "setting":              "Setting",
    "size_bucket":          "Size",
    "enrollment":           "Enrollment",
    "net_price":            "Net Price",
    "graduation_rate":      "Graduation Rate (%)",
    "admission_rate":       "Admission Rate (%)",
    "median_earnings_10yr": "Median Earnings 10yr ($)",
    "median_debt":          "Median Debt ($)",
}

# PDF export layout constants (Step 5.3).
# Helvetica (built-in) covers Latin-1 only — no emoji or block characters.
PDF_PAGE_WIDTH_MM   = 215.9   # US Letter
PDF_PAGE_HEIGHT_MM  = 279.4
PDF_MARGIN_MM       = 12.7    # 0.5 inch
PDF_CONTENT_WIDTH_MM = PDF_PAGE_WIDTH_MM - 2 * PDF_MARGIN_MM  # ~190.5 mm
PDF_CARD_HEIGHT_MM  = 52.0    # fixed height per school card
PDF_CARD_GAP_MM     = 5.0     # vertical gap between cards
# Metric rows rendered inside each school card: (column, short_label, formatter)
PDF_METRICS_STRIP = [
    ("net_price",            "Net price",  lambda v: f"${v:,.0f}"),
    ("graduation_rate",      "Grad rate",  lambda v: f"{v:.0f}%"),
    ("admission_rate",       "Admit rate", lambda v: f"{v:.0f}%"),
    ("median_earnings_10yr", "10yr earn",  lambda v: f"${v:,.0f}"),
    ("median_debt",          "Med debt",   lambda v: f"${v:,.0f}"),
    ("repayment_rate_3yr",   "Repayment",  lambda v: f"{v * 100:.0f}%"),
]

# ============================================================
# MAP VIEW — layout constants (Step 5.4)
# ============================================================
MAP_MAX_MARKERS = 2000           # cap to keep rendering snappy
MAP_HEIGHT_PX = 520              # taller than charts; map needs room to breathe
MAP_MARKER_SIZE = 8              # fixed; color carries the score signal
MAP_DEFAULT_STYLE = "open-street-map"   # no Mapbox token required
# Default map view when no state filter is applied — centers on the
# continental US. Hardcoded because data-driven centering is thrown off
# by US territories and non-contiguous states (PR, AK, HI), pulling the
# centroid off the lower 48.
MAP_DEFAULT_CENTER_LAT = 39.5
MAP_DEFAULT_CENTER_LON = -98.5
MAP_DEFAULT_ZOOM = 3.5

# URL query-param schema (Step F).
# Maps url_param_key -> (session_state_key, type, default).
# Only params that differ from defaults are written to the URL.
# Range sliders (SAT range, enrollment range) are omitted — they default to
# full range (the common case) and tuples don't encode cleanly into a single
# URL param without a custom format.
URL_PARAM_MAP: dict[str, tuple] = {
    # Weights — 7 dimensions, one int each in [0, 5]
    "w_aff":   ("weight_affordability",   int,  3),
    "w_grad":  ("weight_graduation_rate", int,  3),
    "w_ret":   ("weight_retention_rate",  int,  3),
    "w_earn":  ("weight_earnings",        int,  3),
    "w_sel":   ("weight_selectivity",     int,  3),
    "w_debt":  ("weight_low_debt",        int,  3),
    "w_repay": ("weight_repayment",       int,  3),
    # Student test scores (0 = not provided, same as widget default)
    "sat":     ("user_sat_raw",           int,  0),
    "act":     ("user_act_raw",           int,  0),
    # Multiselect filters (comma-joined strings)
    "states":  ("filter_states",          list, []),
    "control": ("filter_controls",        list, []),
    "setting": ("filter_settings",        list, []),
    "size":    ("filter_sizes",           list, []),
    "mission": ("filter_mission",         list, []),
    # Single-value filters
    "pell":    ("filter_pell_min",        int,  0),
    "small":   ("filter_show_small",      bool, False),
    # Pinned schools stored as comma-joined school names
    "pins":    ("pinned_schools",         list, []),
    # Selected CIP code on the Major Explorer tab (Phase 8 — Step 8.5)
    "cip":     ("selected_cip",           int,  0),
    # Income bracket for net price override (Phase 4.4)
    "income":  ("selected_income_bracket", str,  "Don't know / skip"),
    # Active tab hint — written by cross-tab handoffs, read to show load banner
    "tab":     ("_active_tab",            str,  "school_finder"),
    # RIASEC vector for Find Your Fit sharing (Phase 13.4b)
    "riasec":  ("_url_riasec_vector",     str,  ""),
}


def _apply_income_bracket_column(df: pd.DataFrame, bracket: str) -> pd.DataFrame:
    """Add a `_selected_bracket_price` column to df based on the selected bracket.

    For each row, picks the public column if control == 1, else the private column.
    If bracket is the default sentinel, returns df unchanged.
    """
    if bracket == "Don't know / skip" or bracket not in config.INCOME_BRACKETS:
        return df
    pub_col, priv_col = config.INCOME_BRACKETS[bracket]
    if pub_col is None or priv_col is None:
        return df
    df = df.copy()
    df["_selected_bracket_price"] = np.where(
        df["control"] == 1, df[pub_col], df[priv_col]
    )
    return df


def _net_price_column_and_label(df: pd.DataFrame) -> tuple[str, str]:
    """Return (column_name, display_label) for net price based on bracket selection."""
    if "_selected_bracket_price" in df.columns:
        return ("_selected_bracket_price", "Net price (your bracket)")
    return ("net_price", "Net price")


# ============================================================
# PAGE CONFIG — must be the first Streamlit call
# ============================================================
st.set_page_config(
    page_title="College Match Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATA LOADING (cached)
# ============================================================
@st.cache_data
def load_colleges() -> pd.DataFrame:
    path = config.DATA_CLEANED_DIR / config.CLEANED_COLLEGES
    if not path.exists():
        st.error(
            f"Cleaned data file not found at {path}. "
            f"Run `python data_prep.py` to generate it."
        )
        st.stop()
    return pd.read_csv(path, low_memory=False)


# ============================================================
# FILTER LOGIC
# ============================================================
def apply_filters(
    df: pd.DataFrame,
    states: list[str],
    controls: list[str],
    settings: list[str],
    sizes: list[str],
    sat_range: tuple[int, int],
    enrollment_range: tuple[int, int],
    pell_min: int = 0,
    mission_types: list[str] | None = None,
) -> pd.DataFrame:
    result = df.copy()

    if states:
        result = result[result["state"].isin(states)]
    if controls:
        result = result[result["control_label"].isin(controls)]
    if settings:
        result = result[result["setting"].isin(settings)]
    if sizes:
        result = result[result["size_bucket"].isin(sizes)]

    sat_lo, sat_hi = sat_range
    if sat_lo > 400 or sat_hi < 1600:
        mask = result["sat_avg"].between(sat_lo, sat_hi) | result["sat_avg"].isna()
        result = result[mask]

    enroll_lo, enroll_hi = enrollment_range
    result = result[result["enrollment"].between(enroll_lo, enroll_hi)]

    # Pell % floor (pct_pell stored as 0–1; slider is 0–100)
    if pell_min > 0 and "pct_pell" in result.columns:
        result = result[result["pct_pell"].fillna(0) * 100 >= pell_min]

    # Mission-driven institution filter
    if mission_types:
        masks = [
            result[col] == 1
            for label, col in MISSION_TYPE_OPTIONS.items()
            if label in mission_types and col in result.columns
        ]
        if masks:
            combined = masks[0]
            for m in masks[1:]:
                combined = combined | m
            result = result[combined]

    return result


# ============================================================
# SESSION STATE
# ============================================================
def init_session_state() -> None:
    for dim_key in config.SCORING_DIMENSIONS:
        state_key = f"weight_{dim_key}"
        if state_key not in st.session_state:
            st.session_state[state_key] = 3
    if "pinned_schools" not in st.session_state:
        st.session_state["pinned_schools"] = []


def clear_pinned() -> None:
    st.session_state["pinned_schools"] = []


def _apply_preset(preset_name: str) -> None:
    """Write preset weights into session_state so sliders pick them up.

    Because the selectbox renders before the slider loop, mutating session
    state here is visible to the sliders on the same rerun — no st.rerun()
    needed.
    """
    for dim_key, value in profiles.get_preset_weights(preset_name).items():
        st.session_state[f"weight_{dim_key}"] = value


def _clamp_filter_list(key: str, valid: list) -> None:
    """Drop any session_state entries not in the current valid option set.
    Guards against URL-parsed values that reference options no longer present
    in the data (e.g., a state code from a different dataset version).
    """
    if key in st.session_state and isinstance(st.session_state[key], list):
        st.session_state[key] = [v for v in st.session_state[key] if v in valid]


def _cip_filter_label(cip4_str: str) -> str:
    """Return a human-readable label for a CIP4 string for use in banners.

    E.g. '11.07' → 'Computer Science (11.07)'. Falls back to the raw string
    if the CIP can't be found in the Field-of-Study data.
    """
    try:
        fos_df = major_explorer.load_field_of_study()
        picker = major_explorer.build_major_picker_options(fos_df)
        match = picker[picker["cip_code_display"] == cip4_str]
        if not match.empty:
            return match.iloc[0]["display_name"]
    except (OSError, KeyError, ValueError, AttributeError):
        # Data file missing or malformed — fall back to raw CIP string.
        pass
    return cip4_str


def _parse_url_into_session_state() -> None:
    """Read st.query_params and populate session_state with parsed values.

    Runs exactly once per browser session (guarded by _url_parsed flag) so
    subsequent reruns don't overwrite changes the user makes via widgets.
    """
    if st.session_state.get("_url_parsed"):
        return

    qp = st.query_params
    for url_key, (state_key, type_, _default) in URL_PARAM_MAP.items():
        if url_key not in qp:
            continue
        raw = qp[url_key]
        try:
            if type_ is list:
                # Comma-joined encoding: "CA,TX" -> ["CA", "TX"]
                parsed = [v for v in raw.split(",") if v]
            elif type_ is bool:
                parsed = raw == "1"
            elif type_ is int:
                parsed = int(raw)
            elif type_ is str:
                parsed = raw
            else:
                parsed = raw
        except (ValueError, TypeError):
            # Malformed param (truncated URL, hand-edited, old version) — skip.
            continue
        st.session_state[state_key] = parsed

    # Validate the tab param after the generic loop.  The generic str branch
    # accepts any string; decode_tab rejects unknown values so garbage like
    # ?tab=foo doesn't pollute _active_tab.
    raw_tab = st.session_state.get("_active_tab")
    if raw_tab is not None:
        valid_tab = decode_tab(raw_tab)
        if valid_tab is None or valid_tab == "school_finder":
            # Invalid or default — drop it so _write_session_state_to_url skips it.
            st.session_state.pop("_active_tab", None)
        else:
            st.session_state["_active_tab"] = valid_tab
            # One-shot banner trigger: popped by main() on the first render only.
            st.session_state["_url_tab_banner"] = valid_tab

    # Validate the riasec param — decode the raw string into a vector dict
    # stored under _url_riasec_decoded; the page module reads that key.
    raw_riasec = st.session_state.get("_url_riasec_vector", "")
    if raw_riasec:
        decoded = decode_riasec(raw_riasec)
        if decoded is None:
            st.session_state.pop("_url_riasec_vector", None)
        else:
            st.session_state["_url_riasec_decoded"] = decoded

    # Clamp income bracket to known values — garbage ?income=foo resets to default.
    if st.session_state.get("selected_income_bracket") not in config.INCOME_BRACKETS:
        st.session_state["selected_income_bracket"] = "Don't know / skip"

    st.session_state["_url_parsed"] = True


def _write_session_state_to_url() -> None:
    """Serialize current session_state into st.query_params.

    Called at the end of every rerun so the URL mirrors current app state.
    Only writes params that differ from their defaults — keeps URLs short.
    """
    new_params: dict[str, str] = {}
    for url_key, (state_key, type_, default) in URL_PARAM_MAP.items():
        if state_key not in st.session_state:
            continue
        val = st.session_state[state_key]
        # Skip defaults and None — keeps URL clean for the common case
        if val is None or val == default:
            continue
        if type_ is list and not val:
            continue
        # Encode to string
        if type_ is list:
            new_params[url_key] = ",".join(str(v) for v in val)
        elif type_ is bool:
            new_params[url_key] = "1" if val else "0"
        else:
            new_params[url_key] = str(val)

    st.query_params.clear()
    for k, v in new_params.items():
        st.query_params[k] = v


# ============================================================
# SIDEBAR — filters + weights + test scores
# ============================================================
def render_sidebar(df: pd.DataFrame) -> tuple[dict, dict, dict]:
    st.sidebar.title("🎓 College Match Finder")
    st.sidebar.caption("Filter the field, then rank what's left.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filters")

    states_in_data = sorted(df["state"].dropna().unique().tolist())
    _clamp_filter_list("filter_states", states_in_data)
    states = st.sidebar.multiselect(
        "State", options=states_in_data, default=[],
        key="filter_states",
        help="Leave empty to include all states.",
    )

    control_options = sorted(df["control_label"].dropna().unique().tolist())
    _clamp_filter_list("filter_controls", control_options)
    controls = st.sidebar.multiselect(
        "School type", options=control_options, default=[],
        key="filter_controls",
        help="Leave empty to include all types.",
    )

    setting_options = [s for s in config.SETTING_OPTIONS
                       if s in df["setting"].dropna().unique()]
    _clamp_filter_list("filter_settings", setting_options)
    settings = st.sidebar.multiselect("Campus setting", options=setting_options, default=[],
                                      key="filter_settings")

    size_options = [label for label, _, _ in config.SIZE_BUCKETS
                    if label in df["size_bucket"].dropna().unique()]
    _clamp_filter_list("filter_sizes", size_options)
    sizes = st.sidebar.multiselect("School size", options=size_options, default=[],
                                   key="filter_sizes")

    pell_min = st.sidebar.slider(
        "Minimum % Pell Grant recipients",
        min_value=0, max_value=100, value=0, step=5,
        key="filter_pell_min",
        help="Filter to schools where at least this share of students received "
             "a Pell Grant (a proxy for serving lower-income students). "
             "0 = no filter applied.",
    )

    with st.sidebar.expander("Mission-driven institutions"):
        _clamp_filter_list("filter_mission", list(MISSION_TYPE_OPTIONS.keys()))
        mission_types = st.multiselect(
            "Show only:",
            options=list(MISSION_TYPE_OPTIONS.keys()),
            default=[],
            key="filter_mission",
            help="Filter results to schools with at least one of the selected "
                 "mission designations. Leave empty to show all schools.",
        )

    sat_range = st.sidebar.slider(
        "Schools' avg SAT range (for filtering)",
        min_value=400, max_value=1600, value=(400, 1600), step=10,
        help="Keep schools whose average SAT falls in this range. "
             "Test-optional schools (no published SAT) are kept unless "
             "you've narrowed the range. This is separate from your "
             "own score below — that drives the acceptance badge.",
    )

    max_enroll = int(df["enrollment"].max())
    enrollment_range = st.sidebar.slider(
        "Undergraduate enrollment",
        min_value=0, max_value=max_enroll, value=(0, max_enroll), step=500,
    )

    show_small_schools = st.sidebar.checkbox(
        "Show schools with <250 students (less reliable metrics)",
        value=False,
        key="filter_show_small",
    )

    # --------------------------------------------------------
    # FILTER BY MAJOR — Phase 13.2
    # --------------------------------------------------------
    fos_df_for_cip = major_explorer.load_field_of_study()
    cip_picker_df = major_explorer.build_major_picker_options(fos_df_for_cip)
    cip_label_map = dict(
        zip(cip_picker_df["cip_code_display"], cip_picker_df["cip_label"])
    )
    cip_options = ["All majors"] + cip_picker_df["cip_code_display"].tolist()

    def _format_cip_for_filter(val: str) -> str:
        if val == "All majors":
            return "All majors"
        label = cip_label_map.get(val, "")
        return f"{val} — {label}" if label else val

    cip_filter_idx = school_finder.initial_cip_filter_index(cip_options)
    selected_cip_filter = st.sidebar.selectbox(
        "Filter by major (CIP)",
        options=cip_options,
        index=cip_filter_idx,
        format_func=_format_cip_for_filter,
        key="cip_filter_widget",
        help=(
            "Show only schools that offer this major. "
            "Select 'All majors' to show all schools. "
            "This filter works alongside all other sidebar filters. "
            "Tip: click 'See schools strong in this major →' on the "
            "Major Explorer tab to pre-populate this filter."
        ),
    )

    # --------------------------------------------------------
    # YOUR TEST SCORES (NEW in Step 4.2) — drives acceptance badge only
    # --------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("Your test scores (optional)")
    st.sidebar.caption(
        "Enter your own score to see Safety / Match / Reach badges on "
        "pinned schools' detail cards. Leave blank to skip. If both are "
        "provided, SAT is used."
    )

    sat_raw = st.sidebar.number_input(
        "Your SAT composite (400–1600)",
        min_value=0, max_value=1600, value=0, step=10,
        key="user_sat_raw",
        help="Enter 0 to skip.",
    )
    act_raw = st.sidebar.number_input(
        "Your ACT composite (1–36)",
        min_value=0, max_value=36, value=0, step=1,
        key="user_act_raw",
        help="Enter 0 to skip.",
    )
    # Treat 0 as "not provided" since number_input requires a number
    student_sat = float(sat_raw) if sat_raw >= 400 else None
    student_act = float(act_raw) if act_raw >= 1 else None

    selected_income_bracket = st.sidebar.selectbox(
        "Family income bracket (optional)",
        options=list(config.INCOME_BRACKETS.keys()),
        index=list(config.INCOME_BRACKETS.keys()).index("Don't know / skip"),
        key="selected_income_bracket",
        help=(
            "If you select a bracket, the app will use the income-specific net price "
            "from College Scorecard for scoring and display. Otherwise the overall "
            "average is used."
        ),
    )

    # --------------------------------------------------------
    # PRIORITIES
    # --------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.subheader("Priorities")
    st.sidebar.caption("How much does each factor matter to you? (0 = doesn't matter, 5 = very important)")

    # Quick start selectbox (Step E). Renders before the slider loop so
    # _apply_preset's session-state writes are visible to sliders this rerun.
    # No key= on the selectbox: the displayed value is derived from current
    # weights via match_profile(), so moving any slider auto-reverts the
    # selectbox to "Custom" on the next rerun.
    current_weights = {
        dim_key: st.session_state.get(f"weight_{dim_key}", 3)
        for dim_key in config.SCORING_DIMENSIONS
    }
    current_profile = profiles.match_profile(current_weights)
    selected_profile = st.sidebar.selectbox(
        "Quick start",
        options=profiles.PROFILE_ORDER,
        index=profiles.PROFILE_ORDER.index(current_profile),
        help=(
            "Pick a preset to set all 7 weights at once. Adjust any slider "
            "afterward and this resets to 'Custom'."
        ),
    )
    if selected_profile != profiles.CUSTOM_PROFILE and selected_profile != current_profile:
        _apply_preset(selected_profile)
        st.rerun()

    weights = {}
    for dim_key, spec in config.SCORING_DIMENSIONS.items():
        weights[dim_key] = st.sidebar.slider(
            spec["label"],
            min_value=0, max_value=5, step=1,
            key=f"weight_{dim_key}",
            help=spec["description"],
        )

    filter_selections = {
        "states": states,
        "controls": controls,
        "settings": settings,
        "sizes": sizes,
        "sat_range": sat_range,
        "enrollment_range": enrollment_range,
        "pell_min": pell_min,
        "mission_types": mission_types,
        "show_small_schools": show_small_schools,
        "cip_filter": selected_cip_filter,
    }
    student_scores = {
        "sat": student_sat,
        "act": student_act,
    }
    return filter_selections, weights, student_scores


# ============================================================
# SUMMARY BANNER — above results
# ============================================================
def render_summary_banner(
    ranked: pd.DataFrame,
    filter_selections: dict,
    weights: dict,
) -> None:
    active_weights = sorted(
        ((k, w) for k, w in weights.items() if w > 0),
        key=lambda kv: kv[1],
        reverse=True,
    )[:3]

    priority_labels = []
    for key, _ in active_weights:
        label = config.SCORING_DIMENSIONS[key]["label"]
        for prefix in ("High ", "Low "):
            if label.startswith(prefix):
                label = label[len(prefix):]
                break
        priority_labels.append(label)

    filter_pieces = []
    if filter_selections["states"]:
        states = filter_selections["states"]
        filter_pieces.append(
            ", ".join(states) if len(states) <= 3
            else f"{len(states)} states"
        )
    if filter_selections["controls"]:
        filter_pieces.append(" / ".join(filter_selections["controls"]))
    if filter_selections["settings"]:
        filter_pieces.append(" / ".join(filter_selections["settings"]) + " setting")
    if filter_selections["sizes"]:
        sizes = filter_selections["sizes"]
        filter_pieces.append(
            sizes[0] if len(sizes) == 1
            else f"{len(sizes)} size categories"
        )
    sat_lo, sat_hi = filter_selections["sat_range"]
    if sat_lo > 400 or sat_hi < 1600:
        filter_pieces.append(f"SAT {sat_lo}–{sat_hi}")
    enroll_lo, enroll_hi = filter_selections["enrollment_range"]
    if enroll_lo > 0:
        filter_pieces.append(f"≥{enroll_lo:,} enrolled")

    with st.container(border=True):
        st.markdown(f"### **{len(ranked):,}** schools match your filters")
        if priority_labels:
            st.markdown(f"**Ranked by:** {' · '.join(priority_labels)}")
        else:
            st.markdown("*No priorities set — showing neutral match scores.*")
        if filter_pieces:
            st.caption(f"Filters: {' · '.join(filter_pieces)}")
        else:
            st.caption("Filters: None active (all 4-year colleges)")


# ============================================================
# CSV EXPORT (Step 5.2)
# ============================================================

@st.cache_data(show_spinner=False)
def _build_results_csv_bytes(ranked: pd.DataFrame, top_n: int) -> bytes:
    """
    Build UTF-8 CSV bytes for the ranked-results download.

    Cached so unrelated sidebar interactions don't trigger re-encoding.
    Cache key is the DataFrame content + top_n; changes to either
    invalidate the cache automatically via Streamlit's hashing.
    """
    if ranked.empty:
        return b""

    out = ranked.head(top_n).copy()
    out.insert(0, "rank", range(1, len(out) + 1))

    # Keep only desired columns in definition order; skip any absent columns
    # (CI columns are absent when all weights are 0).
    export_columns = dict(CSV_EXPORT_COLUMNS)
    _np_col, _np_label = _net_price_column_and_label(out)
    if _np_col != "net_price":
        export_columns[_np_col] = _np_label
        export_columns.pop("net_price", None)
    keep = [c for c in export_columns if c in out.columns]
    out = out[keep].rename(columns=export_columns)

    return out.to_csv(index=False).encode("utf-8")


# ============================================================
# PDF EXPORT HELPERS (Step 5.3)
# ============================================================

def _truncate_to_width(pdf: FPDF, text: str, max_width_mm: float) -> str:
    """Shorten text with ellipsis so it fits within max_width_mm at current font."""
    if pdf.get_string_width(text) <= max_width_mm:
        return text
    while len(text) > 0 and pdf.get_string_width(text + "...") > max_width_mm:
        text = text[:-1]
    return text + "..."


def _format_filter_lines(filter_selections: dict) -> list[str]:
    """Convert filter_selections into short lines for the PDF cover page."""
    lines: list[str] = []
    states = filter_selections.get("states", [])
    if states:
        lines.append("States: " + (", ".join(states) if len(states) <= 6 else f"{len(states)} states selected"))
    controls = filter_selections.get("controls", [])
    if controls:
        lines.append("Type: " + " / ".join(controls))
    settings = filter_selections.get("settings", [])
    if settings:
        lines.append("Setting: " + " / ".join(settings))
    sizes = filter_selections.get("sizes", [])
    if sizes:
        lines.append("Size: " + " / ".join(sizes))
    pell_min = filter_selections.get("pell_min", 0)
    if pell_min and pell_min > 0:
        lines.append(f"Min. Pell Grant recipients: {pell_min}%")
    mission = filter_selections.get("mission_types", [])
    if mission:
        lines.append("Mission: " + " / ".join(mission))
    sat_range = filter_selections.get("sat_range", (400, 1600))
    if sat_range and (sat_range[0] > 400 or sat_range[1] < 1600):
        lines.append(f"Avg SAT range: {sat_range[0]}-{sat_range[1]}")
    enrollment_range = filter_selections.get("enrollment_range")
    if enrollment_range and enrollment_range[0] > 0:
        lines.append(f"Min enrollment: {enrollment_range[0]:,}")
    if not lines:
        lines.append("None (all 4-year colleges)")
    return lines


def _format_weight_lines(weights: dict) -> list[str]:
    """Convert weights into sorted human-readable lines for the PDF cover page."""
    active = [(k, w) for k, w in weights.items() if w > 0]
    active.sort(key=lambda kv: kv[1], reverse=True)
    if not active:
        return ["No priorities set (neutral matching)."]
    lines = []
    for key, w in active:
        label = config.SCORING_DIMENSIONS[key]["label"]
        bar = "#" * w + "." * (5 - w)
        lines.append(f"{label}: [{bar}] ({w}/5)")
    return lines


# ============================================================
# PDF TEXT SANITIZATION (Step 5.3 patch)
# ============================================================
# fpdf2's built-in Helvetica is Latin-1 only. Any character outside
# 0x00-0xFF (such as en-dashes, smart quotes, the ellipsis character)
# raises FPDFUnicodeEncodingException at PDF generation time.
#
# This helper replaces the common offenders with ASCII equivalents,
# then NFKD-decomposes anything else (so "é" becomes "e" + combining
# accent, the accent gets dropped, and "e" survives), and finally
# strips any leftover non-Latin-1 bytes.
PDF_CHAR_REPLACEMENTS = {
    "–": "-",   # en dash  –
    "—": "-",   # em dash  —
    "−": "-",   # minus sign  −
    "‘": "'",   # left single quote  '
    "’": "'",   # right single quote / apostrophe  '
    "“": '"',   # left double quote  "
    "”": '"',   # right double quote  "
    "…": "...", # ellipsis  …
    " ": " ",   # non-breaking space (Latin-1 valid but renders oddly)
    "​": "",    # zero-width space
    "™": "(TM)",
    "®": "(R)",
    "©": "(C)",
    "•": "*",   # bullet  •
    "·": "*",   # middle dot  ·  (used in summary banner)
}


def _pdf_safe(text: object) -> str:
    """
    Return a Latin-1-safe version of `text` suitable for fpdf2's Helvetica.

    1. Coerce to string.
    2. Apply the explicit replacement table for common typographic chars.
    3. NFKD-normalize and drop combining marks (so "é" → "e", "ñ" → "n").
    4. Encode/decode through latin-1, ignoring anything still untranslatable.

    Idempotent — safe to call on already-clean ASCII strings.
    """
    if text is None:
        return ""
    s = str(text)

    # Step 1: explicit replacements
    for src, dst in PDF_CHAR_REPLACEMENTS.items():
        if src in s:
            s = s.replace(src, dst)

    # Step 2: NFKD decomposition to strip accents from anything still
    # outside Latin-1 (Latin-1 itself supports é/ñ/ü directly, so this
    # mostly catches characters from non-Western scripts).
    s = unicodedata.normalize("NFKD", s)

    # Step 3: drop anything still untranslatable to Latin-1
    s = s.encode("latin-1", errors="ignore").decode("latin-1")

    return s


def _draw_pdf_cover(
    pdf: FPDF,
    filter_selections: dict,
    weights: dict,
    student_scores: dict,
    n_schools: int,
    top_n: int,
) -> None:
    """Render the cover page of the PDF."""
    pdf.add_page()
    lm = PDF_MARGIN_MM
    cw = PDF_CONTENT_WIDTH_MM

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(lm, lm)
    pdf.cell(cw, 12, "College Match Finder", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_x(lm)
    pdf.cell(cw, 7, "Personalized Results Report", new_x="LMARGIN", new_y="NEXT", align="C")

    today_str = pd.Timestamp.today().strftime("%B %d, %Y")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_x(lm)
    pdf.cell(
        cw, 6,
        _pdf_safe(f"Generated {today_str}  |  Showing top {top_n} of {n_schools:,} matching schools"),
        new_x="LMARGIN", new_y="NEXT", align="C",
    )

    pdf.ln(5)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(lm, pdf.get_y(), lm + cw, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_x(lm)
    pdf.cell(cw, 7, "Active Filters", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    for line in _format_filter_lines(filter_selections):
        pdf.set_x(lm + 4)
        pdf.cell(cw - 4, 5, _pdf_safe(line), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_x(lm)
    pdf.cell(cw, 7, "Priorities (Weights)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    for line in _format_weight_lines(weights):
        pdf.set_x(lm + 4)
        pdf.cell(cw - 4, 5, _pdf_safe(line), new_x="LMARGIN", new_y="NEXT")

    sat = student_scores.get("sat")
    act = student_scores.get("act")
    if sat or act:
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_x(lm)
        pdf.cell(cw, 7, "Your Test Scores", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        if sat:
            pdf.set_x(lm + 4)
            pdf.cell(cw - 4, 5, f"SAT: {int(sat)}", new_x="LMARGIN", new_y="NEXT")
        if act:
            pdf.set_x(lm + 4)
            pdf.cell(cw - 4, 5, f"ACT: {int(act)}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(lm, pdf.get_y(), lm + cw, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_x(lm)
    pdf.cell(cw, 5, "School details follow.", new_x="LMARGIN", new_y="NEXT", align="C")


def _draw_school_card(
    pdf: FPDF,
    rank: int,
    school_row: pd.Series,
    weights: dict,
    student_scores: dict,
) -> None:
    """
    Draw one bordered school card. Adds a new page if there is not enough
    room for the full card + gap. Advances the y position by
    PDF_CARD_HEIGHT_MM + PDF_CARD_GAP_MM.
    """
    lm = PDF_MARGIN_MM
    cw = PDF_CONTENT_WIDTH_MM
    card_h = PDF_CARD_HEIGHT_MM

    if pdf.get_y() + card_h + PDF_CARD_GAP_MM > PDF_PAGE_HEIGHT_MM - PDF_MARGIN_MM:
        pdf.add_page()

    y0 = pdf.get_y()

    # Card background + border
    pdf.set_fill_color(*config.PALETTE["pdf_card_bg"])
    pdf.set_draw_color(*config.PALETTE["pdf_card_border"])
    pdf.rect(lm, y0, cw, card_h, style="FD")

    # Rank badge
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_xy(lm + 2, y0 + 2)
    pdf.cell(10, 5, f"#{rank}", align="L")

    # Match score (top-right)
    match_score = school_row.get("match_score")
    if match_score is not None and pd.notna(match_score):
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_xy(lm + cw - 30, y0 + 2)
        pdf.cell(28, 7, f"{float(match_score):.1f}", align="R")

        margin_v = school_row.get("match_score_margin")
        if margin_v is not None and pd.notna(margin_v):
            pdf.set_font("Helvetica", "", 7)
            pdf.set_xy(lm + cw - 30, y0 + 9)
            pdf.cell(28, 4, f"+/- {float(margin_v):.1f}", align="R")

    # Acceptance badge (below score)
    school_sat_25, school_sat_75 = _school_sat_composite_range(school_row)
    acceptance_label = classify_acceptance(
        student_sat=student_scores.get("sat"),
        student_act=student_scores.get("act"),
        school_sat_25=school_sat_25,
        school_sat_75=school_sat_75,
    )
    badge_colors = {
        "Safety": config.PALETTE["pdf_safety_tint"],
        "Match":  config.PALETTE["pdf_match_tint"],
        "Reach":  config.PALETTE["pdf_reach_tint"],
    }.get(acceptance_label, config.PALETTE["pdf_na_tint"])
    pdf.set_fill_color(*badge_colors)
    pdf.set_draw_color(*config.PALETTE["pdf_card_border"])
    pdf.set_font("Helvetica", "", 7)
    pdf.set_xy(lm + cw - 30, y0 + 14)
    pdf.cell(28, 5, _pdf_safe(acceptance_label), align="C", fill=True, border=1)

    # School name
    name = str(school_row.get("school_name") or "Unknown")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(lm + 13, y0 + 2)
    pdf.cell(cw - 45, 6, _truncate_to_width(pdf, _pdf_safe(name), cw - 48), align="L")

    # Location line
    loc_parts: list[str] = []
    for col in ("city", "state", "control_label", "setting"):
        v = school_row.get(col)
        if v is not None and pd.notna(v):
            loc_parts.append(str(v))
    loc_str = " - ".join(loc_parts)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_xy(lm + 13, y0 + 9)
    pdf.cell(cw - 45, 5, _truncate_to_width(pdf, _pdf_safe(loc_str), cw - 48), align="L")

    # Divider
    pdf.set_draw_color(*config.PALETTE["pdf_card_border"])
    pdf.line(lm + 2, y0 + 19, lm + cw - 2, y0 + 19)

    # Metric strips — 3 columns x 2 rows
    col_w = cw / 3
    for idx, (col_name, label, formatter) in enumerate(PDF_METRICS_STRIP):
        if col_name == "net_price" and "_selected_bracket_price" in school_row.index:
            col_name, label = "_selected_bracket_price", "Net price (bracket)"
        row_y = y0 + 21 if idx < 3 else y0 + 33
        col_offset = (idx % 3) * col_w

        val = school_row.get(col_name)
        if val is not None and pd.notna(val):
            try:
                val_str = formatter(float(val))
            except (TypeError, ValueError):
                val_str = "N/A"
        else:
            val_str = "N/A"

        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(lm + col_offset + 3, row_y)
        pdf.cell(col_w - 3, 4, _pdf_safe(label), align="L")

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_xy(lm + col_offset + 3, row_y + 4)
        pdf.cell(col_w - 3, 5, _truncate_to_width(pdf, _pdf_safe(val_str), col_w - 6), align="L")

    # Divider above explainer
    pdf.set_draw_color(*config.PALETTE["pdf_card_border"])
    pdf.line(lm + 2, y0 + 43, lm + cw - 2, y0 + 43)

    # One-line explainer: top-weighted dimension + percentile
    active_w = sorted(
        ((k, w) for k, w in weights.items() if w > 0),
        key=lambda kv: kv[1],
        reverse=True,
    )
    explainer = ""
    if active_w:
        top_key, _ = active_w[0]
        score_v = school_row.get(f"score_{top_key}")
        if score_v is not None and pd.notna(score_v):
            pct = int(round(float(score_v) * 100))
            top_label = config.SCORING_DIMENSIONS[top_key]["label"].lower()
            for prefix in ("high ", "low "):
                if top_label.startswith(prefix):
                    top_label = top_label[len(prefix):]
                    break
            explainer = f"Top priority: {top_label} - {pct}th percentile"

    if explainer:
        pdf.set_font("Helvetica", "I", 7)
        pdf.set_xy(lm + 3, y0 + 44)
        pdf.cell(cw - 6, 5, _truncate_to_width(pdf, _pdf_safe(explainer), cw - 8), align="L")

    pdf.set_y(y0 + card_h + PDF_CARD_GAP_MM)


@st.cache_data(show_spinner="Generating PDF...")
def _build_results_pdf_bytes(
    ranked: pd.DataFrame,
    top_n: int,
    filter_selections: dict,
    weights: dict,
    student_scores: dict,
) -> bytes:
    """
    Build PDF bytes for the ranked-results download.

    Cached so unrelated sidebar interactions don't re-render the PDF.
    Cache key is the DataFrame content + top_n + filter/weight/score dicts;
    any change to these invalidates the cache automatically.
    """
    if ranked.empty:
        return b""

    export_df = ranked.head(top_n)
    n_schools = len(ranked)

    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(PDF_MARGIN_MM, PDF_MARGIN_MM, PDF_MARGIN_MM)
    pdf.set_auto_page_break(auto=False)  # manual page-break in _draw_school_card

    _draw_pdf_cover(pdf, filter_selections, weights, student_scores, n_schools, top_n)

    pdf.add_page()
    pdf.set_y(PDF_MARGIN_MM)

    for rank_idx, (_, row) in enumerate(export_df.iterrows(), start=1):
        _draw_school_card(pdf, rank_idx, row, weights, student_scores)

    return bytes(pdf.output())


def render_export_row(
    ranked: pd.DataFrame,
    filter_selections: dict,
    weights: dict,
    student_scores: dict,
) -> None:
    """
    Row with a row-count selector, a CSV download button, and a PDF download button.
    Hidden entirely when no schools match the current filters.
    The PDF reuses the same top-N value as the CSV (single source of truth).
    """
    if ranked.empty:
        return

    n_results = len(ranked)
    default_n = min(config.DEFAULT_MAX_RESULTS, n_results)

    _spacer, n_col, csv_col, pdf_col = st.columns([3, 1, 1, 1])

    with n_col:
        top_n = st.number_input(
            "Rows to export",
            min_value=1,
            max_value=n_results,
            value=default_n,
            step=10,
            key="csv_export_top_n",
            help=f"Top-ranked schools to include. Max = {n_results:,}.",
        )

    top_n_int = int(top_n)
    today = pd.Timestamp.today().strftime("%Y%m%d")

    with csv_col:
        st.write("")
        st.write("")
        csv_bytes = _build_results_csv_bytes(ranked, top_n_int)
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name=f"college_match_results_top{top_n_int}_{today}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Downloads top N schools with raw numeric values and "
                 "match-score confidence interval bounds.",
        )

    with pdf_col:
        st.write("")
        st.write("")
        pdf_bytes = _build_results_pdf_bytes(
            ranked, top_n_int, filter_selections, weights, student_scores
        )
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=f"college_match_results_top{top_n_int}_{today}.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="PDF report with a cover page (active filters + priorities) "
                 "and one card per school showing key metrics.",
        )


# ============================================================
# PIN SELECTOR — between banner and results table
# ============================================================
def render_pin_selector(full_df: pd.DataFrame) -> list[str]:
    all_school_names = sorted(full_df["school_name"].dropna().unique().tolist())

    current = [s for s in st.session_state["pinned_schools"] if s in all_school_names]
    st.session_state["pinned_schools"] = current

    col_left, col_right = st.columns([5, 1])
    with col_left:
        pinned = st.multiselect(
            "📌 Pin schools for detail view",
            options=all_school_names,
            default=st.session_state["pinned_schools"],
            key="pinned_schools",
            help=(
                "Type to search. You can pin schools from outside your current "
                "filters — pinned schools stay pinned until you unpin them."
            ),
            placeholder="Search and select schools to see detail cards below…",
        )
    with col_right:
        st.write("")
        st.write("")
        st.button(
            "Clear pins",
            on_click=clear_pinned,
            use_container_width=True,
            disabled=len(pinned) == 0,
        )

    return pinned


# ============================================================
# MAIN PANEL — ranked results table
# ============================================================
def render_results(ranked: pd.DataFrame) -> None:
    if ranked.empty:
        st.info("No schools match the current filters. Try loosening them.")
        return

    display = ranked.copy()
    display.insert(0, "rank", range(1, len(display) + 1))

    # CI margin column — "± X.X" when available, "—" when all weights are 0
    if "match_score_margin" in display.columns:
        display["margin_str"] = display["match_score_margin"].apply(
            lambda v: f"± {v:.1f}" if pd.notna(v) else "—"
        )
    else:
        display["margin_str"] = "—"

    np_col, np_label = _net_price_column_and_label(display)
    table_cols = [
        "rank", "school_name", "match_score", "margin_str",
        "state", "city", "control_label",
        "setting", "size_bucket", "enrollment",
        np_col, "graduation_rate", "admission_rate",
        "median_earnings_10yr", "median_debt",
    ]
    table_cols = [c for c in table_cols if c in display.columns]

    st.dataframe(
        display[table_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "rank":                  st.column_config.NumberColumn("#", width="small", format="%d"),
            "school_name":           st.column_config.TextColumn("School"),
            "match_score":           st.column_config.ProgressColumn(
                                         "Match", min_value=0, max_value=100, format="%.0f%%",
                                     ),
            "margin_str":            st.column_config.TextColumn("± margin", width="small"),
            "state":                 st.column_config.TextColumn("State", width="small"),
            "city":                  st.column_config.TextColumn("City"),
            "control_label":         st.column_config.TextColumn("Type"),
            "setting":               st.column_config.TextColumn("Setting", width="small"),
            "size_bucket":           st.column_config.TextColumn("Size"),
            "enrollment":            st.column_config.NumberColumn("Enrollment", format="%d"),
            np_col:                  st.column_config.NumberColumn(np_label, format="$%d"),
            "graduation_rate":       st.column_config.NumberColumn("Grad rate", format="%.0f%%"),
            "admission_rate":        st.column_config.NumberColumn("Admit rate", format="%.0f%%"),
            "median_earnings_10yr":  st.column_config.NumberColumn("10yr earnings", format="$%d"),
            "median_debt":           st.column_config.NumberColumn("Median debt", format="$%d"),
        },
    )


# ============================================================
# ACCEPTANCE BADGE HELPERS (NEW in Step 4.2)
# ============================================================



def _school_sat_composite_range(school_row: pd.Series) -> tuple[float | None, float | None]:
    """
    Return (25th, 75th) percentile SAT composite for a school, computed on
    the fly from the verbal and math sub-score percentiles. Returns (None,
    None) if any component is missing — data_prep.py's cleaning preserves
    NaN honestly, so this lets the badge show N/A rather than fake a number.
    """
    v25 = school_row.get("sat_verbal_25")
    m25 = school_row.get("sat_math_25")
    v75 = school_row.get("sat_verbal_75")
    m75 = school_row.get("sat_math_75")

    if pd.isna(v25) or pd.isna(m25):
        sat_25 = None
    else:
        sat_25 = float(v25) + float(m25)

    if pd.isna(v75) or pd.isna(m75):
        sat_75 = None
    else:
        sat_75 = float(v75) + float(m75)

    return sat_25, sat_75


def _acceptance_explainer(
    label: str,
    student_scores: dict,
    school_sat_25: float | None,
    school_sat_75: float | None,
) -> str:
    """One-line human-readable explanation of what the badge means."""
    # Case 1: no student score provided
    student_sat = student_scores.get("sat")
    student_act = student_scores.get("act")
    if student_sat is None and student_act is None:
        return "Enter your SAT or ACT in the sidebar to see where you stand."

    # Case 2: school has no published SAT range
    if school_sat_25 is None or school_sat_75 is None:
        return "This school doesn't publish SAT percentile ranges — no classification possible."

    # Case 3: have both, explain where the student sits
    # Use SAT if provided, otherwise ACT converted to SAT
    if student_sat is not None:
        student_label = f"Your SAT of {int(student_sat)}"
    else:
        # Convert ACT → SAT for the explainer so the comparison reads cleanly
        act_int = int(round(student_act))
        sat_equiv = config.ACT_TO_SAT.get(act_int)
        if sat_equiv is None:
            student_label = f"Your ACT of {act_int}"
        else:
            student_label = f"Your ACT of {act_int} (≈ SAT {sat_equiv})"

    range_label = f"this school's {int(school_sat_25)}–{int(school_sat_75)} mid-50% range"

    if label == "Safety":
        return f"{student_label} is at or above {range_label}."
    if label == "Match":
        return f"{student_label} falls inside {range_label}."
    if label == "Reach":
        return f"{student_label} is at or below {range_label}."
    return ""


# ============================================================
# DETAIL CARDS — one per pinned school
# ============================================================

CARD_METRIC_ROWS = [
    ("net_price",            "Net price",        lambda v: f"${v:,.0f}"),
    ("graduation_rate",      "Graduation rate",  lambda v: f"{v:.0f}%"),
    ("admission_rate",       "Admission rate",   lambda v: f"{v:.0f}%"),
    ("sat_avg",              "Avg SAT",          lambda v: f"{v:,.0f}"),
    ("median_earnings_10yr", "10yr earnings",    lambda v: f"${v:,.0f}"),
    ("median_debt",          "Median debt",      lambda v: f"${v:,.0f}"),
    ("repayment_rate_3yr",   "Loan repayment",   lambda v: f"{v * 100:.1f}%"),
    ("enrollment",           "Enrollment",       lambda v: f"{v:,.0f}"),
]

# Raw-value formatters for the comparison table, one per scoring dimension.
# graduation_rate and admission_rate are pre-scaled to 0–100 in main();
# retention_rate and repayment_rate_3yr are stored as 0–1 and scaled here.
COMPARISON_RAW_FORMATTERS: dict = {
    "affordability":   lambda v: f"${v:,.0f}",       # net_price
    "graduation_rate": lambda v: f"{v:.0f}%",         # already 0–100
    "retention_rate":  lambda v: f"{v * 100:.0f}%",  # stored 0–1
    "earnings":        lambda v: f"${v:,.0f}",        # median_earnings_10yr
    "selectivity":     lambda v: f"{v:.0f}%",         # admission_rate, already 0–100
    "low_debt":        lambda v: f"${v:,.0f}",        # median_debt
    "repayment":       lambda v: f"{v * 100:.0f}%",  # stored 0–1
}


def _fmt_or_dash(row: pd.Series, col: str, formatter) -> str:
    if col not in row.index:
        return "—"
    val = row[col]
    if pd.isna(val):
        return "—"
    try:
        return formatter(val)
    except (TypeError, ValueError):
        return "—"


def _radar_label(dim_key: str) -> str:
    return config.SCORING_DIMENSIONS[dim_key]["label"]


def build_radar_chart(school_row: pd.Series) -> go.Figure:
    dims = list(config.SCORING_DIMENSIONS.keys())
    labels = [_radar_label(k) for k in dims]

    values = []
    for key in dims:
        score_col = f"score_{key}"
        if score_col in school_row.index and pd.notna(school_row[score_col]):
            values.append(float(school_row[score_col]) * 100)
        else:
            values.append(0.0)

    labels_loop = labels + [labels[0]]
    values_loop = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_loop,
        theta=labels_loop,
        fill="toself",
        name=school_row["school_name"],
        hovertemplate="%{theta}: %{r:.0f}th percentile<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[25, 50, 75, 100],
                ticktext=["25", "50", "75", "100"],
                tickfont=dict(size=10),
            ),
            angularaxis=dict(tickfont=dict(size=11)),
        ),
        showlegend=False,
        margin=dict(l=60, r=60, t=20, b=20),
        height=340,
    )
    return fig


# ============================================================
# DETAIL CARD — new helper functions (Step A)
# ============================================================



def _pct_val(row: pd.Series, col: str) -> float | None:
    """Return a 0–1 proportion from the row, or None if missing."""
    v = row.get(col)
    if v is None or pd.isna(v):
        return None
    return float(v)


def _render_context_badges(school_row: pd.Series) -> None:
    """Compact badge row: Carnegie type, test policy, MSI, religion."""
    parts = []

    carnegie = school_row.get("carnegie_label")
    if pd.notna(carnegie) and carnegie not in ("Unknown", "Not Classified", "Other", None):
        parts.append(str(carnegie))

    test_pol = school_row.get("test_policy_label")
    if pd.notna(test_pol) and test_pol not in ("Unknown", None):
        parts.append(f"Tests: {test_pol}")

    if school_row.get("is_minority_serving"):
        parts.append("Minority-Serving Institution")

    religion = school_row.get("religion_label")
    if pd.notna(religion) and religion not in ("None", None):
        parts.append(f"Affiliation: {religion}")

    if parts:
        st.caption("  ·  ".join(parts))


def _build_demographics_chart(school_row: pd.Series, name: str) -> go.Figure | None:
    """
    Horizontal stacked bar: gender row + race/ethnicity row.
    Returns None if all demographic values are missing.
    """
    pct_w = _pct_val(school_row, "pct_women")
    race_cols = ["pct_black", "pct_hispanic", "pct_asian", "pct_white", "pct_nonresident"]
    race_labels = ["Black/AA", "Hispanic", "Asian", "White", "Non-resident"]
    race_vals = [_pct_val(school_row, c) for c in race_cols]

    has_gender = pct_w is not None
    has_race = any(v is not None for v in race_vals)
    if not has_gender and not has_race:
        return None

    fig = go.Figure()

    if has_gender:
        pct_m = 1.0 - pct_w
        fig.add_trace(go.Bar(
            name="Women", x=[pct_w * 100], y=["Gender"],
            orientation="h", marker_color=config.PALETTE["demo_women"],
            hovertemplate="Women: %{x:.1f}%<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            name="Men/Other", x=[pct_m * 100], y=["Gender"],
            orientation="h", marker_color=config.PALETTE["demo_men_other"],
            hovertemplate="Men/Other: %{x:.1f}%<extra></extra>",
        ))

    if has_race:
        known_sum = sum(v for v in race_vals if v is not None)
        other_val = max(0.0, 1.0 - known_sum)
        all_labels = race_labels + ["Other/Unknown"]
        all_vals = race_vals + [other_val if known_sum > 0 else None]
        all_colors = [
            config.PALETTE["demo_black"],
            config.PALETTE["demo_hispanic"],
            config.PALETTE["demo_asian"],
            config.PALETTE["demo_white"],
            config.PALETTE["demo_nonresident"],
            config.PALETTE["demo_other"],
        ]

        for label, val, color in zip(all_labels, all_vals, all_colors):
            if val is not None and val > 0.001:
                fig.add_trace(go.Bar(
                    name=label, x=[val * 100], y=["Race/Ethnicity"],
                    orientation="h", marker_color=color,
                    hovertemplate=f"{label}: %{{x:.1f}}%<extra></extra>",
                ))

    n_rows = sum([has_gender, has_race])
    fig.update_layout(
        barmode="stack",
        height=60 + n_rows * 50,
        margin=dict(l=115, r=10, t=5, b=5),
        showlegend=True,
        legend=dict(
            orientation="h", y=-0.55, font=dict(size=8),
            traceorder="normal", itemsizing="constant",
        ),
        xaxis=dict(range=[0, 100], ticksuffix="%", tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=9)),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def _render_student_body(school_row: pd.Series, name: str) -> None:
    """Student Body section: demographics chart + outcomes stat block, side by side."""
    st.markdown("---")
    st.markdown("**Student Body**")
    demo_col, outcomes_col = st.columns([1, 1])

    with demo_col:
        fig = _build_demographics_chart(school_row, name)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True, key=f"demo_{name}")
            st.caption(
                "Stacked horizontal bars showing the school's gender breakdown (top row) "
                "and race/ethnicity breakdown (bottom row) of undergraduate enrollment."
            )
        else:
            st.caption("Demographic breakdown not reported.")

        pell = _pct_val(school_row, "pct_pell")
        age25 = _pct_val(school_row, "pct_age_25_plus")
        if pell is not None:
            st.caption(f"Pell Grant recipients: {pell * 100:.0f}%")
        if age25 is not None:
            st.caption(f"Students age 25+: {age25 * 100:.0f}%")

    with outcomes_col:
        st.markdown("**Outcomes detail**")
        earn_6yr  = _pct_val(school_row, "median_earnings_6yr")
        earn_10yr = _pct_val(school_row, "median_earnings_10yr")
        above_hs  = _pct_val(school_row, "pct_earning_above_hs_median_10yr")
        repay     = _pct_val(school_row, "repayment_rate_3yr")
        default   = _pct_val(school_row, "default_rate_3yr")
        sample_n  = school_row.get("earnings_sample_size_10yr")

        rows: list[tuple[str, str]] = []
        if earn_6yr is not None:
            rows.append(("Median earnings (6yr)", f"${earn_6yr:,.0f}"))
        if earn_10yr is not None:
            rows.append(("Median earnings (10yr)", f"${earn_10yr:,.0f}"))
        if above_hs is not None:
            rows.append(("Earned more than HS-only graduates", f"{above_hs * 100:.0f}%"))
        if repay is not None:
            rows.append(("Borrowers repaying loans (3yr)", f"{repay * 100:.0f}%"))
        if default is not None:
            rows.append(("3-year default rate", f"{default * 100:.1f}%"))
        if pd.notna(sample_n):
            rows.append((f"Based on {int(sample_n):,} students", ""))

        if rows:
            for label, value in rows:
                if value:
                    c1, c2 = st.columns([3, 1])
                    c1.caption(label)
                    c2.caption(f"**{value}**")
                else:
                    st.caption(f"*{label}*")
        else:
            st.caption("Outcomes detail not reported.")


def _render_earnings_mobility(school_row: pd.Series, name: str) -> None:
    """Earnings Mobility section: 3-bar chart by family income tercile at entry."""
    st.markdown("---")
    st.markdown("**Earnings Mobility by Family Income**")

    low  = _pct_val(school_row, "mean_earnings_low_income_10yr")
    mid  = _pct_val(school_row, "mean_earnings_mid_income_10yr")
    high = _pct_val(school_row, "mean_earnings_high_income_10yr")

    if low is None and mid is None and high is None:
        st.markdown(
            "<div role='status' style='"
            "background:var(--secondary-background-color,#f0f0f0);"
            "padding:10px 14px;border-radius:4px;"
            "color:var(--text-color,#555);font-size:0.85em;'>"
            "Mobility data not reported for this school.</div>",
            unsafe_allow_html=True,
        )
        st.caption(
            "Earnings 10 years after entry, stratified by family income at college entry. "
            "Source: College Scorecard."
        )
        return

    income_groups = [
        ("Low Income (Q1)",  low,  config.PALETTE["mobility_low"]),
        ("Mid Income (Q2)",  mid,  config.PALETTE["mobility_mid"]),
        ("High Income (Q3)", high, config.PALETTE["mobility_high"]),
    ]

    fig = go.Figure()
    for label, val, color in income_groups:
        if val is not None:
            fig.add_trace(go.Bar(
                name=label, x=[label], y=[val],
                marker_color=color,
                text=[f"${val:,.0f}"],
                textposition="outside",
                hovertemplate=f"{label}: ${val:,.0f}<extra></extra>",
            ))

    fig.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        yaxis=dict(tickprefix="$", title="Mean earnings"),
        xaxis=dict(title=""),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True, key=f"mobility_{name}")
    st.caption(
        "Earnings 10 years after entry, stratified by family income at college entry. "
        "Source: College Scorecard."
    )


def _render_ci_bar(school_row: pd.Series, name: str) -> None:
    """
    Compact horizontal bar showing the 95% CI around the match score.
    Gracefully degrades to a caption-only display when CI is unavailable.
    """
    score  = school_row.get("match_score")
    lower  = school_row.get("match_score_lower")
    upper  = school_row.get("match_score_upper")
    margin = school_row.get("match_score_margin")
    n_rep  = school_row.get("n_dimensions_reported")
    n_tot  = school_row.get("n_dimensions_total")

    # No CI when all weights are 0 (neutral 50% mode) or data missing entirely
    if margin is None or pd.isna(margin):
        if pd.notna(score):
            st.caption(f"Match score: {float(score):.1f}  (No priorities set — CI not computed.)")
        return

    score_f  = float(score)
    lower_f  = float(lower)
    upper_f  = float(upper)

    fig = go.Figure()

    # Full-width background track
    fig.add_shape(type="rect", x0=0, x1=100, y0=0.3, y1=0.7,
                  fillcolor=config.PALETTE["ci_track_bg"], line=dict(width=0))

    # CI band (light blue fill)
    fig.add_shape(type="rect", x0=lower_f, x1=upper_f, y0=0.12, y1=0.88,
                  fillcolor=config.PALETTE["ci_band_fill"],
                  line=dict(color=config.PALETTE["ci_band_border"], width=1))

    # Point-estimate marker (solid vertical line)
    fig.add_shape(type="line", x0=score_f, x1=score_f, y0=0.02, y1=0.98,
                  line=dict(color=config.PALETTE["ci_point"], width=3))

    # Lower / upper numeric labels beside the CI band edges
    label_margin = 3  # minimum distance from edge before showing label
    if lower_f > label_margin:
        fig.add_annotation(x=lower_f, y=0.5, text=f"{lower_f:.1f}",
                           showarrow=False, xanchor="right", xshift=-4,
                           font=dict(size=9, color=config.PALETTE["ci_label_text"]))
    if upper_f < 100 - label_margin:
        fig.add_annotation(x=upper_f, y=0.5, text=f"{upper_f:.1f}",
                           showarrow=False, xanchor="left", xshift=4,
                           font=dict(size=9, color=config.PALETTE["ci_label_text"]))

    # Score label above the point-estimate marker
    fig.add_annotation(x=score_f, y=1.08, text=f"{score_f:.1f}",
                       showarrow=False, yanchor="bottom",
                       font=dict(size=11, color=config.PALETTE["ci_score_text"]))

    fig.update_layout(
        height=90,
        margin=dict(l=10, r=10, t=28, b=10),
        xaxis=dict(
            range=[0, 100],
            tickvals=[0, 25, 50, 75, 100],
            showgrid=True, gridcolor=config.PALETTE["gridline"],
            zeroline=False, tickfont=dict(size=9),
        ),
        yaxis=dict(visible=False, range=[0, 1.15]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key=f"ci_{name}")

    # Caption with coverage context
    _ci_prefix = (
        "Confidence interval band showing the school's match score and the range of plausible "
        "scores given data completeness. "
    )
    if pd.notna(n_rep) and pd.notna(n_tot):
        n_r, n_t = int(n_rep), int(n_tot)
        caption = (
            _ci_prefix
            + f"Match score: {score_f:.1f} "
            f"(95% CI: {lower_f:.1f} — {upper_f:.1f}). "
            f"Based on {n_r} of {n_t} weighted dimensions reported."
        )
        if n_r == n_t:
            caption += " (full data)"
        elif n_t > 0 and n_r < n_t / 2:
            caption += " (limited data — interpret with caution)"
    else:
        caption = (
            _ci_prefix
            + f"Match score: {score_f:.1f} "
            f"(95% CI: {lower_f:.1f} — {upper_f:.1f})."
        )
    st.caption(caption)


def _render_program_outcomes(school_row: pd.Series, name: str) -> None:
    """
    Phase 8 — Step 8.5. Render the school's program-level outcomes for the
    major currently selected on the Major Explorer tab. Three cases:

      Case 1: school does not offer the major at all
      Case 2: school offers the major but reports no values for it
      Case 3: at least one value is reported — render metric tiles
    """
    cip_code = st.session_state.get("selected_cip")
    if cip_code is None or cip_code == 0:
        return

    unit_id_val = school_row.get("unit_id")
    if pd.isna(unit_id_val):
        return

    fos_df = major_explorer.load_field_of_study()
    major_label = major_explorer.get_selected_major_label(fos_df, int(cip_code))
    if major_label is None:
        return

    program = major_explorer.get_school_program_outcomes(
        fos_df, int(unit_id_val), int(cip_code)
    )

    st.markdown(f"**Program-level outcomes — {major_label}**")

    # Case 1: school does not offer this major
    if program is None:
        st.caption(f"_{name} does not offer this major._")
        return

    # Case 2: offers but all four metrics are NaN (cohort below n=30)
    all_missing = all(pd.isna(v) for v in program.values())
    if all_missing:
        st.caption(
            f"_{name} offers this major, but the program's cohort size fell "
            "below the Scorecard's reporting threshold (n < 30)._"
        )
        return

    # Case 3: render metric tiles, em-dash for individual NaN values
    cols = st.columns(4)
    tiles = [
        ("median_earnings_1yr", "Earnings, 1yr"),
        ("median_earnings_4yr", "Earnings, 4yr"),
        ("median_earnings_5yr", "Earnings, 5yr"),
        ("median_debt",         "Median debt"),
    ]
    for col_widget, (col_name, label) in zip(cols, tiles):
        val = program[col_name]
        display = "—" if pd.isna(val) else f"${val:,.0f}"
        col_widget.metric(label, display)


def _render_programs_offered(school_row: pd.Series) -> None:
    """Phase 13.3. 'Programs offered' expander inside the school detail card.

    Lists all bachelor's-level programs at this school from the FoS dataset,
    sorted by median 1-year earnings. Each row has an Explore button that
    pre-selects that CIP in the Major Explorer tab.
    """
    unit_id_val = school_row.get("unit_id")
    if pd.isna(unit_id_val):
        return

    fos_df = major_explorer.load_field_of_study()
    programs_df = major_explorer.get_school_all_programs(fos_df, int(unit_id_val))
    n_programs = len(programs_df)

    if n_programs == 0:
        return

    st.markdown("---")
    with st.expander(f"All programs offered ({n_programs})", expanded=False):
        st.caption(
            "All bachelor's-level programs offered at this school, sorted by median earnings "
            "1 year after graduation. Click Explore to see major-level data including career "
            "paths, wages, and geographic concentration."
        )

        header_cols = st.columns([1, 4, 2, 2, 1])
        header_cols[0].markdown("**CIP**")
        header_cols[1].markdown("**Major**")
        header_cols[2].markdown("**Median earnings (1yr)**")
        header_cols[3].markdown("**Median debt**")
        header_cols[4].markdown("")

        unitid_int = int(unit_id_val)
        for _, row in programs_df.iterrows():
            cols = st.columns([1, 4, 2, 2, 1])
            cols[0].write(row["cip4"])
            cols[1].write(row["major_name"])
            cols[2].write(
                f"${row['median_earnings_1yr']:,.0f}"
                if pd.notna(row["median_earnings_1yr"]) else "—"
            )
            cols[3].write(
                f"${row['median_debt']:,.0f}"
                if pd.notna(row["median_debt"]) else "—"
            )
            cols[4].button(
                "Explore →",
                key=make_button_key("explore_program", unitid_int, row["cip4"]),
                on_click=major_explorer.set_major_explorer_cip,
                args=(row["cip4"],),
                help=f"Explore the {row['major_name']} major in Major Explorer",
            )


def render_detail_card(
    school_row: pd.Series,
    weights: dict,
    student_scores: dict,
    filtered_df: pd.DataFrame | None = None,
    scoring_pool: pd.DataFrame | None = None,
    income_bracket_column: str | None = None,
) -> None:
    """Render one bordered detail card for a single pinned school."""
    name = school_row.get("school_name", "Unknown school")

    # Compute acceptance badge (NEW in Step 4.2)
    school_sat_25, school_sat_75 = _school_sat_composite_range(school_row)
    acceptance_label = classify_acceptance(
        student_sat=student_scores.get("sat"),
        student_act=student_scores.get("act"),
        school_sat_25=school_sat_25,
        school_sat_75=school_sat_75,
    )
    acceptance_caption = _acceptance_explainer(
        acceptance_label, student_scores, school_sat_25, school_sat_75
    )

    with st.container(border=True):
        # Context badges: Carnegie type, test policy, MSI, religion
        _render_context_badges(school_row)

        # Header row: school name + acceptance badge + match score
        header_left, header_right = st.columns([4, 1])
        with header_left:
            location_bits = []
            if pd.notna(school_row.get("city")):
                location_bits.append(school_row["city"])
            if pd.notna(school_row.get("state")):
                location_bits.append(school_row["state"])
            location = ", ".join(location_bits) if location_bits else "Location unknown"

            meta_bits = []
            for col in ("control_label", "setting", "size_bucket"):
                val = school_row.get(col)
                if pd.notna(val):
                    meta_bits.append(str(val))
            meta = " · ".join(meta_bits) if meta_bits else ""

            # School name + inline badge
            st.markdown(f"#### {name}   **{format_acceptance_badge(acceptance_label)}**")
            st.caption(f"{location}" + (f"   |   {meta}" if meta else ""))
            st.caption(acceptance_caption)

        with header_right:
            if "match_score" in school_row.index and pd.notna(school_row["match_score"]):
                st.metric("Match", f"{school_row['match_score']:.0f}%")

        # "Why this rank?" explainer
        explainer = generate_explainer(school_row, weights, top_n_dimensions=2)
        st.markdown(f"> *{explainer}*")

        # Match score CI bar (Step C)
        _render_ci_bar(school_row, name)

        # Sensitivity caption (Step D)
        if filtered_df is not None and "unit_id" in school_row.index:
            unit_id_val = school_row["unit_id"]
            if pd.notna(unit_id_val):
                # Use the broader pool (filtered ∪ outside-filter pinned schools) so a school
                # the user pinned-but-outside-filters still gets a meaningful robustness number
                # instead of always reporting 0%. Falls back to filtered_df if scoring_pool
                # wasn't passed in (defensive).
                sens_pool = scoring_pool if scoring_pool is not None else filtered_df
                sensitivity = compute_sensitivity(
                    sens_pool,
                    weights,
                    school_unitid=unit_id_val,
                    top_n=10,
                    income_bracket_column=income_bracket_column,
                )
                pct = int(round(sensitivity["robustness"] * 100))
                tier = sensitivity["tier"]
                if tier == "robust":
                    st.success(
                        f"**Robust pick** — appears in the top 10 in **{pct}%** of nearby "
                        f"weight settings. Small changes in your priorities don't shake this one."
                    )
                elif tier == "borderline":
                    st.warning(
                        f"**Borderline** — drops in or out of the top 10 in nearby weight "
                        f"settings (in top 10 **{pct}%** of the time). Small priority changes matter here."
                    )
                elif tier == "volatile":
                    st.info(
                        f"**Volatile rank** — only stays in the top 10 in **{pct}%** of "
                        f"nearby weight settings. This school's position depends heavily on your exact weights."
                    )
                else:  # no_priorities
                    st.caption(
                        "_Sensitivity not computed — set at least one weight above 0 to see "
                        "how robust this school's rank is._"
                    )

        # Two columns: metrics grid on the left, radar chart on the right
        metrics_col, chart_col = st.columns([1, 1])

        with metrics_col:
            st.markdown("**Key metrics**")
            for i in range(0, len(CARD_METRIC_ROWS), 2):
                pair = CARD_METRIC_ROWS[i : i + 2]
                cols = st.columns(len(pair))
                for c, (col_name, label, formatter) in zip(cols, pair):
                    if col_name == "net_price" and "_selected_bracket_price" in school_row.index:
                        col_name, label = "_selected_bracket_price", "Net price (your bracket)"
                    c.metric(label, _fmt_or_dash(school_row, col_name, formatter))

        with chart_col:
            st.markdown("**Percentile profile**")
            fig = build_radar_chart(school_row)
            st.plotly_chart(fig, use_container_width=True, key=f"radar_{name}")
            st.caption(
                "Radar chart showing this school's percentile rank within the filtered population "
                "across the 7 scoring dimensions: affordability, graduation rate, retention rate, "
                "earnings, selectivity, low debt, and loan repayment. Higher values are better "
                "for all dimensions."
            )

        # Data completeness footer
        missing = []
        for col_name, label, _ in CARD_METRIC_ROWS:
            if col_name not in school_row.index or pd.isna(school_row[col_name]):
                missing.append(label)
        if missing:
            st.caption(
                f"ℹ️ Not reported: {', '.join(missing)}. "
                f"Missing metrics score at the neutral 50th percentile in the chart."
            )

        # New sections (Step A)
        _render_student_body(school_row, name)
        _render_earnings_mobility(school_row, name)

        # Phase 8 — Step 8.5: Program-level outcomes for the major
        # currently selected on the Major Explorer tab.
        _render_program_outcomes(school_row, name)

        # Phase 13.3 — All programs offered at this school
        _render_programs_offered(school_row)


def _build_pinned_scored_pool(
    pinned_names: list[str],
    filtered: pd.DataFrame,
    full_df: pd.DataFrame,
    weights: dict,
) -> tuple[pd.DataFrame, set[str]]:
    """
    Build a scored DataFrame containing all pinned schools, scoring them
    against the filtered population (plus themselves if outside the filters).
    Returns (scored_pool, outside_filter_names).

    Shared by render_comparison and render_pinned_cards so both views
    always show identical numbers.
    """
    pinned_rows = full_df[full_df["school_name"].isin(pinned_names)]
    missing_from_filtered = pinned_rows[
        ~pinned_rows["school_name"].isin(filtered["school_name"])
    ]
    scoring_pool = pd.concat([filtered, missing_from_filtered], ignore_index=True)
    scoring_pool = scoring_pool.drop_duplicates(subset=["school_name"], keep="first")

    scoring_pool = _apply_income_bracket_column(scoring_pool, st.session_state.get("selected_income_bracket", "Don't know / skip"))
    income_col = "_selected_bracket_price" if "_selected_bracket_price" in scoring_pool.columns else None
    scored_pool = compute_scores(scoring_pool, weights, income_bracket_column=income_col)
    outside_filter_names = set(missing_from_filtered["school_name"].tolist())
    return scored_pool, outside_filter_names


def render_pinned_cards(
    pinned_names: list[str],
    filtered: pd.DataFrame,
    full_df: pd.DataFrame,
    weights: dict,
    student_scores: dict,
) -> None:
    if not pinned_names:
        return

    st.markdown("## Pinned school details")

    scored_pool, outside_filter_names = _build_pinned_scored_pool(
        pinned_names, filtered, full_df, weights
    )

    for name in pinned_names:
        matches = scored_pool[scored_pool["school_name"] == name]
        if matches.empty:
            st.warning(f"Couldn't find data for {name}.")
            continue
        school_row = matches.iloc[0]
        if name in outside_filter_names:
            st.caption(f"🔎 *{name} is outside your current filters but still scored against the filtered population.*")
        income_col = "_selected_bracket_price" if "_selected_bracket_price" in scored_pool.columns else None
        render_detail_card(
            school_row, weights, student_scores,
            filtered_df=filtered,
            scoring_pool=scored_pool,
            income_bracket_column=income_col,
        )


# ============================================================
# MAP VIEW (Step 5.4)
# ============================================================

@st.cache_data(show_spinner=False)
def _build_map_figure(
    ranked: pd.DataFrame,
    filtered_states: list[str],
) -> tuple[go.Figure | None, int, bool]:
    """
    Build a Plotly scattermapbox figure of ranked schools, color-coded by
    match score on an RdYlGn scale.

    Parameters
    ----------
    ranked          : the ranked DataFrame (post-filter)
    filtered_states : the user's state-filter selection. Empty list means
                      no filter; in that case the map defaults to a
                      hardcoded continental-US view rather than computing
                      the centroid (which gets thrown off by AK/HI/PR).

    Returns
    -------
    (fig, n_excluded_missing_coords, was_capped)
        fig                          : the figure, or None if nothing renderable
        n_excluded_missing_coords    : how many ranked schools had no lat/lng
        was_capped                   : True if MAP_MAX_MARKERS truncation kicked in
    """
    if ranked.empty:
        return None, 0, False

    # Drop schools without coordinates — can't plot them.
    has_coords = ranked["latitude"].notna() & ranked["longitude"].notna()
    n_excluded = int((~has_coords).sum())
    plot_df = ranked[has_coords].copy()

    if plot_df.empty:
        return None, n_excluded, False

    # Defensive cap — keep the highest-scoring N if oversized
    was_capped = False
    if len(plot_df) > MAP_MAX_MARKERS:
        plot_df = plot_df.nlargest(MAP_MAX_MARKERS, "match_score")
        was_capped = True

    # Hover text — use a separate column for clean Plotly hovertemplate refs
    def _fmt_dollars(v):
        return f"${v:,.0f}" if pd.notna(v) else "—"
    def _fmt_pct(v):
        return f"{v:.0f}%" if pd.notna(v) else "—"

    plot_df["_hover_loc"] = plot_df.apply(
        lambda r: f"{r['city']}, {r['state']}"
                  if pd.notna(r.get("city")) and pd.notna(r.get("state"))
                  else (r.get("state") if pd.notna(r.get("state")) else ""),
        axis=1,
    )
    _np_col, _ = _net_price_column_and_label(plot_df)
    plot_df["_hover_netprice"] = plot_df[_np_col].apply(_fmt_dollars)
    plot_df["_hover_gradrate"] = plot_df["graduation_rate"].apply(_fmt_pct)

    # Build the map with two traces:
    #   1. Black outline ring (drawn first, so colored markers render on top).
    #      Slightly larger size + solid black + skip hover so it acts as
    #      a pure visibility outline.
    #   2. Colored markers carrying the RdYlGn match-score encoding and the
    #      hover tooltip.
    # Scattermapbox lacks marker.line support, so this two-trace pattern
    # is the canonical Plotly workaround.
    outline_trace = go.Scattermapbox(
        lat=plot_df["latitude"],
        lon=plot_df["longitude"],
        mode="markers",
        marker=dict(
            size=MAP_MARKER_SIZE + 3,
            color=config.PALETTE["map_marker_border"],
            opacity=1.0,
        ),
        hoverinfo="skip",
        showlegend=False,
    )

    colored_trace = go.Scattermapbox(
        lat=plot_df["latitude"],
        lon=plot_df["longitude"],
        mode="markers",
        marker=dict(
            size=MAP_MARKER_SIZE,
            color=plot_df["match_score"],
            colorscale=config.PALETTE["map_score_scale"],
            cmin=0,
            cmax=100,
            colorbar=dict(
                title="Match",
                thickness=12,
                len=0.6,
                tickvals=[0, 25, 50, 75, 100],
            ),
            opacity=0.95,
        ),
        customdata=plot_df[[
            "school_name", "_hover_loc", "match_score",
            "_hover_netprice", "_hover_gradrate",
        ]].to_numpy(),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "%{customdata[1]}<br>"
            "Match score: %{customdata[2]:.1f}<br>"
            "Net price: %{customdata[3]}<br>"
            "Grad rate: %{customdata[4]}"
            "<extra></extra>"
        ),
        showlegend=False,
    )

    fig = go.Figure(data=[outline_trace, colored_trace])

    # Centering: hardcoded continental-US view when no state filter is
    # active (avoids centroid drift from AK/HI/PR outliers). When a state
    # filter IS active, derive center + zoom from the data extent.
    if not filtered_states:
        center_lat = MAP_DEFAULT_CENTER_LAT
        center_lon = MAP_DEFAULT_CENTER_LON
        zoom = MAP_DEFAULT_ZOOM
    else:
        lat_min, lat_max = plot_df["latitude"].min(), plot_df["latitude"].max()
        lon_min, lon_max = plot_df["longitude"].min(), plot_df["longitude"].max()
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2

        # Heuristic zoom from the lat/lng span — Plotly mapbox doesn't have
        # a built-in fitBounds, so we approximate. Larger spans → smaller zoom.
        lat_span = max(lat_max - lat_min, 0.5)
        lon_span = max(lon_max - lon_min, 0.5)
        span = max(lat_span, lon_span)
        # Empirically tuned: span ~20 (large state) → zoom 4; span ~3 (small state) → zoom 6
        if span >= 20:
            zoom = 4
        elif span >= 8:
            zoom = 5
        elif span >= 3:
            zoom = 6
        elif span >= 1:
            zoom = 7
        else:
            zoom = 8

    fig.update_layout(
        mapbox=dict(
            style=MAP_DEFAULT_STYLE,
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom,
        ),
        height=MAP_HEIGHT_PX,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )

    return fig, n_excluded, was_capped


def render_map(ranked: pd.DataFrame, filtered_states: list[str]) -> None:
    """
    Geographic map of ranked schools, color-coded by match score.
    Renders inside a collapsible expander above the comparison view.
    """
    n_total = len(ranked)

    if n_total == 0:
        title = "🗺️ Map of matching schools"
    else:
        title = f"🗺️ Map of matching schools ({n_total:,} schools)"

    with st.expander(title, expanded=False):
        if n_total == 0:
            st.info("No schools match the current filters — nothing to map.")
            return

        fig, n_excluded, was_capped = _build_map_figure(ranked, filtered_states)

        if fig is None:
            st.info(
                "None of the matching schools have published coordinates — "
                "nothing to plot. Try loosening your filters."
            )
            return

        st.plotly_chart(fig, use_container_width=True, key="schools_map")

        # Footer captions — only render the ones that apply
        caption_bits = []
        caption_bits.append(
            "Each dot is one school, colored by match score "
            "(red = low match, green = high match)."
        )
        if was_capped:
            caption_bits.append(
                f"⚠️ Showing the top {MAP_MAX_MARKERS:,} schools by match score "
                f"(of {n_total:,} matching). Rendering all of them slows the map."
            )
        if n_excluded > 0:
            caption_bits.append(
                f"ℹ️ {n_excluded:,} school(s) excluded — no published coordinates."
            )
        st.caption("  ".join(caption_bits))


# ============================================================
# COMPARISON VIEW (Step 5.1)
# ============================================================

def _rank_emojis_for_row(
    raw_values: list,
    direction: str,
) -> list[str]:
    """
    Return one emoji per value indicating where it ranks within the row.

    🟢 = best (or tied for best)
    🔴 = worst (or tied for worst)
    🟡 = neither (only with 3+ schools)
    ""  = missing value

    direction: "higher_better" or "lower_better".
    """
    reported = [v for v in raw_values if v is not None and not (isinstance(v, float) and pd.isna(v))]
    if not reported:
        return ["" for _ in raw_values]

    best = (max if direction == "higher_better" else min)(reported)
    worst = (min if direction == "higher_better" else max)(reported)

    emojis = []
    for v in raw_values:
        if v is None or (isinstance(v, float) and pd.isna(v)):
            emojis.append("")
        elif best == worst:
            emojis.append("🟢")  # all tied
        elif v == best:
            emojis.append("🟢")
        elif v == worst:
            emojis.append("🔴")
        else:
            emojis.append("🟡")
    return emojis


def _build_comparison_table(
    school_rows: list[pd.Series],
    student_scores: dict,
) -> pd.DataFrame:
    """
    Build the side-by-side comparison DataFrame.

    Schools are columns (pin order), metrics are rows. Cells show raw
    values with units, prepended by a rank emoji (🟢/🟡/🔴) for
    direction-aware metrics. Acceptance keeps its own Safety/Match/Reach badge.
    """
    column_order = [row["school_name"] for row in school_rows]
    table_data: dict[str, dict[str, str]] = {name: {} for name in column_order}

    # Match score row (higher is better)
    match_raw = [
        float(row.get("match_score")) if pd.notna(row.get("match_score")) else None
        for row in school_rows
    ]
    match_emojis = _rank_emojis_for_row(match_raw, "higher_better")
    for name, score, emoji in zip(column_order, match_raw, match_emojis):
        if score is None:
            table_data[name]["Match score"] = "—"
        else:
            prefix = f"{emoji} " if emoji else ""
            table_data[name]["Match score"] = f"{prefix}{score:.1f}"

    # Acceptance row (existing badge; no additional rank emoji)
    for name, row in zip(column_order, school_rows):
        sat_25, sat_75 = _school_sat_composite_range(row)
        label = classify_acceptance(
            student_sat=student_scores.get("sat"),
            student_act=student_scores.get("act"),
            school_sat_25=sat_25,
            school_sat_75=sat_75,
        )
        table_data[name]["Acceptance"] = format_acceptance_badge(label)

    # Scoring dimension rows — raw values with units + rank emoji
    for dim_key, spec in config.SCORING_DIMENSIONS.items():
        label = spec["label"]
        col = spec["column"]
        if col == "net_price" and school_rows and "_selected_bracket_price" in school_rows[0].index:
            col = "_selected_bracket_price"
        direction = spec["direction"]
        formatter = COMPARISON_RAW_FORMATTERS.get(dim_key, str)

        raw_values: list = []
        for row in school_rows:
            v = row.get(col)
            raw_values.append(float(v) if v is not None and not pd.isna(v) else None)

        emojis = _rank_emojis_for_row(raw_values, direction)
        for name, raw, emoji in zip(column_order, raw_values, emojis):
            if raw is None:
                table_data[name][label] = "—"
            else:
                prefix = f"{emoji} " if emoji else ""
                try:
                    table_data[name][label] = f"{prefix}{formatter(raw)}"
                except (TypeError, ValueError):
                    table_data[name][label] = "—"

    df = pd.DataFrame(table_data)[column_order]
    df.index.name = "Metric"
    return df


def _build_comparison_chart(school_rows: list[pd.Series]) -> go.Figure:
    """
    Grouped bar chart: one group per scoring dimension, one bar per school.
    Bars show percentile ranks (0–100). Wong 2011 palette for accessibility.
    """
    palette = config.PALETTE["comparison"]

    dims = list(config.SCORING_DIMENSIONS.keys())
    labels = [config.SCORING_DIMENSIONS[k]["label"] for k in dims]

    fig = go.Figure()
    for i, school_row in enumerate(school_rows):
        name = school_row.get("school_name", f"School {i + 1}")
        values = []
        for key in dims:
            col = f"score_{key}"
            if col in school_row.index and pd.notna(school_row[col]):
                values.append(float(school_row[col]) * 100)
            else:
                values.append(0.0)
        fig.add_trace(go.Bar(
            name=name,
            x=labels,
            y=values,
            marker_color=palette[i % len(palette)],
            hovertemplate=f"<b>{name}</b><br>%{{x}}: %{{y:.0f}}th percentile<extra></extra>",
        ))

    fig.update_layout(
        barmode="group",
        height=380,
        margin=dict(l=20, r=20, t=20, b=80),
        yaxis=dict(
            range=[0, 100],
            title="Percentile rank",
            gridcolor=config.PALETTE["gridline"],
        ),
        xaxis=dict(tickangle=-25, tickfont=dict(size=10)),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.45,
            xanchor="center", x=0.5,
            font=dict(size=10),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def render_comparison(
    pinned_names: list[str],
    filtered: pd.DataFrame,
    full_df: pd.DataFrame,
    weights: dict,
    student_scores: dict,
) -> None:
    """Side-by-side comparison view for 2–4 pinned schools."""
    n_pinned = len(pinned_names)

    if n_pinned == 0:
        title = "📊 Compare pinned schools (2–4)"
    else:
        title = f"📊 Compare pinned schools ({n_pinned} pinned)"

    with st.expander(title, expanded=False):

        if n_pinned < 2:
            st.info(
                "Pin **2 to 4 schools** above to compare them side by side. "
                f"You currently have {n_pinned} pinned."
            )
            return

        if n_pinned > config.MAX_COMPARE_SCHOOLS:
            st.warning(
                f"Comparison is limited to {config.MAX_COMPARE_SCHOOLS} schools. "
                f"Showing the first {config.MAX_COMPARE_SCHOOLS} of your "
                f"{n_pinned} pinned schools (in pin order)."
            )
            compare_names = pinned_names[: config.MAX_COMPARE_SCHOOLS]
        else:
            compare_names = list(pinned_names)

        scored_pool, outside_filter_names = _build_pinned_scored_pool(
            compare_names, filtered, full_df, weights
        )

        school_rows: list[pd.Series] = []
        missing_names: list[str] = []
        for name in compare_names:
            matches = scored_pool[scored_pool["school_name"] == name]
            if matches.empty:
                missing_names.append(name)
                continue
            school_rows.append(matches.iloc[0])

        if missing_names:
            st.caption(
                f"⚠️ Couldn't find data for: {', '.join(missing_names)}. "
                f"Skipped from the comparison."
            )

        if len(school_rows) < 2:
            st.info("Need at least 2 schools with available data to compare.")
            return

        outside_in_compare = [n for n in compare_names if n in outside_filter_names]
        if outside_in_compare:
            st.caption(
                "🔎 *Outside current filters but still scored against the filtered population: "
                f"{', '.join(outside_in_compare)}.*"
            )

        # Side-by-side table
        st.markdown("**Side-by-side metrics**")
        compare_df = _build_comparison_table(school_rows, student_scores)
        st.dataframe(compare_df, use_container_width=True)
        st.caption(
            "🟢 = best in row · 🟡 = middle · 🔴 = worst in row. "
            "Direction is metric-aware (lower net price wins, higher earnings win). "
            "Ties are both marked 🟢 (or both 🔴). Missing values show as —."
        )

        # Grouped bar chart
        st.markdown("**Percentile profile by dimension**")
        fig = _build_comparison_chart(school_rows)
        st.plotly_chart(fig, use_container_width=True, key="comparison_chart")

        st.caption(
            "Bar heights are **percentile ranks** within the filtered population "
            "(0 = worst, 100 = best) — useful for cross-dimension comparison. "
            "The table above shows the underlying raw values. "
            "Missing metrics show as 0 in the chart to make missing data visually obvious."
        )


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    # Parse URL params first so widgets pick up the values on their first render
    _parse_url_into_session_state()
    init_session_state()

    df = load_colleges()

    if df["graduation_rate"].max() <= 1.0:
        df["graduation_rate"] = df["graduation_rate"] * 100
    if df["admission_rate"].max() <= 1.0:
        df["admission_rate"] = df["admission_rate"] * 100

    filter_selections, weights, student_scores = render_sidebar(df)

    # Apply the small-schools enrollment floor before all other filters.
    # show_small_schools and cip_filter are popped so they don't reach apply_filters.
    show_small_schools = filter_selections.pop("show_small_schools")
    cip_filter = filter_selections.pop("cip_filter", "All majors")
    base_df = df if show_small_schools else df[df["enrollment"] >= config.MIN_ENROLLMENT_DEFAULT]

    filtered = apply_filters(base_df, **filter_selections)
    # Phase 13.2 — CIP filter: restrict pool to schools offering the selected major.
    fos_df_for_filter = major_explorer.load_field_of_study()
    filtered = school_finder.apply_cip_filter(filtered, cip_filter, fos_df_for_filter)
    filtered = _apply_income_bracket_column(filtered, st.session_state.get("selected_income_bracket", "Don't know / skip"))
    income_col = "_selected_bracket_price" if "_selected_bracket_price" in filtered.columns else None
    ranked = compute_scores(filtered, weights, income_bracket_column=income_col)

    school_finder_tab, major_explorer_tab, find_your_fit_tab = st.tabs(["School Finder", "Major Explorer", "Find Your Fit"])

    # Phase 13.4a — URL tab hint banner. Shown once when a shared URL includes
    # ?tab=<non-default>, since st.tabs() can't be programmatically switched.
    _banner_tab = st.session_state.pop("_url_tab_banner", None)
    if _banner_tab:
        _tab_label = {
            "major_explorer": "Major Explorer",
            "find_your_fit": "Find Your Fit",
        }.get(_banner_tab, _banner_tab)
        st.info(f"📌 This URL is set up for the **{_tab_label}** tab — click the tab above to continue.")

    with school_finder_tab:
        st.title("Results")

        # Phase 13.2 — cross-tab banner: shown once after Major Explorer handoff.
        _xtab_cip = st.session_state.pop("_last_xtab_cip_filter", None)
        if _xtab_cip is not None:
            st.success(
                f"📌 School Finder pre-filtered to **{_cip_filter_label(_xtab_cip)}** — "
                "ranking updated below. Change the major in the sidebar to explore others."
            )

        render_summary_banner(ranked, filter_selections, weights)

        render_export_row(ranked, filter_selections, weights, student_scores)

        pinned_names = render_pin_selector(base_df)

        render_results(ranked)

        render_map(ranked, filter_selections["states"])

        render_comparison(pinned_names, filtered, base_df, weights, student_scores)

        render_pinned_cards(pinned_names, filtered, base_df, weights, student_scores)

        st.caption(
            f"Data through {about_the_data.OLDEST_DATE}, with some sources updated as recently as "
            f"{about_the_data.NEWEST_DATE}. See About the Data for per-source dates."
        )
        about_the_data.render_about_the_data()

    with major_explorer_tab:
        major_explorer.render()

    with find_your_fit_tab:
        find_your_fit.render()

    # Sync current state back to URL so it stays shareable after every interaction
    _write_session_state_to_url()


if __name__ == "__main__":
    main()
