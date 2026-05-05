"""
data_prep.py — Transform raw federal data files into app-ready cleaned CSVs.

Run this once after placing the raw files into data/raw/. It produces:

  data/cleaned/colleges_cleaned.csv         (Phase 1 core — required)
  data/cleaned/field_of_study_cleaned.csv   (Phase 1 optional — skipped if raw missing)
  data/cleaned/campus_safety_cleaned.csv    (Phase 4 — skipped if raw missing)
  data/cleaned/trends.csv                   (Phase 4 — skipped if raw missing)
  data/cleaned/zip_lat_long_cleaned.csv     (Phase 4 — skipped if raw missing)

Each section is self-contained. Running the script is idempotent: existing
cleaned files are overwritten.

Usage:
    python data_prep.py
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

import config

# Pandas emits a mixed-dtype warning for the raw Scorecard file because a
# few columns contain both numbers and the string "PrivacySuppressed".
# We handle that explicitly below, so silence the warning for readability.
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)


# ============================================================
# HELPERS
# ============================================================
def to_numeric_safe(s: pd.Series) -> pd.Series:
    """
    Convert a column to numeric, treating 'PrivacySuppressed', 'NULL', and
    empty strings as NaN. Preserves the original dtype when no conversion
    is needed.
    """
    return pd.to_numeric(s, errors="coerce")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    print(msg, flush=True)


# ============================================================
# STEP 1 — INSTITUTION-LEVEL CLEAN
# ============================================================
def clean_institutions() -> pd.DataFrame:
    """
    Load the Most-Recent-Cohorts-Institution.csv, keep only the columns
    we use, rename them, filter to relevant institutions, and derive the
    helper columns the app expects.
    """
    raw_path = config.DATA_RAW_DIR / config.RAW_SCORECARD_CURRENT
    if not raw_path.exists():
        log(f"ERROR: {raw_path} not found.")
        log("Place the Most-Recent-Cohorts-Institution.csv file in data/raw/ and retry.")
        sys.exit(1)

    # Keep only the columns we actually need. Reading 3,306 columns wastes
    # memory; this drops the file to something much smaller to work with.
    keep_cols = list(config.SCORECARD_COLUMN_RENAMES.keys())
    # CIP columns live in the field-of-study file, not here. Drop them from the
    # keep list if they appear in the institution-level rename map.
    keep_cols = [c for c in keep_cols if c not in ("CIPCODE", "CIPDESC")]

    log(f"Loading {raw_path.name} (keeping {len(keep_cols)} of 3,306 columns)...")
    df = pd.read_csv(
        raw_path,
        usecols=lambda c: c in keep_cols,
        low_memory=False,
        na_values=["PrivacySuppressed", "NULL", "", "NaN"],
    )
    log(f"  Loaded {len(df):,} rows.")

    # Rename to snake_case
    df = df.rename(columns=config.SCORECARD_COLUMN_RENAMES)

    # ------------------------------------------------------------
    # Type coercion for numeric fields
    # ------------------------------------------------------------
    numeric_cols = [
        "admission_rate", "sat_avg", "act_median",
        "sat_verbal_25", "sat_verbal_75", "sat_math_25", "sat_math_75",
        "tuition_in_state", "tuition_out_of_state",
        "net_price_public", "net_price_private",
        "net_price_public_0_30k", "net_price_public_30_48k",
        "net_price_public_48_75k", "net_price_public_75_110k",
        "net_price_public_110k_plus",
        "net_price_private_0_30k", "net_price_private_30_48k",
        "net_price_private_48_75k", "net_price_private_75_110k",
        "net_price_private_110k_plus",
        "graduation_rate_4yr", "graduation_rate_less_4yr",
        "completion_100pct_4yr",
        "retention_rate_4yr", "retention_rate_less_4yr",
        "median_earnings_10yr", "mean_earnings_10yr", "median_earnings_6yr",
        "median_debt", "median_debt_supp",
        "enrollment", "latitude", "longitude",
        # Demographics
        "pct_women", "pct_black", "pct_hispanic", "pct_asian", "pct_white",
        "pct_nonresident", "pct_pell", "pct_federal_loan",
        "pct_age_25_plus", "pct_part_time",
        # Outcomes
        "earnings_sample_size_10yr", "pct_earning_above_25k_10yr",
        "pct_earning_above_hs_median_10yr", "repayment_rate_3yr", "default_rate_3yr",
        # Earnings mobility
        "mean_earnings_low_income_10yr", "mean_earnings_mid_income_10yr",
        "mean_earnings_high_income_10yr",
        # Faculty / instruction
        "instruction_spend_per_fte", "avg_faculty_salary",
        "pct_full_time_faculty", "net_tuition_per_fte",
        # Selectivity / mission
        "test_score_policy", "carnegie_basic", "religious_affiliation",
        "is_hbcu", "is_pbi", "is_hsi", "is_aanapii",
        "is_annhi", "is_tribal", "is_nanti",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = to_numeric_safe(df[col])

    # ------------------------------------------------------------
    # Filter to the universe of institutions the app should surface
    # ------------------------------------------------------------
    before = len(df)

    # Keep only 4-year institutions (ICLEVEL == 1). Two-year and less-than-two-year
    # schools are a different population with different decision criteria — out
    # of scope for this app's audience (4-year-college-bound students).
    df = df[df["institution_level"] == 1].copy()

    # Drop schools with no name (data errors)
    df = df.dropna(subset=["school_name"])

    # Drop schools with no enrollment reported at all — they're usually closed
    # or only offer graduate programs, neither of which fits this app.
    df = df.dropna(subset=["enrollment"])
    df = df[df["enrollment"] > 0]

    log(f"  Filtered to 4-year institutions with reported enrollment: {len(df):,} rows "
        f"(dropped {before - len(df):,}).")

    # 250-enrollment floor moved to app.py runtime toggle (Step A).
    # All 4-year schools with reported enrollment > 0 are retained here.
    log(f"  Keeping all {len(df):,} rows with reported enrollment > 0 "
        f"(250-student floor applied at runtime via sidebar toggle).")

    # ------------------------------------------------------------
    # Derived columns
    # ------------------------------------------------------------
    # Control label (public / private nonprofit / private for-profit)
    df["control_label"] = df["control"].map(config.CONTROL_LABELS)

    # Campus setting from LOCALE
    df["setting"] = df["locale"].map(config.LOCALE_TO_SETTING)

    # Size bucket
    df["size_bucket"] = df["enrollment"].apply(config.enrollment_to_size)

    # ------------------------------------------------------------
    # Unified "net_price" — pick public or private net price based on control
    # ------------------------------------------------------------
    df["net_price"] = np.where(
        df["control"] == 1,                       # public
        df["net_price_public"],
        df["net_price_private"],                  # private nonprofit or for-profit
    )

    # ------------------------------------------------------------
    # Unified "graduation_rate" and "retention_rate" — pick 4yr or less-than-4yr
    # version based on institution_level. Since we already filtered to 4-year
    # schools, the 4yr columns apply universally. But we keep this robust for
    # later if we expand scope.
    # ------------------------------------------------------------
    df["graduation_rate"] = np.where(
        df["institution_level"] == 1,
        df["graduation_rate_4yr"],
        df["graduation_rate_less_4yr"],
    )
    df["retention_rate"] = np.where(
        df["institution_level"] == 1,
        df["retention_rate_4yr"],
        df["retention_rate_less_4yr"],
    )

    # ------------------------------------------------------------
    # Tuition: pick in-state for public schools, out-of-state for private
    # (private schools charge the same regardless of residency)
    # ------------------------------------------------------------
    df["tuition"] = np.where(
        df["control"] == 1,
        df["tuition_in_state"],
        df["tuition_out_of_state"],
    )

    # ------------------------------------------------------------
    # Unified "median_debt" — prefer the suppressed-count-filtered version
    # when available (cohort >= 30 students), fall back to the unfiltered one
    # ------------------------------------------------------------
    if "median_debt_supp" in df.columns:
        df["median_debt"] = df["median_debt"].fillna(df["median_debt_supp"])

    # ------------------------------------------------------------
    # Derived label columns (Step A)
    # ------------------------------------------------------------
    def _map_code(val, mapping, default):
        if val is None or (isinstance(val, float) and val != val):
            return mapping.get(-2, default)  # treat NaN like -2 (not applicable)
        try:
            return mapping.get(int(val), default)
        except (ValueError, TypeError):
            return default

    df["test_policy_label"] = df["test_score_policy"].apply(
        lambda x: _map_code(x, config.ADMCON7_LABELS, "Unknown")
    )
    df["carnegie_label"] = df["carnegie_basic"].apply(
        lambda x: _map_code(x, config.CARNEGIE_BASIC_LABELS, "Other")
    )
    df["religion_label"] = df["religious_affiliation"].apply(
        lambda x: _map_code(x, config.RELIGIOUS_AFFIL_LABELS, "Other religious")
    )

    # Boolean: true if the school is any type of minority-serving institution
    _msi_cols = ["is_hbcu", "is_pbi", "is_hsi", "is_aanapii", "is_annhi", "is_tribal", "is_nanti"]
    _msi_present = [c for c in _msi_cols if c in df.columns]
    df["is_minority_serving"] = (
        df[_msi_present].fillna(0).eq(1).any(axis=1) if _msi_present else False
    )

    return df


def write_institutions(df: pd.DataFrame) -> None:
    out_path = config.DATA_CLEANED_DIR / config.CLEANED_COLLEGES
    ensure_dir(config.DATA_CLEANED_DIR)
    df.to_csv(out_path, index=False)
    log(f"  Wrote {out_path.relative_to(config.PROJECT_ROOT)}  ({len(df):,} rows, "
        f"{len(df.columns)} columns, {out_path.stat().st_size / 1_000_000:.1f} MB)")


# ============================================================
# STEP 2 — FIELD OF STUDY CLEAN
# ============================================================
def clean_field_of_study() -> None:
    raw_path = config.DATA_RAW_DIR / config.RAW_SCORECARD_FIELD_OF_STUDY
    if not raw_path.exists():
        log(f"  SKIP: {raw_path.name} not found — field-of-study data will be unavailable.")
        return

    # We only need a handful of columns from this file
    keep_cols_fos = [
        "UNITID", "INSTNM", "CIPCODE", "CIPDESC",
        "CREDLEV", "CREDDESC",
        "EARN_MDN_1YR", "EARN_MDN_4YR", "EARN_MDN_5YR",
        "DEBT_ALL_STGP_EVAL_MDN",  # median loan debt (all Title IV, any loan)
    ]

    log(f"Loading {raw_path.name}...")
    df = pd.read_csv(
        raw_path,
        usecols=lambda c: c in keep_cols_fos,
        low_memory=False,
        na_values=["PrivacySuppressed", "NULL", "", "NaN"],
    )
    log(f"  Loaded {len(df):,} rows.")

    df = df.rename(columns={
        "UNITID": "unit_id",
        "INSTNM": "school_name",
        "CIPCODE": "cip_code",
        "CIPDESC": "cip_description",
        "CREDLEV": "credential_level",
        "CREDDESC": "credential_label",
        "EARN_MDN_1YR": "median_earnings_1yr",
        "EARN_MDN_4YR": "median_earnings_4yr",
        "EARN_MDN_5YR": "median_earnings_5yr",
        "DEBT_ALL_STGP_EVAL_MDN": "median_debt",
    })

    # Keep only bachelor's degree programs (credlev == 3). Associate and
    # sub-baccalaureate programs are out of scope for this app's audience.
    if "credential_level" in df.columns:
        df = df[df["credential_level"] == 3].copy()
        log(f"  Filtered to bachelor's-level programs: {len(df):,} rows.")

    for col in ["median_earnings_1yr", "median_earnings_4yr", "median_earnings_5yr", "median_debt"]:
        if col in df.columns:
            df[col] = to_numeric_safe(df[col])

    out_path = config.DATA_CLEANED_DIR / config.CLEANED_FIELD_OF_STUDY
    df.to_csv(out_path, index=False)
    log(f"  Wrote {out_path.relative_to(config.PROJECT_ROOT)}  ({len(df):,} rows)")


# ============================================================
# DATA QUALITY REPORT
# ============================================================
def print_quality_report(df: pd.DataFrame) -> None:
    """Print a missingness summary for the columns the scoring engine uses."""
    log("\n--- Data Quality Report ---")
    log(f"Institutions kept: {len(df):,}")
    log(f"  By control: " + ", ".join(
        f"{label}: {count:,}"
        for label, count in df["control_label"].value_counts().items()
    ))
    log(f"  By setting: " + ", ".join(
        f"{label}: {count:,}"
        for label, count in df["setting"].value_counts(dropna=False).items()
    ))

    log("\nMissingness for key scoring columns:")
    scoring_cols = [
        "net_price", "graduation_rate", "retention_rate",
        "admission_rate", "sat_avg", "median_earnings_10yr",
        "median_debt", "latitude", "longitude",
    ]
    for col in scoring_cols:
        if col in df.columns:
            n_missing = df[col].isna().sum()
            pct = n_missing / len(df) * 100
            log(f"  {col:30s}  missing: {n_missing:>5,}  ({pct:5.1f}%)")

    # Spot-check: a couple of well-known schools should be present
    log("\nSpot-check — UCLA, UC Berkeley, Stanford, USC:")
    for name in ["University of California-Los Angeles",
                 "University of California-Berkeley",
                 "Stanford University",
                 "University of Southern California"]:
        match = df[df["school_name"] == name]
        if not match.empty:
            row = match.iloc[0]
            log(f"  {name}: enrollment={row['enrollment']:.0f}, "
                f"net_price=${row['net_price']:,.0f}"
                if pd.notna(row["net_price"]) else
                f"  {name}: enrollment={row['enrollment']:.0f}, net_price=N/A")
        else:
            log(f"  {name}: NOT FOUND")


# ============================================================
# STEP 3 — NY FED LABOR OUTCOMES PARQUET
# ============================================================
def build_nyfed_outcomes() -> pd.DataFrame:
    """
    Parse the NY Fed labor outcomes xlsx, join 5 metrics to CIP4 codes via
    data/nyfed_crosswalk.yaml, average duplicate CIP4s (50.07, 30.20), and
    write data/processed/nyfed_outcomes.parquet.
    """
    xlsx_path = config.DATA_RAW_DIR / "College-labor-data.xlsx"
    crosswalk_path = config.PROJECT_ROOT / "data" / "nyfed_crosswalk.yaml"
    out_path = config.PROJECT_ROOT / "data" / "processed" / "nyfed_outcomes.parquet"

    log(f"Loading {xlsx_path.name} (sheet: 'outcomes by major', header row 11)...")
    df = pd.read_excel(xlsx_path, sheet_name="outcomes by major", header=10)

    df = df[df["Major"] != "Overall"].copy()

    if len(df) != 73:
        raise ValueError(
            f"Expected 73 rows after dropping 'Overall', got {len(df)}. "
            "Check that the xlsx sheet structure hasn't changed."
        )

    expected_cols = [
        "Major",
        "Unemployment Rate",
        "Underemployment Rate",
        "Median Wage Early Career",
        "Median Wage Mid-Career",
        "Share with Graduate Degree",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns in xlsx: {missing}")

    with open(crosswalk_path, encoding="utf-8") as f:
        crosswalk = yaml.safe_load(f)

    metric_cols = [
        "Unemployment Rate",
        "Underemployment Rate",
        "Median Wage Early Career",
        "Median Wage Mid-Career",
        "Share with Graduate Degree",
    ]
    label_to_row = df.set_index("Major")

    rows = []
    for label, cip4s in crosswalk.items():
        if label not in label_to_row.index:
            log(f"  WARNING: NY Fed label '{label}' not found in xlsx — skipping")
            continue
        source = label_to_row.loc[label]
        for cip4 in cip4s:
            rows.append({"cip4": cip4, **{col: source[col] for col in metric_cols}})

    long_df = pd.DataFrame(rows)

    # Group by cip4 and average — collapses intentional duplicates (50.07, 30.20)
    agg_df = long_df.groupby("cip4")[metric_cols].mean().reset_index()

    agg_df = agg_df.rename(columns={
        "Unemployment Rate": "unemployment_rate",
        "Underemployment Rate": "underemployment_rate",
        "Median Wage Early Career": "median_wage_early_career",
        "Median Wage Mid-Career": "median_wage_mid_career",
        "Share with Graduate Degree": "share_with_graduate_degree",
    })

    ensure_dir(out_path.parent)
    agg_df.to_parquet(out_path, index=False)
    log(f"  Wrote {out_path.relative_to(config.PROJECT_ROOT)}  ({len(agg_df):,} rows, {len(agg_df.columns)} columns)")

    return agg_df


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    log("=" * 60)
    log("College Match Finder — Data Preparation")
    log("=" * 60)

    ensure_dir(config.DATA_CLEANED_DIR)

    # Institution-level
    log("\n[1/2] Cleaning institution-level Scorecard data...")
    institutions = clean_institutions()
    write_institutions(institutions)
    print_quality_report(institutions)

    # Field of Study
    log("\n[2/2] Cleaning field-of-study Scorecard data...")
    clean_field_of_study()

    # NY Fed labor outcomes
    log("\n[3/3] Building NY Fed labor outcomes parquet...")
    build_nyfed_outcomes()

    log("\n" + "=" * 60)
    log("Done.")
    log("=" * 60)


if __name__ == "__main__":
    main()
