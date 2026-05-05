"""
test_crosswalk.py — Guards for data/nyfed_crosswalk.yaml structure and the
nyfed_outcomes.parquet produced by build_nyfed_outcomes().

Verifies parse, coverage, intentional-duplicate invariants, and parquet output
correctness so future hand-edits to the YAML or xlsx can't silently break things.
"""

import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
import yaml

from nyfed_outcomes import get_nyfed_outcomes

DATA_DIR = Path(__file__).parent.parent / "data"
CROSSWALK_PATH = DATA_DIR / "nyfed_crosswalk.yaml"
MAJOR_DESC_PATH = DATA_DIR / "major_descriptions.yaml"
NYFED_PARQUET_PATH = DATA_DIR / "processed" / "nyfed_outcomes.parquet"
NYFED_XLSX_PATH = DATA_DIR / "raw" / "College-labor-data.xlsx"

CIP4_PATTERN = re.compile(r"^\d{2}\.\d{2}$")


def _load_crosswalk():
    with open(CROSSWALK_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _all_crosswalk_cip4s(crosswalk):
    """Return set of all unique CIP4 values across all NY Fed labels."""
    return {cip4 for cip4s in crosswalk.values() for cip4 in cip4s}


def test_crosswalk_loads():
    crosswalk = _load_crosswalk()
    assert isinstance(crosswalk, dict), "YAML should parse to a dict"
    assert len(crosswalk) == 73, f"Expected 73 NY Fed labels, got {len(crosswalk)}"


def test_top60_majors_all_covered():
    with open(MAJOR_DESC_PATH, encoding="utf-8") as f:
        major_desc = yaml.safe_load(f)
    crosswalk = _load_crosswalk()
    all_cip4s = _all_crosswalk_cip4s(crosswalk)
    missing = [cip4 for cip4 in major_desc if cip4 not in all_cip4s]
    assert not missing, f"CIP4s in major_descriptions.yaml not in crosswalk: {missing}"


def test_intentional_duplicates_only():
    crosswalk = _load_crosswalk()
    cip4_to_labels = defaultdict(list)
    for label, cip4s in crosswalk.items():
        for cip4 in cip4s:
            cip4_to_labels[cip4].append(label)
    duplicates = {cip4 for cip4, labels in cip4_to_labels.items() if len(labels) >= 2}
    assert duplicates == {"30.20", "50.07"}, (
        f"Expected exactly {{'30.20', '50.07'}} as duplicates, got {duplicates}"
    )


# ============================================================
# NY FED OUTCOMES PARQUET TESTS (Phase 11.2B.1)
# ============================================================

def test_nyfed_outcomes_parquet_exists_and_has_expected_shape():
    assert NYFED_PARQUET_PATH.exists(), (
        f"nyfed_outcomes.parquet not found at {NYFED_PARQUET_PATH}. "
        "Run build_nyfed_outcomes() to generate it."
    )
    df = pd.read_parquet(NYFED_PARQUET_PATH)
    assert 200 <= df.shape[0] <= 230, (
        f"Expected 200–230 rows (unique CIP4s), got {df.shape[0]}"
    )
    expected_cols = [
        "cip4",
        "unemployment_rate",
        "underemployment_rate",
        "median_wage_early_career",
        "median_wage_mid_career",
        "share_with_graduate_degree",
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing expected column: {col}"


def test_nyfed_outcomes_no_duplicate_cip4s_after_averaging():
    df = pd.read_parquet(NYFED_PARQUET_PATH)
    assert df["cip4"].is_unique, (
        f"Duplicate CIP4 codes found in parquet:\n"
        f"{df[df.duplicated('cip4', keep=False)]['cip4'].tolist()}"
    )


def test_nyfed_outcomes_50_07_is_averaged():
    raw = pd.read_excel(NYFED_XLSX_PATH, sheet_name="outcomes by major", header=10)
    metric_cols = [
        "Unemployment Rate",
        "Underemployment Rate",
        "Median Wage Early Career",
        "Median Wage Mid-Career",
        "Share with Graduate Degree",
    ]
    art_history = raw[raw["Major"] == "Art History"][metric_cols].iloc[0]
    fine_arts = raw[raw["Major"] == "Fine Arts"][metric_cols].iloc[0]
    expected = (art_history + fine_arts) / 2

    df = pd.read_parquet(NYFED_PARQUET_PATH)
    row = df[df["cip4"] == "50.07"]
    assert len(row) == 1, "Expected exactly one row for CIP4 50.07"
    r = row.iloc[0]

    assert abs(r["unemployment_rate"] - expected["Unemployment Rate"]) < 1e-6
    assert abs(r["underemployment_rate"] - expected["Underemployment Rate"]) < 1e-6
    assert abs(r["median_wage_early_career"] - expected["Median Wage Early Career"]) < 1e-6
    assert abs(r["median_wage_mid_career"] - expected["Median Wage Mid-Career"]) < 1e-6
    assert abs(r["share_with_graduate_degree"] - expected["Share with Graduate Degree"]) < 1e-6


# ============================================================
# NY FED OUTCOMES LOADER TESTS (Phase 11.2B.2)
# ============================================================

_EXPECTED_KEYS = {
    "unemployment_rate",
    "underemployment_rate",
    "median_wage_early_career",
    "median_wage_mid_career",
    "share_with_graduate_degree",
}


def test_get_nyfed_outcomes_hit_known_cip4():
    result = get_nyfed_outcomes("11.07")
    assert isinstance(result, dict), "Expected a dict for known CIP4 11.07"
    assert set(result.keys()) == _EXPECTED_KEYS, (
        f"Unexpected keys: {set(result.keys())}"
    )
    for key, val in result.items():
        assert isinstance(val, (int, float)) and val is not None, (
            f"Expected numeric value for {key}, got {val!r}"
        )


def test_get_nyfed_outcomes_miss_returns_none():
    result = get_nyfed_outcomes("99.99")
    assert result is None, f"Expected None for unknown CIP4 99.99, got {result!r}"


def test_get_nyfed_outcomes_averaged_cip4_matches_parquet():
    result = get_nyfed_outcomes("50.07")
    assert result is not None, "Expected a dict for averaged CIP4 50.07"
    df = pd.read_parquet(NYFED_PARQUET_PATH)
    row = df[df["cip4"] == "50.07"].iloc[0]
    assert abs(result["unemployment_rate"] - row["unemployment_rate"]) < 1e-6
    assert abs(result["underemployment_rate"] - row["underemployment_rate"]) < 1e-6
    assert abs(result["median_wage_early_career"] - row["median_wage_early_career"]) < 1e-6
    assert abs(result["median_wage_mid_career"] - row["median_wage_mid_career"]) < 1e-6
    assert abs(result["share_with_graduate_degree"] - row["share_with_graduate_degree"]) < 1e-6
