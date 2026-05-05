"""URL parameter encoders/decoders. Pure functions for unit testability.

The orchestration (read/write to st.query_params + session state) lives in
app.py's _parse_url_into_session_state and _write_session_state_to_url.
This module provides just the per-value encoding logic.

Phase 13.4a: tab + Major Explorer CIP.
Phase 13.4b: RIASEC vector.
"""

from __future__ import annotations

from config import RIASEC_DIMENSIONS

VALID_TABS = {"school_finder", "major_explorer", "find_your_fit"}
DEFAULT_TAB = "school_finder"


def encode_tab(tab: str | None) -> str | None:
    """Encode an active tab name for the URL. Returns None for default/unset/invalid."""
    if tab is None or tab == DEFAULT_TAB or tab not in VALID_TABS:
        return None
    return tab


def decode_tab(raw: str | None) -> str | None:
    """Decode a `tab` URL param. Returns None for invalid/missing values."""
    if not raw or raw not in VALID_TABS:
        return None
    return raw


def encode_cip(cip: int | None) -> str | None:
    """Encode a Major Explorer CIP (int) for the URL. Returns None for default/unset."""
    if cip is None or cip == 0:
        return None
    return str(cip)


def decode_cip(raw: str | None) -> int | None:
    """Decode a `cip` URL param. Returns None for invalid/missing values."""
    if not raw:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# RIASEC vector encoding (Phase 13.4b)
# Format: R##I##A##S##E##C## — six (letter, 2-digit integer) pairs.
# Scores are integer sums of 10 O*NET items rated 0–4, so range is 0–40.
# ---------------------------------------------------------------------------

RIASEC_SCORE_MAX = 40   # integer sum of 10 items × 4 max — per O*NET methodology
RIASEC_ENCODED_DIGITS = 2


def encode_riasec(vector: dict | None) -> str | None:
    """Encode a 6-dimension RIASEC vector for the URL.

    Args:
        vector: dict with keys 'R','I','A','S','E','C' and integer values 0-40.
                None or empty dict returns None (skips encoding).

    Returns:
        12-char string like 'R30I40A20S04E10C20', or None if vector is empty/invalid.
    """
    if not vector:
        return None
    parts = []
    for dim in RIASEC_DIMENSIONS:
        score = vector.get(dim)
        if score is None:
            return None  # incomplete vector — don't encode partial data
        clamped = max(0, min(RIASEC_SCORE_MAX, int(score)))
        parts.append(f"{dim}{clamped:02d}")
    return "".join(parts)


def decode_riasec(raw: str | None) -> dict | None:
    """Decode a `riasec` URL param back into a vector dict.

    Returns None for invalid/missing input. Tolerates noise gracefully.
    """
    expected_len = len(RIASEC_DIMENSIONS) * (1 + RIASEC_ENCODED_DIGITS)
    if not raw or len(raw) != expected_len:
        return None
    vector = {}
    pos = 0
    for dim in RIASEC_DIMENSIONS:
        if raw[pos] != dim:
            return None  # dimension out of order or wrong letter
        try:
            score = int(raw[pos + 1 : pos + 1 + RIASEC_ENCODED_DIGITS])
        except ValueError:
            return None
        if score < 0 or score > RIASEC_SCORE_MAX:
            return None  # out of valid range
        vector[dim] = score
        pos += 1 + RIASEC_ENCODED_DIGITS
    return vector
