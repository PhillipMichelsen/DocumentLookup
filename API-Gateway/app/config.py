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

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"


class RabbitMQExchanges(BaseSettings):
    gateway_exchange: dict = {
        "type": "topic",
        "durable": False,
        "auto_delete": True
    }

    embedding_exchange: dict = {
        "type": "topic",
        "durable": False,
        "auto_delete": True
    }

    file_exchange: dict = {
        "type": "topic",
        "durable": False,
        "auto_delete": True
    }


class RabbitMQQueues(BaseSettings):
    job_queue: dict = {
        "durable": False,
        "auto_delete": True
    }

    response_queue: dict = {
        "durable": False,
        "auto_delete": True
    }


# Create instances
settings = Settings()
exchanges = RabbitMQExchanges()
queues = RabbitMQQueues()

