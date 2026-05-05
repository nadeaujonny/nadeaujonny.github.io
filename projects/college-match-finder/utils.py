"""
utils.py — Geographic and classification helpers for College Match Finder.

Three jobs:
  1. Haversine distance between two lat/long points (in miles).
  2. ZIP code → (lat, long) lookup, for translating user-supplied ZIP codes
     into coordinates for distance filtering.
  3. Acceptance likelihood classification (Safety / Match / Reach / N/A)
     based on the student's test score vs. the school's 25th–75th percentile
     range.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

import config


# ============================================================
# HAVERSINE DISTANCE
# ============================================================
# Earth's mean radius in miles. Used by the haversine formula below.
EARTH_RADIUS_MI = 3958.8


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Great-circle distance between two lat/long points, in miles.

    Accepts degrees (not radians) for all four arguments. Returns NaN if any
    input is missing — used in the scoring path where some schools have no
    recorded coordinates.
    """
    # Guard against missing values. The data_prep step leaves 0 missing
    # lat/longs, but defensive coding here keeps the app robust.
    for v in (lat1, lon1, lat2, lon2):
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return float("nan")

    # Convert degrees to radians
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # Haversine formula:
    #   a = sin²(Δlat/2) + cos(lat1)·cos(lat2)·sin²(Δlon/2)
    #   c = 2 · atan2(√a, √(1−a))
    #   d = R · c
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_MI * c


def haversine_vector(df: pd.DataFrame, user_lat: float, user_lon: float,
                     lat_col: str = "latitude", lon_col: str = "longitude") -> pd.Series:
    """
    Vectorized haversine distance from (user_lat, user_lon) to every row in df.

    Returns a Series of distances in miles. Much faster than applying
    haversine_distance row-by-row — matters when the user drags a radius slider
    and we recompute for 2,477 schools on every interaction.
    """
    import numpy as np

    lat1 = math.radians(user_lat)
    lon1 = math.radians(user_lon)
    lat2 = np.radians(df[lat_col].astype(float))
    lon2 = np.radians(df[lon_col].astype(float))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return EARTH_RADIUS_MI * c


# ============================================================
# ZIP CODE LOOKUP
# ============================================================
# The ZIP lookup table is loaded lazily on first use and cached, so the
# Streamlit app doesn't pay the cost on every interaction.
_zip_cache: pd.DataFrame | None = None


def _load_zip_table() -> pd.DataFrame | None:
    """
    Lazily load the cleaned ZIP → lat/long table. Returns None if the file
    hasn't been prepared yet (distance features are optional pre-Phase 4).
    """
    global _zip_cache
    if _zip_cache is not None:
        return _zip_cache

    path = config.DATA_CLEANED_DIR / config.CLEANED_ZIP_LATLONG
    if not path.exists():
        return None

    df = pd.read_csv(path, dtype={"zip": str})
    # Normalize ZIPs to 5-digit zero-padded strings so "90501" and "0501" (CT)
    # both work correctly
    df["zip"] = df["zip"].str.zfill(5)
    _zip_cache = df.set_index("zip")
    return _zip_cache


def zip_to_coords(zip_code: str) -> tuple[float, float] | None:
    """
    Look up (lat, lng) for a U.S. ZIP code. Returns None if the ZIP isn't
    found or if the ZIP table hasn't been built yet.

    Accepts either a string or a number; normalizes to 5-digit zero-padded.
    """
    if zip_code is None or str(zip_code).strip() == "":
        return None

    z = str(zip_code).strip().zfill(5)
    table = _load_zip_table()
    if table is None:
        return None

    if z not in table.index:
        return None

    row = table.loc[z]
    # Column name varies between source files ("lat"/"lng" vs "latitude"/"longitude")
    lat = row.get("lat", row.get("latitude"))
    lng = row.get("lng", row.get("longitude"))
    if pd.isna(lat) or pd.isna(lng):
        return None
    return float(lat), float(lng)


# ============================================================
# ACCEPTANCE LIKELIHOOD
# ============================================================
def _student_sat_equivalent(sat: float | None, act: float | None) -> float | None:
    """
    Return a single SAT-equivalent score from whichever of SAT or ACT the
    student provided. If both are given, SAT wins (per the app spec). If
    neither, return None.
    """
    if sat is not None and not (isinstance(sat, float) and math.isnan(sat)):
        return float(sat)
    if act is not None and not (isinstance(act, float) and math.isnan(act)):
        act_int = int(round(float(act)))
        return float(config.ACT_TO_SAT.get(act_int, float("nan")))
    return None


def classify_acceptance(
    student_sat: float | None,
    student_act: float | None,
    school_sat_25: float | None,
    school_sat_75: float | None,
) -> str:
    """
    Return "Safety", "Match", "Reach", or "N/A".

    Rules:
      - Student score >= school's 75th percentile  →  Safety
      - Student score between 25th and 75th        →  Match
      - Student score <= school's 25th percentile  →  Reach
      - Missing inputs                             →  N/A
    """
    student = _student_sat_equivalent(student_sat, student_act)
    if student is None or math.isnan(student):
        return config.ACCEPTANCE_LABELS["unknown"]
    if pd.isna(school_sat_25) or pd.isna(school_sat_75):
        return config.ACCEPTANCE_LABELS["unknown"]

    if student >= school_sat_75:
        return config.ACCEPTANCE_LABELS["safety"]
    if student <= school_sat_25:
        return config.ACCEPTANCE_LABELS["reach"]
    return config.ACCEPTANCE_LABELS["match"]


# Emoji prefixes for each acceptance-likelihood label. Uses both color AND
# text (per the project's accessibility requirement of never conveying
# information through color alone).
ACCEPTANCE_BADGE_EMOJI = {
    "Safety": "🟢",
    "Match":  "🟡",
    "Reach":  "🔴",
    "N/A":    "⚪",
}


def format_acceptance_badge(label: str) -> str:
    """Return 'EMOJI label' for web-side acceptance badge rendering."""
    return f"{ACCEPTANCE_BADGE_EMOJI.get(label, '⚪')} {label}"


# ============================================================
# CIP CODE FORMATTING
# ============================================================

def format_cip_code(cip_int: int) -> str:
    """Format a 4-digit CIP integer as a 'XX.XX' display string.

    Examples:
        1107 → "11.07"
        4901 → "49.01"
        0 → ""  (sentinel for "no CIP")

    Raises ValueError for negative ints or ints with more than 4 digits.
    """
    if cip_int == 0:
        return ""
    if cip_int < 0 or cip_int > 9999:
        raise ValueError(f"CIP code out of range: {cip_int}")
    return f"{cip_int // 100:02d}.{cip_int % 100:02d}"


def parse_cip_code(cip_str: str) -> int:
    """Parse a 'XX.XX' CIP display string back to a 4-digit integer.

    Examples:
        "11.07" → 1107
        "49.01" → 4901
        "" → 0  (sentinel for "no CIP")

    Raises ValueError for malformed input.
    """
    if not cip_str:
        return 0
    cleaned = cip_str.replace(".", "").strip()
    if not cleaned.isdigit():
        raise ValueError(f"CIP code not parseable: {cip_str!r}")
    return int(cleaned)


def normalize_cip4(cip4) -> str:
    """Normalize a CIP4 code in any common format to the canonical 'XX.XX' string.

    Accepts str, int, or float input. Idempotent on already-formatted strings.
    Handles: '11.07' → '11.07', '1107' → '11.07', '107' → '01.07',
    float 1.0 → '01.00' (pandas may produce floats from CSV columns without
    a dtype override).

    Use this when the input format is uncertain. Use parse_cip_code when the
    input is guaranteed 'XX.XX' format and you need an int.
    """
    s = str(cip4).strip()
    if "." in s:
        left, right = s.split(".", 1)
        return f"{left.zfill(2)}.{right.zfill(2)}"
    s = s.zfill(4)
    return f"{s[:2]}.{s[2:]}"


def make_button_key(prefix: str, *parts) -> str:
    """Build a Streamlit widget key from a prefix and identifier parts.

    Parts are coerced to str and joined with underscores. Use for any
    dynamic button key where collisions across reruns would cause bugs.

        make_button_key("pin_btn", unit_id, cip_code)  # -> "pin_btn_123456_11.0701"
    """
    return "_".join([prefix, *map(str, parts)])


# ============================================================
# WCAG CONTRAST HELPERS
# ============================================================

def relative_luminance(hex_color: str) -> float:
    """Compute WCAG relative luminance of a hex color.

    Args:
        hex_color: Hex string in '#RRGGBB' or '#RGB' format (case-insensitive).

    Returns:
        Relative luminance in 0.0–1.0 per WCAG 2.1 §1.4.3.

    Raises:
        ValueError if hex_color is not a valid 6-char hex after expansion.
    """
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"Expected #RRGGBB, got {hex_color!r}")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

    def _channel(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    """Compute WCAG contrast ratio between two hex colors.

    Returns a value in 1.0–21.0. WCAG AA thresholds:
      - 3.0 for non-text UI components and large text
      - 4.5 for normal-size text
      - 7.0 for AAA-level text contrast

    Args:
        hex_a, hex_b: Hex strings in '#RRGGBB' or '#RGB' format.

    Returns:
        Contrast ratio (always >= 1.0).
    """
    l1 = relative_luminance(hex_a)
    l2 = relative_luminance(hex_b)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
