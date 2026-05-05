"""Tests for Phase 11.3.1 BLS OEWS NAICS-by-SOC data prep.

Validates the cleaned soc_to_naics3.csv output produced by
build_soc_to_naics3() in data_prep_majors.py.
"""
from pathlib import Path

import pandas as pd
import pytest


CLEANED_PATH = Path("data/cleaned/soc_to_naics3.csv")


@pytest.fixture(scope="module")
def soc_to_naics3() -> pd.DataFrame:
    """Load the cleaned dataset for all tests."""
    assert CLEANED_PATH.exists(), (
        f"{CLEANED_PATH} not found. Run "
        "`python data_prep_majors.py` to build it."
    )
    return pd.read_csv(
        CLEANED_PATH,
        dtype={"naics3": str, "soc_code": str},
    )


def test_expected_columns(soc_to_naics3):
    """Output has the exact expected schema."""
    expected = {
        "soc_code", "soc_title", "naics3", "naics3_title",
        "tot_emp", "share_in_naics3",
    }
    assert set(soc_to_naics3.columns) == expected


def test_expected_shape(soc_to_naics3):
    """Row count and uniqueness match the verified-by-hand baseline.

    Tolerances are generous because future BLS releases may shift these
    by a few percent; we want to catch order-of-magnitude regressions,
    not noise.
    """
    assert 16_000 < len(soc_to_naics3) < 19_000, (
        f"Row count {len(soc_to_naics3)} outside expected range. "
        "Baseline (May 2024 release): 17,285."
    )
    n_socs = soc_to_naics3["soc_code"].nunique()
    n_naics = soc_to_naics3["naics3"].nunique()
    assert 800 < n_socs < 870, f"Got {n_socs} SOCs, baseline is 830"
    assert 80 < n_naics < 90, f"Got {n_naics} NAICS3, baseline is 85"


def test_naics3_codes_are_three_chars(soc_to_naics3):
    """3-digit NAICS codes are stored as 3-character strings."""
    assert (soc_to_naics3["naics3"].str.len() == 3).all()


def test_no_suppression_markers_leaked(soc_to_naics3):
    """Suppression markers ('**') were dropped, not coerced to NaN/0."""
    assert soc_to_naics3["tot_emp"].dtype.kind == "i", (
        f"tot_emp should be integer, got {soc_to_naics3['tot_emp'].dtype}"
    )
    assert (soc_to_naics3["tot_emp"] > 0).all(), (
        "All tot_emp should be positive (suppressed rows dropped)"
    )


def test_shares_sum_to_one_per_soc(soc_to_naics3):
    """Within each SOC, the NAICS shares sum to 1.0 by construction."""
    share_sums = soc_to_naics3.groupby("soc_code")["share_in_naics3"].sum()
    # Allow 1e-6 tolerance for float rounding
    assert (share_sums - 1.0).abs().max() < 1e-6, (
        f"Share sums deviate from 1.0: max deviation = "
        f"{(share_sums - 1.0).abs().max()}"
    )


def test_software_developers_top_naics_is_541(soc_to_naics3):
    """Software Developers (15-1252) — NAICS 541 (Professional/Scientific/
    Technical Services) should be the #1 industry by share."""
    sd_top = soc_to_naics3[soc_to_naics3["soc_code"] == "15-1252"].iloc[0]
    assert sd_top["naics3"] == "541", (
        f"Expected Software Devs #1 NAICS = 541, got {sd_top['naics3']}"
    )
    # Should be ~0.42; allow wide tolerance for future releases
    assert 0.30 < sd_top["share_in_naics3"] < 0.55


def test_registered_nurses_top_naics_is_622(soc_to_naics3):
    """Registered Nurses (29-1141) — NAICS 622 (Hospitals) should be the
    #1 industry by share."""
    rn_top = soc_to_naics3[soc_to_naics3["soc_code"] == "29-1141"].iloc[0]
    assert rn_top["naics3"] == "622", (
        f"Expected RN #1 NAICS = 622, got {rn_top['naics3']}"
    )
    # Should be ~0.60; allow wide tolerance
    assert 0.50 < rn_top["share_in_naics3"] < 0.70


def test_government_naics_999_is_present(soc_to_naics3):
    """NAICS 999 (Federal/State/Local Govt) is a legitimate industry in
    this dataset — make sure we didn't accidentally drop it."""
    assert "999" in set(soc_to_naics3["naics3"].unique())


def test_no_six_digit_naics_leaked(soc_to_naics3):
    """We extract 3-digit NAICS from a 6-digit-padded source. Verify no
    6-digit values leaked through."""
    assert not soc_to_naics3["naics3"].str.len().eq(6).any()
