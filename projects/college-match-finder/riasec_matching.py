"""Matching engine that ranks CIP4 majors by Pearson correlation with a user's RIASEC vector.

Bridges riasec_questionnaire.py (user-side scoring) and riasec_distribution.py (major-side
profiles) for the College Match Finder app. The core math is Pearson correlation: each user's
six-dimensional RIASEC vector is correlated against each of the 416 CIP4 major vectors so
that majors whose interest-profile shape most closely resembles the user's profile rank first.
This approach mirrors the O*NET Interest Profiler's own person-job matching algorithm; see the
O*NET Resource Center (https://www.onetcenter.org/IP.html) for the published methodology. The
choice of Pearson (rather than Euclidean distance) is intentional: it captures profile shape
similarity independent of overall response scale, making it robust to respondents who anchor
high or low across the board.

Holland Code derivation: the three RIASEC dimensions with the highest user scores are
identified and their letters concatenated in descending-score order. Ties are broken by
canonical RIASEC order (R before I before A before S before E before C), so an all-equal
vector always yields "RIA".
"""
from typing import Optional

import numpy as np
import pandas as pd

from config import RIASEC_DIMENSIONS  # re-exported for backward compat with test imports
from riasec_distribution import get_all_cip4_vectors


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _validate_user_vector(user_vector: dict) -> None:
    """Raise ValueError if user_vector is missing any of the six RIASEC keys."""
    missing = [d for d in RIASEC_DIMENSIONS if d not in user_vector]
    if missing:
        raise ValueError(f"user_vector missing required key(s): {missing}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_holland_code(user_vector: dict) -> str:
    """Return the user's three-letter Holland Code derived from their RIASEC scores.

    Ranks dimensions by score descending. Ties are broken by canonical RIASEC
    order (R before I before A before S before E before C). An all-equal or
    all-zero vector returns 'RIA' by this rule.

    Args:
        user_vector: dict with keys R, I, A, S, E, C and float values.

    Returns:
        Three-letter string, e.g. 'IRE' or 'SAE'.

    Raises:
        ValueError: if any of the six RIASEC keys are absent.
    """
    _validate_user_vector(user_vector)
    ranked = sorted(
        RIASEC_DIMENSIONS,
        key=lambda d: (-user_vector[d], RIASEC_DIMENSIONS.index(d)),
    )
    return "".join(ranked[:3])


def compute_correlations(user_vector: dict) -> pd.DataFrame:
    """Compute Pearson correlation between the user's RIASEC vector and each CIP4 major.

    When the user vector has zero variance (all six values are equal), Pearson
    correlation is mathematically undefined. In that case every correlation is
    returned as np.nan; callers should prompt the user to vary their responses.

    Majors whose own vector has zero variance or contains any NaN value also yield
    np.nan — these are not filtered out so the caller retains full control.

    Args:
        user_vector: dict with keys R, I, A, S, E, C and float values.

    Returns:
        DataFrame with columns ['cip4', 'correlation', 'R', 'I', 'A', 'S', 'E', 'C'],
        sorted by correlation descending (NaN values last). One row per CIP4 (416 rows).

    Raises:
        ValueError: if any of the six RIASEC keys are absent.
    """
    _validate_user_vector(user_vector)

    df = get_all_cip4_vectors()
    user_arr = np.array([user_vector[d] for d in RIASEC_DIMENSIONS], dtype=float)

    result = df.copy()

    if np.std(user_arr) == 0.0:
        result["correlation"] = np.nan
    else:
        # Per-row Pearson via np.corrcoef — readable and plenty fast for 416 rows
        correlations: list = []
        for _, row in df.iterrows():
            major_arr = np.array([row[d] for d in RIASEC_DIMENSIONS], dtype=float)
            if np.any(np.isnan(major_arr)) or np.std(major_arr) == 0.0:
                correlations.append(np.nan)
            else:
                corr = float(np.corrcoef(user_arr, major_arr)[0, 1])
                correlations.append(corr)
        result["correlation"] = correlations

    result = result.sort_values("correlation", ascending=False, na_position="last")
    result = result.reset_index(drop=True)
    return result[["cip4", "correlation", *RIASEC_DIMENSIONS]]


def get_top_n_matches(user_vector: dict, n: int = 10) -> pd.DataFrame:
    """Return the top n CIP4 majors most aligned with the user's RIASEC vector.

    Drops rows with NaN correlations before selecting top n so that majors with
    no O*NET coverage do not consume a result slot. If the user vector has zero
    variance (all correlations NaN), returns an empty DataFrame.

    Args:
        user_vector: dict with keys R, I, A, S, E, C and float values.
        n: number of top matches to return. Default 10 for the Find Your Fit page;
           Phase 12.3 calls with n=40 for the alignment badge threshold.

    Returns:
        DataFrame with the same columns as compute_correlations(), at most n rows.

    Raises:
        ValueError: if any of the six RIASEC keys are absent.
    """
    df = compute_correlations(user_vector)
    df = df.dropna(subset=["correlation"])
    return df.head(n).reset_index(drop=True)
