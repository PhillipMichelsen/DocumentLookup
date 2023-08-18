from app.config import settings
from app.listeners.clear_job_data_listener import on_message_clear_job_data
from app.listeners.route_request_listener import on_message_route_request
from app.listeners.chat_completion_listener import on_message_chat_completion
from app.listeners.retrieve_context_listener import on_message_retrieve_context
from app.utils.weaviate_utils import weaviate_utils
from app.utils.pika_utils import pika_utils

weaviate_utils.init_connection('weaviate-service', 8080)

# Prepare pika connection and declare exchanges
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_exchanges()

# Register consumer for chat completion request
pika_utils.register_consumer(
    queue_name=settings.chat_completion_queue,
    exchange=settings.service_exchange,
    routing_key=settings.chat_completion_queue_routing_key,
    on_message_callback=on_message_chat_completion,
    auto_delete=False
)

pika_utils.register_consumer(
    queue_name=settings.retrieve_context_queue,
    exchange=settings.service_exchange,
    routing_key=settings.retrieve_context_queue_routing_key,
    on_message_callback=on_message_retrieve_context,
    auto_delete=False
)


# Register consumer for route request
pika_utils.register_consumer(
    queue_name=f'{pika_utils.service_id}_{settings.route_request_queue}',
    exchange=settings.service_exchange,
    routing_key=f'{pika_utils.service_id}_{settings.route_request_queue_routing_key}',
    on_message_callback=on_message_route_request,
    auto_delete=True,
    priority=5
)

# Register consumer for clear job data request
pika_utils.register_consumer(
    queue_name=f'{pika_utils.service_id}_{settings.clear_job_data_queue}',
    exchange=settings.service_exchange,
    routing_key=f'{pika_utils.service_id}_{settings.clear_job_data_queue_routing_key}',
    on_message_callback=on_message_clear_job_data,
    auto_delete=True,
    priority=-1
)

pika_utils.start_consuming()