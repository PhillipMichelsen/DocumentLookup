from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application"""

    cors_allowed_origins: list[str] = ["*"]

    # Core service settings
    service_type: str = "gateway"
    service_name: str = "api_gateway"

    # Redis settings
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"


# Create instances
settings = Settings()
