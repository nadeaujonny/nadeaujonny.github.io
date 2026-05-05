"""Tests for Phase 11.3.3 naics_distribution loader.

Validates get_naics_distribution() in naics_distribution.py: correct
return types, empty-state handling, input-format equivalence, and sort order.
"""
from naics_distribution import get_naics_distribution


def test_loader_returns_dataframe_for_known_cip4():
    """Computer Science (11.07) should return a non-empty DataFrame."""
    result = get_naics_distribution("11.07")
    assert result is not None
    assert len(result) > 0
    assert "naics3" in result.columns
    assert "share_in_naics3" in result.columns


def test_loader_returns_none_for_missing_cip4():
    """Military Technologies CIP4s have no NAICS distribution."""
    assert get_naics_distribution("28.05") is None
    assert get_naics_distribution("28.06") is None


def test_loader_int_format_equivalent_to_dotted():
    """Loader accepts both '11.07' and '1107' and returns identical results."""
    a = get_naics_distribution("11.07")
    b = get_naics_distribution("1107")
    assert a is not None and b is not None
    assert a.equals(b)


def test_loader_results_sorted_descending_by_share():
    """Top NAICS3 row has the highest share (sorted at parquet build time)."""
    cs = get_naics_distribution("11.07")
    assert cs is not None
    shares = cs["share_in_naics3"].tolist()
    assert shares == sorted(shares, reverse=True)
