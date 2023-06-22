from app.listeners.embed_listener import on_message_embed
from app.listeners.cross_encode_listener import on_message_rerank
from app.utils.pika_helper import pika_handler


pika_handler.register_consumer('embedding_queue_embed', 'embed', on_message_embed)
pika_handler.register_consumer('embedding_queue_rerank', 'rerank', on_message_rerank)

pika_handler.start_consuming()
