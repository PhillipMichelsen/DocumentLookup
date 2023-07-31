from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "task_orchestrator_service"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "task_orchestrator_exchange"
    gateway_exchange: str = "gateway_exchange"

    task_response_queue: str = "task_response_queue"
    task_request_queue_routing_key: str = "task_response"

    job_request_queue: str = "job_request_queue"
    job_response_queue_routing_key: str = "job_request"

    # --- Redis settings ---
    redis_host: str = "redis-service"
    redis_port: int = 6379

    # --- YAML Files ---
    task_file: str = "app/jobs.yaml"
    job_file: str = "app/tasks.yaml"
    exchanges_file: str = "app/exchanges.yaml"


# Create instances
settings = Settings()
