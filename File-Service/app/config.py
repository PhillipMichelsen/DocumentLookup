from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "file-service"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "file_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"
    task_orchestrator_response_routing_key: str = "job_response"

    # Queue Names + Routing Keys\
    #vector_queue_embed: str = "vector_queue_embed"
    #vector_queue_embed_routing_key: str = "embed_text"

    # --- Redis settings ---
    redis_host: str = "redis-service"
    redis_port: int = 6379

    # --- Minio settings ---
    minio_host: str = "minio-service"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"

    # --- Weaviate settings ---
    weaviate_host: str = "weaviate-service"


# Create instances
settings = Settings()
