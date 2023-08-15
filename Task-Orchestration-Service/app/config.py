from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "task_orchestrator_service"

    redis_host: str = "redis-service"
    redis_port: int = 6379

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    # Exchanges
    service_exchange: str = "task_orchestrator_exchange"
    gateway_exchange: str = "gateway_exchange"
    task_routing_exchange: str = "task_routing_exchange"

    # Service Queue Names + Routing Keys
    job_request_queue: str = "job_request_queue"
    job_request_queue_routing_key: str = "job_request"

    minio_message_queue: str = "minio_message_queue"
    minio_message_queue_routing_key: str = "minio_message"

    task_response_queue: str = "task_response_queue"
    task_response_queue_routing_key: str = "task_response"

    task_route_response_queue: str = "task_route_response_queue"
    task_route_response_queue_routing_key: str = "task_route_response"

    # Non-Service Queue Names + Routing Keys
    route_request_queue: str = "route_request_queue"
    route_request_queue_routing_key: str = "route_request"

    job_response_queue: str = "job_response_queue"
    job_response_queue_routing_key: str = "job_response"

    # --- YAML Files ---
    task_file: str = "app/tasks.yaml"
    job_file: str = "app/jobs.yaml"
    exchanges_file: str = "app/exchanges.yaml"


# Create instances
settings = Settings()
