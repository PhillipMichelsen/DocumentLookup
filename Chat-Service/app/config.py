from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application"""

    # --- Core service settings ---
    service_name: str = "chat_service"
    openai_api_key: str

    # --- RabbitMQ settings ---
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_username: str = "admin"
    rabbitmq_password: str = "admin123"
    prefetch_count: int = 1

    # Exchanges
    service_exchange: str = "chat_exchange"
    task_orchestrator_exchange: str = "task_orchestrator_exchange"

    # Service Queue Names + Routing Keys

    route_request_queue: str = "route_request_queue"
    route_request_queue_routing_key: str = "route_request"

    clear_job_data_queue: str = "clear_job_data_queue"
    clear_job_data_queue_routing_key: str = "clear_job_data"

    chat_completion_queue: str = "chat_completion_queue"
    chat_completion_queue_routing_key: str = "chat_completion"

    retrieve_context_queue: str = "retrieve_context_queue"
    retrieve_context_queue_routing_key: str = "retrieve_context"

    # Non-Service Queue Names + Routing Keys
    task_orchestrator_task_response_routing_key: str = "task_response"
    task_orchestrator_task_route_response_routing_key: str = "task_route_response"
    task_orchestrator_job_request_queue_routing_key: str = "job_request"
    task_orchestrator_add_tasks_to_job_routing_key: str = "add_tasks_to_job"

    # .env file config
    model_config = SettingsConfigDict(env_file='app/.env', env_file_encoding='utf-8')


# Create instances
settings = Settings()
