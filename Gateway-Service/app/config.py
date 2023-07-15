from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    cors_allowed_origins: list[str] = ["*"]

    # --- Core service settings ---
    service_name: str = "gateway_service"

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"

    service_exchange: str = "gateway_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"
    task_orchestrator_request_routing_key: str = "task_request"


# Create instances
settings = Settings()
