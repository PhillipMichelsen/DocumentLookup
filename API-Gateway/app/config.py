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

    job_response_queue: str = "job_response_queue"
    job_response_queue_routing_key: str = "job_response"

    update_result_queue: str = "update_result_queue"
    update_result_queue_routing_key: str = "update_result"

    task_orchestrator_job_request_queue: str = "job_request_queue"
    task_orchestrator_job_request_routing_key: str = "job_request"

    task_orchestrator_task_response_routing_key: str = "task_response"
    task_orchestrator_task_route_response_routing_key: str = "task_route_response"

# Create instances
settings = Settings()
