"""Tests for Phase 12.3 RIASEC-to-CIP4 alignment helper.

Covers _get_aligned_cip4_set() in page_modules/major_explorer.py:
session-state gating, return shape, cache behaviour, cache invalidation,
and CIP4 dot-format contract.
"""
import pytest
import streamlit as st

from page_modules.major_explorer import _get_aligned_cip4_set
from riasec_distribution import get_riasec_for_cip4


@pytest.fixture(autouse=True)
def clear_session_state():
    """Reset session_state before every test."""
    st.session_state.clear()
    yield
    st.session_state.clear()


def _social_work_vector() -> dict:
    """Return the RIASEC scores for Social Work (44.07) as a user vector."""
    data = get_riasec_for_cip4("44.07")
    assert data is not None, "44.07 must be present in the RIASEC data"
    return data["scores"]


def test_aligned_helper_returns_none_when_no_quiz_taken():
    """No riasec_user_vector in session → helper returns None."""
    assert "riasec_user_vector" not in st.session_state
    result = _get_aligned_cip4_set()
    assert result is None


def test_aligned_helper_returns_set_when_quiz_taken():
    """Known user vector → helper returns a set of exactly 40 CIP4 strings."""
    st.session_state["riasec_user_vector"] = _social_work_vector()
    result = _get_aligned_cip4_set()
    assert isinstance(result, set)
    assert len(result) == 40


def test_aligned_helper_returns_empty_set_for_zero_variance():
    """All-equal user vector → zero Pearson variance → empty set, not None."""
    st.session_state["riasec_user_vector"] = {
        "R": 4.0, "I": 4.0, "A": 4.0, "S": 4.0, "E": 4.0, "C": 4.0
    }
    result = _get_aligned_cip4_set()
    assert result == set(), f"Expected empty set, got {result!r}"


def test_aligned_helper_caches():
    """Cache key is written to session_state after first call."""
    st.session_state["riasec_user_vector"] = _social_work_vector()

    assert "_aligned_cip4_set_cache" not in st.session_state

    _get_aligned_cip4_set()

    assert "_aligned_cip4_set_cache" in st.session_state
    assert "_aligned_cip4_set_cache_vector" in st.session_state

    # Second call should return the same object from cache (no recomputation)
    first = st.session_state["_aligned_cip4_set_cache"]
    _get_aligned_cip4_set()
    second = st.session_state["_aligned_cip4_set_cache"]
    assert first is second


def test_aligned_helper_invalidates_on_vector_change():
    """Changing the user vector causes the cache to be recomputed."""
    st.session_state["riasec_user_vector"] = _social_work_vector()
    first_result = _get_aligned_cip4_set()
    first_fp = st.session_state["_aligned_cip4_set_cache_vector"]

    # Swap to a very different vector (heavily Realistic)
    st.session_state["riasec_user_vector"] = {
        "R": 7.0, "I": 1.0, "A": 1.0, "S": 1.0, "E": 1.0, "C": 1.0
    }
    second_result = _get_aligned_cip4_set()
    second_fp = st.session_state["_aligned_cip4_set_cache_vector"]

    assert first_fp != second_fp, "Cache fingerprint should update on vector change"
    # The two sets will typically differ; at minimum verify they were recomputed
    assert first_result is not second_result


def test_aligned_set_contains_dot_format_cip4s():
    """All returned CIP4 strings use dot format (e.g. '44.07', not '4407')."""
    st.session_state["riasec_user_vector"] = _social_work_vector()
    result = _get_aligned_cip4_set()
    assert result is not None and len(result) > 0
    for cip4 in result:
        assert "." in cip4, (
            f"CIP4 '{cip4}' missing dot separator — expected format like '44.07'"
        )
