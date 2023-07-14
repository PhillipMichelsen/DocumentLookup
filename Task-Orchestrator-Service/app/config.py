import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    # Core service settings
    service_name: str = "task_orchestrator_service"

    service_exchange: str = "task_orchestrator_exchange"
    gateway_exchange: str = "gateway_exchange"

    # Redis settings
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"


# Create instances
settings = Settings()
