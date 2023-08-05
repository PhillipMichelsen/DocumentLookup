import json

from app.handlers.task_route_response_handler import handle_task_route_response


def task_route_response_callback(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_task_route_response(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
