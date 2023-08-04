from app.config import settings
from app.listeners.cross_encode_listener import on_message_rerank
from app.listeners.embed_listener import on_message_embed
from app.listeners.route_response_listener import on_message_route_response
from app.utils.pika_utils import pika_utils


# Register consumers
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_exchanges('app/exchanges.yaml')

pika_utils.register_consumer('vector_embed', 'vector_embed', on_message_embed)
pika_utils.register_consumer('vector_rerank', 'vector_rerank', on_message_rerank)
pika_utils.register_consumer(pika_utils.service_id, pika_utils.service_id, on_message_route_response, 'task_routing_exchange')


# Start consuming messages
pika_utils.start_consuming()
