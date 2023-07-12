import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Settings for the application"""

    # Core service settings
    service_type: str = "service"
    service_name: str = "embedding_service"

    service_exchange: str = "embedding_exchange"
    gateway_exchange: str = "gateway_exchange"

    # Service Specific settings
    embedding_model: str = "multi-qa-mpnet-base-dot-v1"
    cross_encoding_model: str = "ms-marco-MiniLM-L-12-v2"

    embedding_models_folder: str = os.path.join(BASE_DIR, 'embedding_models')

    # Redis settings
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"


# Create instances
settings = Settings()
