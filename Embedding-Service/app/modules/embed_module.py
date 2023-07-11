import os.path
import logging
from typing import List

from sentence_transformers import SentenceTransformer

from app.config import settings

embedding_model = SentenceTransformer(os.path.join(settings.embedding_models_folder, settings.embedding_model))
logging.info("[*] Embedding model loaded!")


def generate_embedding(sentences: List[str]) -> List[List[float]]:
    """Generate embedding for a list of sentences

    :param sentences: Sentences to generate embedding for
    :return: List of embeddings
    """
    embeddings = embedding_model.encode(sentences)
    return embeddings.tolist()
