import logging

from app.listeners.embed_listener import on_message_embed
from app.listeners.cross_encode_listener import on_message_rerank
from app.utils.pika_helper import pika_handler

logging.basicConfig(level=logging.DEBUG)

# Register consumers
pika_handler.register_consumer('embedding_queue_embed', 'embed_text', on_message_embed)
pika_handler.register_consumer('embedding_queue_rerank', 'rerank_text', on_message_rerank)

# Start consuming messages
pika_handler.start_consuming()
