from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "vector_service"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    cross_encoding_model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "vector_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"
    task_orchestrator_response_routing_key: str = "job_response"

    # Queue Names + Routing Keys\
    vector_queue_embed: str = "vector_queue_embed"
    vector_queue_embed_routing_key: str = "embed_text"

    vector_queue_rerank: str = "vector_queue_rerank"
    vector_queue_rerank_routing_key: str = "rerank_text"

    # --- Redis settings ---
    redis_host: str = "redis-service"
    redis_port: int = 6379


# Create instances
settings = Settings()
