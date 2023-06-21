from app.utils.pika_handler import pika_handler
from app.responders.embed import on_message_embed
from app.responders.cross_encode import on_message_rerank


pika_handler.register_consumer('embedding_queue_embed', 'embed', on_message_embed)
pika_handler.register_consumer('embedding_queue_rerank', 'rerank', on_message_rerank)

pika_handler.start_consuming()
