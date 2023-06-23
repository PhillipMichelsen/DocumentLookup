from typing import List, Tuple

from sentence_transformers import CrossEncoder

from app.config import settings

cross_embedding_model = CrossEncoder(settings.cross_embedding_model)


def generate_cross_encoding(query: str, sentences: List[str]) -> List[Tuple[str, float]]:
    """Generate cross-encoding for a query and a list of sentences.

    Uses the cross-encoder model as defined by `settings.cross_embedding_model`.
    :param query: The query sentence.
    :param sentences: The list of sentences to be cross-encoded.
    :return: A list of tuples (sentence, score) where score is the cross-encoding score of the sentence.
    """
    query_sentence_pairs = [[query, sentence] for sentence in sentences]

    scores = cross_embedding_model.predict(query_sentence_pairs)

    return list(zip(sentences, scores))


def rerank(pairs: List[Tuple[str, float]]) -> Tuple[List[str], List[float]]:
    """Rerank a list of sentence-score pairs by score, descending order.

    :param pairs: A list of tuples (sentence, score) where score is the cross-encoding score of the sentence.
    :return: A tuple of two lists: (sentences, scores) where scores are in descending order.
    """
    sorted_pairs = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    sentences_ranked, scores_ranked = zip(*sorted_pairs)

    return list(sentences_ranked), list(scores_ranked)



