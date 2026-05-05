"""
test_utils.py — Unit tests for geographic and classification helpers.

Run with:
    pytest tests/ -v
"""

import math
import pandas as pd
import pytest

import config
from utils import (
    haversine_distance,
    haversine_vector,
    classify_acceptance,
    format_acceptance_badge,
    ACCEPTANCE_BADGE_EMOJI,
    make_button_key,
    normalize_cip4,
    relative_luminance,
    contrast_ratio,
)


# ============================================================
# HAVERSINE DISTANCE
# ============================================================
class TestHaversine:
    def test_same_point_is_zero(self):
        assert haversine_distance(34.05, -118.24, 34.05, -118.24) == pytest.approx(0.0)

    def test_known_la_to_nyc(self):
        """LA (34.0522, -118.2437) to NYC (40.7128, -74.0060) is ~2,445 mi."""
        d = haversine_distance(34.0522, -118.2437, 40.7128, -74.0060)
        assert d == pytest.approx(2445, abs=10)  # within 10 miles

    def test_known_torrance_to_ucla(self):
        """Torrance (33.8358, -118.3406) to UCLA (34.0689, -118.4452) is ~17 mi."""
        d = haversine_distance(33.8358, -118.3406, 34.0689, -118.4452)
        assert d == pytest.approx(17, abs=2)

    def test_symmetric(self):
        """Distance from A→B should equal B→A."""
        d1 = haversine_distance(34.05, -118.24, 40.71, -74.00)
        d2 = haversine_distance(40.71, -74.00, 34.05, -118.24)
        assert d1 == pytest.approx(d2)

    def test_missing_input_returns_nan(self):
        import math
        assert math.isnan(haversine_distance(None, -118.24, 34.05, -118.24))
        assert math.isnan(haversine_distance(float("nan"), -118.24, 34.05, -118.24))

    def test_vector_matches_scalar(self):
        """The vectorized version should give the same result as the scalar one."""
        df = pd.DataFrame({
            "latitude":  [34.0522, 40.7128, 41.8781],
            "longitude": [-118.2437, -74.0060, -87.6298],
        })
        user_lat, user_lon = 33.8358, -118.3406  # Torrance
        vec = haversine_vector(df, user_lat, user_lon)
        scalar = [haversine_distance(user_lat, user_lon,
                                      df.loc[i, "latitude"], df.loc[i, "longitude"])
                  for i in df.index]
        for v, s in zip(vec, scalar):
            assert v == pytest.approx(s, abs=0.1)


# ============================================================
# ACCEPTANCE LIKELIHOOD
# ============================================================
class TestClassifyAcceptance:
    def test_safety_when_above_75th(self):
        """Student SAT above school's 75th percentile = Safety."""
        result = classify_acceptance(student_sat=1500, student_act=None,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "Safety"

    def test_reach_when_below_25th(self):
        """Student SAT below school's 25th percentile = Reach."""
        result = classify_acceptance(student_sat=1100, student_act=None,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "Reach"

    def test_match_when_in_middle(self):
        """Student SAT between 25th and 75th = Match."""
        result = classify_acceptance(student_sat=1300, student_act=None,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "Match"

    def test_safety_at_exact_75th_boundary(self):
        """Student exactly at 75th percentile = Safety (>=)."""
        result = classify_acceptance(student_sat=1400, student_act=None,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "Safety"

    def test_reach_at_exact_25th_boundary(self):
        """Student exactly at 25th percentile = Reach (<=)."""
        result = classify_acceptance(student_sat=1200, student_act=None,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "Reach"

    def test_act_converted_to_sat(self):
        """If only ACT is provided, it should be converted via the concordance table."""
        # ACT 34 ≈ SAT 1500 per the ACT_TO_SAT table; well above a 1400 75th
        result = classify_acceptance(student_sat=None, student_act=34,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "Safety"

    def test_sat_wins_when_both_provided(self):
        """If both SAT and ACT are supplied, SAT takes precedence."""
        # SAT 1100 would be Reach; ACT 34 (SAT 1500 equiv) would be Safety.
        # SAT should win, so result = Reach.
        result = classify_acceptance(student_sat=1100, student_act=34,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "Reach"

    def test_missing_student_score_returns_na(self):
        result = classify_acceptance(student_sat=None, student_act=None,
                                     school_sat_25=1200, school_sat_75=1400)
        assert result == "N/A"

    def test_missing_school_scores_returns_na(self):
        """Test-optional schools with no published SAT range = N/A."""
        result = classify_acceptance(student_sat=1300, student_act=None,
                                     school_sat_25=None, school_sat_75=None)
        assert result == "N/A"


# ============================================================
# make_button_key
# ============================================================

def test_make_button_key_basic():
    assert make_button_key("pin_btn", 123, "11.0701") == "pin_btn_123_11.0701"


def test_make_button_key_single_part():
    assert make_button_key("see_schools", "11.07") == "see_schools_11.07"


def test_make_button_key_coerces_types():
    assert make_button_key("explore", 456, 7.89) == "explore_456_7.89"


# ============================================================
# normalize_cip4
# ============================================================

def test_normalize_cip4_accepts_dotted_format():
    assert normalize_cip4("11.07") == "11.07"


def test_normalize_cip4_accepts_4digit_format():
    assert normalize_cip4("1107") == "11.07"


def test_normalize_cip4_pads_3digit_format():
    """E.g., CIP 01.07 stored as int 107 → padded to '0107' → '01.07'."""
    assert normalize_cip4("107") == "01.07"


# ============================================================
# WCAG contrast helper tests (Phase 6C-1)
# ============================================================

def test_relative_luminance_white_is_one():
    assert relative_luminance("#FFFFFF") == pytest.approx(1.0, abs=0.001)


def test_relative_luminance_black_is_zero():
    assert relative_luminance("#000000") == pytest.approx(0.0, abs=0.001)


def test_contrast_ratio_white_on_black_is_21():
    assert contrast_ratio("#FFFFFF", "#000000") == pytest.approx(21.0, abs=0.05)


def test_contrast_ratio_is_symmetric():
    """Contrast ratio is the same regardless of argument order."""
    a, b = "#0072B2", "#FFFFFF"
    assert contrast_ratio(a, b) == pytest.approx(contrast_ratio(b, a))


# ============================================================
# Acceptance badge rendering (Phase 6C-2 regression guard)
# ============================================================

@pytest.mark.parametrize("key", ["safety", "match", "reach", "unknown"])
def test_acceptance_badge_includes_emoji_and_label(key):
    """format_acceptance_badge must pair the emoji with the text label.

    Regression guard: a future refactor that drops the label or the emoji
    from the rendered string would silently remove accessible text from the
    web-side badge. This test catches that before it ships.
    """
    label = config.ACCEPTANCE_LABELS[key]
    result = format_acceptance_badge(label)
    assert ACCEPTANCE_BADGE_EMOJI[label] in result, (
        f"Expected emoji {ACCEPTANCE_BADGE_EMOJI[label]!r} in badge string for {key!r}, got {result!r}"
    )
    assert label in result, (
        f"Expected label {label!r} in badge string for {key!r}, got {result!r}"
    )
