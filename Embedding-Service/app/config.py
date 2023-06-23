import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Settings for the application"""
    embedding_model_sentences: str = "msmarco-MiniLM-L6-cos-v5"
    cross_embedding_model: str = "cross-encoder/ms-marco-TinyBERT-L-2-v2"

    cache_folder: str = os.path.join(BASE_DIR, 'sentence_models')

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    embedding_exchange: str = "embedding_exchange"
    response_exchange: str = "response_exchange"
    debug: bool = True


# Create instances
settings = Settings()
