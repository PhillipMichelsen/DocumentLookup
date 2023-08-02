import json

from app.handlers.route_response_handler import handle_route_response


def on_message_route_response(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_route_response(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
