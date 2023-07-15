import logging

from app.listeners.embed_listener import on_message_embed
from app.listeners.cross_encode_listener import on_message_rerank
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis_utils
from app.config import settings

logging.basicConfig(level=logging.INFO)

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

pika_utils.register_consumer('embedding_queue_embed', 'embed_text', on_message_embed)
pika_utils.register_consumer('embedding_queue_rerank', 'rerank_text', on_message_rerank)

# Start consuming messages
pika_utils.start_consuming()
