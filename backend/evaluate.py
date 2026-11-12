import argparse
import json
from collections import defaultdict
from math import log2
from pathlib import Path
from statistics import mean


LABELS_PATH = Path(__file__).resolve().parents[1] / "dataset" / "eval" / "queries.json"
CANDIDATES_PER_METHOD = 20


def _hits_at_k(ranked, relevant, k):
    if k < 1:
        raise ValueError("k must be positive")
    seen = set()
    for rank, item in enumerate(ranked[:k], start=1):
        if item in relevant and item not in seen:
            seen.add(item)
            yield rank


def precision_at_k(ranked, relevant, k):
    return sum(1 for _ in _hits_at_k(ranked, relevant, k)) / k


def recall_at_k(ranked, relevant, k):
    hits = sum(1 for _ in _hits_at_k(ranked, relevant, k))
    return hits / len(relevant) if relevant else 0.0


def ndcg_at_k(ranked, relevant, k):
    dcg = sum(1 / log2(rank + 1) for rank in _hits_at_k(ranked, relevant, k))
    ideal_dcg = sum(1 / log2(rank + 1) for rank in range(1, min(k, len(relevant)) + 1))
    return dcg / ideal_dcg if ideal_dcg else 0.0


def reciprocal_rank_at_k(ranked, relevant, k):
    rank = next(_hits_at_k(ranked, relevant, k), None)
    return 1 / rank if rank is not None else 0.0


def query_rankings(query, catalog, limit):
    from backend.app.content_based import keyword_scores
    from backend.app.hybrid import add_hybrid_candidate
    from backend.app.semantic_search import encode_query, load_semantic_index

    tfidf = keyword_scores(query)
    embeddings, index = load_semantic_index()
    embedding = encode_query(query)
    size = min(len(catalog), max(limit, CANDIDATES_PER_METHOD))
    tfidf_ids = tfidf.argsort()[::-1][:size].tolist()
    _, neighbors = index.search(embedding, size)
    semantic_ids = neighbors[0].tolist()

    candidates = dict.fromkeys(
        tfidf_ids[:CANDIDATES_PER_METHOD] + semantic_ids[:CANDIDATES_PER_METHOD]
    )
    hybrid = {}
    for row in candidates:
        add_hybrid_candidate(hybrid, catalog.iloc[row], row, tfidf[row], embeddings[row] @ embedding[0])
    hybrid_ids = sorted(hybrid, key=lambda row: hybrid[row]["hybrid_score"], reverse=True)
    return {"TF-IDF": tfidf_ids, "Semantic": semantic_ids, "Query hybrid": hybrid_ids}


def seed_rankings(seed_rows, limit):
    from sklearn.metrics.pairwise import cosine_similarity

    from backend.app.content_based import create_tfidf_matrix
    from backend.app.hybrid import rank_recommendations
    from backend.app.semantic_search import faiss_similar_movies

    seed = seed_rows[0]
    excluded = set(seed_rows)
    _, matrix, _ = create_tfidf_matrix()
    scores = cosine_similarity(matrix[seed], matrix).ravel()
    candidates = scores.argsort()[::-1][:limit + len(excluded)]
    tfidf_ids = [int(row) for row in candidates if row not in excluded][:limit]

    neighbors = faiss_similar_movies(seed, top_n=limit + len(excluded))
    semantic_ids = [movie["id"] for movie in neighbors if movie["id"] not in excluded][:limit]

    recommendations = rank_recommendations([seed], excluded, limit=limit)
    return {
        "TF-IDF": tfidf_ids,
        "Semantic": semantic_ids,
        "Personalized hybrid": [movie["id"] for movie in recommendations],
    }


def load_benchmark(catalog):
    import pandas as pd

    items = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    raw_ids = pd.to_numeric(catalog["id"], errors="coerce")
    catalog_ids = [int(value) if pd.notna(value) else None for value in raw_ids]
    rows_by_id = defaultdict(list)
    for row, movie_id in enumerate(catalog_ids):
        rows_by_id[movie_id].append(row)

    for item in items:
        for label in item["relevant"]:
            rows = rows_by_id[label["tmdb_id"]]
            if not any(catalog.iloc[row]["title"] == label["title"] for row in rows):
                raise ValueError(f"Label missing from catalog: {label}")
    return items, catalog_ids, rows_by_id


def inspect_ranking(rankings, catalog, catalog_ids, labels, cutoff):
    for name, rows in rankings.items():
        print(f"{name} top {cutoff}:")
        for rank, row in enumerate(rows[:cutoff], start=1):
            print(f"  {rank}. {catalog.iloc[row]['title']} (TMDB {catalog_ids[row]})")
        for label in labels:
            rank = next(
                (position for position, row in enumerate(rows, start=1)
                 if catalog_ids[row] == label["tmdb_id"]),
                None,
            )
            print(f"  Labeled: {label['title']} — rank {rank if rank else 'outside candidates'}")


def main():
    parser = argparse.ArgumentParser(description="Compare keyword, semantic, and hybrid movie ranking")
    parser.add_argument("--k", type=int, default=5, help="Precision cutoff")
    parser.add_argument("--rank-k", type=int, default=10, help="Recall, NDCG, and MRR cutoff")
    parser.add_argument("--inspect", action="append", default=[], help="Also show ranks for an exact benchmark query")
    args = parser.parse_args()
    if min(args.k, args.rank_k) < 1:
        parser.error("cutoffs must be positive")

    from backend.app.data_loader import load_catalog

    catalog = load_catalog()
    items, catalog_ids, rows_by_id = load_benchmark(catalog)
    items_by_query = {item["query"]: item for item in items}
    if any(query not in items_by_query for query in args.inspect):
        parser.error("--inspect requires an exact query from the benchmark")

    limit = max(args.k, args.rank_k)
    query_scores = defaultdict(list)
    seed_scores = defaultdict(list)

    def record(scores, rankings, relevant):
        for name, rows in rankings.items():
            ranked = [catalog_ids[row] for row in rows]
            scores[name].append((
                precision_at_k(ranked, relevant, args.k),
                recall_at_k(ranked, relevant, args.rank_k),
                ndcg_at_k(ranked, relevant, args.rank_k),
                reciprocal_rank_at_k(ranked, relevant, args.rank_k),
            ))

    for item in items:
        seed, *held_out = [label["tmdb_id"] for label in item["relevant"]]
        record(query_scores, query_rankings(item["query"], catalog, limit), {seed, *held_out})
        record(seed_scores, seed_rankings(rows_by_id[seed], limit), set(held_out))

    for title, scores in (("Text queries", query_scores), ("Movie seeds", seed_scores)):
        print(f"\n{title}: macro averages over {len(items)} cases")
        print(f"{'Method':22}  P@{args.k}    R@{args.rank_k}  NDCG@{args.rank_k}   MRR@{args.rank_k}")
        for name, values in scores.items():
            print(f"{name:22}  " + "  ".join(f"{mean(column):.3f}" for column in zip(*values)))

    for query in args.inspect:
        print(f"\nInspecting: {query}")
        rankings = query_rankings(query, catalog, len(catalog))
        inspect_ranking(rankings, catalog, catalog_ids, items_by_query[query]["relevant"], args.k)


if __name__ == "__main__":
    main()
