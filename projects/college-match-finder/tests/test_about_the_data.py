"""
tests/test_about_the_data.py — Phase 6D regression guards.

Three invariants tested:
  1. render_about_the_data() produces markdown containing all 12 expected sources.
  2. OLDEST_DATE and NEWEST_DATE constants are defined and non-empty.
  3. The old School Finder-only expander prose is no longer present in app.py
     (prevents duplication regression if the old content is ever accidentally restored).
"""

from pathlib import Path
from unittest.mock import patch

from page_modules.about_the_data import render_about_the_data, OLDEST_DATE, NEWEST_DATE

# One unique substring per source that must appear in the rendered markdown.
# These are the rendered string values (after Python escape evaluation),
# so O\*NET sources use the backslash-asterisk form that Streamlit receives.
_EXPECTED_SOURCE_SUBSTRINGS = [
    "College Scorecard — Institution-Level Data",
    "College Scorecard — Field of Study Data",
    "NCES CIP–SOC Crosswalk",           # en-dash as in the source
    "Major Descriptions",
    "Major Outcomes",
    "BLS Occupational Employment and Wage Statistics",
    "BLS Employment Projections",
    "BLS NAICS-by-SOC Industry Distribution",
    "BLS OEWS State-Level",
    "O\\*NET Work Context",                  # rendered string contains literal backslash
    "O\\*NET RIASEC Interest Profiles",
    "NY Fed Labor Market Outcomes",
]


def _collect_markdown() -> str:
    """Run render_about_the_data() with st mocked; return all markdown args joined."""
    with patch("page_modules.about_the_data.st") as mock_st:
        render_about_the_data()
    return "\n".join(
        str(c.args[0]) for c in mock_st.markdown.call_args_list if c.args
    )


def test_render_contains_all_12_sources():
    """All 12 data sources must appear in the About the Data expander."""
    combined = _collect_markdown()
    missing = [s for s in _EXPECTED_SOURCE_SUBSTRINGS if s not in combined]
    assert not missing, f"Sources missing from About the Data: {missing}"


def test_source_count_exactly_12():
    """Regression guard: total documented source count must stay at 12."""
    combined = _collect_markdown()
    found = sum(1 for s in _EXPECTED_SOURCE_SUBSTRINGS if s in combined)
    assert found == 12, f"Expected 12 sources documented, found {found}"


def test_freshness_date_constants_defined_and_non_empty():
    """OLDEST_DATE and NEWEST_DATE must be non-empty strings."""
    assert isinstance(OLDEST_DATE, str) and OLDEST_DATE.strip(), \
        "OLDEST_DATE must be a non-empty string"
    assert isinstance(NEWEST_DATE, str) and NEWEST_DATE.strip(), \
        "NEWEST_DATE must be a non-empty string"


def test_old_expander_not_present_in_app_py():
    """The old School Finder-only expander prose must not survive in app.py.

    Regression guard: if someone accidentally restores the old verbose block,
    this test fails before the duplication reaches production.
    """
    app_path = Path(__file__).parent.parent / "app.py"
    text = app_path.read_text(encoding="utf-8")
    assert "BLS occupational data (Major Explorer tab)" not in text, \
        "Old expander heading found in app.py — old content was not fully replaced"
    assert "Equal-weighted aggregation was rejected" not in text, \
        "Old methodology prose found in app.py — old content was not fully replaced"
