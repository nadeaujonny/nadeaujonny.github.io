"""Tests for Phase 11.3.2 CIP4-to-NAICS3 distribution data prep.

Validates the cleaned cip4_naics3_distribution.csv output produced by
build_cip4_naics3_distribution() in data_prep_majors.py.
"""
from pathlib import Path

import pandas as pd
import pytest


CIP4_DIST_PATH = Path("data/cleaned/cip4_naics3_distribution.csv")


@pytest.fixture(scope="module")
def cip4_naics3_dist() -> pd.DataFrame:
    """Load the CIP4-aggregated NAICS distribution for all tests."""
    assert CIP4_DIST_PATH.exists(), (
        f"{CIP4_DIST_PATH} not found. Run "
        "`python data_prep_majors.py` to build it."
    )
    return pd.read_csv(
        CIP4_DIST_PATH,
        dtype={"cip4": str, "naics3": str},
    )


def test_cip4_dist_expected_columns(cip4_naics3_dist):
    """CIP4 distribution has the exact expected schema."""
    expected = {"cip4", "naics3", "naics3_title", "weighted_emp", "share_in_naics3"}
    assert set(cip4_naics3_dist.columns) == expected


def test_cip4_dist_expected_shape(cip4_naics3_dist):
    """Row count, CIP4 count, NAICS3 count match the verified baseline."""
    assert 18_000 < len(cip4_naics3_dist) < 20_000, (
        f"Row count {len(cip4_naics3_dist)} outside expected range. "
        "Baseline (May 2024 BLS + current routing): 18,980."
    )
    n_cip4 = cip4_naics3_dist["cip4"].nunique()
    n_naics = cip4_naics3_dist["naics3"].nunique()
    assert 410 < n_cip4 < 420, f"Got {n_cip4} CIP4s, baseline is 414"
    assert 80 < n_naics < 90, f"Got {n_naics} NAICS3, baseline is 85"


def test_cip4_dist_shares_sum_to_one(cip4_naics3_dist):
    """Within each CIP4, NAICS shares sum to 1.0 by construction."""
    share_sums = cip4_naics3_dist.groupby("cip4")["share_in_naics3"].sum()
    assert (share_sums - 1.0).abs().max() < 1e-6, (
        f"Share sums deviate from 1.0: max deviation = "
        f"{(share_sums - 1.0).abs().max()}"
    )


def test_cip4_dist_naics3_format(cip4_naics3_dist):
    """3-digit NAICS codes are stored as 3-character strings."""
    assert (cip4_naics3_dist["naics3"].str.len() == 3).all()


def test_cip4_dist_cip4_format(cip4_naics3_dist):
    """CIP4 codes use the XX.XX convention (5 chars including the period)."""
    assert (cip4_naics3_dist["cip4"].str.len() == 5).all()
    assert (cip4_naics3_dist["cip4"].str[2] == ".").all()


def test_computer_science_top_naics_is_541(cip4_naics3_dist):
    """Computer Science (11.07) — NAICS 541 (Prof/Sci/Tech Services) #1."""
    cs = cip4_naics3_dist[cip4_naics3_dist["cip4"] == "11.07"].iloc[0]
    assert cs["naics3"] == "541", (
        f"Expected CS top NAICS = 541, got {cs['naics3']}"
    )
    assert 0.30 < cs["share_in_naics3"] < 0.45


def test_registered_nursing_top_naics_is_622(cip4_naics3_dist):
    """Registered Nursing (51.38) — NAICS 622 (Hospitals) #1."""
    rn = cip4_naics3_dist[cip4_naics3_dist["cip4"] == "51.38"].iloc[0]
    assert rn["naics3"] == "622"
    assert 0.45 < rn["share_in_naics3"] < 0.60


def test_education_general_is_pure_611(cip4_naics3_dist):
    """Education General (13.01) — single-SOC routing edge case, should
    be 100% in NAICS 611 (Educational Services)."""
    ed = cip4_naics3_dist[cip4_naics3_dist["cip4"] == "13.01"]
    assert len(ed) == 1, f"Expected 13.01 to have 1 NAICS row, got {len(ed)}"
    assert ed.iloc[0]["naics3"] == "611"
    assert abs(ed.iloc[0]["share_in_naics3"] - 1.0) < 1e-6


def test_military_tech_cip4s_have_no_distribution(cip4_naics3_dist):
    """Military Technologies CIP4s 28.05 and 28.06 have all routing SOCs
    missing from BLS detailed-level data — they correctly drop out of
    the aggregation. This is the canonical empty-state CIP4 case for
    Phase 11.3.3 to handle."""
    for cip in ["28.05", "28.06"]:
        assert (cip4_naics3_dist["cip4"] == cip).sum() == 0, (
            f"Expected CIP {cip} to be absent (no NAICS data), but rows present"
        )


def test_petroleum_engineering_routing_dilution_visible(cip4_naics3_dist):
    """Petroleum Engineering (14.25) — the routing table includes
    25-1032 (Engineering Teachers) which is a large educator SOC, so
    NAICS 611 (Education) should appear in the top 5 for this CIP4
    despite Petroleum Engineering having nothing to do with education.
    This is the same routing-dilution pattern Phase 10.4 documented for
    state-level Location Quotients. Sanity check that the math behaves
    as expected."""
    pe = cip4_naics3_dist[cip4_naics3_dist["cip4"] == "14.25"].head(5)
    top5_naics = set(pe["naics3"].tolist())
    assert "611" in top5_naics, (
        f"Expected NAICS 611 (Education) in Petroleum Engineering top 5 "
        f"due to routing dilution, got: {top5_naics}"
    )
