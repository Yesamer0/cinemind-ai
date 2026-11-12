import argparse
from statistics import mean


# Small, manually labeled semantic retrieval benchmark.
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
    parser = argparse.ArgumentParser(description="Evaluate semantic movie search")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    if args.k < 1:
        parser.error("--k must be positive")

    from backend.app.semantic_search import semantic_search

    scores = []
    for query, relevant in QUERIES.items():
        ranked = [movie["title"] for movie in semantic_search(query, top_n=args.k)]
        score = precision_at_k(ranked, relevant, args.k)
        scores.append(score)
        print(f"{score:.3f}  {query}")
    print(f"Mean Precision@{args.k}: {mean(scores):.3f} ({len(scores)} queries)")


if __name__ == "__main__":
    main()
