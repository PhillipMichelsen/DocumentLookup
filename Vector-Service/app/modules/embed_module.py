from typing import List

from sentence_transformers import SentenceTransformer

from app.config import settings

embedding_model = SentenceTransformer(settings.embedding_model)


def generate_embeddings(sentences: List[str]) -> List[List[float]]:
    """Generate embedding for a list of sentences

    :param sentences: Sentences to generate embedding for
    :return: List of embeddings
    """

    embeddings = embedding_model.encode(sentences)
    return embeddings.tolist()
