from app.config import settings
from typing import List
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(settings.embedding_model_sentences, cache_folder=settings.cache_folder)


def generate_embedding(sentences: List[str]):
    embeddings = embedding_model.encode(sentences)
    return embeddings.tolist()
