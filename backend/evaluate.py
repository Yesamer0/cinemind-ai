import argparse
from statistics import mean


# Small, manually labeled retrieval benchmark.
QUERIES = {
    "toys that come to life when humans leave": {
        "Toy Story", "Toy Story 2", "Toy Story 3", "Small Soldiers",
    },
    "shark attacks in a seaside town": {"Jaws", "Jaws 2", "Jaws: The Revenge"},
    "wizard school and magic lessons": {
        "Harry Potter and the Philosopher's Stone",
        "Harry Potter and the Chamber of Secrets",
        "Harry Potter and the Prisoner of Azkaban",
        "Harry Potter and the Goblet of Fire",
    },
    "dinosaur theme park where the animals escape": {
        "Jurassic Park", "The Lost World: Jurassic Park", "Jurassic Park III", "Jurassic World",
    },
    "a boxing underdog trains for a title fight": {
        "Rocky", "Rocky II", "Rocky III", "Rocky IV", "Rocky Balboa", "Creed",
    },
}


def precision_at_k(ranked, relevant, k):
    if k < 1:
        raise ValueError("k must be positive")
    return len(set(ranked[:k]) & relevant) / k


def main():
    parser = argparse.ArgumentParser(description="Compare TF-IDF and semantic movie search")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    if args.k < 1:
        parser.error("--k must be positive")

    from backend.app.content_based import recommend_by_keyword
    from backend.app.semantic_search import semantic_search

    tfidf_scores = []
    semantic_scores = []
    print(f"Precision@{args.k}")
    print(f"{'TF-IDF':>8} {'Semantic':>8}  Query")
    for query, relevant in QUERIES.items():
        tfidf_titles = recommend_by_keyword(query, top_n=args.k)["title"].tolist()
        semantic_titles = [movie["title"] for movie in semantic_search(query, top_n=args.k)]
        tfidf_score = precision_at_k(tfidf_titles, relevant, args.k)
        semantic_score = precision_at_k(semantic_titles, relevant, args.k)
        tfidf_scores.append(tfidf_score)
        semantic_scores.append(semantic_score)
        print(f"{tfidf_score:8.3f} {semantic_score:8.3f}  {query}")
    print(f"{mean(tfidf_scores):8.3f} {mean(semantic_scores):8.3f}  Mean ({len(QUERIES)} queries)")


if __name__ == "__main__":
    main()
