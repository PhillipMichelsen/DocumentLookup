import json

from app.handlers.route_request_handler import handle_route_request


def on_message_route_request(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_route_request(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
