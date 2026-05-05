"""
data_prep_workcontext.py — Phase 10 data prep for O*NET work-context ratings.

Reads the O*NET 30.2 Work Context file from data/raw/ and produces one cleaned
CSV in data/cleaned/. See data/raw/RAW_DATA_NOTES.md for raw-file documentation
and CC BY 4.0 attribution.

Run from project root:
    python data_prep_workcontext.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW_DIR = Path("data/raw")
CLEANED_DIR = Path("data/cleaned")

WORK_CONTEXT_PATH = RAW_DIR / "Work Context.xlsx"
WORK_CONTEXT_OUTPUT_PATH = CLEANED_DIR / "work_context.csv"

# Numeric-rating Scale IDs (mean ratings on numeric scales).
# CX = generic 1-5 context frequency scale.
# CT = context-type scale used for elements like Duration of Typical Work Week.
# CXP and CTP are percent-endorsing-category rows; we drop them.
NUMERIC_SCALES = {"CX", "CT"}

# Work context elements to surface in the Phase 10.5 panel.
# Keys are element names as they appear in the O*NET file; values are short
# column labels for the cleaned CSV. Element IDs (4.A.X.X.X) are stable across
# releases; element names occasionally get minor rewording.
ELEMENTS_TO_KEEP = {
    "Duration of Typical Work Week": "hours_per_week",
    "Time Pressure": "time_pressure",
    "Freedom to Make Decisions": "decision_autonomy",
    "Frequency of Decision Making": "decision_frequency",
    "Importance of Being Exact or Accurate": "precision_required",
    "Spend Time Standing": "physical_standing",
    "Spend Time Sitting": "physical_sitting",
    "Outdoors, Exposed to All Weather Conditions": "outdoor_work",
    "Indoors, Environmentally Controlled": "indoor_climate_controlled",
    "Work With or Contribute to a Work Group or Team": "teamwork_required",
    "Deal With External Customers or the Public in General": "customer_facing",
    "Telephone Conversations": "phone_use",
    "E-Mail": "email_use",
}


def load_work_context() -> pd.DataFrame:
    """Load the O*NET Work Context file with dtype=str.

    Returns the raw file with all columns and ~297,676 rows. No filtering
    or pivoting yet — those happen in clean_work_context().
    """
    df = pd.read_excel(
        WORK_CONTEXT_PATH,
        header=0,
        dtype=str,
    )
    return df


def clean_work_context(wc_raw: pd.DataFrame) -> pd.DataFrame:
    """Filter and clean the raw Work Context file.

    Steps:
    1. Filter to numeric-rating rows (Scale ID in {CX, CT})
    2. Drop rows where Recommend Suppress == "Y" (low-precision ratings)
    3. Drop rows where Not Relevant == "Y" (element not applicable to occupation)
    4. Coerce Data Value to float; drop rows where coercion yields NaN
    5. Filter to the curated ELEMENTS_TO_KEEP subset

    Note: Both CX and CT scales are kept because they are both numeric mean
    ratings. CT is used for elements like 'Duration of Typical Work Week'
    that are rated on a context-specific scale rather than the generic 1-5
    frequency scale (CX). CXP and CTP (percent-endorsing-category rows) are
    not ratings and are dropped.

    Returns long-format DataFrame, one row per (O*NET-SOC, element) pair.
    """
    df = wc_raw.copy()

    df = df[df["Scale ID"].isin(NUMERIC_SCALES)].copy()
    df = df[df["Recommend Suppress"] != "Y"].copy()
    df = df[df["Not Relevant"] != "Y"].copy()

    df["Data Value"] = pd.to_numeric(df["Data Value"], errors="coerce")
    df = df[df["Data Value"].notna()].copy()

    df = df[df["Element Name"].isin(ELEMENTS_TO_KEEP.keys())].copy()

    df["element_short"] = df["Element Name"].map(ELEMENTS_TO_KEEP)

    df = df[[
        "O*NET-SOC Code", "Title", "Element Name", "element_short",
        "Scale ID", "Data Value", "N",
    ]].rename(columns={
        "O*NET-SOC Code": "onet_soc_code",
        "Title": "occupation_title",
        "Element Name": "element_name",
        "Scale ID": "scale_id",
        "Data Value": "rating",
        "N": "sample_size_str",
    }).reset_index(drop=True)

    df["sample_size"] = pd.to_numeric(df["sample_size_str"], errors="coerce")
    df = df.drop(columns=["sample_size_str"])

    return df


def aggregate_to_bls_soc(wc_clean: pd.DataFrame) -> pd.DataFrame:
    """Aggregate O*NET-SOC variants to 6-digit BLS SOC.

    O*NET-SOC codes have the form '15-1252.00' (8-digit). BLS SOC2018 codes
    have the form '15-1252' (6-digit). Some BLS SOCs map to multiple O*NET-SOC
    variants (e.g., '15-1252.00' and '15-1252.01'). For each (BLS SOC, element)
    pair, we compute the sample-size-weighted mean of the rating across all
    O*NET-SOC variants.

    Args:
        wc_clean: output of clean_work_context()

    Returns:
        Long-format DataFrame, one row per (soc_code, element_short) pair.
    """
    df = wc_clean.copy()
    df["soc_code"] = df["onet_soc_code"].str.split(".").str[0]

    def _weighted_mean(values: pd.Series, weights: pd.Series) -> float:
        mask = values.notna() & weights.notna() & (weights > 0)
        if not mask.any():
            # Fall back to simple mean when all sample-size values are missing
            return float(values.mean()) if values.notna().any() else np.nan
        return float((values[mask] * weights[mask]).sum() / weights[mask].sum())

    def _aggregate_one(group: pd.DataFrame) -> pd.Series:
        return pd.Series({
            "rating": _weighted_mean(group["rating"], group["sample_size"]),
            "n_onet_soc_variants": group["onet_soc_code"].nunique(),
            "total_sample_size": int(group["sample_size"].sum(skipna=True)),
        })

    agg = (
        df.groupby(["soc_code", "element_short"])
        .apply(_aggregate_one)
        .reset_index()
    )
    return agg


def pivot_to_wide(agg: pd.DataFrame) -> pd.DataFrame:
    """Pivot from long format (one row per soc-element) to wide (one row per soc).

    Each element becomes a column. Element columns are ordered to match
    ELEMENTS_TO_KEEP iteration order.

    The `elements_with_data` and `avg_sample_size` coverage columns let the
    Phase 10.5 panel flag low-coverage occupations.

    Returns wide DataFrame with soc_code as the leftmost column, element
    short-name columns to the right, and coverage diagnostics at the far right.
    """
    wide = agg.pivot(index="soc_code", columns="element_short", values="rating")
    element_order = list(ELEMENTS_TO_KEEP.values())
    available = [c for c in element_order if c in wide.columns]
    wide = wide[available].reset_index()
    wide.columns.name = None

    coverage = (
        agg.groupby("soc_code")
        .agg(
            elements_with_data=("rating", lambda s: int(s.notna().sum())),
            avg_sample_size=("total_sample_size", "mean"),
        )
        .reset_index()
    )
    wide = wide.merge(coverage, on="soc_code", how="left")
    return wide


def main() -> None:
    """Run the work-context data-prep pipeline."""
    print("[data_prep_workcontext] Loading raw Work Context file...")
    wc_raw = load_work_context()
    print(f"  Raw rows: {len(wc_raw):,}")
    print(f"  Unique O*NET-SOCs: {wc_raw['O*NET-SOC Code'].nunique()}")
    print(f"  Unique elements:   {wc_raw['Element Name'].nunique()}")

    print("[data_prep_workcontext] Filtering and cleaning...")
    wc_clean = clean_work_context(wc_raw)
    print(f"  After CX/CT filter, suppress drop, NR drop: {len(wc_clean):,}")
    print(f"  Unique elements kept: {wc_clean['element_short'].nunique()} "
          f"(target: {len(ELEMENTS_TO_KEEP)})")
    missing_elements = set(ELEMENTS_TO_KEEP.keys()) - set(wc_clean["element_name"])
    if missing_elements:
        print(f"  WARNING: target elements not found in data: {missing_elements}")

    print("[data_prep_workcontext] Aggregating to 6-digit BLS SOC...")
    agg = aggregate_to_bls_soc(wc_clean)
    print(f"  Aggregated rows: {len(agg):,}")
    print(f"  Unique BLS SOCs: {agg['soc_code'].nunique()}")

    print("[data_prep_workcontext] Pivoting to wide format...")
    wide = pivot_to_wide(agg)
    print(f"  Wide-format rows: {len(wide):,}")
    print(f"  Element coverage stats:")
    for col in ELEMENTS_TO_KEEP.values():
        if col in wide.columns:
            non_null = wide[col].notna().sum()
            print(f"    {col:<32} {non_null:>4} / {len(wide):>4} SOCs "
                  f"({non_null / len(wide) * 100:.0f}%)")

    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    wide.to_csv(WORK_CONTEXT_OUTPUT_PATH, index=False)
    print(f"[data_prep_workcontext] Wrote {WORK_CONTEXT_OUTPUT_PATH}")
    print("[data_prep_workcontext] Done.")


if __name__ == "__main__":
    main()
