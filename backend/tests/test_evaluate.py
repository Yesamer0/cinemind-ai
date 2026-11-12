from math import log2

import pytest

from backend.evaluate import ndcg_at_k, precision_at_k, recall_at_k, reciprocal_rank_at_k


def test_precision_counts_unique_hits_in_first_k():
    assert precision_at_k(["A", "A", "B", "C"], {"A", "C"}, 3) == pytest.approx(1 / 3)


def test_precision_penalizes_unfilled_ranks():
    assert precision_at_k(["A"], {"A"}, 5) == pytest.approx(0.2)


def test_precision_rejects_nonpositive_k():
    with pytest.raises(ValueError, match="positive"):
        precision_at_k([], set(), 0)


def test_recall_counts_unique_relevant_items():
    assert recall_at_k(["A", "A", "B", "C"], {"A", "C"}, 3) == 0.5


def test_ndcg_discounts_late_hits_and_ignores_duplicates():
    expected = (1 / log2(3)) / (1 + 1 / log2(3))
    assert ndcg_at_k(["X", "A", "A"], {"A", "B"}, 3) == pytest.approx(expected)


def test_reciprocal_rank_uses_first_hit_within_cutoff():
    ranked = ["X", "A", "B"]
    assert reciprocal_rank_at_k(ranked, {"A", "B"}, 3) == 0.5
    assert reciprocal_rank_at_k(ranked, {"A", "B"}, 1) == 0.0


def test_rank_metrics_return_zero_without_relevant_items():
    assert recall_at_k(["A"], set(), 3) == 0.0
    assert ndcg_at_k(["A"], set(), 3) == 0.0
    assert reciprocal_rank_at_k(["A"], set(), 3) == 0.0
