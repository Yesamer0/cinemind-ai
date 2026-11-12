from math import log, log2

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

def test_bm25_weights_term_frequency_and_document_length():
    import numpy as np

    from backend.benchmark_rankers import bm25_term_scores

    scores = bm25_term_scores(np.array([1, 2, 1]), np.array([10, 10, 20]), 10, 6, 3)
    assert scores[0] == pytest.approx(log(2))
    assert scores[1] > scores[0] > scores[2]


def test_rrf_rewards_items_found_by_both_methods():
    from backend.benchmark_rankers import reciprocal_rank_fusion

    assert reciprocal_rank_fusion([3, 2], [1, 2]) == [2, 1, 3]


def test_hybrid_ablation_removes_only_rating_and_popularity():
    from backend.app.hybrid import add_hybrid_candidate

    movie = {
        "title": "Sample", "overview": "Overview", "genres": "[]",
        "vote_average": 8, "popularity": 50, "release_date": "2000-01-01", "poster_path": None,
    }
    full, ablated = {}, {}
    add_hybrid_candidate(full, movie, 1, 0.5, 0.2)
    add_hybrid_candidate(ablated, movie, 1, 0.5, 0.2, include_metadata=False)

    assert full[1]["hybrid_score"] == pytest.approx(0.47)
    assert ablated[1]["hybrid_score"] == pytest.approx(0.26)
    assert ablated[1] | {"hybrid_score": full[1]["hybrid_score"]} == full[1]
