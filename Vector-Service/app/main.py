from app.config import settings
from app.listeners.clear_job_data_listener import on_message_clear_job_data
from app.listeners.cross_encode_listener import on_message_rerank
from app.listeners.embed_listener import on_message_embed
from app.listeners.retrieve_closest_entries_listener import on_message_retrieve_closest_entries
from app.listeners.route_request_listener import on_message_route_request
from app.listeners.store_embedding_listener import on_message_store_embedding
from app.utils.pika_utils import pika_utils
from app.utils.postgres_utils import postgres_utils
from app.utils.weaviate_utils import weaviate_utils

postgres_utils.init_connection('postgresql://postgres:postgres@postgres-service:5432/documentlookup')
postgres_utils.create_tables()

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
pika_utils.declare_exchanges()

# Register consumer for embed request
pika_utils.register_consumer(
    queue_name=settings.embed_text_queue,
    exchange=settings.service_exchange,
    routing_key=settings.embed_text_queue_routing_key,
    on_message_callback=on_message_embed,
    auto_delete=False,
    priority=1
)

# Register consumer for rerank request
pika_utils.register_consumer(
    queue_name=settings.rerank_text_queue,
    exchange=settings.service_exchange,
    routing_key=settings.rerank_text_queue_routing_key,
    on_message_callback=on_message_rerank,
    auto_delete=False
)

# Register consumer for store embedding request
pika_utils.register_consumer(
    queue_name=settings.store_embedding_queue,
    exchange=settings.service_exchange,
    routing_key=settings.store_embedding_queue_routing_key,
    on_message_callback=on_message_store_embedding,
    auto_delete=False,
    priority=10
)

# Register consumer for retrieve closest entries request
pika_utils.register_consumer(
    queue_name=settings.retrieve_closest_entries_queue,
    exchange=settings.service_exchange,
    routing_key=settings.retrieve_closest_entries_queue_routing_key,
    on_message_callback=on_message_retrieve_closest_entries,
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

# Start consuming messages
pika_utils.start_consuming()
