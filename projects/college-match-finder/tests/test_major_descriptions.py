"""Tests for major_descriptions.py — Phase 11.1A."""

import pytest
from major_descriptions import get_description, load_major_descriptions


def test_load_returns_dict():
    result = load_major_descriptions()
    assert isinstance(result, dict)
    assert len(result) > 0


def test_get_description_cip4_hit():
    result = get_description("11.07")
    assert result is not None
    for key in ("name", "overview", "what_youll_learn", "typical_classes", "related_majors"):
        assert key in result, f"Missing key: {key}"


def test_get_description_cip6_normalizes():
    assert get_description("11.0701") == get_description("11.07")


def test_get_description_miss_returns_none():
    assert get_description("99.99") is None


def test_get_description_handles_bad_input():
    assert get_description(None) is None
    assert get_description("") is None
    assert get_description("not.a.code") is None


# ---------------------------------------------------------------------------
# Phase 11.1C — stub fallback tests
# ---------------------------------------------------------------------------

def test_covered_major_returns_full_entry():
    """YAML-authored majors return a full entry with no is_stub flag."""
    result = get_description("11.07")
    assert result is not None
    assert not result.get("is_stub", False)
    for key in ("overview", "what_youll_learn", "typical_classes", "related_majors"):
        assert key in result, f"Missing key: {key}"


def test_uncovered_major_returns_stub():
    """CIP4s in the FoS dataset but not in the YAML return a stub dict."""
    # 01.01 (Agricultural Business and Management) is in the cleaned CSV
    # but outside the hand-authored top-60 YAML.
    result = get_description("01.01")
    assert result is not None
    assert result.get("is_stub") is True
    assert result.get("name") is not None
    assert result.get("name") != ""


def test_unknown_cip4_returns_none():
    """CIP4s absent from both the YAML and the FoS dataset return None."""
    assert get_description("99.99") is None
