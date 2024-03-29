from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "vector_service"
    weaviate_host: str = "weaviate-service"
    weaviate_port: str = "8080"

    embedding_model: str = "embedding_models/multi-qa-mpnet-base-dot-v1"
    cross_encoding_model: str = "embedding_models/ms-marco-MiniLM-L-12-v2"
    # embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    # cross_encoding_model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"
    prefetch_count: int = 3

    # Exchanges
    service_exchange: str = "vector_exchange"
    task_routing_exchange: str = "task_routing_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"

    # Service Queue Names + Routing Keys
    embed_text_queue: str = "embed_text_queue"
    embed_text_queue_routing_key: str = "embed_text"

    embed_store_text_queue: str = "embed_store_text_queue"
    embed_store_text_queue_routing_key: str = "embed_store_text"

    rerank_text_queue: str = "rerank_text_queue"
    rerank_text_queue_routing_key: str = "rerank_text"

    retrieve_closest_entries_queue: str = "retrieve_closest_entries_queue"
    retrieve_closest_entries_queue_routing_key: str = "retrieve_closest_entries"

    store_embedding_queue: str = "store_embedding_queue"
    store_embedding_queue_routing_key: str = "store_embedding"

    route_request_queue: str = "route_request_queue"
    route_request_queue_routing_key: str = "route_request"

    clear_job_data_queue: str = "clear_job_data_queue"
    clear_job_data_queue_routing_key: str = "clear_job_data"

    # Non-Service Queue Names + Routing Keys
    task_orchestrator_task_response_routing_key: str = "task_response"
    task_orchestrator_task_route_response_routing_key: str = "task_route_response"

    task_orchestrator_job_request_queue: str = "job_request_queue"
    task_orchestrator_job_request_routing_key: str = "job_request"


# Create instances
settings = Settings()
