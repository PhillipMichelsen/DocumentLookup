from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "file-service"
    grobid_fulltext_endpoint: str = "http://grobid-service:8070/api/processFulltextDocument"
    batch_size: int = 30

    minio_host: str = "minio-service:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"

    weaviate_host: str = "weaviate-service"
    weaviate_port: str = "8080"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"
    prefetch_count: int = 1

    # Exchanges
    service_exchange: str = "file_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"

    # Queue Names + Routing Keys
    file_queue_presigned_url_upload: str = "file_queue_presigned_url_upload"
    file_queue_presigned_url_upload_routing_key: str = "presigned_url_upload"

    file_queue_process_file: str = "file_queue_process_file"
    file_queue_process_file_routing_key: str = "process_file"

    route_request_queue: str = "route_request_queue"
    route_request_queue_routing_key: str = "route_request"

    clear_job_data_queue: str = "clear_job_data_queue"
    clear_job_data_queue_routing_key: str = "clear_job_data"

    get_files_queue: str = "get_files_queue"
    get_files_queue_routing_key: str = "get_files"

    add_entries_queue: str = "add_entries_queue"
    add_entries_queue_routing_key: str = "add_entries"

    # Non-Service Queue Names + Routing Keys
    task_orchestrator_task_response_routing_key: str = "task_response"
    task_orchestrator_task_route_response_routing_key: str = "task_route_response"

    task_orchestrator_job_request_queue: str = "job_request_queue"
    task_orchestrator_job_request_routing_key: str = "job_request"


# Create instances
settings = Settings()
