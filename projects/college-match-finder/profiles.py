# profiles.py — Preset weight bundles for first-time users (V4 Stat Depth E).
"""
Pure-function profile helpers. No Streamlit dependencies — all UI logic lives in app.py.

A "profile" is a named bundle of weight values that initializes all 7 scoring sliders
at once. The dict keys match config.SCORING_DIMENSIONS exactly. The "Custom" sentinel
is reserved as the default selectbox value and is NEVER a key in PRESETS — it indicates
that the user's current weights don't match any preset.
"""
from __future__ import annotations

# The Custom sentinel — reserved selectbox label, never a key in PRESETS.
CUSTOM_PROFILE = "Custom"

# Display order in the selectbox. Custom first so it's the default visible option.
PROFILE_ORDER: list[str] = [
    CUSTOM_PROFILE,
    "Balanced",
    "Career-focused",
    "Affordability-focused",
    "Selectivity-focused",
]

# Preset weight bundles. Keys MUST match config.SCORING_DIMENSIONS exactly.
PRESETS: dict[str, dict[str, int]] = {
    "Balanced": {
        "affordability": 3, "graduation_rate": 3, "retention_rate": 3,
        "earnings": 3, "selectivity": 3, "low_debt": 3, "repayment": 3,
    },
    "Career-focused": {
        "affordability": 2, "graduation_rate": 4, "retention_rate": 3,
        "earnings": 5, "selectivity": 2, "low_debt": 3, "repayment": 4,
    },
    "Affordability-focused": {
        "affordability": 5, "graduation_rate": 3, "retention_rate": 3,
        "earnings": 2, "selectivity": 1, "low_debt": 5, "repayment": 4,
    },
    "Selectivity-focused": {
        "affordability": 2, "graduation_rate": 5, "retention_rate": 4,
        "earnings": 4, "selectivity": 5, "low_debt": 2, "repayment": 3,
    },
}


def get_preset_weights(name: str) -> dict[str, int]:
    """Return the weight bundle for a named profile.

    Raises KeyError for unknown names, including the CUSTOM_PROFILE sentinel
    (callers must guard against that case before calling).
    """
    return dict(PRESETS[name])  # copy so callers can't mutate PRESETS


def match_profile(weights: dict[str, int]) -> str:
    """Given the current 7 weight values, return the matching profile name or 'Custom'.

    Comparison is exact-equality on integer values. If `weights` has extra or missing
    dimension keys relative to a preset, the preset does not match. Returns the FIRST
    match in PROFILE_ORDER (skipping CUSTOM_PROFILE), so the order list defines tiebreaks.
    """
    for name in PROFILE_ORDER:
        if name == CUSTOM_PROFILE:
            continue
        preset = PRESETS[name]
        # Exact equality: same keys, same values
        if set(weights.keys()) == set(preset.keys()) and all(
            weights[k] == preset[k] for k in preset
        ):
            return name
    return CUSTOM_PROFILE
