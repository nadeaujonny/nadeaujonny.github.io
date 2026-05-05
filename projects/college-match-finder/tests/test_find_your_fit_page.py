"""Tests for page_modules/find_your_fit.py — import integrity and constant correctness.

UI behavior (widget rendering, session state transitions, form submission) is
outside the scope of unit tests in this project and is verified manually.
"""

import page_modules.find_your_fit as fyf_module


def test_page_module_imports():
    """page_modules.find_your_fit imports without error."""
    assert fyf_module is not None


def test_dimension_names_complete():
    """DIMENSION_NAMES has exactly the 6 RIASEC keys, all non-empty strings."""
    names = fyf_module.DIMENSION_NAMES
    assert set(names.keys()) == {'R', 'I', 'A', 'S', 'E', 'C'}
    for key, value in names.items():
        assert isinstance(value, str) and len(value) > 0, (
            f"DIMENSION_NAMES['{key}'] must be a non-empty string, got {value!r}"
        )


def test_dimension_descriptions_complete():
    """DIMENSION_DESCRIPTIONS has exactly the 6 RIASEC keys, all non-empty strings."""
    descs = fyf_module.DIMENSION_DESCRIPTIONS
    assert set(descs.keys()) == {'R', 'I', 'A', 'S', 'E', 'C'}
    for key, value in descs.items():
        assert isinstance(value, str) and len(value) > 0, (
            f"DIMENSION_DESCRIPTIONS['{key}'] must be a non-empty string, got {value!r}"
        )


def test_session_keys_unique():
    """All four SESSION_KEYS values are unique strings."""
    values = list(fyf_module.SESSION_KEYS.values())
    assert len(values) == len(set(values)), (
        f"SESSION_KEYS values must be unique; found duplicates in {values}"
    )
    for v in values:
        assert isinstance(v, str) and len(v) > 0


def test_session_keys_includes_user_vector():
    """SESSION_KEYS['user_vector'] must equal 'riasec_user_vector' (load-bearing for Phase 12.3)."""
    assert fyf_module.SESSION_KEYS['user_vector'] == 'riasec_user_vector', (
        "Do not rename this key — Phase 12.3 reads st.session_state['riasec_user_vector'] "
        "to decide whether to show alignment badges in Major Explorer."
    )
