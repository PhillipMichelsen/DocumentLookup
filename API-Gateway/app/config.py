from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    cors_allowed_origins: list[str] = ["*"]

    # --- Core service settings ---
    service_name: str = "gateway_service"
    exchanges_file: str = "app/exchanges.yaml"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "gateway_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"

    task_orchestrator_job_request_queue: str = "job_request_queue"
    task_orchestrator_job_request_routing_key: str = "job_request"


# Create instances
settings = Settings()
