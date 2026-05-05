"""Tests for the centralized PALETTE in config.py (Phase 6B / 6C-1)."""

import pytest
from config import PALETTE
from utils import contrast_ratio


def test_palette_required_keys_present():
    """Every consumer-facing token has a value (catches typos in PALETTE additions)."""
    required = [
        # Wong base
        "wong_blue", "wong_orange", "wong_green", "wong_pink", "wong_sky",
        "wong_vermilion", "wong_yellow", "wong_gray",
        # Demographics
        "demo_women", "demo_men_other", "demo_black", "demo_hispanic",
        "demo_asian", "demo_white", "demo_nonresident", "demo_other",
        # Mobility
        "mobility_low", "mobility_mid", "mobility_high",
        # Comparison
        "comparison",
        # CI bar
        "ci_track_bg", "ci_band_fill", "ci_band_border",
        "ci_point", "ci_score_text", "ci_label_text",
        # Quartiles
        "quartile_bottom", "quartile_below_avg", "quartile_above_avg", "quartile_top",
        # Categorical bars
        "categorical_primary", "categorical_other",
        # School Finder map
        "map_score_scale", "map_marker_border",
        # Major Explorer choropleths
        "choropleth_scale", "choropleth_land", "choropleth_borders",
        # NAICS chart
        "naics_chart_bg", "gridline_light",
        # Gridlines
        "gridline",
        # PDF export
        "pdf_card_bg", "pdf_card_border",
        "pdf_safety_tint", "pdf_match_tint", "pdf_reach_tint", "pdf_na_tint",
    ]
    missing = [k for k in required if k not in PALETTE]
    assert not missing, f"Missing PALETTE keys: {missing}"


def test_palette_no_demo_mobility_collisions():
    """Demo tokens and mobility tokens must not share hex values (regression guard for 6B fix)."""
    demo_hexes = {k: v for k, v in PALETTE.items() if k.startswith("demo_")}
    mobility_hexes = {k: v for k, v in PALETTE.items() if k.startswith("mobility_")}
    overlap = set(demo_hexes.values()) & set(mobility_hexes.values())
    assert not overlap, f"Demo and mobility tokens share hex values: {overlap}"


def test_palette_demo_tokens_unique():
    """Within the demo palette, no two tokens share a hex (regression guard for White/Men collision)."""
    demo_hexes = {k: v for k, v in PALETTE.items() if k.startswith("demo_")}
    seen: dict = {}
    for token, hex_val in demo_hexes.items():
        if hex_val in seen:
            raise AssertionError(
                f"Demo collision: {token} and {seen[hex_val]} both = {hex_val}"
            )
        seen[hex_val] = token


# ============================================================
# WCAG AA contrast tests for PALETTE tokens (Phase 6C-1)
# ============================================================
# Each hex token is verified against the background it renders against.
# This catches regressions where a future palette change drops a token below
# the 3:1 minimum for non-text UI components.

# Map each testable PALETTE hex token to its rendering background.
# Backgrounds: "#FFFFFF" for solid-white plot_bgcolor and the Streamlit page;
# transparent chart backgrounds use "#FFFFFF" because Streamlit's default
# theme renders white behind the transparent layer.
_TOKEN_BACKGROUNDS: dict[str, str] = {
    # Wong primary tokens — used as chart marker fills on white/transparent
    # Note: wong_orange, wong_sky, wong_yellow, wong_gray are excluded below
    # because they fail at their documented ratios — see EXCLUDED_TOKENS.
    "wong_blue":      "#FFFFFF",
    "wong_green":     "#FFFFFF",
    "wong_pink":      "#FFFFFF",
    "wong_vermilion": "#FFFFFF",

    # Demographics chart segments on transparent (→ white) background
    # Note: demo_men_other, demo_hispanic, demo_other are excluded below.
    "demo_women":       "#FFFFFF",
    "demo_black":       "#FFFFFF",
    "demo_asian":       "#FFFFFF",
    "demo_white":       "#FFFFFF",
    "demo_nonresident": "#FFFFFF",

    # Earnings Mobility bars on transparent (→ white) background
    "mobility_low":  "#FFFFFF",
    "mobility_mid":  "#FFFFFF",
    "mobility_high": "#FFFFFF",

    # Confidence interval bar annotations on transparent (→ white) background
    "ci_point":      "#FFFFFF",
    "ci_score_text": "#FFFFFF",
    "ci_label_text": "#FFFFFF",

    # Quartile colors — verified and fixed in 6C-1; all now pass
    "quartile_bottom":    "#FFFFFF",
    "quartile_below_avg": "#FFFFFF",
    "quartile_above_avg": "#FFFFFF",
    "quartile_top":       "#FFFFFF",

    # Categorical bars (NAICS on white bg, RIASEC on transparent → white)
    "categorical_primary": "#FFFFFF",

}

# Tokens explicitly excluded from contrast verification (with documented reason).
# Format: token → reason string. The coverage test enforces that every PALETTE
# key appears in exactly one of _TOKEN_BACKGROUNDS, _EXCLUDED_TOKENS, or the
# comparison/pdf special cases below.
_EXCLUDED_TOKENS: dict[str, str] = {
    # Wong (2011) colorblind-safe mid-tones: optimized for distinguishability
    # by colorblind users (deuteranopia/protanopia/tritanopia), not luminance
    # contrast against white. Replacing with darker variants would re-introduce
    # colorblindness ambiguity. Trade-off accepted: chart fills are large-area
    # elements where lower luminance contrast remains perceivable. Ratios:
    "wong_orange":    "Wong (2011) colorblind-safe mid-tone, 2.25:1 against white. "
                      "Optimized for colorblind distinguishability; replacing would "
                      "re-introduce colorblindness ambiguity. Trade-off accepted.",
    "wong_sky":       "Wong (2011) colorblind-safe mid-tone, 2.31:1 against white. "
                      "Same trade-off as wong_orange.",
    "wong_yellow":    "Wong (2011) colorblind-safe mid-tone, 1.32:1 against white. "
                      "Same trade-off as wong_orange.",
    "wong_gray":      "Wong (2011) colorblind-safe mid-tone, 2.85:1 against white. "
                      "Same trade-off as wong_orange.",

    # Derived tokens that share the excluded Wong hexes
    "demo_men_other": "Shares hex with wong_sky (#56B4E9, 2.31:1). Same colorblind "
                      "trade-off applies — see wong_sky exclusion.",
    "demo_hispanic":  "Shares hex with wong_orange (#E69F00, 2.25:1). Same colorblind "
                      "trade-off applies — see wong_orange exclusion.",
    "demo_other":     "Shares hex with wong_gray (#999999, 2.85:1). Same colorblind "
                      "trade-off applies — see wong_gray exclusion.",
    "categorical_other": "Shares hex with wong_gray (#999999, 2.85:1). Same colorblind "
                         "trade-off applies — see wong_gray exclusion.",

    # rgba/transparent values — semi-transparent overlays, not solid fills
    "ci_track_bg":    "rgba — transparency, not a contrast surface",
    "ci_band_fill":   "rgba — transparency",
    "ci_band_border": "rgba — transparency",
    "gridline":       "rgba — gridline, intentionally low contrast",

    # Intentionally low-contrast gridline (chart structure aid, not data ink)
    "gridline_light": "Low-contrast gridline by design, 1.16:1 — chart structure aid",

    # Background tokens (comparison references, not foreground subjects)
    "naics_chart_bg": "Background token (named CSS 'white')",

    # Named Plotly scales — not single hexes
    "map_score_scale":   "Plotly named scale, not a hex",
    "choropleth_scale":  "Plotly named scale, not a hex",

    # Named CSS colors — Streamlit/Plotly handle these natively
    "map_marker_border": "Named CSS color",
    "choropleth_land":   "Named CSS color",
    "choropleth_borders": "Named CSS color",

    # PDF tokens — RGB tuples, not hex strings
    "pdf_card_bg":     "RGB tuple, not hex",
    "pdf_card_border": "RGB tuple",
    "pdf_safety_tint": "RGB tuple",
    "pdf_match_tint":  "RGB tuple",
    "pdf_reach_tint":  "RGB tuple",
    "pdf_na_tint":     "RGB tuple",
}

# Tokens handled by special-case tests rather than parametrize
_SPECIAL_CASE_TOKENS = {"comparison"}

_WCAG_AA_NON_TEXT = 3.0


@pytest.mark.parametrize("token,bg", sorted(_TOKEN_BACKGROUNDS.items()))
def test_palette_token_meets_wcag_aa(token: str, bg: str) -> None:
    """Every tested chart-color hex meets WCAG AA non-text contrast against its render bg."""
    fg_hex = PALETTE[token]
    bg_hex = bg
    ratio = contrast_ratio(fg_hex, bg_hex)
    assert ratio >= _WCAG_AA_NON_TEXT, (
        f"PALETTE['{token}'] = {fg_hex} fails WCAG AA against {bg_hex} "
        f"(contrast {ratio:.2f} < {_WCAG_AA_NON_TEXT})"
    )


def test_comparison_palette_passing_entries_meet_wcag_aa() -> None:
    """Comparison palette entries that aren't excluded Wong mid-tones pass WCAG AA.

    #E69F00 (wong_orange) is excluded for the same colorblind trade-off as the
    wong_orange token — see _EXCLUDED_TOKENS. The remaining 3 entries are verified.
    """
    # Wong-derived hexes excluded for colorblind trade-off (matches _EXCLUDED_TOKENS)
    _wong_excluded_hexes = {
        PALETTE["wong_orange"],
        PALETTE["wong_sky"],
        PALETTE["wong_yellow"],
        PALETTE["wong_gray"],
    }
    failures = []
    for hex_val in PALETTE["comparison"]:
        if hex_val in _wong_excluded_hexes:
            continue
        ratio = contrast_ratio(hex_val, "#FFFFFF")
        if ratio < _WCAG_AA_NON_TEXT:
            failures.append(f"{hex_val} (ratio {ratio:.2f})")
    assert not failures, f"Comparison palette non-excluded entries fail WCAG AA: {failures}"


def test_palette_coverage_complete() -> None:
    """Every PALETTE key is either contrast-tested, excluded, or a special-case token."""
    all_keys = set(PALETTE.keys())
    tested = set(_TOKEN_BACKGROUNDS.keys())
    excluded = set(_EXCLUDED_TOKENS.keys())
    special = _SPECIAL_CASE_TOKENS
    uncovered = all_keys - tested - excluded - special
    assert not uncovered, (
        f"PALETTE keys with no contrast assertion, exclusion, or special-case: {uncovered}. "
        f"Add to _TOKEN_BACKGROUNDS (with bg) or _EXCLUDED_TOKENS (with reason)."
    )
