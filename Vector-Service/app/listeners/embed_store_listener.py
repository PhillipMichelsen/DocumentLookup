import json

from app.handlers.embed_store_handler import handle_embed_store


def on_message_embed_store(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_embed_store(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
