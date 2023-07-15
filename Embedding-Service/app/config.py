import os

from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "embedding_service"

    embedding_model: str = "multi-qa-mpnet-base-dot-v1"
    cross_encoding_model: str = "ms-marco-MiniLM-L-12-v2"

    embedding_models_folder: str = os.path.join(BASE_DIR, 'embedding_models')

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "embedding_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"
    task_orchestrator_response_routing_key: str = "job_response"

    # --- Redis settings ---
    redis_host: str = "redis-service"
    redis_port: int = 6379


# Create instances
settings = Settings()
