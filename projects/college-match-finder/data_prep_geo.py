"""
data_prep_geo.py — Phase 10 data prep for state-level occupational employment.

Reads the BLS OEWS State May 2024 file from data/raw/ and produces one cleaned
CSV in data/cleaned/. See data/raw/RAW_DATA_NOTES.md for raw-file documentation.

Run from project root:
    python data_prep_geo.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW_DIR = Path("data/raw")
CLEANED_DIR = Path("data/cleaned")

OEWS_STATE_PATH = RAW_DIR / "state_M2024_dl.xlsx"
STATE_OCCUPATIONS_PATH = CLEANED_DIR / "state_occupations.csv"

# OEWS suppression sentinels — same as national file, see RAW_DATA_NOTES.md
OEWS_SUPPRESSION_VALUES = {"*", "**", "#"}

# Numeric columns in the state file (same set as national plus state-only columns)
OEWS_NUMERIC_COLUMNS = [
    "TOT_EMP", "EMP_PRSE", "JOBS_1000", "LOC_QUOTIENT", "PCT_TOTAL", "PCT_RPT",
    "H_MEAN", "A_MEAN", "MEAN_PRSE",
    "H_PCT10", "H_PCT25", "H_MEDIAN", "H_PCT75", "H_PCT90",
    "A_PCT10", "A_PCT25", "A_MEDIAN", "A_PCT75", "A_PCT90",
]


def _filter_state_df(df: pd.DataFrame) -> pd.DataFrame:
    """Filter a raw state OEWS DataFrame to cross-industry, detailed, state-level rows.

    Exposed as a module-level helper so tests can verify filter logic on synthetic
    DataFrames without reading the full ~37k-row Excel file.
    """
    mask = (
        (df["NAICS"] == "000000")
        & (df["O_GROUP"] == "detailed")
        & (df["AREA_TYPE"] == "2")
    )
    return df[mask].copy().reset_index(drop=True)


def load_oews_state() -> pd.DataFrame:
    """Load OEWS state May 2024, filter to detailed cross-industry SOCs.

    Returns one row per state-SOC pair (~36,367 rows after filtering).
    Suppression sentinels (*, **, #) are converted to NaN in numeric columns;
    all numeric columns are coerced to float.

    The state file uses the same column conventions as the national file plus
    state identifiers (AREA, AREA_TITLE, AREA_TYPE, PRIM_STATE) and the
    state-only metrics JOBS_1000 (jobs per 1,000), LOC_QUOTIENT (location
    quotient), PCT_TOTAL, PCT_RPT.
    """
    df = pd.read_excel(
        OEWS_STATE_PATH,
        header=0,
        dtype=str,
    )
    df = _filter_state_df(df)

    # Convert suppression sentinels to NaN, then coerce to numeric.
    # The defensive `if col in df.columns` guard handles any columns BLS may
    # have dropped or renamed in a future release without crashing the loader.
    for col in OEWS_NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = df[col].where(
                ~df[col].isin(OEWS_SUPPRESSION_VALUES),
                other=np.nan,
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def build_state_occupations(state: pd.DataFrame) -> pd.DataFrame:
    """Select and rename columns for the cleaned state-occupations table.

    Output: one row per state-SOC, with state identifiers, employment, location
    quotient, and wage data. Designed to be used by Phase 10.3's CIP4-level
    routing-employment aggregation.

    Args:
        state: output of load_oews_state()

    Returns:
        DataFrame ready to write to data/cleaned/state_occupations.csv
    """
    df = state[[
        "AREA", "AREA_TITLE", "PRIM_STATE",
        "OCC_CODE", "OCC_TITLE",
        "TOT_EMP", "JOBS_1000", "LOC_QUOTIENT",
        "A_MEDIAN", "A_MEAN",
        "A_PCT10", "A_PCT25", "A_PCT75", "A_PCT90",
        "H_MEDIAN", "H_MEAN",
    ]].rename(columns={
        "AREA": "state_fips",
        "AREA_TITLE": "state_name",
        "PRIM_STATE": "state_abbr",
        "OCC_CODE": "soc_code",
        "OCC_TITLE": "occupation_title",
        "TOT_EMP": "total_employment",
        "JOBS_1000": "jobs_per_1000",
        "LOC_QUOTIENT": "location_quotient",
        "A_MEDIAN": "annual_median",
        "A_MEAN": "annual_mean",
        "A_PCT10": "annual_pct10",
        "A_PCT25": "annual_pct25",
        "A_PCT75": "annual_pct75",
        "A_PCT90": "annual_pct90",
        "H_MEDIAN": "hourly_median",
        "H_MEAN": "hourly_mean",
    })

    column_order = [
        "state_fips", "state_abbr", "state_name",
        "soc_code", "occupation_title",
        "total_employment", "location_quotient", "jobs_per_1000",
        "annual_median", "annual_mean",
        "annual_pct10", "annual_pct25", "annual_pct75", "annual_pct90",
        "hourly_median", "hourly_mean",
    ]
    df = df[column_order].sort_values(["state_fips", "soc_code"]).reset_index(drop=True)
    return df


def main() -> None:
    """Run the geo data-prep pipeline."""
    print("[data_prep_geo] Loading state OEWS file...")
    state = load_oews_state()
    print(f"  State rows (detailed cross-industry): {len(state):,}")
    print(f"  Unique states: {state['AREA_TITLE'].nunique()}")
    print(f"  Unique SOCs:   {state['OCC_CODE'].nunique()}")
    print(f"  Suppression rate (TOT_EMP NaN): "
          f"{state['TOT_EMP'].isna().mean() * 100:.1f}%")
    print(f"  Suppression rate (LOC_QUOTIENT NaN): "
          f"{state['LOC_QUOTIENT'].isna().mean() * 100:.1f}%")

    print("[data_prep_geo] Building cleaned state-occupations table...")
    cleaned = build_state_occupations(state)
    print(f"  cleaned rows: {len(cleaned):,}")
    print(f"  Colorado rows present: "
          f"{(cleaned['state_name'] == 'Colorado').sum()}")

    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(STATE_OCCUPATIONS_PATH, index=False)
    print(f"[data_prep_geo] Wrote {STATE_OCCUPATIONS_PATH}")
    print("[data_prep_geo] Done.")


if __name__ == "__main__":
    main()
