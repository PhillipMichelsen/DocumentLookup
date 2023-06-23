from typing import List

from sentence_transformers import SentenceTransformer

from app.config import settings

embedding_model = SentenceTransformer(settings.embedding_model_sentences, cache_folder=settings.cache_folder)


def generate_embedding(sentences: List[str]) -> List[List[float]]:
    """Generate embedding for a list of sentences

    :param sentences: Sentences to generate embedding for
    :return: List of embeddings
    """
    embeddings = embedding_model.encode(sentences)
    return embeddings.tolist()
