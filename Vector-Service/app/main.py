from app.config import settings
from app.listeners.cross_encode_listener import on_message_rerank
from app.listeners.embed_listener import on_message_embed
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis_utils

# Register consumers
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_service_exchange(settings.service_exchange)

job_redis_utils.init_connection(
    host=settings.redis_host,
    port=settings.redis_port,
    db=1
)

pika_utils.register_consumer(settings.vector_queue_embed, settings.vector_queue_embed_routing_key, on_message_embed)
pika_utils.register_consumer(settings.vector_queue_rerank, settings.vector_queue_rerank_routing_key, on_message_rerank)

# Start consuming messages
pika_utils.start_consuming()
