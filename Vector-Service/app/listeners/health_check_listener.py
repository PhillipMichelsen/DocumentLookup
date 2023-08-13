import json

from app.handlers.health_check_handler import handle_health_check


def on_message_health_check(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_health_check(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
