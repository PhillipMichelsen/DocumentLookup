import json

from app.handlers.retrieve_context_handler import handle_retrieve_context


def on_message_retrieve_context(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_retrieve_context(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
