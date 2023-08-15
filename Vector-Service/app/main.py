from app.config import settings
from app.listeners.cross_encode_listener import on_message_rerank
from app.listeners.embed_listener import on_message_embed
from app.listeners.route_request_listener import on_message_route_request
from app.listeners.embed_store_listener import on_message_embed_store
from app.utils.pika_utils import pika_utils
from app.utils.weaviate_utils import weaviate_utils

# Prepare weaviate connection
weaviate_utils.init_connection(
    host=settings.weaviate_host,
    port=settings.weaviate_port,
)

# Prepare pika connection and declare exchanges
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_exchanges(settings.exchanges_file)

# Register consumer for embed request
pika_utils.register_consumer(
    queue_name=settings.embed_text_queue,
    exchange=settings.service_exchange,
    routing_key=settings.embed_text_queue_routing_key,
    on_message_callback=on_message_embed,
    auto_delete=False
)

# Register consumer for embed store request
pika_utils.register_consumer(
    queue_name=settings.embed_store_text_queue,
    exchange=settings.service_exchange,
    routing_key=settings.embed_store_text_queue_routing_key,
    on_message_callback=on_message_embed_store,
    auto_delete=False
)

# Register consumer for rerank request
pika_utils.register_consumer(
    queue_name=settings.rerank_text_queue,
    exchange=settings.service_exchange,
    routing_key=settings.rerank_text_queue_routing_key,
    on_message_callback=on_message_rerank,
    auto_delete=False
)

# Register consumer for route request
pika_utils.register_consumer(
    queue_name=f'{pika_utils.service_id}_{settings.route_request_queue}',
    exchange=settings.task_routing_exchange,
    routing_key=f'{pika_utils.service_id}_{settings.route_request_queue_routing_key}',
    on_message_callback=on_message_route_request,
    auto_delete=True
)

# Start consuming messages
pika_utils.start_consuming()
