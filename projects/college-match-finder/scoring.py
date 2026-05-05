"""
scoring.py — Weighted multi-criteria scoring engine for College Match Finder.

The engine takes a filtered DataFrame of colleges plus a dict of user weights
(one per scoring dimension) and returns the DataFrame augmented with a match
score column and percentile-rank columns per dimension. The match score is a
weighted average of per-dimension percentile ranks, scaled 0–100 for display.

Design choices:

- Percentile rank (not min-max) is used for per-dimension normalization so
  that outliers don't compress the scale, and so the resulting numbers
  ("85th percentile for earnings") are directly interpretable in the UI.

- Missing metric values are imputed to the neutral 50th percentile for that
  dimension. This avoids penalizing a school just because the Department of
  Education doesn't publish the metric, while still letting it rank on
  whatever metrics it does report.

- Dimensions with weight = 0 are dropped from the calculation entirely.
  A school missing data on an irrelevant dimension contributes nothing
  either way.

- Direction is handled at the normalization step: lower-is-better metrics
  (net price, admission rate, debt, crime rate) are inverted so that 1.0
  always means "best in the field."
"""

from __future__ import annotations

import pandas as pd
import numpy as np

import config

# Sensitivity analysis tier thresholds (Stat Depth D).
# A pinned school is "robust" if it stays in the top N in >= 70% of nearby
# weight settings, "borderline" if 40-70%, "volatile" if < 40%.
SENSITIVITY_ROBUST_THRESHOLD = 0.70
SENSITIVITY_BORDERLINE_THRESHOLD = 0.40


# ============================================================
# PER-DIMENSION NORMALIZATION
# ============================================================
def normalize_column(series: pd.Series, direction: str) -> pd.Series:
    """
    Convert a metric column into percentile ranks on [0, 1], where 1.0 = best.

    - direction="higher_better": higher raw value → higher normalized score.
    - direction="lower_better":  lower raw value  → higher normalized score.

    Missing values are imputed to 0.5 (the neutral median). This keeps
    schools with missing data from being artificially penalized while still
    letting them rank on the metrics they do report.

    Percentile rank is computed with pct=True, which scales ranks to (0, 1].
    We use method="average" so that ties get the same rank — important when
    many schools share the same reported value (e.g., multiple schools with
    a 100% graduation rate).
    """
    if direction not in ("higher_better", "lower_better"):
        raise ValueError(f"direction must be 'higher_better' or 'lower_better', got {direction!r}")

    # Rank returns NaN for NaN inputs; we fill those after ranking so that
    # missing values land at the median of the ranked population rather than
    # the mean of the raw population (the two are subtly different).
    ascending = direction == "higher_better"
    ranks = series.rank(pct=True, method="average", ascending=ascending)

    # Impute missing ranks to the neutral 0.5
    ranks = ranks.fillna(0.5)

    return ranks


# ============================================================
# CONFIDENCE INTERVAL HELPER
# ============================================================
def compute_score_uncertainty(
    row: pd.Series,
    weights: dict,
) -> tuple[float, float, float, int, int]:
    """
    Compute a 95% CI around a school's match score using a
    coverage-adjusted standard-error approach.

    Schools with fewer reported dimensions and more disagreement
    across those dimensions receive wider intervals.

    Parameters
    ----------
    row     : a single scored row (must contain match_score and
              score_<key> columns added by compute_scores, plus the
              original metric columns used to detect missing data).
    weights : weights dict; zero-weighted dimensions are ignored.

    Returns
    -------
    (margin, lower, upper, n_reported, n_total) on the 0-100 scale.
    margin/lower/upper are NaN when CI cannot be computed.
    """
    active = {k: w for k, w in weights.items() if w > 0}
    n_total = len(active)
    _nan = float("nan")

    if n_total == 0:
        return (_nan, _nan, _nan, 0, 0)

    match_score_val = row.get("match_score")
    if match_score_val is None or pd.isna(match_score_val):
        return (_nan, _nan, _nan, 0, n_total)
    match_score_val = float(match_score_val)

    # Gather normalized scores only for dimensions where source data exists.
    # We check the original metric column — not the imputed score — to
    # distinguish real data from the neutral 50th-percentile imputation.
    reported_scores: list[float] = []
    for key in active:
        spec = config.SCORING_DIMENSIONS.get(key)
        if spec is None:
            continue
        col = spec["column"]
        col_val = row.get(col)
        if col_val is None or pd.isna(col_val):
            continue  # dimension was imputed; don't count it
        score_val = row.get(f"score_{key}")
        if score_val is not None and not pd.isna(score_val):
            reported_scores.append(float(score_val))

    n_reported = len(reported_scores)

    if n_reported == 0:
        return (_nan, _nan, _nan, 0, n_total)

    if n_reported == 1:
        # Variance undefined for a single point; use a large default to
        # visibly signal low confidence rather than crashing or returning 0.
        margin = 15.0
    else:
        coverage = n_reported / n_total
        variance = float(np.var(reported_scores, ddof=1))  # sample var, 0-1 scale
        se = np.sqrt(variance / n_reported) / np.sqrt(coverage)
        margin = float(1.96 * se * 100)  # scale to 0-100

    lower = float(max(0.0, match_score_val - margin))
    upper = float(min(100.0, match_score_val + margin))
    return (margin, lower, upper, n_reported, n_total)


# ============================================================
# SENSITIVITY ANALYSIS
# ============================================================
def compute_sensitivity(
    df: pd.DataFrame,
    weights: dict,
    school_unitid,
    top_n: int = 10,
    income_bracket_column: str | None = None,
) -> dict:
    """
    Local perturbation sensitivity analysis for a single pinned school.

    For each weighted dimension, perturb the weight by +1 and -1 (clamped to
    [0, 5]), recompute the full ranking on the provided dataframe, and check
    whether the target school remains in the top N. Return the fraction of
    perturbations in which the school stays in the top N.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered dataframe (same population the results table is built from).
        Must contain a 'unit_id' column.
    weights : dict
        Mapping of dimension key -> weight (0-5).
    school_unitid : int or str
        The unit_id of the school being analyzed.
    top_n : int, default 10
        The ranking cutoff used to define "in the top N".
    income_bracket_column : str or None, default None
        Optional column name to use for the affordability dimension in place of
        the default "net_price" column. Forwarded to every internal
        compute_scores call so sensitivity analysis matches the scoring path
        used by the main ranking.

    Returns
    -------
    dict with keys:
        'robustness'      : float in [0.0, 1.0]
        'n_perturbations' : int
        'tier'            : 'robust' | 'borderline' | 'volatile' | 'no_priorities'

    Edge cases
    ----------
    - All weights zero -> robustness=0.5, n_perturbations=0, tier='no_priorities'
    - School not in df -> robustness=0.0, n_perturbations=0, tier='volatile'
    - Perturbed weight equals original (boundary clamp) -> skipped, not counted
    """
    # Edge case: school not in dataframe
    if school_unitid not in df["unit_id"].values:
        return {"robustness": 0.0, "n_perturbations": 0, "tier": "volatile"}

    # Edge case: all weights zero
    if sum(weights.values()) == 0:
        return {"robustness": 0.5, "n_perturbations": 0, "tier": "no_priorities"}

    in_top_n_count = 0
    total_perturbations = 0

    for key in config.SCORING_DIMENSIONS:
        original_weight = weights.get(key, 0)

        for delta in (+1, -1):
            new_weight = max(0, min(5, original_weight + delta))
            # Skip if clamping made this a no-op — keeps the denominator honest
            if new_weight == original_weight:
                continue

            perturbed_weights = dict(weights)
            perturbed_weights[key] = new_weight

            # compute_scores returns sorted descending by match_score
            scored = compute_scores(df, perturbed_weights, income_bracket_column=income_bracket_column)
            top_unitids = scored.head(top_n)["unit_id"].values

            if school_unitid in top_unitids:
                in_top_n_count += 1
            total_perturbations += 1

    # Guard: all weights were already at boundaries (shouldn't happen given the
    # all-zero check above, but avoids division by zero if weights are all 5).
    if total_perturbations == 0:
        return {"robustness": 0.5, "n_perturbations": 0, "tier": "no_priorities"}

    robustness = in_top_n_count / total_perturbations

    if robustness >= SENSITIVITY_ROBUST_THRESHOLD:
        tier = "robust"
    elif robustness >= SENSITIVITY_BORDERLINE_THRESHOLD:
        tier = "borderline"
    else:
        tier = "volatile"

    return {
        "robustness": robustness,
        "n_perturbations": total_perturbations,
        "tier": tier,
    }


# ============================================================
# MAIN SCORING FUNCTION
# ============================================================
def compute_scores(
    df: pd.DataFrame,
    weights: dict,
    income_bracket_column: str | None = None,
) -> pd.DataFrame:
    """
    Compute match scores for every school in `df`.

    Parameters
    ----------
    df : the filtered colleges DataFrame (post hard-filters)
    weights : dict mapping dimension key → weight (float, typically 0–5).
              Keys must be a subset of config.SCORING_DIMENSIONS.
    income_bracket_column : optional override for the affordability column.
              If provided, the affordability dimension uses this column
              instead of `net_price`. Used when the user selects an
              income bracket.

    Returns
    -------
    A copy of `df` with added columns:
      - score_<dimension>       : per-dimension percentile rank [0, 1]
      - match_score             : weighted average, scaled to 0–100
    The returned frame is sorted by match_score descending.
    """
    if df.empty:
        # Add empty columns so downstream code doesn't break on zero-row results
        out = df.copy()
        for key in weights:
            out[f"score_{key}"] = []
        out["match_score"] = []
        for _ci_col in ["match_score_margin", "match_score_lower",
                        "match_score_upper", "n_dimensions_reported", "n_dimensions_total"]:
            out[_ci_col] = []
        return out

    # Drop zero-weighted dimensions
    active_weights = {k: w for k, w in weights.items() if w > 0}

    out = df.copy()

    # If the user supplied no weights at all (all sliders at 0), return the
    # frame with a neutral score so the UI can show something sensible rather
    # than crashing. The results will effectively be in their filter order.
    if not active_weights:
        out["match_score"] = 50.0
        for _ci_col in ["match_score_margin", "match_score_lower",
                        "match_score_upper", "n_dimensions_reported", "n_dimensions_total"]:
            out[_ci_col] = float("nan")
        return out

    # Normalize total weight so the final score is always on a 0–100 scale
    # regardless of how the user sets the sliders (3-2-1 vs. 30-20-10 should
    # produce identical rankings and identical score magnitudes).
    total_weight = sum(active_weights.values())

    # Compute per-dimension normalized scores
    weighted_sum = pd.Series(0.0, index=out.index)
    for key, weight in active_weights.items():
        if key not in config.SCORING_DIMENSIONS:
            raise ValueError(f"Unknown scoring dimension: {key!r}")

        spec = config.SCORING_DIMENSIONS[key]

        # Pick the right column. For the affordability dimension, the UI
        # may have supplied an income-bracket-specific column name.
        if key == "affordability" and income_bracket_column is not None:
            col = income_bracket_column
        else:
            col = spec["column"]

        if col not in out.columns:
            # Column not present in the data (e.g., safety data not loaded).
            # Assign neutral rank so the dimension doesn't break scoring.
            out[f"score_{key}"] = 0.5
        else:
            out[f"score_{key}"] = normalize_column(out[col], spec["direction"])

        weighted_sum += out[f"score_{key}"] * (weight / total_weight)

    out["match_score"] = (weighted_sum * 100).round(1)

    # Compute 95% CI per row (Step C).
    # iterrows is O(n) and fast enough for ~2,500 schools; the list comprehension
    # avoids pandas apply overhead for a tuple-returning function.
    _uncertainty = [
        compute_score_uncertainty(row, active_weights)
        for _, row in out.iterrows()
    ]
    if _uncertainty:
        _margins, _lowers, _uppers, _n_reps, _n_tots = zip(*_uncertainty)
    else:
        _margins = _lowers = _uppers = _n_reps = _n_tots = []
    out["match_score_margin"] = [round(v, 1) if pd.notna(v) else float("nan") for v in _margins]
    out["match_score_lower"]  = [round(v, 1) if pd.notna(v) else float("nan") for v in _lowers]
    out["match_score_upper"]  = [round(v, 1) if pd.notna(v) else float("nan") for v in _uppers]
    out["n_dimensions_reported"] = list(_n_reps)
    out["n_dimensions_total"]    = list(_n_tots)

    return out.sort_values("match_score", ascending=False).reset_index(drop=True)


# ============================================================
# EXPLAINER — natural-language "Why this rank?"
# ============================================================
def generate_explainer(
    school_row: pd.Series,
    weights: dict,
    top_n_dimensions: int = 2,
) -> str:
    """
    Produce a 1–2 sentence explanation of why the given school scored as it did.

    The explainer focuses on the user's top-weighted dimensions (the ones they
    care about most) and reports how the school performed on those specifically.
    If the school's match score is high, it's because it scored well on what
    the user prioritized; if it scored well on a dimension the user weighted 0,
    we don't mention it because it didn't affect the ranking.

    Example output:
      "Stanford University ranks highly because it scores in the 99th
       percentile for earnings and the 98th for graduation rate, which are
       your top priorities."
    """
    # Keep only dimensions with non-zero weight, sorted by weight descending
    active = sorted(
        ((k, w) for k, w in weights.items() if w > 0),
        key=lambda kv: kv[1],
        reverse=True,
    )
    if not active:
        return f"{school_row['school_name']} is shown because it passed your filters. No weights were set."

    top = active[:top_n_dimensions]

    pieces = []
    for key, _weight in top:
        score_col = f"score_{key}"
        if score_col not in school_row.index or pd.isna(school_row[score_col]):
            continue
        percentile = int(round(school_row[score_col] * 100))
        label = config.SCORING_DIMENSIONS[key]["label"].lower()
        # Trim "high " / "low " prefix for cleaner prose
        for prefix in ("high ", "low "):
            if label.startswith(prefix):
                label = label[len(prefix):]
                break
        pieces.append(f"{_ordinal(percentile)} percentile for {label}")

    if not pieces:
        return f"{school_row['school_name']} passed your filters but lacks reported data on your top priorities."

    if len(pieces) == 1:
        body = pieces[0]
    else:
        body = " and ".join([", ".join(pieces[:-1]), pieces[-1]]) if len(pieces) > 2 else " and ".join(pieces)

    return (
        f"{school_row['school_name']} scores in the {body}, "
        f"which {'is' if len(pieces) == 1 else 'are'} your top "
        f"{'priority' if len(pieces) == 1 else 'priorities'}."
    )


def _ordinal(n: int) -> str:
    """Return '1st', '2nd', '3rd', '99th' etc."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
