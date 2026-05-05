"""Tests for URL parameter encoders/decoders in url_state.py.

Phase 13.4a — 8 tests covering encode/decode round-trips and graceful
degradation for invalid inputs. No Streamlit dependency.
Phase 13.4b — 8 tests for RIASEC encode/decode (0-40 integer range).
"""

import pytest

from url_state import decode_cip, decode_tab, encode_cip, encode_tab, encode_riasec, decode_riasec


# ---------- encode_cip / decode_cip ----------


def test_encode_cip_int_to_string():
    assert encode_cip(1107) == "1107"


def test_encode_cip_default_returns_none():
    """Default CIP (0) and None should not be encoded — keeps URLs clean."""
    assert encode_cip(None) is None
    assert encode_cip(0) is None


def test_decode_cip_round_trips():
    assert decode_cip(encode_cip(1107)) == 1107


def test_decode_cip_invalid_returns_none():
    """Garbage in URL should degrade gracefully, not raise."""
    assert decode_cip("not_a_cip") is None
    assert decode_cip("") is None
    assert decode_cip(None) is None


# ---------- encode_tab / decode_tab ----------


def test_encode_tab_default_returns_none():
    """School Finder is the default tab and must never appear in the URL."""
    assert encode_tab("school_finder") is None
    assert encode_tab(None) is None


def test_encode_tab_non_default_encodes():
    assert encode_tab("major_explorer") == "major_explorer"
    assert encode_tab("find_your_fit") == "find_your_fit"


def test_decode_tab_invalid_returns_none():
    """Unknown tab names should degrade gracefully, not raise."""
    assert decode_tab("nonexistent_tab") is None
    assert decode_tab("") is None
    assert decode_tab(None) is None


def test_tab_round_trips():
    for tab in ["major_explorer", "find_your_fit"]:
        assert decode_tab(encode_tab(tab)) == tab


# ---------- encode_riasec / decode_riasec ----------


def test_encode_riasec_full_vector():
    vector = {"R": 30, "I": 40, "A": 20, "S": 4, "E": 10, "C": 20}
    assert encode_riasec(vector) == "R30I40A20S04E10C20"


def test_encode_riasec_zero_pads_single_digit():
    """Single-digit scores must zero-pad to 2 digits."""
    vector = {"R": 5, "I": 8, "A": 0, "S": 4, "E": 12, "C": 16}
    assert encode_riasec(vector) == "R05I08A00S04E12C16"


def test_encode_riasec_none_or_empty_returns_none():
    assert encode_riasec(None) is None
    assert encode_riasec({}) is None


def test_encode_riasec_incomplete_vector_returns_none():
    """If any dimension is missing, don't encode partial data."""
    vector = {"R": 30, "I": 40}  # missing A, S, E, C
    assert encode_riasec(vector) is None


def test_decode_riasec_round_trips():
    vector = {"R": 30, "I": 40, "A": 20, "S": 4, "E": 10, "C": 20}
    assert decode_riasec(encode_riasec(vector)) == vector


def test_decode_riasec_zero_padded_round_trip():
    vector = {"R": 5, "I": 8, "A": 0, "S": 4, "E": 12, "C": 16}
    assert decode_riasec(encode_riasec(vector)) == vector


def test_decode_riasec_invalid_returns_none():
    """Garbage in URL should not raise."""
    assert decode_riasec("not_a_riasec") is None
    assert decode_riasec("R30I40A20S04E10") is None  # too short — missing C
    assert decode_riasec("X30I40A20S04E10C20") is None  # X is not a valid dimension
    assert decode_riasec("") is None
    assert decode_riasec(None) is None


def test_decode_riasec_out_of_range_returns_none():
    """Scores > 40 are invalid per the O*NET 0-40 range."""
    assert decode_riasec("R99I40A20S04E10C20") is None
    assert decode_riasec("R41I40A20S04E10C20") is None  # just one over the max
