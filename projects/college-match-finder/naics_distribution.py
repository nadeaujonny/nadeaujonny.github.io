"""Loader for Phase 11.3.2 CIP4-level NAICS3 industry distribution.

Mirrors the loader pattern established by nyfed_outcomes.py and
major_descriptions.py: LRU-cached, importable from any working
directory via Path(__file__).parent, and tolerant to both the
'XX.XX' and 'XXXX' CIP4 input formats already in use across the app.
"""
from functools import lru_cache
from pathlib import Path

import pandas as pd

from utils import normalize_cip4

# Anchor to this module's directory so the loader works regardless of
# the caller's working directory (tests, REPL, Streamlit). Same pattern
# nyfed_outcomes.py uses.
CSV_PATH = Path(__file__).parent / "data" / "cleaned" / "cip4_naics3_distribution.csv"


@lru_cache(maxsize=1)
def _load() -> pd.DataFrame:
    """Load the cleaned distribution once per session.

    Cached because the CSV is static on disk and is read by every
    Major Explorer page render.
    """
    return pd.read_csv(CSV_PATH, dtype={"cip4": str, "naics3": str})


def get_naics_distribution(cip4: str) -> pd.DataFrame | None:
    """Return the NAICS3 distribution for a CIP4, or None if missing.

    Args:
        cip4: '11.07' or '1107' format both accepted.

    Returns:
        DataFrame with columns naics3, naics3_title, weighted_emp,
        share_in_naics3, sorted descending by share. Or None if the
        CIP4 has no NAICS distribution (e.g., 28.05/28.06 Military
        Technologies, where all routing SOCs lack detailed BLS data).
    """
    target = normalize_cip4(cip4)
    df = _load()
    sub = df[df["cip4"] == target]
    if sub.empty:
        return None
    return sub.drop(columns=["cip4"]).reset_index(drop=True)
