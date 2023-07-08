from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for the application

    Attributes:
        cors_allowed_origins (list[str]): List of allowed origins for CORS
        rabbitmq_host (str): RabbitMQ host
        rabbitmq_username (str): RabbitMQ username
        rabbitmq_password (str): RabbitMQ password
    """
    cors_allowed_origins: list[str] = ["*"]

    # Core service settings
    service_type: str = "gateway"
    service_name: str = "api_gateway"

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"


# Create instances
settings = Settings()
