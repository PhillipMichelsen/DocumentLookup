from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "file-service"
    grobid_fulltext_endpoint: str = "http://grobid-service:8070/api/processFulltextDocument"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "file_exchange"
    task_routing_exchange: str = "task_routing_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"

    # Queue Names + Routing Keys\
    file_queue_presigned_url_upload: str = "file_queue_presigned_url_upload"
    file_queue_presigned_url_upload_routing_key: str = "presigned_url_upload"

    file_queue_process_file: str = "file_queue_process_file"
    file_queue_process_file_routing_key: str = "process_file"

    route_request_queue: str = "route_request_queue"
    route_request_queue_routing_key: str = "route_request"

    # Non-Service Queue Names + Routing Keys
    task_orchestrator_task_response_routing_key: str = "task_response"
    task_orchestrator_task_route_response_routing_key: str = "task_route_response"

    # --- Redis settings ---
    redis_host: str = "redis-service"
    redis_port: int = 6379

    # --- Minio settings ---
    minio_host: str = "minio-service:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"

    # --- Weaviate settings ---
    weaviate_host: str = "weaviate-service"

    # --- YAML Files ---
    exchanges_file: str = "app/exchanges.yaml"


# Create instances
settings = Settings()
