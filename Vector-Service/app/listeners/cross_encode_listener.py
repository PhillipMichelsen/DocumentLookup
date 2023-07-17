import json

from app.handlers.cross_encode_handler import handle_cross_encode


def on_message_rerank(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_cross_encode(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
