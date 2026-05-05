"""
test_scoring.py — Unit tests for the scoring engine and explainer.

Run with:
    pytest tests/ -v

These tests use tiny hand-built DataFrames with known values so that the
correct ranking / score / explainer output can be verified by hand. If any
of these fail, something in scoring.py is wrong.
"""

import math

import numpy as np
import pandas as pd
import pytest

import config
from scoring import normalize_column, compute_scores, compute_score_uncertainty, generate_explainer


# ============================================================
# FIXTURES — small hand-built DataFrames
# ============================================================
@pytest.fixture
def five_schools():
    """
    Five fake schools with known values across every scoring dimension.

    Laid out so that School A dominates on everything (highest earnings,
    highest graduation rate, lowest debt, lowest net price, etc.), School E
    is worst on everything, and B/C/D are in between. This makes the
    "correct" ranking unambiguous.
    """
    return pd.DataFrame({
        "school_name": ["A", "B", "C", "D", "E"],
        "net_price":              [10_000, 15_000, 20_000, 25_000, 30_000],  # lower = better
        "graduation_rate":        [0.95,   0.85,   0.75,   0.65,   0.55],    # higher = better
        "retention_rate":         [0.98,   0.92,   0.86,   0.80,   0.74],    # higher = better
        "median_earnings_10yr":   [85_000, 70_000, 55_000, 45_000, 35_000],  # higher = better
        "admission_rate":         [0.10,   0.25,   0.50,   0.70,   0.90],    # lower = better
        "median_debt":            [15_000, 18_000, 22_000, 26_000, 30_000],  # lower = better
        "repayment_rate_3yr":     [0.90,   0.80,   0.70,   0.60,   0.50],    # higher = better
        "incidents_per_1000_students": [0.5, 1.0, 1.5, 2.0, 2.5],            # lower = better
    })


# ============================================================
# NORMALIZE_COLUMN
# ============================================================
class TestNormalizeColumn:
    def test_higher_better_direction(self):
        """Higher raw values should get higher normalized scores."""
        s = pd.Series([10, 20, 30, 40, 50])
        result = normalize_column(s, "higher_better")
        assert result.iloc[0] < result.iloc[-1]
        # Ranks are percentiles of positions; 5 unique values → 0.2, 0.4, ..., 1.0
        assert result.iloc[-1] == pytest.approx(1.0)

    def test_lower_better_direction(self):
        """Lower raw values should get higher normalized scores."""
        s = pd.Series([10, 20, 30, 40, 50])
        result = normalize_column(s, "lower_better")
        assert result.iloc[0] > result.iloc[-1]
        assert result.iloc[0] == pytest.approx(1.0)

    def test_missing_values_get_neutral_rank(self):
        """NaN inputs should be imputed to 0.5."""
        s = pd.Series([10, 20, np.nan, 40, 50])
        result = normalize_column(s, "higher_better")
        assert result.iloc[2] == 0.5

    def test_invalid_direction_raises(self):
        with pytest.raises(ValueError):
            normalize_column(pd.Series([1, 2, 3]), "sideways")

    def test_ties_get_same_rank(self):
        """When multiple schools share a value, they should get the same rank."""
        s = pd.Series([10, 20, 20, 20, 50])
        result = normalize_column(s, "higher_better")
        assert result.iloc[1] == result.iloc[2] == result.iloc[3]


# ============================================================
# COMPUTE_SCORES
# ============================================================
class TestComputeScores:
    def test_single_dimension_ranking_matches_sort(self, five_schools):
        """
        If only one dimension has weight, the ranking should exactly match
        sorting by that metric alone. This is the most important sanity test —
        it catches direction bugs (e.g., flipping higher/lower by mistake).
        """
        weights = {"earnings": 1.0}
        result = compute_scores(five_schools, weights)
        # School A has the highest earnings, so should rank first
        assert result.iloc[0]["school_name"] == "A"
        assert result.iloc[-1]["school_name"] == "E"

    def test_lower_better_dimension_ranks_correctly(self, five_schools):
        """Same test but for a lower-is-better dimension."""
        weights = {"affordability": 1.0}
        result = compute_scores(five_schools, weights)
        # School A has the lowest net price, so should rank first
        assert result.iloc[0]["school_name"] == "A"
        assert result.iloc[-1]["school_name"] == "E"

    def test_weight_magnitude_does_not_affect_ranking(self, five_schools):
        """Weights (3, 2, 1) and (30, 20, 10) should produce identical rankings."""
        w_small = {"earnings": 3, "affordability": 2, "graduation_rate": 1}
        w_large = {"earnings": 30, "affordability": 20, "graduation_rate": 10}
        r_small = compute_scores(five_schools, w_small)
        r_large = compute_scores(five_schools, w_large)
        assert list(r_small["school_name"]) == list(r_large["school_name"])
        # Scores should also be equal (weights are normalized)
        pd.testing.assert_series_equal(r_small["match_score"], r_large["match_score"])

    def test_zero_weights_excluded(self, five_schools):
        """Setting a dimension to 0 should exclude it entirely."""
        # If we weight earnings=1 and graduation_rate=0, the ranking should
        # match earnings-only
        w_full = {"earnings": 1, "graduation_rate": 0}
        w_earnings_only = {"earnings": 1}
        r_full = compute_scores(five_schools, w_full)
        r_earnings = compute_scores(five_schools, w_earnings_only)
        assert list(r_full["school_name"]) == list(r_earnings["school_name"])

    def test_score_on_0_to_100_scale(self, five_schools):
        """Match scores should fall in [0, 100]."""
        weights = {"earnings": 1, "affordability": 1}
        result = compute_scores(five_schools, weights)
        assert result["match_score"].min() >= 0
        assert result["match_score"].max() <= 100

    def test_missing_data_does_not_crash(self):
        """A school missing a metric should still rank on the metrics it has."""
        df = pd.DataFrame({
            "school_name": ["A", "B"],
            "net_price": [10_000, np.nan],
            "graduation_rate": [0.8, 0.9],
            "retention_rate": [0.9, 0.85],
            "median_earnings_10yr": [60_000, 70_000],
            "admission_rate": [0.3, 0.4],
            "median_debt": [20_000, 22_000],
            "repayment_rate_3yr": [0.75, 0.85],
            "incidents_per_1000_students": [1.0, 1.5],
        })
        weights = {"affordability": 1, "graduation_rate": 1}
        result = compute_scores(df, weights)
        # Should not raise; both schools should get a valid match_score
        assert len(result) == 2
        assert not result["match_score"].isna().any()

    def test_empty_dataframe(self):
        """Zero-row input should not crash."""
        df = pd.DataFrame({"school_name": [], "net_price": [], "graduation_rate": [],
                           "retention_rate": [], "median_earnings_10yr": [],
                           "admission_rate": [], "median_debt": [],
                           "repayment_rate_3yr": [],
                           "incidents_per_1000_students": []})
        result = compute_scores(df, {"affordability": 1})
        assert len(result) == 0

    def test_all_zero_weights_returns_neutral_score(self, five_schools):
        """If the user leaves every slider at 0, return a neutral score of 50."""
        weights = {"earnings": 0, "affordability": 0}
        result = compute_scores(five_schools, weights)
        assert (result["match_score"] == 50.0).all()

    def test_compute_scores_uses_income_bracket_column_when_provided(self):
        """When income_bracket_column is provided, scoring uses it instead of net_price."""
        df = pd.DataFrame({
            "UNITID": [1, 2, 3],
            "net_price":                [10000, 20000, 30000],   # default: row 1 cheapest
            "_selected_bracket_price":  [30000, 20000, 10000],   # inverted: row 3 cheapest
            "graduation_rate":          [0.8, 0.7, 0.6],
            "retention_rate":           [0.9, 0.8, 0.7],
            "median_earnings_10yr":     [50000, 50000, 50000],
            "admission_rate":           [0.5, 0.5, 0.5],
            "median_debt":              [20000, 20000, 20000],
            "repayment_rate_3yr":       [0.7, 0.7, 0.7],
        })
        weights = {"affordability": 5, "graduation_rate": 0, "retention": 0,
                   "earnings": 0, "selectivity": 0, "debt": 0, "repayment": 0}

        # With override: row 3 should rank #1 (cheapest in bracket column)
        ranked = compute_scores(df, weights, income_bracket_column="_selected_bracket_price")
        assert ranked.iloc[0]["UNITID"] == 3

        # Without override: row 1 should rank #1 (cheapest in net_price)
        ranked_default = compute_scores(df, weights)
        assert ranked_default.iloc[0]["UNITID"] == 1


# ============================================================
# GENERATE_EXPLAINER
# ============================================================
class TestExplainer:
    def test_mentions_top_weighted_dimension(self, five_schools):
        weights = {"earnings": 5, "affordability": 1}
        scored = compute_scores(five_schools, weights)
        top_school = scored.iloc[0]
        explainer = generate_explainer(top_school, weights)
        # The explainer should mention "earnings" (the top-weighted dimension)
        assert "earnings" in explainer.lower()

    def test_includes_school_name(self, five_schools):
        weights = {"earnings": 1}
        scored = compute_scores(five_schools, weights)
        top_school = scored.iloc[0]
        explainer = generate_explainer(top_school, weights)
        assert top_school["school_name"] in explainer

    def test_no_weights_gracefully_handled(self, five_schools):
        weights = {}
        scored = compute_scores(five_schools, weights)
        top_school = scored.iloc[0]
        explainer = generate_explainer(top_school, weights)
        # Should return *something* rather than crashing
        assert isinstance(explainer, str)
        assert len(explainer) > 0


# ============================================================
# CONFIDENCE INTERVAL (Step C)
# ============================================================
def _make_row(source_cols: dict, score_cols: dict, match_score: float = 80.0) -> pd.Series:
    """
    Build a synthetic scored row for compute_score_uncertainty tests.

    source_cols : {column_name: value} — original metric columns;
                  NaN means the dimension had no data.
    score_cols  : {score_key: value}  — normalized score columns added
                  by compute_scores (e.g. {"score_affordability": 0.78}).
    """
    data: dict = {"match_score": match_score}
    data.update(source_cols)
    data.update(score_cols)
    return pd.Series(data)


# Canonical column names from SCORING_DIMENSIONS
_SRC = {k: v["column"] for k, v in config.SCORING_DIMENSIONS.items()}
_ALL_WEIGHTS = {k: 1 for k in config.SCORING_DIMENSIONS}


class TestCI:
    def test_ci_full_coverage_tight(self):
        """7-of-7 dimensions reported with near-identical scores → margin < 5."""
        # Normalized scores are tightly clustered around 0.80
        scores = {
            "score_affordability":   0.78,
            "score_graduation_rate": 0.80,
            "score_retention_rate":  0.82,
            "score_earnings":        0.79,
            "score_selectivity":     0.81,
            "score_low_debt":        0.80,
            "score_repayment":       0.80,
        }
        # All source columns present and non-null
        sources = {col: 1.0 for col in _SRC.values()}
        row = _make_row(sources, scores)

        margin, lower, upper, n_rep, n_tot = compute_score_uncertainty(row, _ALL_WEIGHTS)
        assert n_rep == 7
        assert n_tot == 7
        assert margin < 5.0, f"Expected tight CI but got margin={margin:.2f}"
        assert lower >= 0.0
        assert upper <= 100.0

    def test_ci_partial_coverage_wider(self):
        """3-of-7 dimensions reported → margin is wider than full-coverage case."""
        # Same three scores, but only those three source columns are non-null
        scores_full = {
            "score_affordability":   0.78,
            "score_graduation_rate": 0.82,
            "score_retention_rate":  0.79,
            "score_earnings":        0.80,
            "score_selectivity":     0.81,
            "score_low_debt":        0.80,
            "score_repayment":       0.80,
        }
        sources_full = {col: 1.0 for col in _SRC.values()}
        row_full = _make_row(sources_full, scores_full)
        margin_full, *_ = compute_score_uncertainty(row_full, _ALL_WEIGHTS)

        # Partial: only affordability, graduation_rate, retention_rate reported
        scores_partial = dict(scores_full)  # same normalized values
        scores_partial.update({  # imputed for unreported dims — not counted
            "score_earnings": 0.5, "score_selectivity": 0.5,
            "score_low_debt": 0.5, "score_repayment": 0.5,
        })
        sources_partial = {
            _SRC["affordability"]:    1.0,
            _SRC["graduation_rate"]:  1.0,
            _SRC["retention_rate"]:   1.0,
            _SRC["earnings"]:         float("nan"),
            _SRC["selectivity"]:      float("nan"),
            _SRC["low_debt"]:         float("nan"),
            _SRC["repayment"]:        float("nan"),
        }
        row_partial = _make_row(sources_partial, scores_partial)
        margin_partial, _, _, n_rep, n_tot = compute_score_uncertainty(row_partial, _ALL_WEIGHTS)

        assert n_rep == 3
        assert n_tot == 7
        assert margin_partial > margin_full, (
            f"Partial ({margin_partial:.2f}) should be wider than full ({margin_full:.2f})"
        )

    def test_ci_single_dimension_default_se(self):
        """Only 1 dimension reported → margin falls back to the default 15.0."""
        sources = {col: float("nan") for col in _SRC.values()}
        sources[_SRC["earnings"]] = 70_000.0  # only earnings reported
        scores = {f"score_{k}": 0.5 for k in config.SCORING_DIMENSIONS}
        scores["score_earnings"] = 0.80
        row = _make_row(sources, scores)

        margin, lower, upper, n_rep, n_tot = compute_score_uncertainty(row, _ALL_WEIGHTS)
        assert n_rep == 1
        assert margin == pytest.approx(15.0)
        assert lower == pytest.approx(max(0.0, 80.0 - 15.0))
        assert upper == pytest.approx(min(100.0, 80.0 + 15.0))

    def test_ci_bounds_clipped(self):
        """Computed CI extending beyond [0, 100] must be clipped."""
        sources = {col: float("nan") for col in _SRC.values()}
        sources[_SRC["affordability"]] = 20_000.0  # single dimension → margin=15

        scores_high = {f"score_{k}": 0.5 for k in config.SCORING_DIMENSIONS}
        scores_high["score_affordability"] = 0.98
        row_high = _make_row(sources, scores_high, match_score=98.0)
        _, _, upper_high, _, _ = compute_score_uncertainty(row_high, _ALL_WEIGHTS)
        assert upper_high == pytest.approx(100.0), "Upper bound should be clipped at 100"

        scores_low = {f"score_{k}": 0.5 for k in config.SCORING_DIMENSIONS}
        scores_low["score_affordability"] = 0.02
        row_low = _make_row(sources, scores_low, match_score=2.0)
        _, lower_low, _, _, _ = compute_score_uncertainty(row_low, _ALL_WEIGHTS)
        assert lower_low == pytest.approx(0.0), "Lower bound should be clipped at 0"

    def test_ci_all_weights_zero(self):
        """
        When every weight is 0, compute_scores returns NaN CI columns —
        which the UI renders as '—' (no priorities set).
        """
        df = pd.DataFrame({
            "school_name": ["A", "B"],
            "net_price": [10_000, 15_000],
            "graduation_rate": [0.8, 0.9],
            "retention_rate": [0.85, 0.88],
            "median_earnings_10yr": [60_000, 70_000],
            "admission_rate": [0.3, 0.4],
            "median_debt": [20_000, 22_000],
            "repayment_rate_3yr": [0.75, 0.85],
            "retention_rate_4yr": [0.85, 0.88],
        })
        weights = {k: 0 for k in config.SCORING_DIMENSIONS}
        result = compute_scores(df, weights)
        assert "match_score_margin" in result.columns
        assert result["match_score_margin"].isna().all(), (
            "Margin should be NaN when all weights are 0"
        )


# ============================================================
# SENSITIVITY ANALYSIS (Step D)
# ============================================================
class TestSensitivity:
    """Unit tests for compute_sensitivity()."""

    def _make_df(self):
        """
        12-school dataframe with deterministic monotonic ordering.
        School with unit_id=1 dominates every dimension; higher unit_id = worse.
        Column names match config.SCORING_DIMENSIONS column specs exactly.
        """
        rows = []
        for i in range(1, 13):
            rows.append({
                "unit_id":              i,
                "school_name":          f"School {i}",
                "net_price":            10_000 + i * 1_000,      # lower better
                "graduation_rate":      max(0.01, 1.0 - i * 0.05),  # higher better
                "retention_rate_4yr":   max(0.01, 1.0 - i * 0.05),  # higher better
                "median_earnings_10yr": max(1_000, 80_000 - i * 2_000),  # higher better
                "admission_rate":       min(0.99, 0.05 + i * 0.05),  # lower better
                "median_debt":          10_000 + i * 1_000,      # lower better
                "repayment_rate_3yr":   max(0.01, 1.0 - i * 0.05),  # higher better
            })
        return pd.DataFrame(rows)

    def test_robustness_bounded(self):
        """Robustness is always in [0.0, 1.0] and tier is one of the valid values."""
        from scoring import compute_sensitivity
        df = self._make_df()
        weights = {
            "affordability": 3, "graduation_rate": 3, "retention_rate": 2,
            "earnings": 4, "selectivity": 2, "low_debt": 3, "repayment": 3,
        }
        result = compute_sensitivity(df, weights, school_unitid=5, top_n=10)
        assert 0.0 <= result["robustness"] <= 1.0
        assert result["n_perturbations"] > 0
        assert result["tier"] in ("robust", "borderline", "volatile")

    def test_top_school_stays_in_top_n(self):
        """The clear #1 school remains in the top 10 across all perturbations."""
        from scoring import compute_sensitivity
        df = self._make_df()
        weights = {
            "affordability": 3, "graduation_rate": 3, "retention_rate": 2,
            "earnings": 4, "selectivity": 2, "low_debt": 3, "repayment": 3,
        }
        result = compute_sensitivity(df, weights, school_unitid=1, top_n=10)
        assert result["robustness"] == 1.0
        assert result["tier"] == "robust"

    def test_all_zero_weights_returns_neutral(self):
        """All-zero weights returns robustness=0.5 and tier='no_priorities'."""
        from scoring import compute_sensitivity
        df = self._make_df()
        weights = {
            "affordability": 0, "graduation_rate": 0, "retention_rate": 0,
            "earnings": 0, "selectivity": 0, "low_debt": 0, "repayment": 0,
        }
        result = compute_sensitivity(df, weights, school_unitid=1, top_n=10)
        assert result["robustness"] == 0.5
        assert result["tier"] == "no_priorities"
        assert result["n_perturbations"] == 0

    def test_sensitivity_uses_income_bracket_column(self):
        """When income_bracket_column is provided, perturbations score against it."""
        from scoring import compute_sensitivity
        df = pd.DataFrame({
            "unit_id": [1, 2, 3, 4, 5],
            "name": ["A", "B", "C", "D", "E"],
            "net_price": [10000, 12000, 14000, 16000, 18000],
            # Inverted ordering: school with cheapest bracket price is most expensive overall
            "_selected_bracket_price": [50000, 40000, 30000, 20000, 10000],
            "graduation_rate": [0.8, 0.7, 0.6, 0.5, 0.4],
            "retention_rate_4yr": [0.9, 0.8, 0.7, 0.6, 0.5],
            "median_earnings_10yr": [60000, 55000, 50000, 45000, 40000],
            "admission_rate": [0.5, 0.5, 0.5, 0.5, 0.5],
            "median_debt": [20000, 20000, 20000, 20000, 20000],
            "repayment_rate_3yr": [0.7, 0.7, 0.7, 0.7, 0.7],
        })
        # Heavy affordability weight: school 5 should be #1 with bracket override (cheapest in bracket)
        weights = {"affordability": 5, "graduation_rate": 0, "retention_rate": 0,
                   "earnings": 0, "selectivity": 0, "low_debt": 0, "repayment": 0}

        sens_with = compute_sensitivity(
            df, weights, school_unitid=5, top_n=3,
            income_bracket_column="_selected_bracket_price",
        )
        sens_without = compute_sensitivity(
            df, weights, school_unitid=5, top_n=3,
        )

        # With bracket override, school 5 is #1 → robust across perturbations
        # Without override, school 5 is #5 (most expensive) → falls out of top 3 quickly
        assert sens_with["robustness"] > sens_without["robustness"], (
            f"Bracket override should improve robustness for school 5 "
            f"(with={sens_with['robustness']}, without={sens_without['robustness']})"
        )

    def test_sensitivity_outside_filter_school_with_broader_pool(self):
        """A school that would be filtered out of a narrow set still gets a real
        robustness score when evaluated against a broader pool (pinned-school case)."""
        from scoring import compute_sensitivity
        # Broader pool includes all 5 schools, including school 99 (the "pinned outside filter")
        broader_pool = pd.DataFrame({
            "unit_id": [1, 2, 3, 99, 4],
            "name": ["A", "B", "C", "Pinned", "E"],
            "net_price": [10000, 15000, 20000, 12000, 25000],
            "graduation_rate": [0.5, 0.6, 0.7, 0.85, 0.4],
            "retention_rate_4yr": [0.7, 0.7, 0.7, 0.9, 0.7],
            "median_earnings_10yr": [50000, 50000, 50000, 70000, 50000],
            "admission_rate": [0.5, 0.5, 0.5, 0.3, 0.5],
            "median_debt": [20000, 20000, 20000, 20000, 20000],
            "repayment_rate_3yr": [0.7, 0.7, 0.7, 0.7, 0.7],
        })
        weights = {"affordability": 3, "graduation_rate": 5, "retention_rate": 3,
                   "earnings": 3, "selectivity": 3, "low_debt": 0, "repayment": 0}

        # School 99 has the best graduation rate, retention, earnings, and selectivity
        # → should be highly robust, NOT 0% volatile
        sens = compute_sensitivity(
            broader_pool, weights, school_unitid=99, top_n=3,
        )

        assert sens["n_perturbations"] > 0, "School 99 should be evaluated, not skipped"
        assert sens["robustness"] > 0.5, (
            f"Strong school in broader pool should be robust, got {sens['robustness']}"
        )
        assert sens["tier"] in ("robust", "borderline"), (
            f"Should not be volatile, got {sens['tier']}"
        )
