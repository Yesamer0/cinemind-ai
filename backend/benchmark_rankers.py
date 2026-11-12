from collections import defaultdict
from functools import lru_cache

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from backend.app.content_based import clean_text, create_tfidf_matrix


BM25_K1 = 1.2
BM25_B = 0.75
RRF_K = 60


def bm25_term_scores(term_counts, doc_lengths, avg_length, doc_count, doc_frequency):
    idf = np.log1p((doc_count - doc_frequency + 0.5) / (doc_frequency + 0.5))
    length_norm = BM25_K1 * (1 - BM25_B + BM25_B * doc_lengths / avg_length)
    return idf * term_counts * (BM25_K1 + 1) / (term_counts + length_norm)


@lru_cache(maxsize=1)
def _bm25_index():
    tfidf, _, movies = create_tfidf_matrix()
    counter = CountVectorizer(vocabulary=tfidf.vocabulary_)
    counts = counter.transform(movies["clean_overview"]).tocsc()
    lengths = np.asarray(counts.sum(axis=1)).ravel()
    return counts, lengths, float(lengths.mean()), counter.build_analyzer(), tfidf.vocabulary_


def bm25_ranking(query, limit):
    counts, lengths, avg_length, analyze, vocabulary = _bm25_index()
    scores = np.zeros(counts.shape[0])
    for token in sorted(set(analyze(clean_text(query))) & vocabulary.keys()):
        term = vocabulary[token]
        start, end = counts.indptr[term:term + 2]
        rows = counts.indices[start:end]
        scores[rows] += bm25_term_scores(
            counts.data[start:end], lengths[rows], avg_length, len(scores), len(rows)
        )
    ranked = np.argsort(-scores, kind="stable")
    return [int(row) for row in ranked[:limit] if scores[row] > 0]


def reciprocal_rank_fusion(*rankings):
    scores = defaultdict(float)
    for ranked in rankings:
        for rank, item in enumerate(ranked, start=1):
            scores[item] += 1 / (RRF_K + rank)
    return sorted(scores, key=lambda item: (-scores[item], item))
