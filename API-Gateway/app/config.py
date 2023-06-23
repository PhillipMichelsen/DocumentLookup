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


class ExchangesAndRouting(BaseSettings):
    """Exchanges and routing keys for the application

    Attributes:
        embedding_exchange (str): Embedding exchange name
        embedding_embed_routing_key (str): Embedding routing key
        embedding_rerank_routing_key (str): Rerank routing key
        file_exchange (str): File exchange name
        file_get_presigned_url_routing_key (str): Get presigned url routing key
        file_file_uploaded_routing_key (str): File uploaded routing key
        response_exchange (str): Response exchange name
    """
    embedding_exchange: str = "embedding_exchange"
    embedding_embed_routing_key: str = "embed"
    embedding_rerank_routing_key: str = "rerank"

    file_exchange: str = "file_exchange"
    file_get_presigned_url_routing_key: str = "get_presigned_url"
    file_file_uploaded_routing_key: str = "file_uploaded"

    response_exchange: str = "response_exchange"


# Create instances
settings = Settings()
exchanges_routing = ExchangesAndRouting()
