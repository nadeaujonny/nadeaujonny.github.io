"""
data_prep_riasec.py — Phase 12.1 data prep for O*NET RIASEC interest scores.

Reads O*NET Interests.xlsx from data/raw/, filters to Occupational Interest
(Scale ID == 'OI') rows, aggregates the six RIASEC dimensions from O*NET-SOC
to CIP4 level using employment-weighted averaging, and writes:

    data/cleaned/cip4_riasec.csv

Weighting: BLS OEWS total employment from occupations_master.csv (not present
in cip4_to_soc.csv). SOCs that are missing from occupations_master.csv fall
back to a weight of 1 (equal weighting for that SOC). SOCs missing from the
Interests file are skipped; coverage_pct reflects how many routing SOCs
contributed to each CIP4's scores.

Run from project root:
    python data_prep_riasec.py
"""

from pathlib import Path

import pandas as pd

from config import RIASEC_DIMENSIONS

RAW_DIR = Path("data/raw")
CLEANED_DIR = Path("data/cleaned")

INTERESTS_PATH = RAW_DIR / "Interests.xlsx"
ROUTING_PATH = CLEANED_DIR / "cip4_to_soc.csv"
EMPLOYMENT_PATH = CLEANED_DIR / "occupations_master.csv"
OUTPUT_PATH = CLEANED_DIR / "cip4_riasec.csv"

_ELEMENT_TO_DIM: dict[str, str] = {
    "Realistic": "R",
    "Investigative": "I",
    "Artistic": "A",
    "Social": "S",
    "Enterprising": "E",
    "Conventional": "C",
}


def load_interests() -> pd.DataFrame:
    """Load Interests.xlsx and filter to Occupational Interest (OI) rows.

    Returns long-format DataFrame with one row per (O*NET-SOC code, RIASEC
    dimension). High-point rows (Scale ID == 'IH') are dropped.
    """
    df = pd.read_excel(INTERESTS_PATH, dtype=str)
    df = df[df["Scale ID"] == "OI"].copy()
    df["Data Value"] = pd.to_numeric(df["Data Value"], errors="coerce")
    df = df[df["Data Value"].notna()].copy()
    return df


def aggregate_to_bls_soc(interests: pd.DataFrame) -> pd.DataFrame:
    """Collapse O*NET-SOC variants to 6-digit BLS SOC and pivot to wide format.

    O*NET-SOC codes are 8-digit ('15-1252.00'); BLS SOC2018 codes are 6-digit
    ('15-1252'). Some BLS SOCs map to multiple O*NET-SOC variants. We take the
    simple mean across variants within each (BLS SOC, RIASEC dimension) pair —
    Interests.xlsx does not include sample sizes, so equal-variant weighting is
    the only option at this stage.

    Returns wide DataFrame: one row per BLS SOC, columns soc_code + R/I/A/S/E/C.
    """
    df = interests.copy()
    df["soc_code"] = df["O*NET-SOC Code"].str.split(".").str[0]
    df["dim"] = df["Element Name"].map(_ELEMENT_TO_DIM)
    df = df[df["dim"].notna()].copy()

    agg = (
        df.groupby(["soc_code", "dim"])["Data Value"]
        .mean()
        .reset_index()
    )

    wide = agg.pivot(index="soc_code", columns="dim", values="Data Value")
    wide = wide.reindex(columns=RIASEC_DIMENSIONS).reset_index()
    wide.columns.name = None
    return wide


def load_routing_table() -> pd.DataFrame:
    """Load the CIP4-to-SOC routing table (cip4_to_soc.csv).

    Returns DataFrame with cip4 (dot-format string) and SOC2018Code columns.
    """
    return pd.read_csv(
        ROUTING_PATH,
        dtype={"cip4": str, "SOC2018Code": str},
    )


def load_employment_weights() -> pd.DataFrame:
    """Load BLS OEWS total employment per SOC from occupations_master.csv.

    Returns DataFrame with soc_code and total_employment_oews. Used as the
    aggregation weight; SOCs absent from this file receive weight = 1.
    """
    df = pd.read_csv(EMPLOYMENT_PATH, dtype={"soc_code": str})
    return df[["soc_code", "total_employment_oews"]].copy()


def aggregate_to_cip4(
    soc_wide: pd.DataFrame,
    routing: pd.DataFrame,
    employment: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate SOC-level RIASEC scores to CIP4 level.

    For each CIP4, computes the employment-weighted average of each RIASEC
    dimension across routing SOCs that have Interests data. SOCs without
    Interests data are excluded from the weighted sum; coverage_pct records
    the fraction that did contribute.

    Args:
        soc_wide: output of aggregate_to_bls_soc() — wide, one row per SOC.
        routing: CIP4-to-SOC crosswalk from cip4_to_soc.csv.
        employment: total_employment_oews per SOC from occupations_master.csv.

    Returns:
        DataFrame with columns: cip4, R, I, A, S, E, C, n_socs, coverage_pct.
        Includes CIP4s with 0% coverage (empty-state cases) so the loader in
        Phase 12.1d can return None for them.
    """
    merged = (
        routing
        .merge(employment, left_on="SOC2018Code", right_on="soc_code", how="left")
        .merge(soc_wide, left_on="SOC2018Code", right_on="soc_code", how="left")
    )

    missing_riasec = merged[merged["R"].isna()]["SOC2018Code"].unique()
    if len(missing_riasec) > 0:
        print(f"  {len(missing_riasec)} SOCs in routing table have no RIASEC data "
              f"(excluded from weighted averages)")

    rows: list[dict] = []
    for cip4, group in merged.groupby("cip4"):
        n_total = len(group)
        has_data = group["R"].notna()
        n_with_data = int(has_data.sum())
        coverage_pct = 100.0 * n_with_data / n_total if n_total > 0 else 0.0

        if n_with_data == 0:
            rows.append({
                "cip4": cip4,
                **{d: float("nan") for d in RIASEC_DIMENSIONS},
                "n_socs": 0,
                "coverage_pct": 0.0,
            })
            continue

        sub = group[has_data].copy()
        weights = sub["total_employment_oews"].fillna(1.0)
        weight_sum = float(weights.sum())
        if weight_sum == 0.0:
            weights = pd.Series(1.0, index=sub.index)
            weight_sum = float(len(sub))

        row: dict = {"cip4": cip4, "n_socs": n_with_data, "coverage_pct": coverage_pct}
        for dim in RIASEC_DIMENSIONS:
            row[dim] = float((sub[dim] * weights).sum() / weight_sum)
        rows.append(row)

    out = pd.DataFrame(rows)[["cip4", *RIASEC_DIMENSIONS, "n_socs", "coverage_pct"]]
    return out


def build_cip4_riasec() -> None:
    """Build cip4_riasec.csv. Public entry point; called from __main__."""
    print("[data_prep_riasec] Loading Interests.xlsx (OI rows only)...")
    interests = load_interests()
    print(f"  OI rows:               {len(interests):,}")
    print(f"  Unique O*NET-SOC codes: {interests['O*NET-SOC Code'].nunique()}")

    print("[data_prep_riasec] Aggregating to BLS SOC, pivoting to wide format...")
    soc_wide = aggregate_to_bls_soc(interests)
    print(f"  Unique BLS SOCs with RIASEC: {len(soc_wide)}")

    print("[data_prep_riasec] Loading routing table and employment weights...")
    routing = load_routing_table()
    employment = load_employment_weights()
    print(f"  Routing table: {len(routing):,} rows, {routing['cip4'].nunique()} CIP4s, "
          f"{routing['SOC2018Code'].nunique()} unique SOCs")
    print(f"  Employment data: {len(employment)} SOCs")

    print("[data_prep_riasec] Aggregating to CIP4 level...")
    cip4_riasec = aggregate_to_cip4(soc_wide, routing, employment)

    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    cip4_riasec.to_csv(OUTPUT_PATH, index=False)

    n_total = len(cip4_riasec)
    n_full = int((cip4_riasec["coverage_pct"] == 100.0).sum())
    n_zero = int((cip4_riasec["coverage_pct"] == 0.0).sum())
    mean_cov = float(cip4_riasec["coverage_pct"].mean())
    n_socs_desc = cip4_riasec["n_socs"].describe()

    print(f"\n[data_prep_riasec] Summary:")
    print(f"  Total CIP4s:          {n_total}")
    print(f"  100% coverage:        {n_full} ({100 * n_full / n_total:.1f}%)")
    print(f"  0% coverage (empty):  {n_zero}")
    print(f"  Mean coverage_pct:    {mean_cov:.1f}%")
    print(f"  n_socs  min={n_socs_desc['min']:.0f}  "
          f"median={n_socs_desc['50%']:.0f}  "
          f"max={n_socs_desc['max']:.0f}")

    if n_zero > 0:
        zero_cips = cip4_riasec[cip4_riasec["coverage_pct"] == 0.0]["cip4"].tolist()
        print(f"  0%-coverage CIP4s (empty-state cases for Phase 12.3): {zero_cips}")

    print(f"\n  {OUTPUT_PATH} — {n_total} rows × {len(cip4_riasec.columns)} cols, "
          f"mean coverage {mean_cov:.1f}%, {n_full} CIP4s at 100%")
    print("[data_prep_riasec] Done.")


if __name__ == "__main__":
    build_cip4_riasec()
