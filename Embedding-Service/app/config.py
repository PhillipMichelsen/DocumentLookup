from pydantic import BaseSettings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    embedding_model_sentences: str = "msmarco-MiniLM-L6-cos-v5"
    cross_embedding_model: str = "cross-encoder/ms-marco-TinyBERT-L-2-v2"

    cache_folder: str = os.path.join(BASE_DIR, 'sentence_models')

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"


settings = Settings()
