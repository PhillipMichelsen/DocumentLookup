import json

from app.handlers.store_embedding_handler import handle_store_embedding


def on_message_store_embedding(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_store_embedding(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
