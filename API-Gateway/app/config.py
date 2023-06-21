from pydantic import BaseSettings


class Settings(BaseSettings):
    cors_allowed_origins: list[str] = ["*"]

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"


class ExchangesAndRouting(BaseSettings):
    embedding_exchange: str = "embedding_exchange"
    embedding_embed_routing_key: str = "embed"
    embedding_rerank_routing_key: str = "rerank"

    file_exchange: str = "file_exchange"
    file_get_presigned_url_routing_key: str = "get_presigned_url"
    file_file_uploaded_routing_key: str = "file_uploaded"

    response_exchange: str = "response_exchange"


settings = Settings()
exchanges_routing = ExchangesAndRouting()
