from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "vector_service"

    embedding_model: str = "embedding_models/all-MiniLM-L6-v2"
    cross_encoding_model: str = "embedding_models/ms-marco-MiniLM-L-12-v2"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "vector_exchange"

    task_orchestrator_exchange: str = "task_orchestrator_exchange"
    task_orchestrator_task_response_routing_key: str = "task_response"
    task_orchestrator_task_route_response_routing_key: str = "task_route_response"

    # Queue Names + Routing Keys
    vector_exchange_embed_queue: str = "vector_queue_embed"
    vector_exchange_embed_routing_key: str = "vector_embed"

    vector_exchange_rerank_queue: str = "vector_queue_rerank"
    vector_exchange_rerank_routing_key: str = "vector_rerank"

    # --- Redis settings ---
    redis_host: str = "redis-service"
    redis_port: int = 6379


# Create instances
settings = Settings()
