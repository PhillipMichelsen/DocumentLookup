from typing import List, Tuple

from sentence_transformers import CrossEncoder

from app.config import settings

cross_embedding_model = CrossEncoder(settings.cross_embedding_model)


def rerank(query: str, sentences: List[str]) -> Tuple[List[str], List[float]]:
    scores = generate_cross_encoding(query, sentences)

    sorted_pairs = sorted(zip(sentences, scores), key=lambda pair: pair[1], reverse=True)
    sentences_ranked, scores_ranked = zip(*sorted_pairs)

    return list(sentences_ranked), list(scores_ranked)


def generate_cross_encoding(query: str, sentences: List[str]) -> List[float]:
    query_sentence_pairs = [[query, sentence] for sentence in sentences]

    return cross_embedding_model.predict(query_sentence_pairs)
