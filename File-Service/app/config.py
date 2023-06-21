from pydantic import BaseSettings


class Settings(BaseSettings):
    MINIO_ENDPOINT: str = "file-service-minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "test"

    POSTGRES_URL: str = "postgresql://admin:admin123@0.0.0.0:5432/file_service"

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"
    self_exchange: str = "file_exchange"
    response_exchange: str = "response_exchange"

    grobid_host: str = "grobid"
    grobid_port: int = 8070


class ServiceEndpoints(BaseSettings):
    embed_embedding: str = "http://api-gateway-api:8000/embedding/embed"
    rerank_embedding: str = "http://api-gateway-api:8000/embedding/rerank"

    process_fulltext_grobid: str = "http://file-service-grobid:8070/api/processFulltextDocument"


settings = Settings()
service_endpoints = ServiceEndpoints()
