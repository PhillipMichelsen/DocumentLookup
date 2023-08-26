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
    prefetch_count: int = 3

    # Exchanges
    service_exchange: str = "task_orchestrator_exchange"
    gateway_exchange: str = "gateway_exchange"
    task_routing_exchange: str = "task_routing_exchange"

    # Service Queue Names + Routing Keys
    job_request_queue: str = "job_request_queue"
    job_request_queue_routing_key: str = "job_request"

    minio_put_event_queue: str = "minio_put_event_queue"
    minio_put_event_queue_routing_key: str = "minio_put_event"

    task_response_queue: str = "task_response_queue"
    task_response_queue_routing_key: str = "task_response"

    task_route_response_queue: str = "task_route_response_queue"
    task_route_response_queue_routing_key: str = "task_route_response"

    task_clear_data_response_queue: str = "task_clear_data_response_queue"
    task_clear_data_response_queue_routing_key: str = "task_clear_data_response"

    add_tasks_to_job_queue: str = "add_tasks_to_job_queue"
    add_tasks_to_job_queue_routing_key: str = "add_tasks_to_job"

    # Non-Service Queue Names + Routing Keys
    route_request_queue: str = "route_request_queue"
    route_request_queue_routing_key: str = "route_request"

    clear_job_data_queue: str = "clear_job_data_queue"
    clear_job_data_queue_routing_key: str = "clear_job_data"

    job_response_queue: str = "job_response_queue"
    job_response_queue_routing_key: str = "job_response"


# Create instances
settings = Settings()
