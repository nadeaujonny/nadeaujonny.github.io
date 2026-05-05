"""
config.py — Central configuration for College Match Finder.

All constants, column mappings, category labels, and scoring dimension
definitions live here. Every other module imports from this file so that
renaming a source column or adjusting a scoring direction only requires a
change in one place.

Field name references are based on the College Scorecard Institution-Level
Data Documentation (U.S. Department of Education). The raw files use cryptic
uppercase names (e.g. ADM_RATE, MD_EARN_WNE_P10); we rename them on load to
the snake_case names used throughout the app.
"""

from pathlib import Path

# ============================================================
# PATHS
# ============================================================
PROJECT_ROOT = Path(__file__).parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"

# Raw input files (user places these in data/raw/)
RAW_SCORECARD_CURRENT = "Most-Recent-Cohorts-Institution.csv"
RAW_SCORECARD_FIELD_OF_STUDY = "Most-Recent-Cohorts-Field-of-Study.csv"

# ----- Scope-cut (April 2026) -----
# Historical Scorecard snapshots, Clery Act safety data, and the ZIP→lat/lng
# lookup were originally planned for Phase 4 (trend arrows, safety scoring,
# distance filtering). All three were cut from scope after the ED bulk-data
# host moved and the interactive Clery download proved impractical to
# automate. The app uses six scoring dimensions instead of seven, and
# geographic filtering is handled via the existing state multiselect.
# These constants are retained (commented out) so that reviving the features
# later requires only uncommenting and re-running data_prep.py.
#
# RAW_SCORECARD_TREND_1 = "MERGED2019_20_PP.csv"
# RAW_SCORECARD_TREND_2 = "MERGED2021_22_PP.csv"
# RAW_CLERY_CRIME = "Criminal_Offenses_On_campus.csv"
# RAW_CLERY_VAWA = "VAWA_Offenses_On_campus.csv"
# RAW_ZIP_LATLONG = "zip_lat_long.csv"

# Cleaned output files (produced by data_prep.py, consumed by app.py)
CLEANED_COLLEGES = "colleges_cleaned.csv"
CLEANED_FIELD_OF_STUDY = "field_of_study_cleaned.csv"
# CLEANED_CAMPUS_SAFETY = "campus_safety_cleaned.csv"   # scope-cut
# CLEANED_TRENDS = "trends.csv"                         # scope-cut
# CLEANED_ZIP_LATLONG = "zip_lat_long_cleaned.csv"      # scope-cut


# ============================================================
# COLUMN RENAMING — raw Scorecard name → clean snake_case name
# ============================================================
SCORECARD_COLUMN_RENAMES = {
    # Identifiers
    "UNITID": "unit_id",
    "OPEID": "ope_id",
    "INSTNM": "school_name",
    "CITY": "city",
    "STABBR": "state",
    "ZIP": "zip_code",
    "LATITUDE": "latitude",
    "LONGITUDE": "longitude",

    # Institution profile
    "CONTROL": "control",                   # 1=public, 2=private nonprofit, 3=private for-profit
    "LOCALE": "locale",                     # campus setting (11–43)
    "UGDS": "enrollment",                   # undergraduate enrollment
    "ICLEVEL": "institution_level",         # 1=4yr, 2=2yr, 3=<2yr
    "PREDDEG": "predominant_degree",
    "HIGHDEG": "highest_degree",
    "CCBASIC": "carnegie_basic",

    # Admissions
    "ADM_RATE": "admission_rate",
    "SAT_AVG": "sat_avg",
    "ACTCMMID": "act_median",
    "SATVR25": "sat_verbal_25",
    "SATVR75": "sat_verbal_75",
    "SATMT25": "sat_math_25",
    "SATMT75": "sat_math_75",

    # Cost
    "TUITIONFEE_IN": "tuition_in_state",
    "TUITIONFEE_OUT": "tuition_out_of_state",
    "NPT4_PUB": "net_price_public",
    "NPT4_PRIV": "net_price_private",
    # Net price by income bracket (Title IV, public)
    "NPT41_PUB": "net_price_public_0_30k",
    "NPT42_PUB": "net_price_public_30_48k",
    "NPT43_PUB": "net_price_public_48_75k",
    "NPT44_PUB": "net_price_public_75_110k",
    "NPT45_PUB": "net_price_public_110k_plus",
    # Net price by income bracket (Title IV, private)
    "NPT41_PRIV": "net_price_private_0_30k",
    "NPT42_PRIV": "net_price_private_30_48k",
    "NPT43_PRIV": "net_price_private_48_75k",
    "NPT44_PRIV": "net_price_private_75_110k",
    "NPT45_PRIV": "net_price_private_110k_plus",

    # Outcomes
    "C150_4": "graduation_rate_4yr",
    "C150_L4": "graduation_rate_less_4yr",
    "C100_4": "completion_100pct_4yr",
    "RET_FT4": "retention_rate_4yr",
    "RET_FTL4": "retention_rate_less_4yr",

    # Earnings — 10 years after entry, working and not enrolled
    "MD_EARN_WNE_P10": "median_earnings_10yr",
    "MN_EARN_WNE_P10": "mean_earnings_10yr",
    "MD_EARN_WNE_P6": "median_earnings_6yr",

    # Debt
    "GRAD_DEBT_MDN": "median_debt",
    "GRAD_DEBT_MDN_SUPP": "median_debt_supp",

    # Program flags (used for major filters)
    "CIPCODE": "cip_code",
    "CIPDESC": "cip_description",

    # Demographics
    "UGDS_WOMEN":           "pct_women",
    "UGDS_BLACK":           "pct_black",
    "UGDS_HISP":            "pct_hispanic",
    "UGDS_ASIAN":           "pct_asian",
    "UGDS_WHITE":           "pct_white",
    "UGDS_NRA":             "pct_nonresident",
    "PCTPELL":              "pct_pell",
    "PCTFLOAN":             "pct_federal_loan",
    "UG25ABV":              "pct_age_25_plus",
    "PPTUG_EF":             "pct_part_time",

    # Outcomes (additions — MD_EARN_WNE_P6 already mapped above)
    "COUNT_WNE_P10":        "earnings_sample_size_10yr",
    "GT_25K_P10":           "pct_earning_above_25k_10yr",
    "GT_THRESHOLD_P10":     "pct_earning_above_hs_median_10yr",
    "RPY_3YR_RT":           "repayment_rate_3yr",
    "CDR3":                 "default_rate_3yr",

    # Earnings mobility — mean earnings by family income tercile at entry
    "MN_EARN_WNE_INC1_P10": "mean_earnings_low_income_10yr",
    "MN_EARN_WNE_INC2_P10": "mean_earnings_mid_income_10yr",
    "MN_EARN_WNE_INC3_P10": "mean_earnings_high_income_10yr",

    # Faculty / instruction
    "INEXPFTE":             "instruction_spend_per_fte",
    "AVGFACSAL":            "avg_faculty_salary",
    "PFTFAC":               "pct_full_time_faculty",
    "TUITFTE":              "net_tuition_per_fte",

    # Selectivity nuance
    "ADMCON7":              "test_score_policy",

    # Mission flags (0/1 indicators)
    "HBCU":                 "is_hbcu",
    "PBI":                  "is_pbi",
    "HSI":                  "is_hsi",
    "AANAPII":              "is_aanapii",
    "ANNHI":                "is_annhi",
    "TRIBAL":               "is_tribal",
    "NANTI":                "is_nanti",
    "RELAFFIL":             "religious_affiliation",
}


# ============================================================
# CATEGORY LOOKUPS
# ============================================================
# CONTROL (institutional control)
CONTROL_LABELS = {
    1: "Public",
    2: "Private nonprofit",
    3: "Private for-profit",
}

# LOCALE (campus setting) → grouped into plain-English categories
LOCALE_TO_SETTING = {
    11: "City",       12: "City",       13: "City",
    21: "Suburb",     22: "Suburb",     23: "Suburb",
    31: "Town",       32: "Town",       33: "Town",
    41: "Rural",      42: "Rural",      43: "Rural",
}
SETTING_OPTIONS = ["City", "Suburb", "Town", "Rural"]

# School size buckets (by undergraduate enrollment)
SIZE_BUCKETS = [
    ("Very small (< 1,000)", 0, 1_000),
    ("Small (1,000–2,999)", 1_000, 3_000),
    ("Medium (3,000–9,999)", 3_000, 10_000),
    ("Large (10,000–19,999)", 10_000, 20_000),
    ("Very large (20,000+)", 20_000, float("inf")),
]


def enrollment_to_size(n):
    """Map an enrollment count to a size bucket label."""
    if n is None or (isinstance(n, float) and n != n):  # NaN
        return None
    for label, lo, hi in SIZE_BUCKETS:
        if lo <= n < hi:
            return label
    return None


# ============================================================
# U.S. STATES (for the state filter)
# ============================================================
US_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC", "PR",
]


# ============================================================
# INCOME BRACKETS (for conditional net-price scoring)
# ============================================================
INCOME_BRACKETS = {
    "$0–$30,000":      ("net_price_public_0_30k",      "net_price_private_0_30k"),
    "$30,001–$48,000": ("net_price_public_30_48k",     "net_price_private_30_48k"),
    "$48,001–$75,000": ("net_price_public_48_75k",     "net_price_private_48_75k"),
    "$75,001–$110,000":("net_price_public_75_110k",    "net_price_private_75_110k"),
    "$110,001+":       ("net_price_public_110k_plus",  "net_price_private_110k_plus"),
    "Don't know / skip": (None, None),   # falls back to net_price (overall)
}


# ============================================================
# TEST SCORE POLICY LABELS (ADMCON7)
# ============================================================
ADMCON7_LABELS = {
    1: "Required",
    2: "Recommended",
    3: "Not Required",
    4: "Unknown",
    5: "Considered",
}


# ============================================================
# CARNEGIE BASIC CLASSIFICATION LABELS (CCBASIC)
# ============================================================
CARNEGIE_BASIC_LABELS = {
    -2: "Unknown",
    -1: "Not Classified",
    15: "Doctoral — Very High Research",
    16: "Doctoral — High Research",
    17: "Doctoral/Professional",
    18: "Master's — Larger Programs",
    19: "Master's — Medium Programs",
    20: "Master's — Small Programs",
    21: "Bacc — Arts & Sciences",
    22: "Bacc — Diverse Fields",
    23: "Bacc/Associate's",
    24: "Special Focus — Faith-Related",
    25: "Special Focus — Medical",
    26: "Special Focus — Health Professions",
    27: "Special Focus — Engineering",
    28: "Special Focus — Technology",
    29: "Special Focus — Business",
    30: "Special Focus — Arts & Design",
    31: "Special Focus — Law",
    32: "Special Focus — Other",
    33: "Tribal Colleges",
}


# ============================================================
# RELIGIOUS AFFILIATION LABELS (RELAFFIL)
# ============================================================
# -2 / null → "None" (secular or not applicable)
# Everything not listed → "Other religious"
RELIGIOUS_AFFIL_LABELS = {
    -2: "None",
    -1: "None",
    22: "Roman Catholic",
    24: "Baptist",
    27: "Lutheran",
    28: "Presbyterian",
    30: "Episcopal",
    33: "Methodist",
    37: "Jewish",
    42: "Seventh-day Adventist",
    43: "Church of Christ",
    52: "Nondenominational Christian",
    57: "Latter-day Saints",
    60: "Islamic",
    66: "Mennonite",
    71: "United Church of Christ",
    76: "Assemblies of God",
    80: "Christian Reformed",
    91: "Jesuit",
    97: "Other religious",
}


# ============================================================
# SCORING DIMENSIONS
# ============================================================
# Each dimension defines:
#   label:       display name shown in the UI
#   column:      the metric column in the cleaned data
#   direction:   "higher_better" or "lower_better"
#   description: shown in tooltips / explainers
#
# Scope note (April 2026): originally defined seven dimensions; the
# "safety" dimension was removed along with the Clery Act data pipeline
# (see top of file). Step B re-introduced a 7th dimension using the
# repayment_rate_3yr column extracted in Step A.
SCORING_DIMENSIONS = {
    "affordability": {
        "label": "Low Net Price",
        "column": "net_price",            # default; overridden if income bracket selected
        "direction": "lower_better",
        "description": "Average net price paid after grants and scholarships.",
    },
    "graduation_rate": {
        "label": "High Graduation Rate",
        "column": "graduation_rate",
        "direction": "higher_better",
        "description": "Share of first-time, full-time students who graduate within 150% of normal time.",
    },
    "retention_rate": {
        "label": "High Retention Rate",
        "column": "retention_rate_4yr",
        "direction": "higher_better",
        "description": "Share of first-time, full-time students who return for their second year.",
    },
    "earnings": {
        "label": "High Earnings After Graduation",
        "column": "median_earnings_10yr",
        "direction": "higher_better",
        "description": "Median earnings 10 years after entry, working and not enrolled.",
    },
    "selectivity": {
        "label": "High Selectivity",
        "column": "admission_rate",
        "direction": "lower_better",
        "description": "Admission rate — lower means more selective.",
    },
    "low_debt": {
        "label": "Low Student Debt",
        "column": "median_debt",
        "direction": "lower_better",
        "description": "Median federal loan debt of students who completed a degree.",
    },
    "repayment": {
        "label": "High Loan Repayment Rate",
        "column": "repayment_rate_3yr",
        "direction": "higher_better",
        "description": (
            "Share of borrowers who have paid down at least $1 of principal "
            "3 years after entering repayment. Higher is better — indicates "
            "graduates can manage their debt."
        ),
    },
    # "safety" dimension removed — see scope note above.
}


# ============================================================
# ACCEPTANCE LIKELIHOOD CLASSIFICATION
# ============================================================
# Given a student's SAT (or ACT-to-SAT-equivalent) score and a school's
# 25th/75th percentile SAT range, classify the school as Safety / Match / Reach.
ACCEPTANCE_LABELS = {
    "safety": "Safety",
    "match": "Match",
    "reach": "Reach",
    "unknown": "N/A",
}

# Simple ACT-to-SAT concordance (approximate; based on College Board tables)
ACT_TO_SAT = {
    36: 1590, 35: 1540, 34: 1500, 33: 1460, 32: 1430, 31: 1400,
    30: 1370, 29: 1340, 28: 1310, 27: 1280, 26: 1240, 25: 1210,
    24: 1180, 23: 1140, 22: 1110, 21: 1080, 20: 1040, 19: 1010,
    18:  970, 17:  930, 16:  890, 15:  850, 14:  800, 13:  760,
    12:  710, 11:  670, 10:  630,  9:  590,
}


# ============================================================
# DATA PREP FILTERS
# ============================================================
# Minimum undergraduate enrollment for an institution to be included in the
# cleaned dataset. Set during Phase 4 after observing that schools below this
# threshold produce noisy metrics (retention, graduation, earnings become
# highly sensitive to small-cohort effects) and dominated the top of
# retention-sorted lists with tiny institutions not comparable to the
# flagship universities users are typically evaluating. Applied in
# data_prep.py's clean_institutions step.
MIN_ENROLLMENT = 250           # kept for backward compatibility
MIN_ENROLLMENT_DEFAULT = 250   # runtime floor when "Show small schools" toggle is OFF
MIN_ENROLLMENT_FLOOR = 0       # no floor when toggle is ON


# ============================================================
# DISPLAY / UI
# ============================================================
DEFAULT_MAX_RESULTS = 50
MAX_COMPARE_SCHOOLS = 4

# DEFAULT_DISTANCE_RADIUS_MI = 100   # scope-cut (distance filter removed)


# ============================================================
# PHASE 10 — MAJOR EXPLORER GEOGRAPHIC CONCENTRATION
# ============================================================
# Phase 10.4 — Choropleth color-scale cap
# LQ values are uncapped in the data; only the color-scale z-array is clamped.
# Hover tooltips show original uncapped values.
LQ_CAP_FOR_CHOROPLETH = 5.0


# ============================================================
# RIASEC DIMENSIONS (Holland Code ordering)
# ============================================================
RIASEC_DIMENSIONS: tuple[str, ...] = ("R", "I", "A", "S", "E", "C")


# ============================================================
# PALETTE — centralized color decisions for charts, badges, PDF
# ============================================================
# Wong (2011) colorblind-safe categorical palette + chart-specific tokens.
# All chart code imports from here rather than using inline hex literals.
# Changes here cascade to every chart in the app.  To change one chart's
# color without affecting others, add a new token rather than editing an
# existing one.

PALETTE: dict = {
    # ----- Wong 2011 colorblind-safe categorical (primary tokens) -----
    "wong_blue":      "#0072B2",
    "wong_orange":    "#E69F00",
    "wong_green":     "#009E73",
    "wong_pink":      "#CC79A7",
    "wong_sky":       "#56B4E9",
    "wong_vermilion": "#D55E00",
    "wong_yellow":    "#F0E442",
    "wong_gray":      "#999999",

    # ----- Demographics chart (race/ethnicity + gender stacked bars) -----
    # 6B fix: "White" was #56B4E9 (collision with "Men/Other"); replaced with
    # #9A7D0A (ochre). Verified ≥ 3:1 contrast against white (WCAG AA
    # non-text minimum). #F0E442 (wong_yellow) failed verification at 1.32:1
    # and was replaced.
    "demo_women":       "#CC79A7",   # wong_pink
    "demo_men_other":   "#56B4E9",   # wong_sky
    "demo_black":       "#0072B2",   # wong_blue
    "demo_hispanic":    "#E69F00",   # wong_orange
    "demo_asian":       "#009E73",   # wong_green
    "demo_white":       "#9A7D0A",   # ochre (was #56B4E9 — collision fix)
    "demo_nonresident": "#D55E00",   # wong_vermilion
    "demo_other":       "#999999",   # wong_gray

    # ----- Earnings Mobility chart (income terciles) -----
    # Distinct from demographics palette to avoid same-hex ambiguity
    # (e.g., "Black/AA" and "Low Income" previously shared #0072B2).
    # All three hexes verified ≥ 3:1 contrast against white (WCAG AA
    # non-text minimum). #C2A5CF (2.19:1) and #A6DBA0 (1.58:1) failed
    # verification and were replaced with #9B59B6 and #1E8449.
    "mobility_low":  "#7B3294",   # dark purple   (7.70:1)
    "mobility_mid":  "#9B59B6",   # amethyst      (4.67:1)
    "mobility_high": "#1E8449",   # emerald green (4.72:1)

    # ----- Comparison chart (up to 4 schools) -----
    "comparison": ["#0072B2", "#E69F00", "#009E73", "#CC79A7"],

    # ----- Confidence interval band (pinned card CI bar) -----
    "ci_track_bg":    "rgba(200,200,200,0.15)",
    "ci_band_fill":   "rgba(99,143,255,0.22)",
    "ci_band_border": "rgba(0,114,178,0.35)",
    "ci_point":       "#0072B2",   # wong_blue
    "ci_score_text":  "#0072B2",
    "ci_label_text":  "#555",      # numeric boundary labels beside the band

    # ----- Work environment quartile coloring (Major Explorer) -----
    # 6C-1 fix: all quartile hexes verified ≥ 3.0:1 contrast against white (WCAG AA
    # non-text minimum). #94a3b8 (2.56:1), #cbd5e1 (1.48:1), and #7da7e8 (2.45:1)
    # failed verification and were replaced with #5596cd (3.17:1), #4a8cca (3.56:1),
    # and #2f7dc5 (4.32:1). Even luminance steps preserve the dark→light = top→bottom
    # quartile ordering.
    "quartile_bottom":    "#5596cd",   # medium-light blue  (3.17:1)
    "quartile_below_avg": "#4a8cca",   # medium blue        (3.56:1)
    "quartile_above_avg": "#2f7dc5",   # medium-dark blue   (4.32:1)
    "quartile_top":       "#2563eb",   # dark blue          (5.17:1)

    # ----- Categorical bars (NAICS distribution, RIASEC profile) -----
    # 6B fix: switch from default Plotly blue (#1f77b4) to wong_blue.
    "categorical_primary": "#0072B2",   # wong_blue
    "categorical_other":   "#999999",   # wong_gray (for "Other" rows)

    # ----- School Finder map (scattermapbox) -----
    "map_score_scale":   "RdYlGn",   # Plotly named scale: low=red, high=green
    "map_marker_border": "black",

    # ----- Major Explorer choropleths (Choropleth, not scattermapbox) -----
    "choropleth_scale":   "Viridis",   # Plotly named scale
    "choropleth_land":    "lightgray",
    "choropleth_borders": "white",

    # ----- NAICS distribution bar chart (intentionally distinct from other charts) -----
    # Uses a white background and lighter gridlines (#eee) rather than the
    # transparent background + heavier gridline (rgba(180,180,180,0.25)) used
    # in the CI bar and comparison chart.  Keep these as separate tokens to
    # preserve the intentional style difference.
    "naics_chart_bg": "white",
    "gridline_light": "#eee",           # NAICS distribution x-axis grid

    # ----- Chart gridlines (CI bar, comparison chart) -----
    "gridline": "rgba(180,180,180,0.25)",

    # ----- PDF export (RGB tuples for fpdf2) -----
    "pdf_card_bg":     (245, 245, 245),
    "pdf_card_border": (180, 180, 180),
    "pdf_safety_tint": (200, 230, 200),
    "pdf_match_tint":  (255, 243, 200),
    "pdf_reach_tint":  (255, 210, 210),
    "pdf_na_tint":     (220, 220, 220),
}
