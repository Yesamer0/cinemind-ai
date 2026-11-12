import pytest

from backend.evaluate import precision_at_k


def test_precision_counts_unique_hits_in_first_k():
    assert precision_at_k(["A", "A", "B", "C"], {"A", "C"}, 3) == pytest.approx(1 / 3)


def test_precision_penalizes_unfilled_ranks():
    assert precision_at_k(["A"], {"A"}, 5) == pytest.approx(0.2)


def test_precision_rejects_nonpositive_k():
    with pytest.raises(ValueError, match="positive"):
        precision_at_k([], set(), 0)
