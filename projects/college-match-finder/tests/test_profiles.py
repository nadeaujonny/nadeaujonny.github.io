"""Unit tests for profiles.py — pure functions, no Streamlit dependency."""
import pytest

from profiles import (
    CUSTOM_PROFILE,
    PROFILE_ORDER,
    PRESETS,
    get_preset_weights,
    match_profile,
)


class TestPresetsStructure:
    def test_all_presets_have_seven_dimensions(self):
        """Every preset must define all 7 scoring dimensions."""
        expected_dims = {
            "affordability", "graduation_rate", "retention_rate",
            "earnings", "selectivity", "low_debt", "repayment",
        }
        for name, weights in PRESETS.items():
            assert set(weights.keys()) == expected_dims, (
                f"Preset '{name}' has dimensions {set(weights.keys())}, expected {expected_dims}"
            )

    def test_all_preset_values_in_range(self):
        """Every weight value must be in [0, 5]."""
        for name, weights in PRESETS.items():
            for dim, val in weights.items():
                assert 0 <= val <= 5, f"Preset '{name}' has {dim}={val}, out of [0,5]"

    def test_custom_not_in_presets(self):
        """The Custom sentinel must never be a PRESETS key."""
        assert CUSTOM_PROFILE not in PRESETS

    def test_profile_order_matches_presets_plus_custom(self):
        """PROFILE_ORDER contains exactly Custom + every PRESETS key."""
        assert PROFILE_ORDER[0] == CUSTOM_PROFILE
        assert set(PROFILE_ORDER[1:]) == set(PRESETS.keys())


class TestGetPresetWeights:
    def test_returns_correct_bundle(self):
        weights = get_preset_weights("Balanced")
        assert weights == {
            "affordability": 3, "graduation_rate": 3, "retention_rate": 3,
            "earnings": 3, "selectivity": 3, "low_debt": 3, "repayment": 3,
        }

    def test_returns_copy_not_reference(self):
        """Mutating the returned dict must not affect PRESETS."""
        weights = get_preset_weights("Balanced")
        weights["affordability"] = 999
        assert PRESETS["Balanced"]["affordability"] == 3

    def test_unknown_name_raises(self):
        with pytest.raises(KeyError):
            get_preset_weights("Nonexistent")

    def test_custom_sentinel_raises(self):
        """Custom is a sentinel, not a real profile — must raise."""
        with pytest.raises(KeyError):
            get_preset_weights(CUSTOM_PROFILE)


class TestMatchProfile:
    def test_balanced_all_threes(self):
        weights = {
            "affordability": 3, "graduation_rate": 3, "retention_rate": 3,
            "earnings": 3, "selectivity": 3, "low_debt": 3, "repayment": 3,
        }
        assert match_profile(weights) == "Balanced"

    def test_each_preset_round_trips(self):
        """For every preset, get_preset_weights → match_profile returns the same name."""
        for name in PRESETS:
            weights = get_preset_weights(name)
            assert match_profile(weights) == name, (
                f"{name} did not round-trip through match_profile"
            )

    def test_one_off_returns_custom(self):
        """A single weight off by one should yield 'Custom'."""
        weights = get_preset_weights("Balanced")
        weights["affordability"] = 4  # was 3
        assert match_profile(weights) == CUSTOM_PROFILE

    def test_missing_key_returns_custom(self):
        weights = {"affordability": 3, "graduation_rate": 3}  # incomplete
        assert match_profile(weights) == CUSTOM_PROFILE

    def test_extra_key_returns_custom(self):
        weights = get_preset_weights("Balanced")
        weights["extra_dim"] = 3
        assert match_profile(weights) == CUSTOM_PROFILE
