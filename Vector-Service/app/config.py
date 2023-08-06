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
    task_routing_exchange: str = "task_routing_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"

    # Non-Service Queue Names + Routing Keys
    task_orchestrator_task_response_routing_key: str = "task_response"
    task_orchestrator_task_route_response_routing_key: str = "task_route_response"

    # Service Queue Names + Routing Keys
    embed_text_queue: str = "embed_text_queue"
    embed_text_queue_routing_key: str = "embed_text"

    rerank_text_queue: str = "rerank_text_queue"
    rerank_text_queue_routing_key: str = "rerank_text"

    route_request_queue: str = "route_request_queue"
    route_request_queue_routing_key: str = "route_request"

    # --- Redis settings ---
    redis_host: str = "redis-service"
    redis_port: int = 6379

    # --- YAML Files ---
    exchanges_file: str = "app/exchanges.yaml"


# Create instances
settings = Settings()
