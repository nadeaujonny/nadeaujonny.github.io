"""
data_prep_majors.py — Phase 9 data prep for major-level occupational data.

Reads three raw files from data/raw/ and produces two cleaned CSVs in
data/cleaned/. See data/raw/RAW_DATA_NOTES.md for raw-file documentation.

Run from project root:
    python data_prep_majors.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW_DIR = Path("data/raw")
CLEANED_DIR = Path("data/cleaned")

CROSSWALK_PATH = RAW_DIR / "CIP2020_SOC2018_Crosswalk.xlsx"
OEWS_PATH = RAW_DIR / "national_M2024_dl.xlsx"
EP_PATH = RAW_DIR / "occupation.xlsx"

OCCUPATIONS_MASTER_PATH = CLEANED_DIR / "occupations_master.csv"
CIP4_TO_SOC_PATH = CLEANED_DIR / "cip4_to_soc.csv"
MAJOR_OUTCOMES_PATH = CLEANED_DIR / "major_outcomes.csv"
STATE_OCCUPATIONS_PATH = CLEANED_DIR / "state_occupations.csv"
CIP4_STATE_EMPLOYMENT_PATH = CLEANED_DIR / "cip4_state_employment.csv"
WORK_CONTEXT_INPUT_PATH = CLEANED_DIR / "work_context.csv"
CIP4_WORK_CONTEXT_PATH = CLEANED_DIR / "cip4_work_context.csv"

# OEWS suppression sentinels — see RAW_DATA_NOTES.md
OEWS_SUPPRESSION_VALUES = {"*", "**", "#"}

# EP missing-data sentinel
EP_MISSING_VALUE = "—"  # em dash, U+2014

# OEWS columns to convert from string to numeric in the cleaned output
OEWS_NUMERIC_COLUMNS = [
    "TOT_EMP", "EMP_PRSE", "H_MEAN", "A_MEAN", "MEAN_PRSE",
    "H_PCT10", "H_PCT25", "H_MEDIAN", "H_PCT75", "H_PCT90",
    "A_PCT10", "A_PCT25", "A_MEDIAN", "A_PCT75", "A_PCT90",
]

# EP columns to convert from string to numeric
EP_NUMERIC_COLUMNS = [
    "employment_2024", "employment_2034",
    "employment_change_numeric", "employment_change_percent",
    "percent_self_employed", "annual_openings_avg",
    "median_annual_wage_2024",
]


def load_crosswalk() -> pd.DataFrame:
    """Load the CIP-SOC sheet of the crosswalk with dtype=str.

    Returns the raw 6-digit CIP <-> SOC mapping table with NO_MATCH rows
    excluded. Columns: CIP2020Code, CIP2020Title, SOC2018Code, SOC2018Title.
    """
    df = pd.read_excel(
        CROSSWALK_PATH,
        sheet_name="CIP-SOC",
        header=0,
        dtype=str,
    )
    # Drop NO_MATCH rows (SOC code 99-9999)
    df = df[df["SOC2018Code"] != "99-9999"].copy()
    return df.reset_index(drop=True)


def aggregate_crosswalk_to_cip4(xwalk: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the 6-digit-CIP crosswalk to 4-digit-CIP level.

    The Field of Study Scorecard reports earnings at 4-digit CIP granularity
    (e.g., '11.07' = Computer Science). The crosswalk uses 6-digit CIP
    (e.g., '11.0701' = Computer Science, General). For Phase 9, we take the
    union of all SOCs across each 4-digit parent's 6-digit children.

    Returns a DataFrame with one row per (cip4, SOC2018Code) pair. Columns:
    cip4, SOC2018Code, SOC2018Title, source_cip6_count (how many 6-digit
    CIPs under this cip4 mapped to this SOC).
    """
    df = xwalk.copy()
    # 4-digit CIP = first 5 chars (e.g., '11.0701' -> '11.07')
    df["cip4"] = df["CIP2020Code"].str[:5]

    # Group by (cip4, SOC) and count source 6-digit CIPs
    agg = (
        df.groupby(["cip4", "SOC2018Code", "SOC2018Title"])
        .size()
        .reset_index(name="source_cip6_count")
    )
    return agg


def load_oews() -> pd.DataFrame:
    """Load OEWS national May 2024, filter to cross-industry detailed SOCs.

    Returns ~831 rows, one per detailed SOC code, with all 32 OEWS columns.
    Suppression sentinels (*, **, #) are converted to NaN in the numeric
    columns. All numeric columns are coerced to float.
    """
    df = pd.read_excel(
        OEWS_PATH,
        sheet_name="national_M2024_dl",
        header=0,
        dtype=str,
    )
    # Filter to cross-industry detailed occupations
    mask = (df["I_GROUP"] == "cross-industry") & (df["O_GROUP"] == "detailed")
    df = df[mask].copy().reset_index(drop=True)

    # Convert suppression sentinels to NaN, then coerce to numeric
    for col in OEWS_NUMERIC_COLUMNS:
        df[col] = df[col].where(~df[col].isin(OEWS_SUPPRESSION_VALUES), other=np.nan)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def load_ep() -> pd.DataFrame:
    """Load BLS Employment Projections Table 1.2, filter to line items.

    Returns ~832 rows, one per detailed SOC code. Columns are renamed from
    BLS's verbose form to snake_case. Em-dash sentinels become NaN.
    """
    df = pd.read_excel(
        EP_PATH,
        sheet_name="Table 1.2",
        header=1,
        dtype=str,
    )
    # Strip whitespace from column names (BLS files have inconsistent padding)
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]

    # Filter to line items only (drops Summary rows and footnote rows)
    df = df[df["Occupation type"] == "Line item"].copy().reset_index(drop=True)

    # Rename columns to snake_case
    rename_map = {
        "2024 National Employment Matrix title": "occupation_title",
        "2024 National Employment Matrix code": "soc_code",
        "Employment, 2024": "employment_2024",
        "Employment, 2034": "employment_2034",
        "Employment change, numeric, 2024–34": "employment_change_numeric",
        "Employment change, percent, 2024–34": "employment_change_percent",
        "Percent self employed, 2024": "percent_self_employed",
        "Occupational openings, 2024–34 annual average": "annual_openings_avg",
        "Median annual wage, dollars, 2024[1]": "median_annual_wage_2024",
        "Typical education needed for entry": "typical_education",
        "Work experience in a related occupation": "work_experience",
        "Typical on-the-job training needed to attain competency in the occupation": "typical_training",
    }
    df = df.rename(columns=rename_map)

    # Drop columns we don't need in the cleaned output
    drop_cols = [
        "Occupation type",
        "Employment distribution, percent, 2024",
        "Employment distribution, percent, 2034",
        "Related Occupational Outlook Handbook (OOH) content xlsx",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Strip leading/trailing whitespace from occupation_title (BLS has padding here)
    df["occupation_title"] = df["occupation_title"].str.strip()

    # Replace em-dash with NaN, then coerce numeric columns
    df = df.replace(EP_MISSING_VALUE, np.nan)
    for col in EP_NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def build_occupations_master(oews: pd.DataFrame, ep: pd.DataFrame) -> pd.DataFrame:
    """Join OEWS wages with EP projections on SOC code.

    Wage source priority: OEWS (richer percentile detail). EP's median wage
    is dropped to avoid double-sourcing.

    Returns ~832 rows (the EP universe is the master, since it has the broader
    coverage). SOCs in EP but not OEWS will have NaN wage columns.
    """
    oews_subset = oews[[
        "OCC_CODE", "OCC_TITLE", "TOT_EMP",
        "H_MEAN", "A_MEAN",
        "H_PCT10", "H_PCT25", "H_MEDIAN", "H_PCT75", "H_PCT90",
        "A_PCT10", "A_PCT25", "A_MEDIAN", "A_PCT75", "A_PCT90",
    ]].rename(columns={
        "OCC_CODE": "soc_code",
        "OCC_TITLE": "oews_occupation_title",
        "TOT_EMP": "total_employment_oews",
        "H_MEAN": "hourly_mean",
        "A_MEAN": "annual_mean",
        "H_PCT10": "hourly_pct10",
        "H_PCT25": "hourly_pct25",
        "H_MEDIAN": "hourly_median",
        "H_PCT75": "hourly_pct75",
        "H_PCT90": "hourly_pct90",
        "A_PCT10": "annual_pct10",
        "A_PCT25": "annual_pct25",
        "A_MEDIAN": "annual_median",
        "A_PCT75": "annual_pct75",
        "A_PCT90": "annual_pct90",
    })

    # EP is the master (has 832 rows; OEWS has 831). Left-join OEWS onto EP.
    # Drop EP's median_annual_wage_2024 — OEWS provides this with more detail.
    ep_subset = ep.drop(columns=["median_annual_wage_2024"])

    merged = ep_subset.merge(oews_subset, on="soc_code", how="left")

    column_order = [
        "soc_code", "occupation_title",
        # Projections (EP)
        "employment_2024", "employment_2034",
        "employment_change_numeric", "employment_change_percent",
        "annual_openings_avg", "percent_self_employed",
        # Education (EP)
        "typical_education", "work_experience", "typical_training",
        # Wages (OEWS)
        "annual_median", "annual_mean",
        "annual_pct10", "annual_pct25", "annual_pct75", "annual_pct90",
        "hourly_median", "hourly_mean",
        "hourly_pct10", "hourly_pct25", "hourly_pct75", "hourly_pct90",
        "total_employment_oews", "oews_occupation_title",
    ]
    merged = merged[column_order]
    return merged


def build_major_outcomes(
    occupations_master: pd.DataFrame,
    cip4_to_soc: pd.DataFrame,
    crosswalk: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate per-SOC numbers to per-CIP4 numbers, weighted by SOC employment.

    For each 4-digit CIP, computes the employment-weighted average of:
    - annual_median (wage)
    - annual_pct25, annual_pct75 (wage spread)
    - employment_change_percent (10-year growth rate)

    Plus straight aggregates:
    - total_employment_routing (sum of total_employment_oews across routing SOCs)
    - n_routing_socs (count of distinct SOCs the CIP4 routes to)
    - n_socs_with_wage_data (count where annual_median is non-null)
    - n_socs_with_projection_data (count where employment_change_percent is non-null)

    Plus a label:
    - cip4_title (taken from the lowest-numbered 6-digit CIP title under this CIP4)

    Note: routing SOCs that don't appear in occupations_master (the ~47
    aggregation-level SOCs that OEWS/EP split) are dropped from the inner join
    and thus excluded from the weighted average for their CIP4s.

    Args:
        occupations_master: per-SOC table from build_occupations_master()
        cip4_to_soc: routing pairs from aggregate_crosswalk_to_cip4()
        crosswalk: raw crosswalk for CIP4 title lookup (uses CIP2020Title)

    Returns:
        DataFrame with one row per CIP4. ~440 rows.
    """
    # 1. Build CIP4 title lookup from lowest-numbered 6-digit child
    xwalk_with_cip4 = crosswalk.copy()
    xwalk_with_cip4["cip4"] = xwalk_with_cip4["CIP2020Code"].str[:5]
    cip4_titles = (
        xwalk_with_cip4.sort_values("CIP2020Code")
        .drop_duplicates(subset="cip4", keep="first")
        [["cip4", "CIP2020Title"]]
        .rename(columns={"CIP2020Title": "cip4_title"})
    )
    cip4_titles["cip4_title"] = cip4_titles["cip4_title"].str.rstrip(".")

    # 2. Join routing pairs to per-SOC data
    joined = cip4_to_soc.merge(
        occupations_master,
        left_on="SOC2018Code",
        right_on="soc_code",
        how="inner",
    )

    # 3. Compute employment-weighted aggregates per CIP4
    def _weighted_mean(values: pd.Series, weights: pd.Series) -> float:
        """Employment-weighted mean. Returns NaN if no rows have both value and weight."""
        mask = values.notna() & weights.notna() & (weights > 0)
        if not mask.any():
            return np.nan
        return float((values[mask] * weights[mask]).sum() / weights[mask].sum())

    def _aggregate_one_cip4(group: pd.DataFrame) -> pd.Series:
        w = group["total_employment_oews"]
        return pd.Series({
            "weighted_annual_median": _weighted_mean(group["annual_median"], w),
            "weighted_annual_pct25": _weighted_mean(group["annual_pct25"], w),
            "weighted_annual_pct75": _weighted_mean(group["annual_pct75"], w),
            "weighted_employment_change_percent": _weighted_mean(
                group["employment_change_percent"], w
            ),
            "total_employment_routing": w.sum(skipna=True),
            "n_routing_socs": len(group),
            "n_socs_with_wage_data": int(group["annual_median"].notna().sum()),
            "n_socs_with_projection_data": int(
                group["employment_change_percent"].notna().sum()
            ),
        })

    agg = joined.groupby("cip4").apply(_aggregate_one_cip4).reset_index()

    # 4. Merge in CIP4 titles
    result = agg.merge(cip4_titles, on="cip4", how="left")

    # 5. Order columns and sort
    column_order = [
        "cip4", "cip4_title",
        "weighted_annual_median",
        "weighted_annual_pct25", "weighted_annual_pct75",
        "weighted_employment_change_percent",
        "total_employment_routing",
        "n_routing_socs",
        "n_socs_with_wage_data",
        "n_socs_with_projection_data",
    ]
    result = result[column_order].sort_values("cip4").reset_index(drop=True)
    return result


def build_cip4_state_employment(
    state_occupations: pd.DataFrame,
    cip4_to_soc: pd.DataFrame,
    occupations_master: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate per-SOC state employment up to per-CIP4 state employment.

    For each (CIP4, state) pair, sum routing-SOC TOT_EMP and compute a
    true CIP4-level location quotient using state_total_emp and
    national_total_emp as denominators. Apply a 50% coverage threshold:
    cells where less than half of routing-SOC national employment is
    observed at the state level have NaN metrics.

    Inputs:
        state_occupations: DataFrame from state_occupations.csv
            (35,427 rows; columns include state_abbr, soc_code, total_employment)
        cip4_to_soc: DataFrame from cip4_to_soc.csv
            (2,618 rows; columns: cip4, SOC2018Code)
        occupations_master: DataFrame from occupations_master.csv
            (832 rows; columns include soc_code, total_employment_oews [national])

    Output:
        DataFrame with columns:
            cip4 (str)
            state (str, 2-letter postal code)
            total_employment (float, NaN if coverage_pct < 0.50)
            location_quotient (float, NaN if coverage_pct < 0.50)
            coverage_pct (float, always populated, 0.0 to 1.0)
            n_routing_socs (int, total routing SOCs for this CIP4)
            n_observed_socs (int, routing SOCs with non-NaN state TOT_EMP)
        Roughly 414 CIP4s × 51 states = ~21,114 rows.
    """
    # 1. Validate input columns
    required = {
        "state_occupations": {"state_abbr", "soc_code", "total_employment"},
        "cip4_to_soc": {"cip4", "SOC2018Code"},
        "occupations_master": {"soc_code", "total_employment_oews"},
    }
    for name, cols in required.items():
        df = {"state_occupations": state_occupations,
              "cip4_to_soc": cip4_to_soc,
              "occupations_master": occupations_master}[name]
        missing = cols - set(df.columns)
        if missing:
            raise KeyError(f"{name} missing required columns: {missing}")

    # 2. Normalize dtypes on join keys and numeric columns
    so = state_occupations[["state_abbr", "soc_code", "total_employment"]].copy()
    so["soc_code"] = so["soc_code"].astype(str)
    so["total_employment"] = pd.to_numeric(so["total_employment"], errors="coerce")

    c2s = cip4_to_soc[["cip4", "SOC2018Code"]].copy()
    c2s["cip4"] = c2s["cip4"].astype(str)
    c2s["soc_code"] = c2s["SOC2018Code"].astype(str)

    om = occupations_master[["soc_code", "total_employment_oews"]].copy()
    om["soc_code"] = om["soc_code"].astype(str)
    om["total_employment_oews"] = pd.to_numeric(
        om["total_employment_oews"], errors="coerce"
    )

    # 3. Compute global denominators ONCE (before any CIP4 filtering)
    national_total_emp = om["total_employment_oews"].sum(skipna=True)
    state_total_emp_by_state = (
        so.groupby("state_abbr")["total_employment"].sum(skipna=True)
    )

    # 4. Build national employment lookup (SOCs with NaN national emp excluded)
    national_emp_by_soc = (
        om.dropna(subset=["total_employment_oews"])
        .set_index("soc_code")["total_employment_oews"]
        .to_dict()
    )

    # 5. Attach national employment to each routing (cip4, soc) pair
    routing = c2s[["cip4", "soc_code"]].copy()
    routing["natl_emp"] = routing["soc_code"].map(national_emp_by_soc)

    # 6. Per-CIP4 totals: total routing national emp and routing SOC count
    cip4_stats = (
        routing.groupby("cip4")
        .agg(
            total_routing_natl_emp=("natl_emp", "sum"),
            n_routing_socs=("soc_code", "size"),
        )
        .reset_index()
    )

    # 7. Expand routing pairs to all (cip4, soc, state) combos via left join.
    #    Rows where state_occupations has no record for a SOC get NaN state_abbr.
    expanded = routing.merge(
        so.rename(columns={"total_employment": "state_emp"}),
        on="soc_code",
        how="left",
    )

    # 8. Build the complete (cip4, state) grid — all CIP4s × all 51 states
    all_cip4s = routing["cip4"].unique()
    all_states = so["state_abbr"].dropna().unique()
    grid = pd.DataFrame(
        [(c, s) for c in all_cip4s for s in all_states],
        columns=["cip4", "state"],
    )

    # 9. Aggregate observed employment by (cip4, state) from expanded pairs
    #    Only rows where state is known (routing SOC appears in state_occupations)
    exp_known = expanded[expanded["state_abbr"].notna()].copy()
    exp_known["is_observed"] = exp_known["state_emp"].notna()
    # Contributions are NaN for suppressed SOCs so sum(skipna) excludes them
    exp_known["state_emp_contrib"] = exp_known["state_emp"].where(
        exp_known["is_observed"]
    )
    exp_known["obs_natl_contrib"] = exp_known["natl_emp"].where(
        exp_known["is_observed"]
    )

    agg_state = (
        exp_known.groupby(["cip4", "state_abbr"])
        .agg(
            state_routing_emp=("state_emp_contrib", "sum"),
            observed_routing_natl_emp=("obs_natl_contrib", "sum"),
            n_observed_socs=("is_observed", "sum"),
        )
        .reset_index()
        .rename(columns={"state_abbr": "state"})
    )
    agg_state["n_observed_socs"] = agg_state["n_observed_socs"].astype(int)

    # 10. Merge grid → per-CIP4 stats → per-(CIP4, state) stats
    result = grid.merge(cip4_stats, on="cip4", how="left")
    result = result.merge(agg_state, on=["cip4", "state"], how="left")

    # Fill NaN for (cip4, state) pairs where no routing SOC appears in state_occupations
    result["state_routing_emp"] = result["state_routing_emp"].fillna(0.0)
    result["observed_routing_natl_emp"] = result["observed_routing_natl_emp"].fillna(0.0)
    result["n_observed_socs"] = result["n_observed_socs"].fillna(0).astype(int)
    result["n_routing_socs"] = result["n_routing_socs"].fillna(0).astype(int)

    # 11. Coverage diagnostic: fraction of routing-SOC national emp that is observed
    result["coverage_pct"] = np.where(
        result["total_routing_natl_emp"] > 0,
        result["observed_routing_natl_emp"] / result["total_routing_natl_emp"],
        0.0,
    ).clip(0.0, 1.0)

    # 12. Apply 50% threshold and compute output metrics
    result["state_total_emp"] = result["state"].map(state_total_emp_by_state)

    has_coverage = result["coverage_pct"] >= 0.50
    safe_lq_denom = (
        result["state_total_emp"].notna()
        & (result["state_total_emp"] > 0)
        & (result["total_routing_natl_emp"] > 0)
        & (national_total_emp > 0)
    )

    result["total_employment"] = np.where(
        has_coverage, result["state_routing_emp"], np.nan
    )
    result["location_quotient"] = np.where(
        has_coverage & safe_lq_denom,
        (result["state_routing_emp"] / result["state_total_emp"])
        / (result["total_routing_natl_emp"] / national_total_emp),
        np.nan,
    )

    # 13. Select output columns and sort deterministically
    output_cols = [
        "cip4", "state",
        "total_employment", "location_quotient", "coverage_pct",
        "n_routing_socs", "n_observed_socs",
    ]
    result = result[output_cols].sort_values(["cip4", "state"]).reset_index(drop=True)

    # 14. Summary diagnostics
    n_rows = len(result)
    nan_emp_pct = result["total_employment"].isna().mean() * 100
    cov50_pct = (result["coverage_pct"] >= 0.50).mean() * 100
    cov0_pct = (result["coverage_pct"] == 0.0).mean() * 100
    lq_vals = result["location_quotient"].dropna()
    print(
        f"[build_cip4_state_employment] {n_rows} rows "
        f"({result['cip4'].nunique()} CIP4s × {result['state'].nunique()} states)"
    )
    print(f"  NaN total_employment: {nan_emp_pct:.1f}%")
    print(f"  coverage_pct >= 0.50: {cov50_pct:.1f}%  |  coverage_pct = 0.0: {cov0_pct:.1f}%")
    if len(lq_vals) > 0:
        print(
            f"  LQ range (non-NaN): {lq_vals.min():.3f} – {lq_vals.max():.1f}, "
            f"median: {lq_vals.median():.3f}"
        )

    return result


def build_cip4_work_context(
    work_context: pd.DataFrame,
    cip4_to_soc: pd.DataFrame,
    occupations_master: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate per-SOC O*NET work context elements up to per-CIP4
    weighted composites.

    For each CIP4, compute a routing-SOC-employment-weighted average
    of each of the 13 work-context elements. Apply a 50% coverage
    threshold: CIP4s where less than half of routing-SOC national
    employment has work-context data have all 13 element columns set
    to NaN.

    Inputs:
        work_context: DataFrame from work_context.csv
            (774 rows; columns: soc_code, 13 element columns,
             elements_with_data, avg_sample_size)
        cip4_to_soc: DataFrame from cip4_to_soc.csv
            (2,618 rows; columns: cip4, SOC2018Code)
        occupations_master: DataFrame from occupations_master.csv
            (832 rows; columns include soc_code, total_employment_oews)

    Output:
        DataFrame with columns:
            cip4 (str)
            13 element columns (float, NaN if pct_routing_emp_with_context < 0.50)
            n_routing_socs (int)
            n_routing_socs_with_context (int)
            pct_routing_emp_with_context (float, 0.0 to 1.0)
        ~414 rows.
    """
    # 1. Discover element columns dynamically — all cols except the metadata ones
    non_element_cols = {"soc_code", "elements_with_data", "avg_sample_size"}
    ELEMENT_COLS = [c for c in work_context.columns if c not in non_element_cols]
    if not ELEMENT_COLS:
        raise ValueError("work_context has no element columns")

    # Validate required columns
    for name, df, required in [
        ("work_context", work_context, {"soc_code"} | set(ELEMENT_COLS)),
        ("cip4_to_soc", cip4_to_soc, {"cip4", "SOC2018Code"}),
        ("occupations_master", occupations_master, {"soc_code", "total_employment_oews"}),
    ]:
        missing = required - set(df.columns)
        if missing:
            raise KeyError(f"{name} missing required columns: {missing}")

    # 2. Build national employment lookup (SOCs with NaN national emp excluded)
    om = occupations_master[["soc_code", "total_employment_oews"]].copy()
    om["soc_code"] = om["soc_code"].astype(str)
    om["total_employment_oews"] = pd.to_numeric(om["total_employment_oews"], errors="coerce")
    national_emp_by_soc = (
        om.dropna(subset=["total_employment_oews"])
        .set_index("soc_code")["total_employment_oews"]
        .to_dict()
    )

    # 3. Build work-context lookup: soc_code -> {element: value}
    #    SOCs whose entire row is NaN across all elements are excluded.
    wc = work_context[["soc_code"] + ELEMENT_COLS].copy()
    wc["soc_code"] = wc["soc_code"].astype(str)
    for col in ELEMENT_COLS:
        wc[col] = pd.to_numeric(wc[col], errors="coerce")
    wc_by_soc = (
        wc[wc[ELEMENT_COLS].notna().any(axis=1)]
        .set_index("soc_code")[ELEMENT_COLS]
        .to_dict(orient="index")
    )

    # 4. Normalize cip4_to_soc join key
    c2s = cip4_to_soc[["cip4", "SOC2018Code"]].copy()
    c2s["cip4"] = c2s["cip4"].astype(str)
    c2s["soc_code"] = c2s["SOC2018Code"].astype(str)

    # 5. Per-CIP4 aggregation
    rows = []
    for cip4_val, group in c2s.groupby("cip4"):
        routing_set = set(group["soc_code"].tolist())

        total_routing_emp = sum(
            national_emp_by_soc[soc] for soc in routing_set if soc in national_emp_by_soc
        )

        # Routing SOCs that have both work-context data and non-NaN national employment
        routing_socs_with_context = {
            soc for soc in routing_set
            if soc in wc_by_soc and soc in national_emp_by_soc
        }
        observed_routing_emp = sum(
            national_emp_by_soc[soc] for soc in routing_socs_with_context
        )

        pct = observed_routing_emp / total_routing_emp if total_routing_emp > 0 else 0.0

        if pct < 0.50:
            # All-or-nothing: fail the threshold → NaN for all 13 elements
            element_values = {col: np.nan for col in ELEMENT_COLS}
        else:
            element_values = {}
            for col in ELEMENT_COLS:
                # Per-element NaN exclusion within the CIP4-level gate
                num = 0.0
                denom = 0.0
                for soc in routing_socs_with_context:
                    val = wc_by_soc[soc][col]
                    if not pd.isna(val):
                        emp = national_emp_by_soc[soc]
                        num += val * emp
                        denom += emp
                element_values[col] = num / denom if denom > 0 else np.nan

        row = {"cip4": cip4_val}
        row.update(element_values)
        row["n_routing_socs"] = len(routing_set)
        row["n_routing_socs_with_context"] = len(routing_socs_with_context)
        row["pct_routing_emp_with_context"] = pct
        rows.append(row)

    result = pd.DataFrame(rows)

    # Enforce dtypes
    result["cip4"] = result["cip4"].astype(str)
    for col in ELEMENT_COLS:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    result["n_routing_socs"] = result["n_routing_socs"].astype(int)
    result["n_routing_socs_with_context"] = result["n_routing_socs_with_context"].astype(int)
    result["pct_routing_emp_with_context"] = pd.to_numeric(
        result["pct_routing_emp_with_context"], errors="coerce"
    )

    # Order columns deterministically: cip4, elements, diagnostics
    col_order = ["cip4"] + ELEMENT_COLS + [
        "n_routing_socs", "n_routing_socs_with_context", "pct_routing_emp_with_context"
    ]
    result = result[col_order].sort_values("cip4").reset_index(drop=True)

    n_rows = len(result)
    pct_pass = (result["pct_routing_emp_with_context"] >= 0.50).mean() * 100
    n_zero = (result["n_routing_socs_with_context"] == 0).sum()
    print(f"[build_cip4_work_context] {n_rows} CIP4 rows")
    print(f"  % passing 50% coverage threshold: {pct_pass:.1f}%")
    print(f"  CIP4s with no work-context SOCs: {n_zero}")

    return result


def build_soc_to_naics3() -> pd.DataFrame:
    """
    Build SOC → 3-digit NAICS employment distribution from BLS OEWS
    May 2024 national industry-specific (3-digit NAICS) file.

    For each detailed SOC occupation, computes the share of total
    cross-industry employment occurring in each 3-digit NAICS industry.
    Shares sum to 1.0 within each SOC by construction (after filtering
    out BLS suppression).

    Source: data/raw/oesm24in4/nat3d_M2024_dl.xlsx
    Filters applied:
      - O_GROUP == 'detailed' (specific 6-character SOC codes only)
      - TOT_EMP != '**' (drops BLS-suppressed cells)
      - No OWN_CODE filter needed: each NAICS appears under exactly
        one ownership code in this file.

    Returns DataFrame with columns:
        soc_code, soc_title, naics3, naics3_title, tot_emp, share_in_naics3
    Sorted by (soc_code, share_in_naics3 desc).
    """
    raw_path = Path("data/raw/oesm24in4/nat3d_M2024_dl.xlsx")

    # Read everything as string so the `**` suppression marker is preserved
    # and 6-digit NAICS codes don't lose any digits.
    df = pd.read_excel(raw_path, sheet_name="nat3d_M2024_dl", dtype=str)

    # Filter to detailed-SOC, non-suppressed rows
    df = df[df["O_GROUP"] == "detailed"].copy()
    df = df[df["TOT_EMP"] != "**"].copy()
    df["TOT_EMP"] = df["TOT_EMP"].astype(int)

    # Extract 3-digit NAICS from the 6-digit column (e.g., '113000' -> '113')
    df["naics3"] = df["NAICS"].str[:3]

    # Compute within-SOC share. By construction this sums to 1.0 per SOC.
    soc_totals = df.groupby("OCC_CODE")["TOT_EMP"].transform("sum")
    df["share_in_naics3"] = df["TOT_EMP"] / soc_totals

    out = df.rename(columns={
        "OCC_CODE": "soc_code",
        "OCC_TITLE": "soc_title",
        "NAICS_TITLE": "naics3_title",
        "TOT_EMP": "tot_emp",
    })[["soc_code", "soc_title", "naics3", "naics3_title", "tot_emp", "share_in_naics3"]]

    return out.sort_values(
        ["soc_code", "share_in_naics3"],
        ascending=[True, False],
    ).reset_index(drop=True)


def build_cip4_naics3_distribution() -> pd.DataFrame:
    """
    Aggregate SOC → 3-digit NAICS distribution up to CIP4 level.

    For each CIP4 major, computes the share of national employment in
    each 3-digit NAICS industry, weighted by the national employment
    of each routing SOC. Larger SOCs (e.g., 25-1041 Postsecondary
    Teachers, which routes to many CIP4s) naturally contribute more
    weight to the CIP4s they appear under — matching the same
    employment-weighted aggregation pattern Phase 10.4 used for state
    location quotients.

    Sources:
      - data/cleaned/cip4_to_soc.csv (Phase 9 routing table)
      - data/cleaned/soc_to_naics3.csv (Phase 11.3.1)

    Coverage notes:
      - ~86 of 2,618 routing rows reference SOCs missing from the BLS
        detailed-level industry data. Silently dropped by the inner join.
      - 2 CIP4s (28.05, 28.06 Military Technologies) end up with no
        NAICS distribution because all their routing SOCs are missing.
        Renderer handles via empty-state pattern.

    Returns DataFrame with columns:
        cip4, naics3, naics3_title, weighted_emp, share_in_naics3
    Sorted by (cip4, share_in_naics3 desc). Shares sum to 1.0 per CIP4.
    """
    routing_path = Path("data/cleaned/cip4_to_soc.csv")
    soc_naics_path = Path("data/cleaned/soc_to_naics3.csv")

    routing = pd.read_csv(
        routing_path,
        dtype={"cip4": str, "SOC2018Code": str},
    ).rename(columns={"SOC2018Code": "soc_code"})

    soc_to_naics3 = pd.read_csv(
        soc_naics_path,
        dtype={"soc_code": str, "naics3": str},
    )

    # Inner join: routing × NAICS distribution.
    # Each routing (cip4, soc) row fans out to N rows for the N NAICS3
    # codes that SOC employs into. tot_emp is the SOC's employment in
    # that NAICS — using it directly gives employment-weighted aggregation.
    joined = routing.merge(
        soc_to_naics3[["soc_code", "naics3", "naics3_title", "tot_emp"]],
        on="soc_code",
        how="inner",
    )

    # Aggregate to CIP4 × NAICS3
    agg = (
        joined.groupby(["cip4", "naics3", "naics3_title"], as_index=False)["tot_emp"]
        .sum()
        .rename(columns={"tot_emp": "weighted_emp"})
    )

    # Normalize within CIP4 (shares sum to 1.0 per CIP4)
    cip_totals = agg.groupby("cip4")["weighted_emp"].transform("sum")
    agg["share_in_naics3"] = agg["weighted_emp"] / cip_totals

    return agg.sort_values(
        ["cip4", "share_in_naics3"],
        ascending=[True, False],
    ).reset_index(drop=True)


def main() -> None:
    """Run the full data-prep pipeline."""
    print("[data_prep_majors] Loading raw files...")
    xwalk = load_crosswalk()
    oews = load_oews()
    ep = load_ep()
    print(f"  Crosswalk: {len(xwalk)} CIP-SOC mappings, "
          f"{xwalk['CIP2020Code'].nunique()} unique CIPs")
    print(f"  OEWS:      {len(oews)} detailed SOCs")
    print(f"  EP:        {len(ep)} line-item SOCs")

    print("[data_prep_majors] Aggregating crosswalk to 4-digit CIP...")
    cip4_to_soc = aggregate_crosswalk_to_cip4(xwalk)
    print(f"  cip4_to_soc rows: {len(cip4_to_soc)}, "
          f"unique CIP4: {cip4_to_soc['cip4'].nunique()}")

    print("[data_prep_majors] Building occupations master...")
    occ_master = build_occupations_master(oews, ep)
    print(f"  occupations_master rows: {len(occ_master)}")

    socs_in_xwalk = set(cip4_to_soc["SOC2018Code"])
    socs_in_master = set(occ_master["soc_code"])
    missing = socs_in_xwalk - socs_in_master
    print(f"[data_prep_majors] Crosswalk SOCs NOT in occupations_master: "
          f"{len(missing)} (these are aggregation-level SOCs split by OEWS/EP)")

    print("[data_prep_majors] Building major outcomes (CIP4 aggregates)...")
    major_outcomes = build_major_outcomes(occ_master, cip4_to_soc, xwalk)
    print(f"  major_outcomes rows: {len(major_outcomes)}")
    print(f"  CIP4s with full data: "
          f"{major_outcomes['weighted_annual_median'].notna().sum()}")
    print(f"  CIP4s with no wage data: "
          f"{major_outcomes['weighted_annual_median'].isna().sum()}")

    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    occ_master.to_csv(OCCUPATIONS_MASTER_PATH, index=False)
    cip4_to_soc.to_csv(CIP4_TO_SOC_PATH, index=False)
    major_outcomes.to_csv(MAJOR_OUTCOMES_PATH, index=False)
    print(f"[data_prep_majors] Wrote {OCCUPATIONS_MASTER_PATH}")
    print(f"[data_prep_majors] Wrote {CIP4_TO_SOC_PATH}")
    print(f"[data_prep_majors] Wrote {MAJOR_OUTCOMES_PATH}")

    print("[data_prep_majors] Loading state_occupations for CIP4 aggregation...")
    state_occ = pd.read_csv(STATE_OCCUPATIONS_PATH, dtype={"soc_code": str})
    print(f"  state_occupations rows: {len(state_occ)}")

    print("[data_prep_majors] Building CIP4 state employment...")
    cip4_state_emp = build_cip4_state_employment(state_occ, cip4_to_soc, occ_master)

    lq_vals = cip4_state_emp["location_quotient"].dropna()
    print(
        f"  rows out: {len(cip4_state_emp)}, "
        f"NaN total_employment: {cip4_state_emp['total_employment'].isna().mean()*100:.1f}%"
    )
    print(
        f"  coverage_pct >= 0.50: {(cip4_state_emp['coverage_pct'] >= 0.50).mean()*100:.1f}%"
    )
    if len(lq_vals) > 0:
        print(
            f"  LQ range: {lq_vals.min():.3f} – {lq_vals.max():.1f}, "
            f"median: {lq_vals.median():.3f}"
        )

    cip4_state_emp.to_csv(CIP4_STATE_EMPLOYMENT_PATH, index=False)
    print(f"[data_prep_majors] Wrote {CIP4_STATE_EMPLOYMENT_PATH}")

    print("[data_prep_majors] Loading work_context for CIP4 aggregation...")
    work_context = pd.read_csv(WORK_CONTEXT_INPUT_PATH, dtype={"soc_code": str})
    print(f"  work_context rows: {len(work_context)}")

    print("[data_prep_majors] Building CIP4 work context...")
    cip4_work_ctx = build_cip4_work_context(work_context, cip4_to_soc, occ_master)

    pct_pass_wc = (cip4_work_ctx["pct_routing_emp_with_context"] >= 0.50).mean() * 100
    print(
        f"  rows out: {len(cip4_work_ctx)}, "
        f"% passing 50% threshold: {pct_pass_wc:.1f}%"
    )
    diag_cols = {"cip4", "n_routing_socs", "n_routing_socs_with_context",
                 "pct_routing_emp_with_context"}
    el_cols = [c for c in cip4_work_ctx.columns if c not in diag_cols]
    for col in el_cols:
        vals = cip4_work_ctx[col].dropna()
        if len(vals) > 0:
            print(
                f"  {col}: mean={vals.mean():.3f}, median={vals.median():.3f}, "
                f"range=[{vals.min():.3f}, {vals.max():.3f}]"
            )

    cip4_work_ctx.to_csv(CIP4_WORK_CONTEXT_PATH, index=False)
    print(f"[data_prep_majors] Wrote {CIP4_WORK_CONTEXT_PATH}")

    # Phase 11.3.1
    print("Building soc_to_naics3...")
    soc_to_naics3 = build_soc_to_naics3()
    out_path = Path("data/cleaned/soc_to_naics3.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    soc_to_naics3.to_csv(out_path, index=False)
    print(f"  Wrote {len(soc_to_naics3):,} rows to {out_path}")
    print(f"  Unique SOCs: {soc_to_naics3['soc_code'].nunique()}")
    print(f"  Unique NAICS3: {soc_to_naics3['naics3'].nunique()}")

    # Phase 11.3.2
    print("Building cip4_naics3_distribution...")
    cip4_naics = build_cip4_naics3_distribution()
    out_path = Path("data/cleaned/cip4_naics3_distribution.csv")
    cip4_naics.to_csv(out_path, index=False)
    print(f"  Wrote {len(cip4_naics):,} rows to {out_path}")
    print(f"  Unique CIP4s: {cip4_naics['cip4'].nunique()}")
    print(f"  Unique NAICS3: {cip4_naics['naics3'].nunique()}")

    print("[data_prep_majors] Done.")


if __name__ == "__main__":
    main()
