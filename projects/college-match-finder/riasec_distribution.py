"""Loader for Phase 12.1 CIP4-level RIASEC interest profile data.

Reads cip4_riasec.csv (416 rows × 9 columns) produced by Phase 12.1 and
exposes two public functions. get_riasec_for_cip4() returns the six O*NET
IRT-scaled RIASEC scores plus metadata for a single CIP4 as a typed dict,
or None for CIP4s with no O*NET interest coverage (e.g., Liberal Arts 24.01,
which has zero routing SOCs with usable O*NET data — n_socs == 0, all scores
NaN). get_all_cip4_vectors() returns the full 416-row RIASEC matrix for batch
Pearson correlation in Phase 12.3. Both rely on the same lru_cache load so
the CSV is read at most once per session.
"""
from functools import lru_cache
from pathlib import Path
from typing import Optional

import pandas as pd

from config import RIASEC_DIMENSIONS
from utils import normalize_cip4

_CSV_PATH = Path(__file__).parent / "data" / "cleaned" / "cip4_riasec.csv"


@lru_cache(maxsize=1)
def _load_riasec_data() -> pd.DataFrame:
    """Load the cleaned RIASEC data once per session.

    Cached because the CSV is static on disk and is read by every
    page render that annotates majors with RIASEC alignment.
    """
    return pd.read_csv(_CSV_PATH, dtype={"cip4": str})


def get_riasec_for_cip4(cip4: str) -> Optional[dict]:
    """Return the RIASEC interest profile for a CIP4, or None if unavailable.

    Args:
        cip4: '44.07' or '4407' format both accepted; float inputs tolerated.

    Returns:
        Dict with shape::

            {
                'cip4': '44.07',
                'scores': {'R': 1.66, 'I': 3.52, 'A': 2.69,
                           'S': 6.47, 'E': 3.57, 'C': 3.55},
                'n_socs': 7,
                'coverage_pct': 77.78,
            }

        or None if the CIP4 has no O*NET interest data (n_socs == 0, all
        scores NaN — e.g., Liberal Arts 24.01, Military Tech 28.05/28.06).
    """
    target = normalize_cip4(cip4)
    df = _load_riasec_data()
    row = df[df["cip4"] == target]
    if row.empty:
        return None
    r = row.iloc[0]
    if pd.isna(r["R"]):
        return None
    return {
        "cip4": target,
        "scores": {col: float(r[col]) for col in RIASEC_DIMENSIONS},
        "n_socs": int(r["n_socs"]),
        "coverage_pct": float(r["coverage_pct"]),
    }


def get_all_cip4_vectors() -> pd.DataFrame:
    """Return the full 416-row RIASEC matrix for batch correlation.

    Returns:
        DataFrame with columns ['cip4', 'R', 'I', 'A', 'S', 'E', 'C'].
        Includes rows with NaN scores (e.g., 24.01 Liberal Arts); callers
        should dropna() before computing Pearson correlations.
    """
    df = _load_riasec_data()
    return df[["cip4", *RIASEC_DIMENSIONS]].copy()
