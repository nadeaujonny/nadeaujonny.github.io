"""
test_data_prep_majors.py — Tests for data_prep_majors.py.

Run with:
    pytest tests/ -v

Tests read the actual raw files in data/raw/ — same files used in production.
"""

import numpy as np
import pandas as pd
import pytest

from data_prep_majors import (
    load_crosswalk,
    load_oews,
    load_ep,
    aggregate_crosswalk_to_cip4,
    build_occupations_master,
    build_major_outcomes,
    build_cip4_state_employment,
    build_cip4_work_context,
    OEWS_SUPPRESSION_VALUES,
    EP_MISSING_VALUE,
)


# ============================================================
# load_crosswalk
# ============================================================

def test_load_crosswalk_dtype_is_string():
    """CIP codes must be strings, not floats. Floats corrupt leading zeros."""
    xwalk = load_crosswalk()
    # pandas 2.2+ on Python 3.13 returns StringDtype instead of object for
    # dtype=str; both are string-backed and correctly preserve leading zeros.
    assert pd.api.types.is_string_dtype(xwalk["CIP2020Code"])
    # Spot-check a code that would lose its leading zero as float
    assert "01.0000" in xwalk["CIP2020Code"].values


def test_load_crosswalk_row_count():
    xwalk = load_crosswalk()
    # 6097 total mappings minus the rows where SOC == '99-9999' (NO_MATCH)
    assert len(xwalk) > 5800  # Tolerance for any future minor revisions
    assert "99-9999" not in xwalk["SOC2018Code"].values


def test_load_crosswalk_known_mapping_computer_science():
    """CIP 11.0701 (Computer Science) maps to SOC 15-1252 (Software Developers)."""
    xwalk = load_crosswalk()
    cs_socs = xwalk[xwalk["CIP2020Code"] == "11.0701"]["SOC2018Code"].values
    assert "15-1252" in cs_socs


def test_load_crosswalk_known_mapping_mathematics():
    """CIP 27.0101 (Mathematics, General) maps to mathematicians and data scientists."""
    xwalk = load_crosswalk()
    math_socs = set(xwalk[xwalk["CIP2020Code"] == "27.0101"]["SOC2018Code"])
    assert {"15-2021", "15-2041", "15-2051"}.issubset(math_socs)


# ============================================================
# aggregate_crosswalk_to_cip4
# ============================================================

def test_aggregate_crosswalk_cip4_format():
    """4-digit CIP must be 5 characters (XX.XX)."""
    xwalk = load_crosswalk()
    agg = aggregate_crosswalk_to_cip4(xwalk)
    assert agg["cip4"].str.len().eq(5).all()


def test_aggregate_crosswalk_cip4_is_unique_per_soc():
    """Each (cip4, SOC) pair appears once after aggregation."""
    xwalk = load_crosswalk()
    agg = aggregate_crosswalk_to_cip4(xwalk)
    duplicates = agg.duplicated(subset=["cip4", "SOC2018Code"])
    assert not duplicates.any()


def test_aggregate_crosswalk_cip4_software_developers_in_1107():
    """CIP4 11.07 (Computer Science family) should include SOC 15-1252."""
    xwalk = load_crosswalk()
    agg = aggregate_crosswalk_to_cip4(xwalk)
    cs_family_socs = agg[agg["cip4"] == "11.07"]["SOC2018Code"].values
    assert "15-1252" in cs_family_socs


# ============================================================
# load_oews
# ============================================================

def test_load_oews_row_count():
    """OEWS filtered to cross-industry + detailed should yield exactly 831 rows."""
    oews = load_oews()
    assert len(oews) == 831
    assert oews["OCC_CODE"].nunique() == 831


def test_load_oews_filter_applied():
    """All rows must be cross-industry and detailed."""
    oews = load_oews()
    assert (oews["I_GROUP"] == "cross-industry").all()
    assert (oews["O_GROUP"] == "detailed").all()


def test_load_oews_numeric_columns_are_numeric():
    """Wage columns must be float, not str. Suppression strings become NaN."""
    oews = load_oews()
    assert pd.api.types.is_numeric_dtype(oews["A_MEDIAN"])
    assert pd.api.types.is_numeric_dtype(oews["TOT_EMP"])


def test_load_oews_software_developers_median_wage():
    """Software Developers (15-1252) should have $133,080 annual median wage."""
    oews = load_oews()
    sd = oews[oews["OCC_CODE"] == "15-1252"].iloc[0]
    assert sd["A_MEDIAN"] == 133080


def test_load_oews_no_suppression_strings_in_numeric():
    """Suppression sentinels must not appear as raw strings in numeric columns."""
    oews = load_oews()
    for col in ["A_MEDIAN", "A_MEAN", "TOT_EMP"]:
        for sentinel in OEWS_SUPPRESSION_VALUES:
            assert sentinel not in oews[col].astype(str).values


# ============================================================
# load_ep
# ============================================================

def test_load_ep_row_count():
    """EP filtered to line items should yield exactly 832 rows."""
    ep = load_ep()
    assert len(ep) == 832
    assert ep["soc_code"].nunique() == 832


def test_load_ep_renamed_columns():
    """Columns must use snake_case names."""
    ep = load_ep()
    expected_cols = {
        "soc_code", "occupation_title",
        "employment_2024", "employment_2034",
        "employment_change_numeric", "employment_change_percent",
        "annual_openings_avg", "percent_self_employed",
        "median_annual_wage_2024",
        "typical_education", "work_experience", "typical_training",
    }
    assert expected_cols.issubset(set(ep.columns))


def test_load_ep_em_dash_replaced():
    """Em-dash sentinel must not appear anywhere after cleaning."""
    ep = load_ep()
    for col in ep.columns:
        if ep[col].dtype == object:
            assert EP_MISSING_VALUE not in ep[col].dropna().values


def test_load_ep_numeric_columns():
    """Numeric columns must be float."""
    ep = load_ep()
    for col in ["employment_2024", "employment_change_percent", "median_annual_wage_2024"]:
        assert pd.api.types.is_numeric_dtype(ep[col])


def test_load_ep_software_developers_growth():
    """Software Developers projected to grow 15.8% from 2024 to 2034."""
    ep = load_ep()
    sd = ep[ep["soc_code"] == "15-1252"].iloc[0]
    assert sd["employment_change_percent"] == 15.8
    assert sd["typical_education"] == "Bachelor's degree"


def test_load_ep_occupation_title_stripped():
    """Occupation titles must not have leading/trailing whitespace."""
    ep = load_ep()
    for title in ep["occupation_title"]:
        assert title == title.strip()


# ============================================================
# build_occupations_master
# ============================================================

def test_occupations_master_row_count():
    """Master row count equals EP line-item count (832)."""
    oews = load_oews()
    ep = load_ep()
    master = build_occupations_master(oews, ep)
    assert len(master) == 832


def test_occupations_master_no_duplicate_socs():
    oews = load_oews()
    ep = load_ep()
    master = build_occupations_master(oews, ep)
    assert master["soc_code"].is_unique


def test_occupations_master_oews_wages_present_for_overlapping_soc():
    """For SOCs in both EP and OEWS, wage data must be populated."""
    oews = load_oews()
    ep = load_ep()
    master = build_occupations_master(oews, ep)
    sd = master[master["soc_code"] == "15-1252"].iloc[0]
    assert sd["annual_median"] == 133080
    assert sd["employment_change_percent"] == 15.8


def test_occupations_master_ep_only_soc_has_nan_wages():
    """SOC 45-3031 is in EP but not OEWS; wage columns must be NaN."""
    oews = load_oews()
    ep = load_ep()
    master = build_occupations_master(oews, ep)
    only_in_ep = master[master["soc_code"] == "45-3031"]
    if len(only_in_ep) > 0:
        assert pd.isna(only_in_ep.iloc[0]["annual_median"])


def test_occupations_master_no_double_sourced_wage():
    """The EP median_annual_wage_2024 column must NOT be in the master.

    OEWS is the wage source. Including both creates ambiguity about which to use.
    """
    oews = load_oews()
    ep = load_ep()
    master = build_occupations_master(oews, ep)
    assert "median_annual_wage_2024" not in master.columns


# ---- build_major_outcomes ----

def test_major_outcomes_row_count_reasonable():
    """One row per 4-digit CIP that has at least one valid SOC mapping."""
    xwalk = load_crosswalk()
    oews = load_oews()
    ep = load_ep()
    cip4_to_soc = aggregate_crosswalk_to_cip4(xwalk)
    occ_master = build_occupations_master(oews, ep)
    result = build_major_outcomes(occ_master, cip4_to_soc, xwalk)
    # Roughly 400-460 CIP4s — varies slightly with NO_MATCH filtering
    assert 400 <= len(result) <= 470
    assert result["cip4"].is_unique


def test_major_outcomes_cip4_format():
    """All cip4 values are 5 characters wide (XX.XX)."""
    xwalk = load_crosswalk()
    oews = load_oews()
    ep = load_ep()
    cip4_to_soc = aggregate_crosswalk_to_cip4(xwalk)
    occ_master = build_occupations_master(oews, ep)
    result = build_major_outcomes(occ_master, cip4_to_soc, xwalk)
    assert result["cip4"].str.len().eq(5).all()


def test_major_outcomes_computer_science_wage_in_expected_range():
    """CIP4 11.07 (Computer Science family) — weighted median wage should be
    close to Software Developers' $133,080 because that SOC has the largest
    employment weight in the routing set. Allow $90K-$140K to accommodate
    drag from teaching SOCs."""
    xwalk = load_crosswalk()
    oews = load_oews()
    ep = load_ep()
    cip4_to_soc = aggregate_crosswalk_to_cip4(xwalk)
    occ_master = build_occupations_master(oews, ep)
    result = build_major_outcomes(occ_master, cip4_to_soc, xwalk)
    cs_row = result[result["cip4"] == "11.07"].iloc[0]
    assert 90000 <= cs_row["weighted_annual_median"] <= 140000
    # Computer Science routes to many SOCs
    assert cs_row["n_routing_socs"] >= 8


def test_major_outcomes_weighted_calc_hand_verified():
    """Hand-computed weighted average for a small, controllable case.

    Use synthetic occupations_master and cip4_to_soc rather than real data,
    so we can verify the math directly without depending on the full pipeline.
    """
    occ_master = pd.DataFrame({
        "soc_code": ["11-1011", "11-1021"],
        "occupation_title": ["A", "B"],
        "annual_median": [100000.0, 50000.0],
        "annual_pct25": [80000.0, 40000.0],
        "annual_pct75": [120000.0, 60000.0],
        "employment_change_percent": [10.0, 4.0],
        "total_employment_oews": [1000.0, 3000.0],  # 25% / 75% weights
        "employment_2024": [np.nan, np.nan],
        "employment_2034": [np.nan, np.nan],
        "employment_change_numeric": [np.nan, np.nan],
        "annual_openings_avg": [np.nan, np.nan],
        "percent_self_employed": [np.nan, np.nan],
        "typical_education": [None, None],
        "work_experience": [None, None],
        "typical_training": [None, None],
        "annual_mean": [np.nan, np.nan],
        "annual_pct10": [np.nan, np.nan],
        "annual_pct90": [np.nan, np.nan],
        "hourly_median": [np.nan, np.nan],
        "hourly_mean": [np.nan, np.nan],
        "hourly_pct10": [np.nan, np.nan],
        "hourly_pct25": [np.nan, np.nan],
        "hourly_pct75": [np.nan, np.nan],
        "hourly_pct90": [np.nan, np.nan],
        "oews_occupation_title": ["A", "B"],
    })
    cip4_to_soc = pd.DataFrame({
        "cip4": ["99.99", "99.99"],
        "SOC2018Code": ["11-1011", "11-1021"],
        "SOC2018Title": ["A", "B"],
        "source_cip6_count": [1, 1],
    })
    xwalk = pd.DataFrame({
        "CIP2020Code": ["99.9999"],
        "CIP2020Title": ["Test."],
        "SOC2018Code": ["11-1011"],
        "SOC2018Title": ["A"],
    })
    result = build_major_outcomes(occ_master, cip4_to_soc, xwalk)
    row = result[result["cip4"] == "99.99"].iloc[0]
    # Weighted median: (100000*1000 + 50000*3000) / (1000 + 3000) = 62500
    assert row["weighted_annual_median"] == pytest.approx(62500.0)
    # Weighted growth: (10*1000 + 4*3000) / 4000 = 5.5
    assert row["weighted_employment_change_percent"] == pytest.approx(5.5)
    assert row["n_routing_socs"] == 2


def test_major_outcomes_handles_all_nan_wages():
    """If every routing SOC has NaN wage, weighted_annual_median must be NaN
    (not 0, not raise). n_socs_with_wage_data must be 0."""
    occ_master = pd.DataFrame({
        "soc_code": ["99-9991"],
        "occupation_title": ["X"],
        "annual_median": [np.nan],
        "annual_pct25": [np.nan],
        "annual_pct75": [np.nan],
        "employment_change_percent": [np.nan],
        "total_employment_oews": [1000.0],
        "employment_2024": [np.nan],
        "employment_2034": [np.nan],
        "employment_change_numeric": [np.nan],
        "annual_openings_avg": [np.nan],
        "percent_self_employed": [np.nan],
        "typical_education": [None],
        "work_experience": [None],
        "typical_training": [None],
        "annual_mean": [np.nan],
        "annual_pct10": [np.nan],
        "annual_pct90": [np.nan],
        "hourly_median": [np.nan],
        "hourly_mean": [np.nan],
        "hourly_pct10": [np.nan],
        "hourly_pct25": [np.nan],
        "hourly_pct75": [np.nan],
        "hourly_pct90": [np.nan],
        "oews_occupation_title": ["X"],
    })
    cip4_to_soc = pd.DataFrame({
        "cip4": ["99.99"],
        "SOC2018Code": ["99-9991"],
        "SOC2018Title": ["X"],
        "source_cip6_count": [1],
    })
    xwalk = pd.DataFrame({
        "CIP2020Code": ["99.9999"],
        "CIP2020Title": ["Test."],
        "SOC2018Code": ["99-9991"],
        "SOC2018Title": ["X"],
    })
    result = build_major_outcomes(occ_master, cip4_to_soc, xwalk)
    row = result[result["cip4"] == "99.99"].iloc[0]
    assert pd.isna(row["weighted_annual_median"])
    assert row["n_socs_with_wage_data"] == 0
    assert row["n_routing_socs"] == 1


# ============================================================
# build_cip4_state_employment
# ============================================================

def test_cip4_state_employment_basic_aggregation():
    """One CIP4, two routing SOCs, three states. Hand-computed total_employment."""
    so = pd.DataFrame({
        "state_abbr": ["CA", "CA", "TX", "TX", "NY", "NY"],
        "soc_code":   ["11-1011", "11-1021", "11-1011", "11-1021", "11-1011", "11-1021"],
        "total_employment": [1000.0, 2000.0, 500.0, np.nan, 800.0, 600.0],
    })
    c2s = pd.DataFrame({"cip4": ["99.01", "99.01"], "SOC2018Code": ["11-1011", "11-1021"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                        "total_employment_oews": [50000.0, 100000.0]})
    result = build_cip4_state_employment(so, c2s, om)
    assert len(result) == 3
    ca = result[(result["cip4"] == "99.01") & (result["state"] == "CA")].iloc[0]
    assert ca["total_employment"] == pytest.approx(3000.0)
    assert ca["coverage_pct"] == pytest.approx(1.0)
    tx = result[(result["cip4"] == "99.01") & (result["state"] == "TX")].iloc[0]
    assert pd.isna(tx["total_employment"])          # coverage = 50k/150k ≈ 0.33 < 0.50
    assert tx["coverage_pct"] == pytest.approx(50000.0 / 150000.0)
    ny = result[(result["cip4"] == "99.01") & (result["state"] == "NY")].iloc[0]
    assert ny["total_employment"] == pytest.approx(1400.0)


def test_cip4_state_employment_lq_formula():
    """State share = 20%, national share = 10% → expected LQ = 2.0."""
    # state_occupations: routing SOC (state_emp=2000) + non-routing SOC (state_emp=8000)
    # state_total = 10000; national_routing = 10000; national_total = 100000
    so = pd.DataFrame({
        "state_abbr": ["XX", "XX"],
        "soc_code":   ["11-1011", "99-9999"],
        "total_employment": [2000.0, 8000.0],
    })
    c2s = pd.DataFrame({"cip4": ["99.01"], "SOC2018Code": ["11-1011"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "99-9999"],
                        "total_employment_oews": [10000.0, 90000.0]})
    result = build_cip4_state_employment(so, c2s, om)
    row = result[(result["cip4"] == "99.01") & (result["state"] == "XX")].iloc[0]
    assert row["location_quotient"] == pytest.approx(2.0)


def test_cip4_state_employment_coverage_threshold():
    """Coverage = 0.40 (suppressed SOC holds 60% of national routing emp) → NaN metrics."""
    so = pd.DataFrame({
        "state_abbr": ["XX", "XX"],
        "soc_code":   ["11-1011", "11-1021"],
        "total_employment": [100.0, np.nan],   # SOC_B suppressed
    })
    c2s = pd.DataFrame({"cip4": ["99.01", "99.01"], "SOC2018Code": ["11-1011", "11-1021"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                        "total_employment_oews": [40000.0, 60000.0]})
    result = build_cip4_state_employment(so, c2s, om)
    row = result[(result["cip4"] == "99.01") & (result["state"] == "XX")].iloc[0]
    assert pd.isna(row["total_employment"])
    assert pd.isna(row["location_quotient"])
    assert row["coverage_pct"] == pytest.approx(0.40)
    assert row["n_observed_socs"] == 1
    assert row["n_routing_socs"] == 2


def test_cip4_state_employment_coverage_above_threshold():
    """Coverage = 0.70 (observed SOC holds 70%) → metrics populated, only observed emp counted."""
    so = pd.DataFrame({
        "state_abbr": ["XX", "XX"],
        "soc_code":   ["11-1011", "11-1021"],
        "total_employment": [np.nan, 500.0],   # SOC_A suppressed, SOC_B observed
    })
    c2s = pd.DataFrame({"cip4": ["99.01", "99.01"], "SOC2018Code": ["11-1011", "11-1021"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                        "total_employment_oews": [30000.0, 70000.0]})
    result = build_cip4_state_employment(so, c2s, om)
    row = result[(result["cip4"] == "99.01") & (result["state"] == "XX")].iloc[0]
    assert row["coverage_pct"] == pytest.approx(0.70)
    assert row["total_employment"] == pytest.approx(500.0)  # only SOC_B counted
    assert not pd.isna(row["location_quotient"])


def test_cip4_state_employment_full_suppression():
    """All routing SOCs suppressed in a state → coverage = 0.0, NaN metrics."""
    so = pd.DataFrame({
        "state_abbr": ["XX", "XX"],
        "soc_code":   ["11-1011", "11-1021"],
        "total_employment": [np.nan, np.nan],
    })
    c2s = pd.DataFrame({"cip4": ["99.01", "99.01"], "SOC2018Code": ["11-1011", "11-1021"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                        "total_employment_oews": [50000.0, 50000.0]})
    result = build_cip4_state_employment(so, c2s, om)
    row = result[(result["cip4"] == "99.01") & (result["state"] == "XX")].iloc[0]
    assert pd.isna(row["total_employment"])
    assert pd.isna(row["location_quotient"])
    assert row["coverage_pct"] == pytest.approx(0.0)
    assert row["n_observed_socs"] == 0
    assert row["n_routing_socs"] == 2


def test_major_outcomes_completeness_columns_match_truth():
    """For real data: n_socs_with_wage_data should equal the count of routing
    SOCs whose annual_median is non-null. Sanity check on the bookkeeping."""
    xwalk = load_crosswalk()
    oews = load_oews()
    ep = load_ep()
    cip4_to_soc = aggregate_crosswalk_to_cip4(xwalk)
    occ_master = build_occupations_master(oews, ep)
    result = build_major_outcomes(occ_master, cip4_to_soc, xwalk)

    # Cross-check 11.07 (Computer Science)
    cs_socs = cip4_to_soc[cip4_to_soc["cip4"] == "11.07"]["SOC2018Code"].values
    cs_socs_in_master = occ_master[occ_master["soc_code"].isin(cs_socs)]
    expected_n_routing = len(cs_socs_in_master)
    expected_n_with_wage = cs_socs_in_master["annual_median"].notna().sum()

    cs_row = result[result["cip4"] == "11.07"].iloc[0]
    assert cs_row["n_routing_socs"] == expected_n_routing
    assert cs_row["n_socs_with_wage_data"] == int(expected_n_with_wage)


# ============================================================
# build_cip4_work_context
# ============================================================

def test_cip4_work_context_basic_weighted_mean():
    """One CIP4, two routing SOCs — hand-computed employment-weighted mean."""
    wc = pd.DataFrame({
        "soc_code": ["11-1011", "11-1021"],
        "el_a": [4.0, 2.0],
        "el_b": [3.0, 1.0],
        "elements_with_data": [2, 2],
        "avg_sample_size": [10.0, 10.0],
    })
    c2s = pd.DataFrame({"cip4": ["99.01", "99.01"], "SOC2018Code": ["11-1011", "11-1021"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                       "total_employment_oews": [1000.0, 3000.0]})
    result = build_cip4_work_context(wc, c2s, om)
    row = result[result["cip4"] == "99.01"].iloc[0]
    # el_a: (4*1000 + 2*3000) / 4000 = 10000/4000 = 2.5
    assert row["el_a"] == pytest.approx(2.5)
    # el_b: (3*1000 + 1*3000) / 4000 = 6000/4000 = 1.5
    assert row["el_b"] == pytest.approx(1.5)
    assert row["n_routing_socs"] == 2
    assert row["n_routing_socs_with_context"] == 2


def test_cip4_work_context_coverage_threshold():
    """CIP4 with 30% coverage fails the 50% threshold — all element columns NaN."""
    wc = pd.DataFrame({
        "soc_code": ["11-1011"],          # Only SOC A has context
        "el_a": [4.0],
        "elements_with_data": [1],
        "avg_sample_size": [10.0],
    })
    c2s = pd.DataFrame({
        "cip4": ["99.01", "99.01", "99.01"],
        "SOC2018Code": ["11-1011", "11-1021", "11-1031"],
    })
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021", "11-1031"],
                       "total_employment_oews": [300.0, 400.0, 300.0]})
    result = build_cip4_work_context(wc, c2s, om)
    row = result[result["cip4"] == "99.01"].iloc[0]
    assert pd.isna(row["el_a"])
    assert row["pct_routing_emp_with_context"] == pytest.approx(0.30)
    assert row["n_routing_socs_with_context"] == 1


def test_cip4_work_context_per_element_nan_exclusion():
    """Above 50% threshold: each element excludes NaN SOCs from its own weighted mean."""
    wc = pd.DataFrame({
        "soc_code": ["11-1011", "11-1021"],
        "el_x": [4.0, np.nan],    # SOC A has it; SOC B does not
        "el_y": [np.nan, 3.0],    # SOC B has it; SOC A does not
        "elements_with_data": [1, 1],
        "avg_sample_size": [10.0, 10.0],
    })
    c2s = pd.DataFrame({"cip4": ["99.01", "99.01"], "SOC2018Code": ["11-1011", "11-1021"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                       "total_employment_oews": [600.0, 400.0]})
    result = build_cip4_work_context(wc, c2s, om)
    row = result[result["cip4"] == "99.01"].iloc[0]
    assert row["el_x"] == pytest.approx(4.0)   # only SOC A contributes
    assert row["el_y"] == pytest.approx(3.0)   # only SOC B contributes


def test_cip4_work_context_all_socs_missing_from_wc():
    """All routing SOCs absent from work_context — n_with_context=0, pct=0, NaN elements."""
    wc = pd.DataFrame({
        "soc_code": ["99-0001"],     # unrelated SOC, not in routing
        "el_a": [4.0],
        "elements_with_data": [1],
        "avg_sample_size": [10.0],
    })
    c2s = pd.DataFrame({"cip4": ["99.01", "99.01"], "SOC2018Code": ["11-1011", "11-1021"]})
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                       "total_employment_oews": [1000.0, 2000.0]})
    result = build_cip4_work_context(wc, c2s, om)
    row = result[result["cip4"] == "99.01"].iloc[0]
    assert row["n_routing_socs_with_context"] == 0
    assert row["pct_routing_emp_with_context"] == pytest.approx(0.0)
    assert pd.isna(row["el_a"])


def test_cip4_work_context_diagnostic_columns_always_present():
    """Diagnostic columns are populated even when element columns are NaN (failing coverage)."""
    wc = pd.DataFrame({
        "soc_code": ["11-1011"],
        "el_a": [4.0],
        "elements_with_data": [1],
        "avg_sample_size": [10.0],
    })
    c2s = pd.DataFrame({
        "cip4": ["99.01", "99.01"],
        "SOC2018Code": ["11-1011", "11-1021"],
    })
    # SOC A has 10% of routing employment — fails the 50% threshold
    om = pd.DataFrame({"soc_code": ["11-1011", "11-1021"],
                       "total_employment_oews": [100.0, 900.0]})
    result = build_cip4_work_context(wc, c2s, om)
    row = result[result["cip4"] == "99.01"].iloc[0]
    assert pd.isna(row["el_a"])
    assert row["n_routing_socs"] == 2
    assert row["n_routing_socs_with_context"] == 1
    assert not pd.isna(row["pct_routing_emp_with_context"])
    assert row["pct_routing_emp_with_context"] == pytest.approx(0.10)
